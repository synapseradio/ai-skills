/**
 * Shape and validate data before it reaches a chart.
 *
 * Reads CSV, TSV, or JSON rows, keeps the named fields, converts each value to its
 * type, and writes prepared data as JSON. Writes nothing and exits 1 when a value
 * would make the chart misstate the data.
 *
 *   bun --install=fallback prepare_data.ts INPUT --x FIELD --y FIELD [--series FIELD]
 *                  [--x-type category|number|date] [--drop-missing] --out OUT.json
 *
 *   bun --install=fallback prepare_data.ts LINKS --shape sankey --source FIELD --target FIELD --value FIELD
 *                  [--nodes NODES] [--node-id FIELD] [--node-label FIELD] --out OUT.json
 *
 *   bun --install=fallback prepare_data.ts LINKS --shape network --source FIELD --target FIELD [--value FIELD]
 *                  [--nodes NODES] [--node-id FIELD] [--node-label FIELD]
 *                  [--node-group FIELD] --out OUT.json
 *
 *   bun --install=fallback prepare_data.ts INPUT --shape choropleth --region FIELD --value FIELD
 *                  [--geojson FILE [--feature-id PROPERTY] [--feature-name PROPERTY]]
 *                  --out OUT.json
 *
 * LINKS holds one row per link. NODES holds one row per node; without it the nodes
 * are the names the links use. A choropleth joins each row to a country of the
 * bundled world atlas by its name or ISO 3166-1 numeric code, or to a feature of
 * the GeoJSON file by the named property. The GeoJSON holds polygons in longitude
 * and latitude.
 *
 * Exit codes: 0 prepared, 1 problems found, 2 unusable arguments or input.
 */

import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { parseArgs } from "node:util";

export const X_TYPES = ["category", "number", "date"];
export const SHAPES = ["rows", "sankey", "network", "choropleth"];
export const ATLAS = join(
  dirname(import.meta.dir),
  "assets",
  "world-atlas-countries-110m.json",
);
const GROUPED_NUMBER = /^-?\d{1,3}(,\d{3})+(\.\d+)?$/;
const YEAR_MONTH = /^\d{4}-\d{2}$/;
const PLAIN_NUMBER = /^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$/;

export type Row = Record<string, unknown>;
export type Issue = [code: string, message: string];

/** The arguments or the input file cannot be read at all. */
export class Unusable extends Error {}

// Text helpers that keep every printed message in the form the Python scripts used.

/** Python's repr for the values these scripts print. */
export function pyRepr(value: unknown): string {
  if (value === null || value === undefined) return "None";
  if (typeof value === "boolean") return value ? "True" : "False";
  if (typeof value === "number") return String(value);
  if (Array.isArray(value)) return `[${value.map(pyRepr).join(", ")}]`;
  if (typeof value !== "string") return JSON.stringify(value);
  const quote = value.includes("'") && !value.includes('"') ? '"' : "'";
  let out = quote;
  for (const char of value) {
    if (char === "\\") out += "\\\\";
    else if (char === quote) out += `\\${quote}`;
    else if (char === "\n") out += "\\n";
    else if (char === "\r") out += "\\r";
    else if (char === "\t") out += "\\t";
    else if (char < " " || char === "\x7f") {
      out += `\\x${char.charCodeAt(0).toString(16).padStart(2, "0")}`;
    } else out += char;
  }
  return out + quote;
}

/** Python's `str` for the values these scripts print. */
export function pyStr(value: unknown): string {
  if (typeof value === "string") return value;
  return pyRepr(value);
}

/** Python's `:g` format: six significant digits, trailing zeros removed. */
export function pyG(value: number, digits = 6): string {
  if (value === 0) return "0";
  const exponent = Math.floor(Math.log10(Math.abs(Number(value.toPrecision(digits)))));
  if (exponent < -4 || exponent >= digits) {
    const [mantissa = "", power = "0"] = value.toExponential(digits - 1).split("e");
    const trimmed = mantissa.includes(".") ? mantissa.replace(/\.?0+$/, "") : mantissa;
    const sign = power.startsWith("-") ? "-" : "+";
    return `${trimmed}e${sign}${power.replace(/^[+-]/, "").padStart(2, "0")}`;
  }
  const fixed = value.toFixed(Math.max(0, digits - 1 - exponent));
  return fixed.includes(".") ? fixed.replace(/\.?0+$/, "") : fixed;
}

