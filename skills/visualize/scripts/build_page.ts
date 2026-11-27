/**
 * Build one self-contained HTML chart page from a spec and prepared rows.
 *
 * The page holds its data, a text summary, and a data table, and loads the chart
 * library by pinned https import when it opens.
 *
 *   bun --install=fallback build_page.ts SPEC.json --data ROWS.json --out PAGE.html [--chart-js FILE]
 *
 * ROWS.json is the file prepare_data.ts writes: rows for bar, line, area, and
 * scatter, nodes and links for sankey and network, or regions for choropleth.
 * `--chart-js` replaces the generated chart definition with hand-written code.
 *
 * Exit codes: 0 page written, 1 the spec and the data disagree, 2 unusable input.
 */

import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { parseArgs } from "node:util";
import { type Issue, pyDumps, pyG, pyRepr, pyStr, strerror, Unusable } from "./prepare_data.ts";

export const CHARTS_PACKAGE = "@tanstack/charts";
export const CHARTS_VERSION = "1.5.0";
export const CDN_BASE = `https://esm.sh/${CHARTS_PACKAGE}@${CHARTS_VERSION}`;

const BACKGROUND = "#ffffff";
const PALETTE = ["#0072b2", "#d55e00", "#009e73", "#cc79a7", "#000000"];

const ROW_CHARTS = ["bar", "line", "area", "scatter"];
const GRAPH_CHARTS = ["sankey", "network"];
const OWN_SHAPE_CHARTS = [...GRAPH_CHARTS, "choropleth"];
const CHARTS = [...ROW_CHARTS, ...OWN_SHAPE_CHARTS];

// A choropleth loads what the chart library leaves to the page: the projection, the
// continuous colour scale, and the world atlas with its converter.
export const MAP_URLS: Record<string, string> = {
  projection: "https://esm.sh/d3-geo@3.1.1",
  scale: "https://esm.sh/d3-scale@4.0.2",
  converter: "https://esm.sh/topojson-client@3.1.0",
  atlas: "https://esm.sh/world-atlas@2.0.2/countries-110m.json",
};
const RAMP = ["#deebf7", "#08519c"];
const NO_VALUE_COLOR = "#f1f3f5";
const MAX_NODES: Record<string, number> = { sankey: 40, network: 60 };
const LINK_COLOR = "#6c757d";
const PREPARED_KEYS: Record<string, string[]> = {
  rows: ["x", "y", "series", "xType", "seriesValues", "rows"],
  sankey: ["weighted", "groupValues", "nodes", "links"],
  network: ["weighted", "groupValues", "nodes", "links"],
  choropleth: ["atlas", "regionsWithoutValue", "regions", "features"],
};
const TEMPLATE = join(dirname(import.meta.dir), "assets", "page.html");

// Spec and prepared data are untyped JSON.
type Json = any;
type Imports = Record<string, string[]>;

function loadJson(path: string): Json {
  let text: string;
  try {
    text = readFileSync(path, "utf-8");
  } catch (error) {
    throw new Unusable(`cannot read ${path}: ${strerror(error)}`);
  }
  try {
    return JSON.parse(text);
  } catch (error) {
    throw new Unusable(`${path} is not valid JSON: ${(error as Error).message}`);
  }
}

function textAt(spec: Json, dotted: string): string {
  let value = spec;
  for (const part of dotted.split(".")) {
    value = value && typeof value === "object" && !Array.isArray(value) ? value[part] : null;
  }
  return typeof value === "string" ? value.trim() : "";
}

