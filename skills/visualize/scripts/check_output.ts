/**
 * Check a finished visualization before it is handed over.
 *
 * Reads each HTML chart page or Markdown file and reports every defect that would
 * leave a reader without the chart, its values, or its meaning.
 *
 *   bun --install=fallback check_output.ts PATH [PATH ...]
 *
 * Prints one `path: code: message` line per defect, or `path: ok`.
 * Exit codes: 0 no defect, 1 defects found, 2 a path cannot be read or checked.
 */

import { readFileSync } from "node:fs";
import { extname } from "node:path";
import { CDN_BASE, CHARTS_PACKAGE, CHARTS_VERSION, MAP_URLS } from "./build_page.ts";
import { type Measurement, measurePage } from "./measure_scene.ts";
import { ATLAS, type Issue, pyG, pyRepr } from "./prepare_data.ts";

type Triple = readonly [number, number, number];
type Matrix = readonly [Triple, Triple, Triple];

// Colour-vision-deficiency simulation matrices at full severity, applied to linear RGB:
// https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html
const CVD_MATRICES: [string, Matrix][] = [
  [
    "protanopia",
    [
      [0.152286, 1.052583, -0.204868],
      [0.114503, 0.786281, 0.099216],
      [-0.003882, -0.048116, 1.051998],
    ],
  ],
  [
    "deuteranopia",
    [
      [0.367322, 0.860646, -0.227968],
      [0.280085, 0.672501, 0.047413],
      [-0.01182, 0.04294, 0.968881],
    ],
  ],
  [
    "tritanopia",
    [
      [1.255528, -0.076749, -0.178779],
      [-0.078411, 0.930809, 0.147602],
      [0.004733, 0.691367, 0.3039],
    ],
  ],
];
const MIN_COLOR_DISTANCE = 12.0;
const MIN_GRAPHIC_CONTRAST = 3.0;
const MIN_RAMP_LIGHTNESS_SPAN = 40.0;