/** Python's `json.dumps` with its default separators. */
export function pyDumps(value: unknown, ensureAscii = true): string {
  if (value === null || value === undefined) return "null";
  if (Array.isArray(value)) return `[${value.map((item) => pyDumps(item, ensureAscii)).join(", ")}]`;
  if (typeof value === "object") {
    const entries = Object.entries(value as Row).filter(([, item]) => item !== undefined);
    return `{${entries
      .map(([key, item]) => `${pyDumps(key, ensureAscii)}: ${pyDumps(item, ensureAscii)}`)
      .join(", ")}}`;
  }
  const text = JSON.stringify(value);
  return ensureAscii ? escapeNonAscii(text) : text;
}

/** Python's `json.dumps(value, indent=2)`. */
export function pyDumpsIndented(value: unknown): string {
  return escapeNonAscii(JSON.stringify(value, null, 2));
}

function escapeNonAscii(text: string): string {
  let out = "";
  for (let index = 0; index < text.length; index += 1) {
    const code = text.charCodeAt(index);
    out += code > 0x7f ? `\\u${code.toString(16).padStart(4, "0")}` : text.charAt(index);
  }
  return out;
}

const ERROR_TEXT: Record<string, string> = {
  ENOENT: "No such file or directory",
  EACCES: "Permission denied",
  EISDIR: "Is a directory",
  ENOTDIR: "Not a directory",
};

/** The operating system's wording for a failed file read. */
export function strerror(error: unknown): string {
  const code = (error as { code?: string }).code ?? "";
  return ERROR_TEXT[code] ?? (error as Error).message;
}

function readText(path: string): string {
  try {
    const text = readFileSync(path, "utf-8");
    return text.charCodeAt(0) === 0xfeff ? text.slice(1) : text;
  } catch (error) {
    throw new Unusable(`cannot read ${path}: ${strerror(error)}`);
  }
}

function parseCsv(text: string, delimiter: string): Row[] {
  const records: string[][] = [];
  let record: string[] = [];
  let field = "";
  let quoted = false;
  let touched = false;
  const endRecord = () => {
    record.push(field);
    if (touched || record.length > 1 || record[0] !== "") records.push(record);
    record = [];
    field = "";
    touched = false;
  };
  for (let index = 0; index < text.length; index += 1) {
    const char = text.charAt(index);
    if (quoted) {
      if (char === '"' && text.charAt(index + 1) === '"') {
        field += '"';
        index += 1;
      } else if (char === '"') quoted = false;
      else field += char;
    } else if (char === '"') {
      quoted = true;
      touched = true;
    } else if (char === delimiter) {
      record.push(field);
      field = "";
      touched = true;
    } else if (char === "\n" || char === "\r") {
      if (char === "\r" && text.charAt(index + 1) === "\n") index += 1;
      endRecord();
    } else {
      field += char;
      touched = true;
    }
  }
  if (field !== "" || record.length > 0) endRecord();
  const [header, ...body] = records;
  if (!header) return [];
  return body.map((values) => {
    const row: Row = {};
    header.forEach((name, position) => {
      row[name] = values[position];
    });
    return row;
  });
}

export function readRows(path: string): Row[] {
  const lower = path.toLowerCase();
  const text = readText(path);
  if (lower.endsWith(".csv") || lower.endsWith(".tsv")) {
    return parseCsv(text, lower.endsWith(".tsv") ? "\t" : ",");
  }
  if (lower.endsWith(".json")) {
    let loaded: unknown;
    try {
      loaded = JSON.parse(text);
    } catch (error) {
      throw new Unusable(`${path} is not valid JSON: ${(error as Error).message}`);
    }
    const rows =
      loaded && typeof loaded === "object" && !Array.isArray(loaded)
        ? (loaded as Row).rows
        : loaded;
    if (
      !Array.isArray(rows) ||
      !rows.every((row) => row && typeof row === "object" && !Array.isArray(row))
    ) {
      throw new Unusable(`${path} must hold a list of objects, or an object with a 'rows' list`);
    }
    return rows as Row[];
  }
  throw new Unusable(`${path} has an unsupported extension; use .csv, .tsv, or .json`);
}

export function isMissing(value: unknown): boolean {
  return value === null || value === undefined || (typeof value === "string" && value.trim() === "");
}