function isObject(value: unknown): boolean {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function validate(spec: Json, prepared: Json): Issue[] {
  const problems: Issue[] = [];
  const chart = spec.chart;
  const shape = prepared.shape;
  if (CHARTS.includes(chart)) {
    const wanted = OWN_SHAPE_CHARTS.includes(chart) ? chart : "rows";
    if (shape !== wanted) {
      return [
        [
          "chart-data-mismatch",
          `a ${chart} chart draws data prepared with --shape ${wanted}; ` +
            `this data was prepared with --shape ${shape}`,
        ],
      ];
    }
  }
  if (shape === "choropleth") return validateChoropleth(spec, prepared);
  if (shape !== "rows") return validateGraph(spec, prepared);
  const xType = prepared.xType;
  const series = prepared.series;
  const rows: Json[] = prepared.rows;

  const required = ["title", "summary", "x.label", "y.label", "y.unit"];
  if (series) required.push("series.label");
  if (chart === "scatter") required.push("x.unit");
  for (const dotted of required) {
    if (!textAt(spec, dotted)) {
      problems.push(["spec-missing", `the spec needs a non-empty ${dotted}`]);
    }
  }

  if (!CHARTS.includes(chart)) {
    problems.push(["chart-unknown", `chart is ${pyRepr(chart)}; this script draws ${CHARTS.join(", ")}`]);
    return problems;
  }

  const ordered = Boolean(isObject(spec.x) && spec.x.ordered);
  if (chart === "bar" && xType === "number") {
    problems.push([
      "chart-data-mismatch",
      "bars need categories on x; a numeric x reads as a scatter or a line",
    ]);
  }
  if ((chart === "line" || chart === "area") && xType === "category" && !ordered) {
    problems.push([
      "chart-data-mismatch",
      `a ${chart} joins neighbours, so x must be a date, a number, or categories with ` +
        "a real order; set x.ordered to true for ordered categories, or draw bars",
    ]);
  }
  if (chart === "scatter" && xType !== "number") {
    problems.push(["chart-data-mismatch", "a scatter needs a number on x"]);
  }

  if (prepared.seriesValues.length > PALETTE.length) {
    problems.push([
      "too-many-series",
      `${prepared.seriesValues.length} series exceed the ${PALETTE.length} colours that stay ` +
        "distinct; keep the series the claim needs and fold the rest into one",
    ]);
  }
  const stacked = chart === "area" || (chart === "bar" && spec.bars === "stacked");
  if (series && stacked && rows.some((row) => row[prepared.y] < 0)) {
    problems.push([
      "stack-negative",
      "a stack cannot show values below zero; draw grouped bars or lines",
    ]);
  }
  if (chart === "line" || chart === "area") {
    const counts = new Map<unknown, number>();
    for (const row of rows) {
      const key = row[series] ?? null;
      counts.set(key, (counts.get(key) ?? 0) + 1);
    }
    if (Math.min(...counts.values()) < 2) {
      problems.push(["too-few-points", `a ${chart} needs two or more points in every series`]);
    }
  }
  return problems;
}

function validateGraph(spec: Json, prepared: Json): Issue[] {
  const problems: Issue[] = [];
  const chart = spec.chart;
  const required = ["title", "summary", "nodes.label"];
  if (prepared.weighted) required.push("value.label", "value.unit");
  if (prepared.groupValues.length > 0) required.push("group.label");
  for (const dotted of required) {
    if (!textAt(spec, dotted)) {
      problems.push(["spec-missing", `the spec needs a non-empty ${dotted}`]);
    }
  }
  if (!CHARTS.includes(chart)) {
    problems.push(["chart-unknown", `chart is ${pyRepr(chart)}; this script draws ${CHARTS.join(", ")}`]);
    return problems;
  }
  if (prepared.nodes.length > (MAX_NODES[chart] as number)) {
    problems.push([
      "too-many-nodes",
      `${prepared.nodes.length} nodes exceed the ${MAX_NODES[chart]} a ${chart} keeps ` +
        "readable; combine nodes, or show the links as a table",
    ]);
  }
  if (prepared.groupValues.length > PALETTE.length) {
    problems.push([
      "too-many-series",
      `${prepared.groupValues.length} groups exceed the ${PALETTE.length} colours that ` +
        "stay distinct; keep the groups the claim needs and fold the rest into one",
    ]);
  }
  return problems;
}

function validateChoropleth(spec: Json, prepared: Json): Issue[] {
  const problems: Issue[] = [];
  for (const dotted of ["title", "summary", "region.label", "value.label", "value.unit"]) {
    if (!textAt(spec, dotted)) {
      problems.push(["spec-missing", `the spec needs a non-empty ${dotted}`]);
    }
  }
  if (!CHARTS.includes(spec.chart)) {
    problems.push([
      "chart-unknown",
      `chart is ${pyRepr(spec.chart)}; this script draws ${CHARTS.join(", ")}`,
    ]);
    return problems;
  }
  const values = new Set(prepared.regions.map((region: Json) => region.value));
  if (values.size < 2) {
    problems.push([
      "constant-values",
      "every region holds the same value, so a map shows one colour; state the value in a sentence",
    ]);
  }
  return problems;
}

function axisLabel(axis: Json): string {
  const label = axis.label.trim();
  const unit = (axis.unit || "").trim();
  return unit && !label.toLowerCase().includes(unit.toLowerCase()) ? `${label} (${unit})` : label;
}

/** Order bar categories by total value unless the spec keeps the given order. */
function categoryDomain(spec: Json, prepared: Json): unknown[] {
  const { x, y } = prepared;
  const totals = new Map<unknown, number>();
  for (const row of prepared.rows) totals.set(row[x], (totals.get(row[x]) ?? 0) + row[y]);
  const given = [...totals.keys()];
  const keepGiven = spec.sort === "given" || prepared.xType === "date" || spec.x.ordered;
  return keepGiven
    ? given
    : [...given].sort((a, b) => (totals.get(b) as number) - (totals.get(a) as number));
}

/** Tick whole days as dates, one tick per observed day while they fit the axis. */
function dateTicks(prepared: Json): string {
  const days = [...new Set<string>(prepared.rows.map((row: Json) => row[prepared.x]))].sort();
  if (days.some((day) => day.length !== 10)) return "";
  const parts: Record<string, string> = { month: "short", day: "numeric", timeZone: "UTC" };
  if ((days[0] as string).slice(0, 4) !== (days.at(-1) as string).slice(0, 4)) {
    parts.year = "numeric";
  }
  const label = `format: (value) => new Intl.DateTimeFormat('en', ${pyDumps(parts)}).format(value)`;
  const values =
    days.length <= 8 ? `values: ${pyDumps(days)}.map((day) => new Date(day)), ` : "";
  return `, ticks: { ${values}${label} }`;
}

/** Import names by subpath, and the JavaScript body that returns the definition. */
function chartJs(spec: Json, prepared: Json): [Imports, string] {
  const chart = spec.chart;
  const x = pyDumps(prepared.x);
  const y = pyDumps(prepared.y);
  const series = pyDumps(prepared.series);
  const hasSeries = Boolean(prepared.series);
  const xType = prepared.xType;
  const horizontal = chart === "bar" && spec.orientation === "horizontal";
  const root = new Set(["defineChart"]);
  const scales: Record<string, string> = { linear: "scaleLinear" };
  const lines: string[] = [];

  if (xType === "date" && chart !== "bar") {
    lines.push(`const rows = data.rows.map((row) => ({ ...row, [${x}]: new Date(row[${x}]) }))`);
  } else {
    lines.push("const rows = data.rows");
  }

  const measure = `{ scale: scaleLinear, nice: true, grid: true, axis: { label: ${pyDumps(axisLabel(spec.y))} } }`;
  const positionLabel = pyDumps(axisLabel(spec.x));
  const paint = hasSeries ? "" : `, fill: ${pyDumps(PALETTE[0])}`;
  const stroke = hasSeries ? "" : `, stroke: ${pyDumps(PALETTE[0])}`;
  const marks: string[] = [];
  let xScale: string;
  let yScale: string;

  if (chart === "bar") {
    scales.band = "scaleBand";
    const domain = pyDumps(categoryDomain(spec, prepared));
    const position = `{ scale: () => scaleBand().domain(${domain}).padding(0.16), axis: { label: ${positionLabel} } }`;
    let layout = "";
    if (hasSeries && spec.bars !== "stacked") {
      root.add("group");
      layout = ", layout: group()";
    }
    const colour = hasSeries ? `, color: ${series}` : "";
    if (horizontal) {
      root.add("barX");
      marks.push(`barX(rows, { x: ${y}, y: ${x}${colour}${layout}, inset: 2${paint} })`);
      xScale = measure;
      yScale = position;
    } else {
      root.add("barY");
      marks.push(`barY(rows, { x: ${x}, y: ${y}${colour}${layout}, inset: 2${paint} })`);
      xScale = position;
      yScale = measure;
    }
  } else {
    if (xType === "date") {
      scales.time = "scaleUtc";
      xScale = `{ scale: scaleUtc, axis: { label: ${positionLabel}${dateTicks(prepared)} } }`;
    } else if (xType === "number") {
      xScale = `{ scale: scaleLinear, nice: true, axis: { label: ${positionLabel} } }`;
    } else {
      scales.point = "scalePoint";
      xScale = `{ scale: () => scalePoint().padding(0.2), axis: { label: ${positionLabel} } }`;
    }
    yScale = measure;
    const groupBy = hasSeries ? `, z: ${series}` : "";
    if (chart === "line") {
      root.add("lineY");
      marks.push(`lineY(rows, { x: ${x}, y: ${y}${groupBy}, points: true${stroke} })`);
    } else if (chart === "area") {
      root.add("areaY");
      root.add("ruleY");
      let stack = "";
      if (hasSeries) {
        root.add("stack");
        stack = `, color: ${series}, layout: stack()`;
      }
      marks.push(`areaY(rows, { x: ${x}, y: ${y}${stack}, fillOpacity: 0.8${paint} })`);
      marks.push("ruleY([0])");
    } else {
      root.add("dot");
      marks.push(`dot(rows, { x: ${x}, y: ${y}${groupBy}, r: 4${paint} })`);
    }
  }

  lines.push("return defineChart({");
  lines.push("  marks: [");
  for (const mark of marks) lines.push(`    ${mark},`);
  lines.push("  ],");
  lines.push(`  scales: {\n    x: ${xScale},\n    y: ${yScale},\n  },`);
  if (hasSeries) {
    root.add("colorLegend");
    const legend = pyDumps(spec.series.label.trim());
    lines.push("  color: {");
    lines.push("    domain: data.prepared.seriesValues,");
    lines.push("    range: data.colors,");
    lines.push(`    legend: colorLegend({ label: ${legend} }),`);
    lines.push("  },");
  }
  lines.push("  tooltip,");
  lines.push("})");

  const imports: Imports = { "": [...root].sort(), "/tooltip": ["tooltip"] };
  for (const [subpath, name] of Object.entries(scales)) imports[`/scales/${subpath}`] = [name];
  return [imports, lines.join("\n")];
}

function sankeyJs(): [Imports, string] {
  const color = pyDumps(PALETTE[0]);
  const body = `const amount = (value) => value.toLocaleString("en")
const ribbon = {
  line: ([[x1, y1], [x2, y2]]) =>
    \`M\${x1},\${y1}C\${(x1 + x2) / 2},\${y1} \${(x1 + x2) / 2},\${y2} \${x2},\${y2}\`,
  area: () => "",
}
return defineChart({
  marks: [
    sankeyDiagram({
      nodes: data.nodes,
      links: data.links,
      nodeKey: "id",
      source: "source",
      target: "target",
      value: "value",
      nodeWidth: 14,
      nodePadding: 18,
      inset: 8,
      marks: ({ nodes, links }) => {
        const lastLayer = Math.max(...nodes.map((node) => node.layer))
        const onRight = (node) => node.layer === lastLayer
        return [
          link(links, {
            x1: "x1", y1: "y1", x2: "x2", y2: "y2", key: "key",
            strokeWidth: (flow) => Math.max(1, flow.width),
            stroke: ${color}, strokeOpacity: 0.35, lineCap: "butt", curve: ribbon,
          }),
          rect(nodes, { x1: "x0", x2: "x1", y1: "y0", y2: "y1", key: "key", inset: 0, fill: ${color} }),
          text(nodes, {
            x: (node) => (onRight(node) ? node.x0 : node.x1),
            y: "y",
            text: (node) => \`\${node.data.label} \${amount(node.value)}\`,
            key: "key",
            anchor: (node) => (onRight(node) ? "end" : "start"),
            dx: (node) => (onRight(node) ? -6 : 6),
            dy: 4,
            fill: "currentColor",
            fontSize: 12,
          }),
        ]
      },
    }),
  ],
  scales: { x: null, y: null },
  guides: false,
  margin: 0,
})`;
  return [
    { "": ["defineChart", "link", "rect", "text"], "/network/sankey": ["sankeyDiagram"] },
    body,
  ];
}

function networkJs(spec: Json, prepared: Json): [Imports, string] {
  const grouped = prepared.groupValues.length > 0;
  const root = ["defineChart", "dot", "link", "text"];
  let width = "1.5";
  if (prepared.weighted) width = "(edge) => 1 + (5 * edge.value) / largest";
  const paint = grouped ? 'color: "group"' : `fill: ${pyDumps(PALETTE[0])}`;
  const lines = [
    "const largest = Math.max(1, ...data.links.map((edge) => edge.value ?? 1))",
    "const graph = forceLayout(data.nodes, data.links, {",
    '  nodeKey: "id",',
    '  source: "source",',
    '  target: "target",',
    "  iterations: 300,",
    "  forces: [",
    '    { type: "link", distance: 48 },',
    '    { type: "manyBody", strength: -160 },',
    '    { type: "center" },',
    '    { type: "collide", radius: 16 },',
    "  ],",
    "})",
    "return defineChart({",
    "  marks: [",
    "    link(graph.links, {",
    '      x1: "x1", y1: "y1", x2: "x2", y2: "y2",',
    "      key: (edge) => `${edge.source}->${edge.target}`,",
    `      stroke: ${pyDumps(LINK_COLOR)}, strokeWidth: ${width},`,
    "    }),",
    `    dot(graph.nodes, { x: "x", y: "y", key: "id", r: 6, ${paint} }),`,
    "    text(graph.nodes, {",
    '      x: "x", y: "y", text: "label", key: "id", dy: -10, fill: "currentColor", fontSize: 11,',
    "    }),",
    "  ],",
    "  scales: {",
    "    x: { scale: () => scaleLinear().domain(graph.xDomain), axis: false },",
    "    y: { scale: () => scaleLinear().domain(graph.yDomain), axis: false },",
    "  },",
  ];
  if (grouped) {
    root.push("colorLegend");
    const legend = pyDumps(spec.group.label.trim());
    lines.push(
      "  color: {",
      "    domain: data.prepared.groupValues,",
      "    range: data.colors,",
      `    legend: colorLegend({ label: ${legend} }),`,
      "  },",
    );
  }
  lines.push("})");
  return [
    {
      "": [...root].sort(),
      "/network/force": ["forceLayout"],
      "/scales/linear": ["scaleLinear"],
    },
    lines.join("\n"),
  ];
}

function choroplethJs(spec: Json, prepared: Json): [Imports, string] {
  const world = prepared.atlas === "world";
  const url: Record<string, string> = {};
  for (const [name, value] of Object.entries(MAP_URLS)) url[name] = pyDumps(value);
  const legend = pyDumps(axisLabel(spec.value));
  const lines = [
    `const { ${world ? "geoEqualEarth" : "geoMercator"} } = await import(${url.projection})`,
    `const { scaleSequential } = await import(${url.scale})`,
  ];
  if (world) {
    lines.push(
      `const { feature } = await import(${url.converter})`,
      `const response = await fetch(${url.atlas})`,
      "if (!response.ok) throw new Error(`The world atlas answered ${response.status}.`)",
      "const topology = await response.json()",
      "const features = feature(topology, topology.objects.countries).features.map(",
      "  (shape) => ({ ...shape, id: shape.properties.name }),",
      ")",
      'const projection = { type: geoEqualEarth, fit: "sphere", inset: 4 }',
    );
  } else {
    lines.push(
      "const features = data.features",
      'const projection = { type: geoMercator, fit: { type: "FeatureCollection", features }, inset: 4 }',
    );
  }
  lines.push(
    "const values = new Map(data.regions.map((region) => [region.key, region.value]))",
    "const channel = (hex, index) => parseInt(hex.slice(1 + 2 * index, 3 + 2 * index), 16)",
    "const [light, dark] = data.ramp",
    "const ramp = (t) =>",
    "  `rgb(${[0, 1, 2]",
    "    .map((i) => Math.round(channel(light, i) + t * (channel(dark, i) - channel(light, i))))",
    '    .join(",")})`',
    "const extent = [data.regions.at(-1).value, data.regions[0].value]",
    `const edge = { key: (shape) => shape.id, projection, stroke: ${pyDumps(LINK_COLOR)}, strokeWidth: 0.5 }`,
    "const layers = [",
    `  [features.filter((shape) => !values.has(shape.id)), { ...edge, fill: ${pyDumps(NO_VALUE_COLOR)} }],`,
    "  [features.filter((shape) => values.has(shape.id)), { ...edge, color: (shape) => values.get(shape.id) }],",
    "]",
    "return defineChart({",
    "  marks: layers.filter(([shapes]) => shapes.length).map(([shapes, options]) => geoShape(shapes, options)),",
    "  scales: { x: null, y: null },",
    "  color: {",
    "    scale: () => scaleSequential(ramp).domain(extent),",
    `    legend: colorLegend({ label: ${legend}, format: (value) => value.toLocaleString("en") }),`,
    "  },",
    "})",
  );
  return [{ "": ["colorLegend", "defineChart"], "/geo": ["geoShape"] }, lines.join("\n")];
}

function importLines(imports: Imports): string {
  const all: Imports = { ...imports, "/dom": ["mountChart"] };
  return Object.entries(all)
    .sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0))
    .map(
      ([subpath, names]) =>
        `  const { ${names.join(", ")} } = await import(${pyDumps(CDN_BASE + subpath)})`,
    )
    .join("\n");
}