const MERMAID_TYPES = new Set([
  "flowchart",
  "graph",
  "sequenceDiagram",
  "classDiagram",
  "stateDiagram",
  "stateDiagram-v2",
  "erDiagram",
  "journey",
  "gantt",
  "pie",
  "quadrantChart",
  "requirementDiagram",
  "gitGraph",
  "mindmap",
  "timeline",
  "sankey-beta",
  "xychart-beta",
  "block-beta",
  "C4Context",
]);
const BAR_LINE = /^(?<label>.*?\S)\s+(?<bar>█+[▏▎▍▌▋▊▉]?|[▏▎▍▌▋▊▉])\s+(?<rest>\S.*)$/;
const PARTIAL_BLOCKS = "▏▎▍▌▋▊▉";
const NUMBER = /-?\d[\d,]*(?:\.\d+)?/;
const IMPORT =
  /import\s*\(\s*['"]([^'"]+)['"]\s*\)|(?:^|[\s;])import\s[^'"();]*?['"]([^'"]+)['"]/gm;
const FETCH = /fetch\s*\(\s*['"]([^'"]+)['"]/g;
const HEX = /^#[0-9a-fA-F]{6}$/;
const EXTERNAL = /^(?:https?:)?\/\//;

function linearRgb(hex: string): Triple {
  const channel = (offset: number) => Number.parseInt(hex.slice(offset, offset + 2), 16) / 255;
  const linear = (c: number) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
  return [linear(channel(1)), linear(channel(3)), linear(channel(5))];
}

/** WCAG contrast ratio: https://www.w3.org/TR/WCAG22/#dfn-contrast-ratio */
export function contrastRatio(first: string, second: string): number {
  const luminance = (hex: string) => {
    const [r, g, b] = linearRgb(hex);
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  const a = luminance(first);
  const b = luminance(second);
  return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
}

/** CIE L*a*b* under D65 from linear sRGB. */
function lab(rgb: Triple): Triple {
  const [r, g, b] = rgb.map((c) => Math.min(1, Math.max(0, c))) as [number, number, number];
  const xyz = [
    (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047,
    0.2126729 * r + 0.7151522 * g + 0.072175 * b,
    (0.0193339 * r + 0.119192 * g + 0.9503041 * b) / 1.08883,
  ];
  const [fx, fy, fz] = xyz.map((t) => (t > 0.008856 ? t ** (1 / 3) : 7.787 * t + 16 / 116)) as [
    number,
    number,
    number,
  ];
  return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)];
}

/** Euclidean distance in L*a*b*, after simulating a colour-vision deficiency when given. */
function colorDistance(first: string, second: string, matrix: Matrix | null): number {
  const seen = (hex: string): Triple => {
    let rgb = linearRgb(hex);
    if (matrix) {
      rgb = matrix.map((row) => row[0] * rgb[0] + row[1] * rgb[1] + row[2] * rgb[2]) as unknown as Triple;
    }
    return lab(rgb);
  };
  const a = seen(first);
  const b = seen(second);
  return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5;
}

function colorDefects(colors: string[], background: string): Issue[] {
  const defects: Issue[] = [];
  for (const color of colors) {
    const ratio = contrastRatio(color, background);
    if (ratio < MIN_GRAPHIC_CONTRAST) {
      defects.push([
        "color-low-contrast",
        `${color} has contrast ${ratio.toFixed(2)}:1 on ${background}; marks need ${pyG(MIN_GRAPHIC_CONTRAST)}:1`,
      ]);
    }
  }
  const views: [string, Matrix | null][] = [["typical vision", null], ...CVD_MATRICES];
  colors.forEach((first, index) => {
    for (const second of colors.slice(index + 1)) {
      let name = "";
      let distance = Number.POSITIVE_INFINITY;
      for (const [viewName, matrix] of views) {
        const candidate = colorDistance(first, second, matrix);
        if (candidate < distance) {
          name = viewName;
          distance = candidate;
        }
      }
      if (distance < MIN_COLOR_DISTANCE) {
        defects.push([
          "color-confusable",
          `${first} and ${second} sit ${distance.toFixed(1)} apart under ${name}; ` +
            `series colours need ${pyG(MIN_COLOR_DISTANCE)}`,
        ]);
      }
    }
  });
  return defects;
}

const ENTITIES: Record<string, string> = {
  amp: "&",
  lt: "<",
  gt: ">",
  quot: '"',
  apos: "'",
  nbsp: " ",
};

function decodeEntities(text: string): string {
  return text.replace(/&(?:#x([0-9a-fA-F]+)|#(\d+)|([a-zA-Z]+));/g, (whole, hex, dec, name) => {
    if (hex) return String.fromCodePoint(Number.parseInt(hex, 16));
    if (dec) return String.fromCodePoint(Number.parseInt(dec, 10));
    return ENTITIES[name as string] ?? whole;
  });
}

type ScriptPart = { type: string; id: string; src: string | null; text: string };

/** Collects the parts of a chart page the checks read. */
class PageReader {
  lang = "";
  ids = new Map<string, string>();
  text: Record<string, string> = { title: "", h1: "", "viz-summary": "" };
  external: string[] = [];
  scripts: ScriptPart[] = [];
  headerCells: string[] = [];
  unscopedHeaders = 0;
  bodyRows = 0;
  tables = 0;
  captions = 0;
  private open: [string, string][] = [];
  private script: ScriptPart | null = null;
  private inTbody = false;
  private inThead = false;

  feed(html: string): void {
    let position = 0;
    let pending = "";
    const flush = () => {
      if (pending) this.handleData(decodeEntities(pending));
      pending = "";
    };
    while (position < html.length) {
      const next = html.indexOf("<", position);
      if (next === -1) {
        pending += html.slice(position);
        break;
      }
      pending += html.slice(position, next);
      position = next;
      if (html.startsWith("<!--", position)) {
        const end = html.indexOf("-->", position + 4);
        position = end === -1 ? html.length : end + 3;
        continue;
      }
      const tag = /^<(\/?)([a-zA-Z][^\s/>]*)((?:"[^"]*"|'[^']*'|[^'">])*)>/.exec(html.slice(position));
      if (!tag) {
        if (/^<[!?]/.test(html.slice(position, position + 2))) {
          const end = html.indexOf(">", position);
          position = end === -1 ? html.length : end + 1;
          continue;
        }
        pending += "<";
        position += 1;
        continue;
      }
      position += tag[0].length;
      const name = (tag[2] as string).toLowerCase();
      flush();
      if (tag[1]) {
        this.handleEndTag(name);
        continue;
      }
      const raw = tag[3] as string;
      this.handleStartTag(name, parseAttributes(raw));
      if (/\/\s*$/.test(raw)) this.handleEndTag(name);
      else if (name === "script" || name === "style") {
        const close = new RegExp(`</${name}\\s*>`, "i").exec(html.slice(position));
        const end = close ? position + close.index : html.length;
        if (end > position) this.handleData(html.slice(position, end));
        position = close ? end + close[0].length : html.length;
        this.handleEndTag(name);
      }
    }
    flush();
  }

  private handleStartTag(tag: string, attrs: Map<string, string>): void {
    if (tag === "html") this.lang = (attrs.get("lang") ?? "").trim();
    const id = attrs.get("id");
    if (id) this.ids.set(id, tag);
    for (const name of ["src", "href", "poster", "data"]) {
      const value = attrs.get(name) ?? "";
      if (tag !== "a" && EXTERNAL.test(value)) {
        this.external.push(`<${tag} ${name}=${pyRepr(value)}>`);
      }
    }
    if (tag === "script") {
      this.script = {
        type: attrs.get("type") ?? "",
        id: attrs.get("id") ?? "",
        src: attrs.get("src") ?? null,
        text: "",
      };
      const src = attrs.get("src");
      if (src && !EXTERNAL.test(src)) this.external.push(`<script src=${pyRepr(src)}>`);
    } else if (tag === "table") this.tables += 1;
    else if (tag === "caption") this.captions += 1;
    else if (tag === "thead") this.inThead = true;
    else if (tag === "tbody") this.inTbody = true;
    else if (tag === "tr" && this.inTbody) this.bodyRows += 1;
    else if (tag === "th" && this.inThead) {
      this.headerCells.push("");
      if (attrs.get("scope") !== "col") this.unscopedHeaders += 1;
    }
    const key = id === "viz-summary" ? "viz-summary" : tag;
    if (key in this.text || (tag === "th" && this.inThead)) this.open.push([tag, key]);
  }

  private handleEndTag(tag: string): void {
    if (tag === "script" && this.script !== null) {
      this.scripts.push(this.script);
      this.script = null;
    } else if (tag === "thead") this.inThead = false;
    else if (tag === "tbody") this.inTbody = false;
    if (this.open.length > 0 && (this.open.at(-1) as [string, string])[0] === tag) this.open.pop();
  }

  private handleData(data: string): void {
    if (this.script !== null) {
      this.script.text += data;
      return;
    }
    for (const [tag, key] of this.open) {
      if (tag === "th") this.headerCells[this.headerCells.length - 1] += data;
      else this.text[key] += data;
    }
  }
}