/** A finite number, or null when the value is not a plain number. */
export function toNumber(value: unknown): number | null {
  if (typeof value === "boolean") return null;
  if (typeof value === "number") return Number.isFinite(value) ? value : null;
  let text = pyStr(value).trim();
  if (GROUPED_NUMBER.test(text)) text = text.replaceAll(",", "");
  if (!PLAIN_NUMBER.test(text)) return null;
  const number = Number(text);
  return Number.isFinite(number) ? number : null;
}

function validDate(year: number, month: number, day: number): boolean {
  const probe = new Date(Date.UTC(year, month - 1, day));
  return (
    probe.getUTCFullYear() === year && probe.getUTCMonth() === month - 1 && probe.getUTCDate() === day
  );
}

const DATE_TIME =
  /^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})(?::(\d{2})(?:\.(\d{1,6}))?)?(Z|[+-]\d{2}:\d{2})?$/;

/** An ISO date or date-time string, or null when the value is not ISO 8601. */
export function toDate(value: unknown): string | null {
  if (typeof value === "number") return null;
  let text = pyStr(value).trim();
  if (YEAR_MONTH.test(text)) text += "-01";
  if (text.length === 10) {
    const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(text);
    if (!match) return null;
    return validDate(Number(match[1]), Number(match[2]), Number(match[3])) ? text : null;
  }
  const match = DATE_TIME.exec(text);
  if (!match) return null;
  const [, year, month, day, hour, minute, second = "00", fraction, zone] = match;
  if (!validDate(Number(year), Number(month), Number(day))) return null;
  if (Number(hour) > 23 || Number(minute) > 59 || Number(second) > 59) return null;
  const micro = fraction ? `.${fraction.padEnd(6, "0")}` : "";
  const offset = zone === "Z" ? "+00:00" : (zone ?? "");
  return `${year}-${month}-${day}T${hour}:${minute}:${second}${micro}${offset}`;
}

function inferXType(values: unknown[]): string {
  if (values.every((value) => toNumber(value) !== null)) return "number";
  if (values.every((value) => toDate(value) !== null)) return "date";
  return "category";
}

function columnsOf(rows: Row[]): string[] {
  const known = new Set<string>();
  for (const row of rows) for (const key of Object.keys(row)) known.add(key);
  return [...known].sort();
}

function lessThan(a: unknown, b: unknown): number {
  if (typeof a === "number" && typeof b === "number") return a - b;
  const left = String(a);
  const right = String(b);
  return left < right ? -1 : left > right ? 1 : 0;
}

type Prepared = { prepared: Row | null; problems: Issue[]; notes: Issue[] };