/** Python's `html.escape`. */
export function htmlEscape(text: string): string {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#x27;");
}

function withGrouping(text: string): string {
  const [whole = "", fraction] = text.split(".");
  const sign = whole.startsWith("-") ? "-" : "";
  const digits = whole.replace("-", "").replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return fraction === undefined ? `${sign}${digits}` : `${sign}${digits}.${fraction}`;
}

function formatCell(value: unknown): string {
  if (typeof value !== "number") return htmlEscape(pyStr(value));
  if (Number.isInteger(value)) return withGrouping(String(value));
  const text = pyG(value);
  return text.includes("e") ? text : withGrouping(text);
}

function tableHtml(spec: Json, prepared: Json): string {
  const { x, y, series } = prepared;
  const columns: [string, string, boolean][] = [[x, axisLabel(spec.x), prepared.xType === "number"]];
  if (series) columns.push([series, spec.series.label.trim(), false]);
  columns.push([y, axisLabel(spec.y), true]);
  return oneTable(
    spec.title.trim(),
    columns.map(([, label, numeric]) => [label, numeric]),
    prepared.rows.map((row: Json) => columns.map(([field]) => row[field])),
  );
}

/** Render one table from (header, is numeric) columns and rows of cell values. */
function oneTable(caption: string, columns: [string, boolean][], rows: unknown[][]): string {
  const out = ["<table>", `<caption>${htmlEscape(caption)}</caption>`, "<thead><tr>"];
  for (const [label, numeric] of columns) {
    const css = numeric ? ' class="num"' : "";
    out.push(`<th scope="col"${css}>${htmlEscape(label)}</th>`);
  }
  out.push("</tr></thead>");
  out.push("<tbody>");
  for (const row of rows) {
    const cells = columns
      .map(([, numeric], index) => `${numeric ? '<td class="num">' : "<td>"}${formatCell(row[index])}</td>`)
      .join("");
    out.push(`<tr>${cells}</tr>`);
  }
  out.push("</tbody>");
  out.push("</table>");
  return out.join("\n");
}