function parseAttributes(raw: string): Map<string, string> {
  const attrs = new Map<string, string>();
  const pattern = /([^\s"'<>/=]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?/g;
  for (const match of raw.matchAll(pattern)) {
    const name = (match[1] as string).toLowerCase();
    if (attrs.has(name)) continue;
    attrs.set(name, decodeEntities(match[2] ?? match[3] ?? match[4] ?? ""));
  }
  return attrs;
}

/** A failure the Python checker would have raised as a built-in exception. */
class PyError extends Error {
  constructor(readonly repr: string) {
    super(repr);
  }
}

// Page data is untyped JSON.
type Json = any;

function field(object: Json, key: string): Json {
  if (!object || typeof object !== "object" || Array.isArray(object)) {
    throw new PyError(`TypeError('${Array.isArray(object) ? "list" : "object"} indices must be strings')`);
  }
  if (!(key in object)) throw new PyError(`KeyError(${pyRepr(key)})`);
  return object[key];
}

const MEASURE_LIMIT_MS = 20_000;

/** The page's measurement, or the defect that says why it could not be taken. */
async function measureBounded(html: string): Promise<Measurement | Issue> {
  let timer: ReturnType<typeof setTimeout> | undefined;
  const timeout = new Promise<Issue>((resolve) => {
    timer = setTimeout(
      () => resolve(["measure-failed", `measuring the drawing took more than ${MEASURE_LIMIT_MS / 1000} seconds`]),
      MEASURE_LIMIT_MS,
    );
  });
  try {
    return await Promise.race([measurePage(html), timeout]);
  } catch (error) {
    return ["measure-failed", `measuring the drawing failed: ${(error as Error).message}`];
  } finally {
    clearTimeout(timer);
  }
}

async function checkHtml(text: string): Promise<Issue[]> {
  const page = new PageReader();
  page.feed(text);
  const defects: Issue[] = [];
  const need = (present: unknown, code: string, message: string) => {
    if (!present) defects.push([code, message]);
  };

  need(page.lang, "no-lang", "the html element has no lang attribute");
  need(page.text.title?.trim(), "no-title", "the page has no title");
  need(page.text.h1?.trim(), "no-heading", "the page has no h1 stating what the chart shows");
  need(page.text["viz-summary"]?.trim(), "no-summary", "no text summary with id viz-summary");
  need(page.ids.has("viz-chart"), "no-mount", "no element with id viz-chart for the chart");
  need(
    page.ids.has("viz-status"),
    "no-status",
    "no element with id viz-status to report a failed load",
  );

  for (const found of page.external) {
    defects.push(["external-resource", `${found} loads a file from outside the page`]);
  }

  let shape: unknown = null;
  const dataScripts = page.scripts.filter((script) => script.id === "viz-data");
  if (dataScripts.length > 0) {
    let loaded: Json = null;
    try {
      loaded = JSON.parse((dataScripts[0] as ScriptPart).text);
    } catch {
      loaded = null;
    }
    shape = loaded && typeof loaded === "object" && !Array.isArray(loaded) ? loaded.shape : null;
  }
  const mapUrls = new Set(shape === "choropleth" ? Object.values(MAP_URLS) : []);

  const code = page.scripts
    .filter((script) => script.type === "module" && !script.src)
    .map((script) => script.text)
    .join("\n");
  const specifiers = [...code.matchAll(IMPORT)].map((match) => (match[1] || match[2]) as string);
  const fetched = [...code.matchAll(FETCH)].map((match) => match[1] as string);
  for (const specifier of [...specifiers, ...fetched]) {
    if (specifier === CDN_BASE || specifier.startsWith(`${CDN_BASE}/`)) continue;
    if (mapUrls.has(specifier)) continue;
    if (specifier.includes(CHARTS_PACKAGE)) {
      defects.push([
        "unpinned-import",
        `${pyRepr(specifier)} is not pinned to ${CHARTS_PACKAGE}@${CHARTS_VERSION}`,
      ]);
    } else {
      defects.push([
        "foreign-import",
        `${pyRepr(specifier)} is not a file this kind of page may load`,
      ]);
    }
  }
  const handWritten = shape === "custom" && page.scripts.some((script) => script.id === "viz-layout");
  need(
    specifiers.length > 0 || handWritten,
    "no-chart-import",
    "no module script imports the chart library",
  );
  need(code.includes("ariaLabel"), "no-aria-label", "the chart is mounted without an ariaLabel");

  let rows: Json[] | null = null;
  let tablesWanted = 1;
  let measured: Measurement | null = null;
  let measureFailure: Issue | null = null;
  if (dataScripts.length > 0) {
    const outcome = await measureBounded(text);
    if (Array.isArray(outcome)) measureFailure = outcome;
    else measured = outcome;
  }
  if (dataScripts.length === 0) {
    defects.push(["no-data", "no script with id viz-data holds the data"]);
  } else {
    let colors: Json = [];
    let background: Json = "";
    let unit: Json = null;
    let unitWanted = true;
    try {
      const data = JSON.parse((dataScripts[0] as ScriptPart).text);
      const dataShape = field(data, "shape");
      const graph = dataShape === "sankey" || dataShape === "network";
      const choropleth = dataShape === "choropleth";
      if (graph) {
        const nodes = field(data, "nodes");
        const links = field(data, "links");
        if (!Array.isArray(nodes) || !Array.isArray(links)) {
          throw new PyError("TypeError('can only concatenate list to list')");
        }
        rows = [...nodes, ...links];
      } else {
        rows = field(data, choropleth ? "regions" : "rows");
      }
      colors = field(data, "colors");
      background = field(data, "background");
      unit = field(data, "unit");
      unitWanted = graph ? field(field(data, "prepared"), "weighted") : true;
      if (!rows || !Array.isArray(rows) || rows.length === 0) {
        throw new PyError("ValueError('the data is empty')");
      }
      if (!Array.isArray(colors)) throw new PyError("TypeError('can only concatenate list to list')");
      if (![...colors, background].every((c) => typeof c === "string" && HEX.test(c))) {
        throw new PyError("ValueError('colors and background must be six-digit hex')");
      }
      if (choropleth) {
        const ramp = field(data, "ramp");
        if (
          !Array.isArray(ramp) ||
          ramp.length !== 2 ||
          !ramp.every((c) => typeof c === "string" && HEX.test(c))
        ) {
          throw new PyError("ValueError('ramp must hold two six-digit hex colours')");
        }
        const span = lab(linearRgb(ramp[0]))[0] - lab(linearRgb(ramp[1]))[0];
        if (span < MIN_RAMP_LIGHTNESS_SPAN) {
          defects.push([
            "ramp-flat",
            `the ramp runs ${span.toFixed(0)} lightness steps from light to dark; ` +
              `a reader needs ${pyG(MIN_RAMP_LIGHTNESS_SPAN)} to rank regions`,
          ]);
        }
        let drawable: Set<string>;
        if (field(data, "features") === null) {
          const atlas = JSON.parse(readFileSync(ATLAS, "utf-8")) as { regions: { name: string }[] };
          drawable = new Set(atlas.regions.map((region) => region.name));
        } else {
          drawable = new Set(field(data, "features").map((feature: Json) => field(feature, "id")));
        }
        for (const region of rows) {
          if (!drawable.has(field(region, "key"))) {
            defects.push([
              "region-unmatched",
              `no shape on the map has the key ${pyRepr(field(region, "key"))}`,
            ]);
          }
        }
      }
      if (graph) {
        tablesWanted = 2;
        const known = new Set(data.nodes.map((node: Json) => field(node, "id")));
        for (const link of data.links) {
          for (const end of [field(link, "source"), field(link, "target")]) {
            if (!known.has(end)) {
              defects.push(["link-unknown-node", `a link names ${pyRepr(end)}, which no node has`]);
            }
          }
        }
      }
      // A map is coloured by its ramp, which the ramp check covers; its no-value grey is meant to recede.
      const painted = choropleth ? [] : (measured?.colors ?? []);
      defects.push(...colorDefects([...new Set([...colors, ...painted])], background));
      const named = typeof unit === "string" && unit.trim();
      if (unitWanted) need(named, "no-unit", "viz-data names no unit for the values");
      if (unitWanted && named) {
        need(
          page.headerCells.some((cell) => cell.toLowerCase().includes(unit.trim().toLowerCase())),
          "no-unit",
          `no table header names the unit ${pyRepr(unit)}`,
        );
      }
    } catch (error) {
      if (error instanceof SyntaxError) {
        defects.push(["bad-data", `viz-data is unusable: ValueError(${pyRepr(error.message)})`]);
      } else if (error instanceof PyError) {
        defects.push(["bad-data", `viz-data is unusable: ${error.repr}`]);
      } else if (error instanceof TypeError) {
        defects.push(["bad-data", `viz-data is unusable: TypeError(${pyRepr(error.message)})`]);
      } else throw error;
      rows = null;
    }
  }

  if (page.tables < tablesWanted) {
    defects.push([
      "no-table",
      `the page has ${page.tables} data tables and needs ${tablesWanted}`,
    ]);
  } else {
    need(page.captions >= page.tables, "table-no-caption", "a data table has no caption");
    need(page.unscopedHeaders === 0, "table-no-scope", "a table header cell lacks scope=col");
    if (rows !== null && page.bodyRows !== rows.length) {
      defects.push([
        "table-row-mismatch",
        `the table has ${page.bodyRows} rows and the data has ${rows.length}`,
      ]);
    }
  }
  if (measureFailure) defects.push(measureFailure);
  for (const { code: measuredCode, message } of measured?.defects ?? []) {
    defects.push([measuredCode, message]);
  }
  return defects;
}

const LINE_BREAK = new RegExp("\\r\\n|[\\n\\r\\v\\f\\x1c-\\x1e\\x85\\u2028\\u2029]");

/** The info string and body lines of each fenced code block. */
function fencedBlocks(text: string): [string, string[]][] {
  const blocks: [string, string[]][] = [];
  let current: [string, string[]] | null = null;
  let fence = "";
  for (const line of text.split(LINE_BREAK)) {
    const stripped = line.trim();
    const opener = /^(`{3,}|~{3,})\s*(\S*)/.exec(stripped);
    if (current === null && opener) {
      fence = opener[1] as string;
      current = [opener[2] as string, []];
    } else if (
      current !== null &&
      stripped.startsWith(fence) &&
      [...stripped].every((char) => char === fence.charAt(0))
    ) {
      blocks.push(current);
      current = null;
    } else if (current !== null) current[1].push(line);
  }
  return blocks;
}

function balanced(source: string): boolean {
  const pairs: Record<string, string> = { ")": "(", "]": "[", "}": "{" };
  const stack: string[] = [];
  for (const char of source.replace(/"[^"\n]*"/g, "")) {
    if ("([{".includes(char)) stack.push(char);
    else if (char in pairs && stack.pop() !== pairs[char]) return false;
  }
  return stack.length === 0;
}

function barDefects(lines: string[]): Issue[] {
  const bars: [string, number, number][] = [];
  for (const line of lines) {
    const match = BAR_LINE.exec(line);
    const number = match ? NUMBER.exec(match.groups?.rest as string) : null;
    if (match && number) {
      const drawn = match.groups?.bar as string;
      let length = 0;
      for (const char of drawn) {
        if (char === "█") length += 1;
        else if (PARTIAL_BLOCKS.includes(char)) length += (PARTIAL_BLOCKS.indexOf(char) + 1) / 8;
      }
      bars.push([match.groups?.label as string, length, Number(number[0].replaceAll(",", ""))]);
    }
  }
  if (bars.length < 2) return [];
  let widest = bars[0] as [string, number, number];
  for (const bar of bars) if (bar[2] > widest[2]) widest = bar;
  const [, longest, largest] = widest;
  if (largest <= 0) return [];
  const defects: Issue[] = [];
  for (const [label, length, value] of bars) {
    const expected = (value / largest) * longest;
    if (Math.abs(length - expected) > 1) {
      defects.push([
        "bar-not-proportional",
        `${pyRepr(label)} draws ${pyG(length)} blocks for ${pyG(value)}; in proportion it draws ` +
          `${expected.toFixed(1)}`,
      ]);
    }
  }
  return defects;
}

function checkMarkdown(text: string): Issue[] {
  const defects: Issue[] = [];
  for (const [info, lines] of fencedBlocks(text)) {
    if (info === "mermaid") {
      const body = lines.filter((line) => line.trim() && !line.trim().startsWith("%%"));
      const keyword = body.length > 0 ? ((body[0] as string).split(/\s+/).find(Boolean) ?? "") : "";
      if (!MERMAID_TYPES.has(keyword)) {
        defects.push(["mermaid-unknown-type", `a mermaid block opens with ${pyRepr(keyword)}`]);
      }
      if (!balanced(body.join("\n"))) {
        defects.push(["mermaid-unbalanced", "a mermaid block has unbalanced brackets"]);
      }
    } else defects.push(...barDefects(lines));
  }

  const outside = text.replace(/^(`{3,}|~{3,}).*?^\1\s*$/gms, "");
  let table: string[] = [];
  for (const line of [...outside.split(LINE_BREAK), ""]) {
    if (line.trim().startsWith("|")) {
      table.push(line.trim());
      continue;
    }
    if (table.length >= 2) {
      const widths = new Set(
        table.map((row) => row.replace(/^\|+|\|+$/g, "").split(/(?<!\\)\|/).length),
      );
      const head = pyRepr((table[0] as string).slice(0, 40));
      if (!/^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?$/.test(table[1] as string)) {
        defects.push(["table-no-separator", `the table starting ${head} has no header separator`]);
      } else if (widths.size > 1) {
        defects.push(["table-ragged", `the table starting ${head} has rows of differing widths`]);
      }
    }
    table = [];
  }
  return defects;
}

/** Defects for one file. Throws for a file this script cannot check. */
async function checkFile(path: string): Promise<Issue[]> {
  const text = readFileSync(path, "utf-8");
  const suffix = extname(path).toLowerCase();
  if (suffix === ".html" || suffix === ".htm") return checkHtml(text);
  if (suffix === ".md" || suffix === ".markdown") return checkMarkdown(text);
  throw new Error(`${extname(path) || "no"} extension; this script checks .html and .md`);
}

const ERRNO: Record<string, [number, string]> = {
  ENOENT: [2, "No such file or directory"],
  EACCES: [13, "Permission denied"],
  ENOTDIR: [20, "Not a directory"],
  EISDIR: [21, "Is a directory"],
};

function describe(error: unknown, path: string): string {
  const entry = ERRNO[(error as { code?: string }).code ?? ""];
  return entry ? `[Errno ${entry[0]}] ${entry[1]}: ${pyRepr(path)}` : (error as Error).message;
}

const USAGE = `Check a finished visualization before it is handed over.

Reads each HTML chart page or Markdown file and reports every defect that would
leave a reader without the chart, its values, or its meaning.

  bun --install=fallback check_output.ts PATH [PATH ...]

Prints one \`path: code: message\` line per defect, or \`path: ok\`.
Exit codes: 0 no defect, 1 defects found, 2 a path cannot be read or checked.`;

export async function main(argv: string[]): Promise<number> {
  if (argv.length === 0 || argv[0] === "-h" || argv[0] === "--help") {
    console.log(USAGE);
    return argv.length > 0 ? 0 : 2;
  }
  let worst = 0;
  for (const path of argv) {
    let defects: Issue[];
    try {
      defects = await checkFile(path);
    } catch (error) {
      console.error(`${path}: cannot check: ${describe(error, path)}`);
      worst = 2;
      continue;
    }
    if (defects.length === 0) console.log(`${path}: ok`);
    for (const [code, message] of defects) console.log(`${path}: ${code}: ${message}`);
    if (defects.length > 0) worst = Math.max(worst, 1);
  }
  return worst;
}

if (import.meta.main) process.exit(await main(process.argv.slice(2)));