export function prepare(
  rows: Row[],
  x: string,
  y: string,
  series: string | undefined,
  xType: string | undefined,
  dropMissing: boolean,
): Prepared {
  const problems: Issue[] = [];
  const notes: Issue[] = [];
  const fields = [x, y, series].filter((field): field is string => Boolean(field));

  if (rows.length === 0) {
    return { prepared: null, problems: [["empty", "the input holds no rows"]], notes };
  }
  const known = columnsOf(rows);
  for (const field of fields) {
    if (!known.includes(field)) {
      problems.push(["missing-field", `no column named ${pyRepr(field)}; columns are ${pyRepr(known)}`]);
    }
  }
  if (problems.length > 0) return { prepared: null, problems, notes };

  const kept: [number, Row][] = [];
  let dropped = 0;
  rows.forEach((row, offset) => {
    const index = offset + 1;
    const absent = fields.filter((field) => isMissing(row[field]));
    if (absent.length === 0) kept.push([index, row]);
    else if (dropMissing) dropped += 1;
    else problems.push(["missing-value", `row ${index} has no value for ${pyRepr(absent)}`]);
  });
  if (dropped) {
    notes.push(["dropped-rows", `dropped ${dropped} of ${rows.length} rows with a missing value`]);
  }
  if (kept.length === 0 && problems.length === 0) {
    problems.push(["empty", "no row has a value in every named column"]);
  }
  if (problems.length > 0) return { prepared: null, problems, notes };

  const resolvedType = xType || inferXType(kept.map(([, row]) => row[x]));
  const convertX = (value: unknown): unknown => {
    if (resolvedType === "number") return toNumber(value);
    if (resolvedType === "date") return toDate(value);
    return pyStr(value).trim();
  };
  const xCode = resolvedType === "date" ? "not-a-date" : "not-a-number";

  let preparedRows: Row[] = [];
  const seen = new Map<string, number>();
  for (const [index, row] of kept) {
    const xValue = convertX(row[x]);
    const yValue = toNumber(row[y]);
    if (xValue === null) {
      problems.push([xCode, `row ${index}: ${x} is ${pyRepr(row[x])}, which is not a ${resolvedType}`]);
    }
    if (yValue === null) {
      problems.push([
        "not-a-number",
        `row ${index}: ${y} is ${pyRepr(row[y])}; strip units and symbols from the value`,
      ]);
    }
    if (xValue === null || yValue === null) continue;
    const out: Row = { [x]: xValue, [y]: yValue };
    if (series) out[series] = pyStr(row[series]).trim();
    const key = JSON.stringify([xValue, series ? out[series] : null]);
    const earlier = seen.get(key);
    if (earlier !== undefined) {
      problems.push([
        "duplicate-key",
        `rows ${earlier} and ${index} share ${x}=${pyRepr(xValue)}` +
          (series ? ` and ${series}=${pyRepr(out[series])}` : "") +
          "; decide how they aggregate before charting",
      ]);
    } else seen.set(key, index);
    preparedRows.push(out);
  }
  if (problems.length > 0) return { prepared: null, problems, notes };

  if (resolvedType === "number" || resolvedType === "date") {
    const ordered = [...preparedRows].sort((a, b) => lessThan(a[x], b[x]));
    if (ordered.some((row, index) => row !== preparedRows[index])) {
      notes.push(["sorted", `sorted rows by ${x}`]);
    }
    preparedRows = ordered;
  }

  const values = preparedRows.map((row) => row[y] as number);
  const low = Math.min(...values);
  const high = Math.max(...values);
  if (low < 0) notes.push(["negative-values", `${y} goes below zero; a stacked chart cannot show it`]);
  if (low === high) notes.push(["constant", `every ${y} equals ${values[0]}`]);
  const seriesValues: string[] = [];
  if (series) {
    for (const row of preparedRows) {
      if (!seriesValues.includes(row[series] as string)) seriesValues.push(row[series] as string);
    }
  }

  const prepared: Row = {
    shape: "rows",
    x,
    y,
    series: series ?? null,
    xType: resolvedType,
    seriesValues,
    rows: preparedRows,
  };
  notes.unshift([
    "summary",
    `${preparedRows.length} rows; ${x} is ${resolvedType}; ${y} runs ${low} to ${high}` +
      (series ? `; ${seriesValues.length} series in ${series}` : ""),
  ]);
  return { prepared, problems, notes };
}

type GraphNode = { id: string; label: string; group?: string };
type GraphLink = { source: string; target: string; value?: number };

/** One node id on a directed cycle, or null when the links form none. */
function findCycle(nodes: GraphNode[], links: GraphLink[]): string | null {
  const waiting = new Map<string, number>(nodes.map((node) => [node.id, 0]));
  for (const link of links) waiting.set(link.target, (waiting.get(link.target) ?? 0) + 1);
  const ready = [...waiting].filter(([, count]) => count === 0).map(([id]) => id);
  while (ready.length > 0) {
    const nodeId = ready.pop() as string;
    waiting.delete(nodeId);
    for (const link of links) {
      if (link.source === nodeId) {
        const left = (waiting.get(link.target) ?? 0) - 1;
        waiting.set(link.target, left);
        if (left === 0) ready.push(link.target);
      }
    }
  }
  return waiting.keys().next().value ?? null;
}

type GraphFields = {
  source: string;
  target: string;
  value?: string;
  id: string;
  label?: string;
  group?: string;
};