/** The node table and the link table that stand in for a sankey or a network. */
function graphTablesHtml(spec: Json, prepared: Json): string {
  const { nodes, links, weighted } = prepared;
  const label = new Map<string, string>(nodes.map((node: Json) => [node.id, node.label]));
  const amount = weighted ? axisLabel(spec.value) : "";
  const title = spec.title.trim();

  const nodeColumns: [string, boolean][] = [[spec.nodes.label.trim(), false]];
  if (prepared.groupValues.length > 0) nodeColumns.push([spec.group.label.trim(), false]);
  if (spec.chart === "sankey") {
    nodeColumns.push([`In: ${amount}`, true], [`Out: ${amount}`, true]);
  } else nodeColumns.push(["Links", true]);
  const nodeRows = nodes.map((node: Json) => {
    const entering = links.filter((link: Json) => link.target === node.id);
    const leaving = links.filter((link: Json) => link.source === node.id);
    const row: unknown[] = [node.label];
    if (prepared.groupValues.length > 0) row.push(node.group);
    if (spec.chart === "sankey") {
      row.push(
        entering.reduce((sum: number, link: Json) => sum + link.value, 0),
        leaving.reduce((sum: number, link: Json) => sum + link.value, 0),
      );
    } else row.push(entering.length + leaving.length);
    return row;
  });

  const linkColumns: [string, boolean][] = [["From", false], ["To", false]];
  if (weighted) linkColumns.push([amount, true]);
  const linkRows = links.map((link: Json) => {
    const row: unknown[] = [label.get(link.source), label.get(link.target)];
    if (weighted) row.push(link.value);
    return row;
  });
  return [
    oneTable(`${title}: nodes`, nodeColumns, nodeRows),
    oneTable(`${title}: links`, linkColumns, linkRows),
  ].join("\n");
}