export function prepareGraph(
  shape: string,
  linkRows: Row[],
  nodeRows: Row[] | null,
  fields: GraphFields,
): Prepared {
  const problems: Issue[] = [];
  const notes: Issue[] = [];
  const { source, target, value, id: nodeId, label: nodeLabel, group: nodeGroup } = fields;
  const directed = shape === "sankey";

  if (linkRows.length === 0) {
    return { prepared: null, problems: [["empty", "the links file holds no rows"]], notes };
  }
  const known = columnsOf(linkRows);
  for (const field of [source, target, value]) {
    if (field && !known.includes(field)) {
      problems.push([
        "missing-field",
        `no link column named ${pyRepr(field)}; columns are ${pyRepr(known)}`,
      ]);
    }
  }
  if (nodeRows !== null) {
    const nodeKnown = columnsOf(nodeRows);
    for (const field of [nodeId, nodeLabel, nodeGroup]) {
      if (field && !nodeKnown.includes(field)) {
        problems.push([
          "missing-field",
          `no node column named ${pyRepr(field)}; columns are ${pyRepr(nodeKnown)}`,
        ]);
      }
    }
  }
  if (problems.length > 0) return { prepared: null, problems, notes };

  const nodes: GraphNode[] = [];
  const byId = new Map<string, GraphNode>();
  if (nodeRows !== null) {
    nodeRows.forEach((row, offset) => {
      const index = offset + 1;
      if (isMissing(row[nodeId])) {
        problems.push(["missing-value", `node row ${index} has no value for ${nodeId}`]);
        return;
      }
      const key = pyStr(row[nodeId]).trim();
      if (byId.has(key)) {
        problems.push(["duplicate-node", `node row ${index} repeats ${nodeId}=${pyRepr(key)}`]);
        return;
      }
      const label = nodeLabel ? row[nodeLabel] : undefined;
      const node: GraphNode = { id: key, label: isMissing(label) ? key : pyStr(label).trim() };
      if (nodeGroup) {
        if (isMissing(row[nodeGroup])) {
          problems.push(["missing-value", `node row ${index} has no value for ${nodeGroup}`]);
          return;
        }
        node.group = pyStr(row[nodeGroup]).trim();
      }
      byId.set(key, node);
      nodes.push(node);
    });
  }

  const links: GraphLink[] = [];
  const seen = new Map<string, number>();
  linkRows.forEach((row, offset) => {
    const index = offset + 1;
    const absent = [source, target, value].filter((field) => field && isMissing(row[field]));
    if (absent.length > 0) {
      problems.push(["missing-value", `link row ${index} has no value for ${pyRepr(absent)}`]);
      return;
    }
    const ends = [pyStr(row[source]).trim(), pyStr(row[target]).trim()] as [string, string];
    const link: GraphLink = { source: ends[0], target: ends[1] };
    let usable = true;
    for (const end of ends) {
      if (byId.has(end)) continue;
      if (nodeRows === null) {
        const node = { id: end, label: end };
        byId.set(end, node);
        nodes.push(node);
      } else {
        problems.push([
          "unknown-node",
          `link row ${index} names ${pyRepr(end)}, which the nodes file lacks`,
        ]);
        usable = false;
      }
    }
    if (ends[0] === ends[1]) {
      problems.push(["self-link", `link row ${index} joins ${pyRepr(ends[0])} to itself`]);
      usable = false;
    }
    if (value) {
      const number = toNumber(row[value]);
      if (number === null) {
        problems.push([
          "not-a-number",
          `link row ${index}: ${value} is ${pyRepr(row[value])}; strip units and symbols`,
        ]);
        usable = false;
      } else if (number <= 0) {
        problems.push([
          "not-positive",
          `link row ${index}: ${value} is ${number}; a link needs a value above zero`,
        ]);
        usable = false;
      } else link.value = number;
    }
    const key = JSON.stringify(directed ? ends : [...ends].sort());
    const earlier = seen.get(key);
    if (earlier !== undefined) {
      problems.push([
        "duplicate-key",
        `link rows ${earlier} and ${index} join the same two nodes; ` +
          "decide how they aggregate before charting",
      ]);
      usable = false;
    } else seen.set(key, index);
    if (usable) links.push(link);
  });
  if (problems.length > 0) return { prepared: null, problems, notes };

  const linked = new Set(links.flatMap((link) => [link.source, link.target]));
  const alone = nodes.filter((node) => !linked.has(node.id)).map((node) => node.id);
  if (directed) {
    for (const name of alone) {
      problems.push(["unlinked-node", `node ${pyRepr(name)} has no link, so no flow reaches it`]);
    }
    const onCycle = findCycle(nodes, links);
    if (onCycle !== null) {
      problems.push([
        "cycle",
        `the links loop back through ${pyRepr(onCycle)}; a sankey needs flow in one direction`,
      ]);
    }
    for (const node of nodes) {
      const inflow = links
        .filter((link) => link.target === node.id)
        .reduce((sum, link) => sum + (link.value ?? 0), 0);
      const outflow = links
        .filter((link) => link.source === node.id)
        .reduce((sum, link) => sum + (link.value ?? 0), 0);
      if (inflow && outflow && Math.abs(inflow - outflow) > 1e-9 * Math.max(inflow, outflow)) {
        problems.push([
          "unbalanced-node",
          `node ${pyRepr(node.id)} takes in ${pyG(inflow)} and sends out ${pyG(outflow)}; ` +
            "add the missing flow or name where the difference goes",
        ]);
      }
    }
  } else if (alone.length > 0) {
    notes.push(["unlinked-nodes", `${alone.length} nodes have no link: ${pyRepr(alone)}`]);
  }
  if (problems.length > 0) return { prepared: null, problems, notes };

  const groupValues: string[] = [];
  for (const node of nodes) {
    if (node.group !== undefined && !groupValues.includes(node.group)) groupValues.push(node.group);
  }
  const prepared: Row = {
    shape,
    weighted: Boolean(value),
    groupValues,
    nodes,
    links,
  };
  let summary = `${nodes.length} nodes; ${links.length} links`;
  if (value) {
    const values = links.map((link) => link.value as number);
    summary += `; ${value} runs ${Math.min(...values)} to ${Math.max(...values)}`;
  }
  if (groupValues.length > 0) summary += `; ${groupValues.length} groups in ${nodeGroup}`;
  notes.unshift(["summary", summary]);
  return { prepared, problems, notes };
}

type Position = [number, number];

function ringIsCounterclockwise(ring: Position[]): boolean {
  let total = 0;
  for (let index = 0; index + 1 < ring.length; index += 1) {
    const a = ring[index] as Position;
    const b = ring[index + 1] as Position;
    total += a[0] * b[1] - b[0] * a[1];
  }
  return total > 0;
}

/** Wind outer rings clockwise and holes counterclockwise, as a spherical projection reads them. */
function rewind(geometry: { type: string; coordinates: Position[][] | Position[][][] }): number {
  const polygons = (
    geometry.type === "Polygon" ? [geometry.coordinates] : geometry.coordinates
  ) as Position[][][];
  let reversedRings = 0;
  for (const polygon of polygons) {
    polygon.forEach((ring, index) => {
      if (ringIsCounterclockwise(ring) === (index === 0)) {
        ring.reverse();
        reversedRings += 1;
      }
    });
  }
  return reversedRings;
}

type Feature = {
  type: "Feature";
  id: string;
  properties: { name: string };
  geometry: Row;
};

type FeatureRead = { features: Feature[]; problems: Issue[]; notes: Issue[] };

function readFeatures(path: string, idProperty?: string, nameProperty?: string): FeatureRead {
  const text = readText(path);
  let loaded: unknown;
  try {
    loaded = JSON.parse(text);
  } catch (error) {
    throw new Unusable(`${path} is not valid JSON: ${(error as Error).message}`);
  }
  const features =
    loaded && typeof loaded === "object" && !Array.isArray(loaded)
      ? ((loaded as Row).features as Row[] | undefined)
      : undefined;
  if (!Array.isArray(features) || features.length === 0) {
    throw new Unusable(`${path} must be a GeoJSON FeatureCollection with features`);
  }

  const problems: Issue[] = [];
  const notes: Issue[] = [];
  const kept: Feature[] = [];
  const seen = new Set<string>();
  let rewound = 0;
  features.forEach((feature, offset) => {
    const index = offset + 1;
    const properties = ((feature.properties as Row | null) ?? {}) as Row;
    const geometry = ((feature.geometry as Row | null) ?? {}) as Row;
    const rawKey = idProperty ? properties[idProperty] : feature.id;
    if (isMissing(rawKey)) {
      problems.push(["missing-value", `feature ${index} has no ${idProperty || "id"} to join on`]);
      return;
    }
    const key = pyStr(rawKey).trim();
    if (seen.has(key)) {
      problems.push(["duplicate-region", `feature ${index} repeats the key ${pyRepr(key)}`]);
      return;
    }
    seen.add(key);
    if (geometry.type !== "Polygon" && geometry.type !== "MultiPolygon") {
      problems.push([
        "not-a-region",
        `feature ${pyRepr(key)} is a ${pyStr(geometry.type ?? null)}; a choropleth fills polygons`,
      ]);
      return;
    }
    try {
      rewound += rewind(geometry as Parameters<typeof rewind>[0]);
    } catch (error) {
      problems.push([
        "not-a-region",
        `feature ${pyRepr(key)} has unreadable coordinates: ${(error as Error).name}`,
      ]);
      return;
    }
    const name = nameProperty ? properties[nameProperty] : undefined;
    kept.push({
      type: "Feature",
      id: key,
      properties: { name: isMissing(name) ? key : pyStr(name).trim() },
      geometry,
    });
  });
  if (rewound) {
    notes.push(["rewound", `reversed ${rewound} rings to the winding the projection reads`]);
  }
  return { features: kept, problems, notes };
}