function indent(text: string, prefix: string): string {
  return text
    .split(/\r\n|\r|\n/)
    .map((line) => (line ? prefix + line : line))
    .join("\n");
}

function strip(text: string, char: string): string {
  let start = 0;
  let end = text.length;
  while (start < end && text.charAt(start) === char) start += 1;
  while (end > start && text.charAt(end - 1) === char) end -= 1;
  return text.slice(start, end);
}

function build(spec: Json, prepared: Json, customJs: string | null): string {
  const shape = prepared.shape;
  let body: string;
  let importsText: string;
  if (customJs !== null) {
    body = strip(customJs, "\n");
    importsText = importLines({});
  } else {
    let imports: Imports;
    if (shape === "choropleth") [imports, body] = choroplethJs(spec, prepared);
    else if (shape === "sankey") [imports, body] = sankeyJs();
    else if (shape === "network") [imports, body] = networkJs(spec, prepared);
    else [imports, body] = chartJs(spec, prepared);
    importsText = importLines(imports);
  }

  const data: Json = { spec, shape, background: BACKGROUND };
  let footnote = "";
  let height: number;
  let table: string;
  const pick = (keys: string[]) => Object.fromEntries(keys.map((key) => [key, prepared[key]]));
  if (shape === "choropleth") {
    height = 420;
    data.prepared = pick(["atlas", "regionsWithoutValue"]);
    data.colors = RAMP.slice(1);
    data.ramp = RAMP;
    data.unit = spec.value.unit;
    data.regions = prepared.regions;
    data.features = prepared.features;
    table = oneTable(
      spec.title.trim(),
      [
        [spec.region.label.trim(), false],
        [axisLabel(spec.value), true],
      ],
      prepared.regions.map((region: Json) => [region.label, region.value]),
    );
    if (prepared.regionsWithoutValue) footnote = '<p class="source">Regions in grey have no value.</p>';
  } else if (shape === "rows") {
    const horizontal = spec.chart === "bar" && spec.orientation === "horizontal";
    height = horizontal
      ? Math.max(240, 80 + 30 * new Set(prepared.rows.map((row: Json) => row[prepared.x])).size)
      : 380;
    data.prepared = pick(["x", "y", "series", "xType", "seriesValues"]);
    data.colors = PALETTE.slice(0, Math.max(1, prepared.seriesValues.length));
    data.unit = spec.y.unit;
    data.rows = prepared.rows;
    table = tableHtml(spec, prepared);
  } else {
    height = 460;
    data.prepared = pick(["weighted", "groupValues"]);
    data.colors = PALETTE.slice(0, Math.max(1, prepared.groupValues.length));
    data.unit = prepared.weighted ? spec.value.unit : null;
    data.nodes = prepared.nodes;
    data.links = prepared.links;
    table = graphTablesHtml(spec, prepared);
  }
  const subtitle = textAt(spec, "subtitle");
  const source = textAt(spec, "source");
  const replacements: [string, string][] = [
    ["__TITLE__", htmlEscape(spec.title.trim())],
    ["__SUBTITLE__", subtitle ? `<p class="subtitle">${htmlEscape(subtitle)}</p>` : ""],
    ["__SUMMARY__", htmlEscape(spec.summary.trim())],
    ["__SOURCE__", (source ? `<p class="source">Source: ${htmlEscape(source)}</p>` : "") + footnote],
    ["__TABLE__", table],
    ["__DATA__", pyDumps(data, false).replaceAll("</", "<\\/")],
    ["__IMPORTS__", importsText],
    ["__CHART__", indent(body, "    ")],
    ["__HEIGHT__", String(height)],
    ["__BACKGROUND__", BACKGROUND],
    ["__CDN_HOST__", CDN_BASE.split("/")[2] as string],
  ];
  let page = readFileSync(TEMPLATE, "utf-8");
  for (const [token, value] of replacements) page = page.split(token).join(value);
  return page;
}