export function prepareChoropleth(
  rows: Row[],
  region: string,
  value: string,
  features: Feature[] | null,
): Prepared {
  const problems: Issue[] = [];
  const notes: Issue[] = [];
  if (rows.length === 0) {
    return { prepared: null, problems: [["empty", "the input holds no rows"]], notes };
  }
  const known = columnsOf(rows);
  for (const field of [region, value]) {
    if (!known.includes(field)) {
      problems.push(["missing-field", `no column named ${pyRepr(field)}; columns are ${pyRepr(known)}`]);
    }
  }
  if (problems.length > 0) return { prepared: null, problems, notes };

  const names = new Map<string, string>();
  const lookup = new Map<string, string>();
  if (features === null) {
    const atlas = JSON.parse(readFileSync(ATLAS, "utf-8")) as {
      regions: { id: string; name: string }[];
    };
    for (const entry of atlas.regions) {
      names.set(entry.name, entry.name);
      lookup.set(entry.name.toLowerCase(), entry.name);
      if (entry.id) {
        lookup.set(entry.id, entry.name);
        lookup.set(entry.id.replace(/^0+/, ""), entry.name);
      }
    }
  } else {
    for (const feature of features) {
      names.set(feature.id, feature.properties.name);
      lookup.set(feature.id, feature.id);
      lookup.set(feature.id.toLowerCase(), feature.id);
    }
  }

  const regions: { key: string; label: string; value: number }[] = [];
  const seen = new Map<string, number>();
  rows.forEach((row, offset) => {
    const index = offset + 1;
    const absent = [region, value].filter((field) => isMissing(row[field]));
    if (absent.length > 0) {
      problems.push(["missing-value", `row ${index} has no value for ${pyRepr(absent)}`]);
      return;
    }
    const given = pyStr(row[region]).trim();
    const key = lookup.get(given) || lookup.get(given.toLowerCase());
    const number = toNumber(row[value]);
    if (key === undefined) {
      problems.push([
        "unknown-region",
        `row ${index}: ${pyRepr(given)} matches no region of the ` +
          (features === null ? "world atlas" : "GeoJSON file"),
      ]);
    }
    if (number === null) {
      problems.push([
        "not-a-number",
        `row ${index}: ${value} is ${pyRepr(row[value])}; strip units and symbols from the value`,
      ]);
    }
    if (key === undefined || number === null) return;
    const earlier = seen.get(key);
    if (earlier !== undefined) {
      problems.push([
        "duplicate-key",
        `rows ${earlier} and ${index} both give a value for ${pyRepr(key)}; ` +
          "decide how they aggregate before charting",
      ]);
      return;
    }
    seen.set(key, index);
    regions.push({ key, label: names.get(key) as string, value: number });
  });
  if (problems.length > 0) return { prepared: null, problems, notes };

  const values = regions.map((entry) => entry.value);
  const low = Math.min(...values);
  const high = Math.max(...values);
  if (low === high) {
    notes.push(["constant", `every ${value} equals ${values[0]}; the map shows one colour`]);
  }
  const without = names.size - regions.length;
  if (without) {
    notes.push(["regions-without-value", `${without} of ${names.size} regions have no value`]);
  }
  regions.sort((a, b) => b.value - a.value);
  const prepared: Row = {
    shape: "choropleth",
    atlas: features === null ? "world" : null,
    regionsWithoutValue: without,
    regions,
    features,
  };
  notes.unshift(["summary", `${regions.length} regions; ${value} runs ${low} to ${high}`]);
  return { prepared, problems, notes };
}

function fail(message: string): never {
  console.error(`error: ${message}`);
  process.exit(2);
}