function fail(message: string): number {
  console.error(`error: ${message}`);
  return 2;
}

export function main(argv: string[]): number {
  let parsed: ReturnType<typeof parseArgs>;
  try {
    parsed = parseArgs({
      args: argv,
      allowPositionals: true,
      options: {
        data: { type: "string" },
        out: { type: "string" },
        "chart-js": { type: "string" },
      },
    });
  } catch (error) {
    return fail((error as Error).message);
  }
  const values = parsed.values as Record<string, string | undefined>;
  if (parsed.positionals.length !== 1) return fail("the following arguments are required: spec");
  if (!values.data) return fail("the following arguments are required: --data");
  if (!values.out) return fail("the following arguments are required: --out");

  let spec: Json;
  let prepared: Json;
  let customJs: string | null = null;
  try {
    spec = loadJson(parsed.positionals[0] as string);
    prepared = loadJson(values.data);
    if (values["chart-js"]) {
      try {
        customJs = readFileSync(values["chart-js"], "utf-8");
      } catch (error) {
        return fail(`cannot read ${values["chart-js"]}: ${strerror(error)}`);
      }
    }
  } catch (error) {
    if (error instanceof Unusable) return fail(error.message);
    throw error;
  }
  let usable = isObject(spec) && isObject(prepared);
  if (usable) {
    const wanted = PREPARED_KEYS[prepared.shape];
    usable = wanted !== undefined && wanted.every((key) => key in prepared);
  }
  if (!usable) {
    return fail("the spec must be a JSON object and --data must be a file prepare_data.ts wrote");
  }

  let problems = validate(spec, prepared);
  if (customJs !== null) problems = problems.filter(([code]) => code === "spec-missing");
  if (problems.length > 0) {
    for (const [code, message] of problems) console.log(`problem: ${code}: ${message}`);
    return 1;
  }
  writeFileSync(values.out, build(spec, prepared, customJs), "utf-8");
  console.log(`wrote ${values.out}`);
  return 0;
}

if (import.meta.main) process.exit(main(process.argv.slice(2)));