export function main(argv: string[]): number {
  let parsed: ReturnType<typeof parseArgs>;
  try {
    parsed = parseArgs({
      args: argv,
      allowPositionals: true,
      options: {
        shape: { type: "string", default: "rows" },
        x: { type: "string" },
        y: { type: "string" },
        source: { type: "string" },
        target: { type: "string" },
        value: { type: "string" },
        nodes: { type: "string" },
        "node-id": { type: "string", default: "id" },
        "node-label": { type: "string" },
        "node-group": { type: "string" },
        region: { type: "string" },
        geojson: { type: "string" },
        "feature-id": { type: "string" },
        "feature-name": { type: "string" },
        series: { type: "string" },
        "x-type": { type: "string" },
        "drop-missing": { type: "boolean", default: false },
        out: { type: "string" },
      },
    });
  } catch (error) {
    return fail((error as Error).message);
  }
  const { values: args, positionals } = parsed as {
    values: Record<string, string | boolean | undefined>;
    positionals: string[];
  };
  const text = (name: string) => args[name] as string | undefined;
  if (positionals.length !== 1) return fail("the following arguments are required: input");
  const input = positionals[0] as string;
  const shape = text("shape") as string;
  if (!SHAPES.includes(shape)) return fail(`argument --shape: invalid choice: ${pyRepr(shape)}`);
  const xType = text("x-type");
  if (xType !== undefined && !X_TYPES.includes(xType)) {
    return fail(`argument --x-type: invalid choice: ${pyRepr(xType)}`);
  }
  const out = text("out");
  if (!out) return fail("the following arguments are required: --out");

  const needed: Record<string, string[]> = {
    rows: ["x", "y"],
    sankey: ["source", "target", "value"],
    network: ["source", "target"],
    choropleth: ["region", "value"],
  };
  const absent = (needed[shape] as string[]).filter((name) => !text(name)).map((name) => `--${name}`);
  if (absent.length > 0) return fail(`--shape ${shape} needs ${absent.join(", ")}`);
  if (shape === "sankey" && text("node-group")) return fail("--node-group applies to --shape network");
  if ((text("node-label") || text("node-group")) && !text("nodes")) {
    return fail("--node-label and --node-group read the file --nodes names");
  }
  if ((text("feature-id") || text("feature-name")) && !text("geojson")) {
    return fail("--feature-id and --feature-name read the file --geojson names");
  }

  let features: Feature[] | null = null;
  let featureProblems: Issue[] = [];
  let featureNotes: Issue[] = [];
  let rows: Row[];
  let nodeRows: Row[] | null = null;
  try {
    rows = readRows(input);
    nodeRows = text("nodes") ? readRows(text("nodes") as string) : null;
    if (text("geojson")) {
      const read = readFeatures(text("geojson") as string, text("feature-id"), text("feature-name"));
      features = read.features;
      featureProblems = read.problems;
      featureNotes = read.notes;
    }
  } catch (error) {
    if (error instanceof Unusable) return fail(error.message);
    throw error;
  }

  let result: Prepared;
  let problems: Issue[];
  let notes: Issue[];
  if (shape === "choropleth") {
    result = prepareChoropleth(rows, text("region") as string, text("value") as string, features);
    problems = [...featureProblems, ...result.problems];
    notes = [...result.notes.slice(0, 1), ...featureNotes, ...result.notes.slice(1)];
  } else if (shape === "rows") {
    result = prepare(
      rows,
      text("x") as string,
      text("y") as string,
      text("series"),
      xType,
      Boolean(args["drop-missing"]),
    );
    problems = result.problems;
    notes = result.notes;
  } else {
    result = prepareGraph(shape, rows, nodeRows, {
      source: text("source") as string,
      target: text("target") as string,
      value: text("value"),
      id: text("node-id") as string,
      label: text("node-label"),
      group: text("node-group"),
    });
    problems = result.problems;
    notes = result.notes;
  }
  for (const [code, message] of notes) console.log(`note: ${code}: ${message}`);
  if (problems.length > 0) {
    for (const [code, message] of problems) console.log(`problem: ${code}: ${message}`);
    return 1;
  }
  writeFileSync(out, `${pyDumpsIndented(result.prepared)}\n`, "utf-8");
  console.log(`wrote ${out}`);
  return 0;
}

if (import.meta.main) process.exit(main(process.argv.slice(2)));
