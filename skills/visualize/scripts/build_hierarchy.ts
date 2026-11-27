/**
 * Build a collapsible tree page or a zoomable treemap page from rows of paths and values.
 *
 *   bun --install=fallback build_hierarchy.ts ROWS.csv --path COL --value COL --spec SPEC.json
 *                  --chart tree|treemap --out PAGE.html [--delimiter /]
 *
 * ROWS holds one row per leaf, as CSV, TSV, or JSON. `--path` names the column holding
 * the leaf's path, split on the delimiter (default `/`); `--value` names the column
 * holding a nonnegative number that is summed through each parent. The spec takes
 * `title`, `subtitle`, `summary`, `source`, and `y.unit`.
 *
 * Exit codes: 0 page written, 1 the rows or the spec cannot be drawn, 2 unusable input.
 */

import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { parseArgs } from "node:util";
import { BACKGROUND, htmlEscape, isObject, loadJson, oneTable, PALETTE, textAt } from "./build_page.ts";
import {
  type Issue,
  isMissing,
  pyDumps,
  pyRepr,
  pyStr,
  readRows,
  type Row,
  toNumber,
  Unusable,
} from "./prepare_data.ts";

const CHARTS = ["tree", "treemap"];
const HEIGHTS: Record<string, number> = { tree: 480, treemap: 520 };
const ASSETS = join(dirname(import.meta.dir), "assets");

type Node = {
  name: string;
  key: string;
  value: number;
  leaf: boolean;
  children: Map<string, Node>;
};

type HierarchyRow = { key: string; depth: number; value: number };

function makeNode(name: string, key: string): Node {
  return { name, key, value: 0, leaf: false, children: new Map() };
}

/** Build the tree of nodes from the rows, or the problems that stop it. */
function buildTree(
  rows: Row[],
  pathColumn: string,
  valueColumn: string,
  delimiter: string,
): { root: Node | null; problems: Issue[] } {
  const problems: Issue[] = [];
  const root = makeNode(".", ".");
  const leaves = new Map<string, number>();
  rows.forEach((row, offset) => {
    const index = offset + 1;
    if (isMissing(row[pathColumn]) || isMissing(row[valueColumn])) {
      const absent = [pathColumn, valueColumn].filter((column) => isMissing(row[column]));
      problems.push(["missing-value", `row ${index} has no value for ${pyRepr(absent)}`]);
      return;
    }
    const segments = pyStr(row[pathColumn])
      .split(delimiter)
      .map((segment) => segment.trim())
      .filter(Boolean);
    const value = toNumber(row[valueColumn]);
    if (segments.length === 0) {
      problems.push(["empty-path", `row ${index}: ${pathColumn} is ${pyRepr(row[pathColumn])}, which names no path`]);
      return;
    }
    if (segments.some((segment) => segment.includes("/"))) {
      problems.push([
        "bad-segment",
        `row ${index}: ${pathColumn} is ${pyRepr(row[pathColumn])}; a name inside a path cannot hold "/"`,
      ]);
      return;
    }
    if (value === null) {
      problems.push([
        "not-a-number",
        `row ${index}: ${valueColumn} is ${pyRepr(row[valueColumn])}; strip units and symbols from the value`,
      ]);
      return;
    }
    if (value < 0) {
      problems.push(["negative-value", `row ${index}: ${valueColumn} is ${value}; a share cannot be negative`]);
      return;
    }
    const key = segments.join("/");
    const earlier = leaves.get(key);
    if (earlier !== undefined) {
      problems.push([
        "duplicate-key",
        `rows ${earlier} and ${index} both give ${pyRepr(key)}; decide how they aggregate before charting`,
      ]);
      return;
    }
    leaves.set(key, index);
    let node = root;
    const walked: Node[] = [root];
    segments.forEach((segment, depth) => {
      const childKey = segments.slice(0, depth + 1).join("/");
      let child = node.children.get(segment);
      if (!child) {
        child = makeNode(segment, childKey);
        node.children.set(segment, child);
      }
      node = child;
      walked.push(child);
    });
    node.leaf = true;
    for (const step of walked) step.value += value;
  });
  if (problems.length === 0) {
    const visit = (node: Node) => {
      if (node.leaf && node.children.size > 0) {
        problems.push([
          "path-conflict",
          `${pyRepr(node.key)} is a leaf in one row and a directory in another`,
        ]);
      }
      for (const child of node.children.values()) visit(child);
    };
    visit(root);
  }
  if (problems.length === 0 && root.children.size === 0) {
    problems.push(["empty", "the input holds no rows"]);
  }
  return { root: problems.length === 0 ? root : null, problems };
}

/** One row per node, directories before files, the larger first, each parent ahead of its children. */
function flatten(root: Node): HierarchyRow[] {
  const out: HierarchyRow[] = [];
  const visit = (node: Node, depth: number) => {
    out.push({ key: node.key, depth, value: node.value });
    const children = [...node.children.values()].sort(
      (a, b) =>
        Number(a.children.size === 0) - Number(b.children.size === 0) ||
        b.value - a.value ||
        (a.name < b.name ? -1 : a.name > b.name ? 1 : 0),
    );
    for (const child of children) visit(child, depth + 1);
  };
  visit(root, 0);
  return out;
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
        path: { type: "string" },
        value: { type: "string" },
        spec: { type: "string" },
        chart: { type: "string" },
        out: { type: "string" },
        delimiter: { type: "string", default: "/" },
      },
    });
  } catch (error) {
    return fail((error as Error).message);
  }
  const values = parsed.values as Record<string, string | undefined>;
  if (parsed.positionals.length !== 1) return fail("the following arguments are required: rows");
  for (const name of ["path", "value", "spec", "chart", "out"]) {
    if (!values[name]) return fail(`the following arguments are required: --${name}`);
  }
  const chart = values.chart as string;
  if (!CHARTS.includes(chart)) return fail(`argument --chart: invalid choice: ${pyRepr(chart)}`);
  const delimiter = values.delimiter as string;
  if (!delimiter) return fail("argument --delimiter: the delimiter cannot be empty");

  let rows: Row[];
  let spec: unknown;
  let template: string;
  try {
    rows = readRows(parsed.positionals[0] as string);
    spec = loadJson(values.spec as string);
    try {
      template = readFileSync(join(ASSETS, `${chart}.html`), "utf-8");
    } catch {
      return fail(`the ${chart} template is missing from ${ASSETS}`);
    }
  } catch (error) {
    if (error instanceof Unusable) return fail(error.message);
    throw error;
  }
  if (!isObject(spec)) return fail("the spec must be a JSON object");

  const problems: Issue[] = [];
  for (const dotted of ["title", "summary", "y.unit"]) {
    if (!textAt(spec, dotted)) problems.push(["spec-missing", `the spec needs a non-empty ${dotted}`]);
  }
  const known = new Set<string>();
  for (const row of rows) for (const key of Object.keys(row)) known.add(key);
  for (const column of [values.path as string, values.value as string]) {
    if (rows.length > 0 && !known.has(column)) {
      problems.push([
        "missing-field",
        `no column named ${pyRepr(column)}; columns are ${pyRepr([...known].sort())}`,
      ]);
    }
  }
  if (rows.length === 0) problems.push(["empty", "the input holds no rows"]);
  let tree: Node | null = null;
  if (problems.length === 0) {
    const built = buildTree(rows, values.path as string, values.value as string, delimiter);
    tree = built.root;
    problems.push(...built.problems);
  }
  if (problems.length > 0 || tree === null) {
    for (const [code, message] of problems) console.log(`problem: ${code}: ${message}`);
    return 1;
  }

  const unit = textAt(spec, "y.unit");
  const hierarchy = flatten(tree);
  const data = {
    spec,
    shape: "custom",
    chart,
    background: BACKGROUND,
    colors: PALETTE,
    unit,
    height: HEIGHTS[chart],
    rows: hierarchy,
  };
  const table = oneTable(
    textAt(spec, "title"),
    [
      ["Path", false],
      [`Total ${unit}`, true],
    ],
    hierarchy.map((row) => [row.key, row.value]),
  );
  const subtitle = textAt(spec, "subtitle");
  const source = textAt(spec, "source");
  const replacements: [string, string][] = [
    ["__TITLE__", htmlEscape(textAt(spec, "title"))],
    ["__SUBTITLE__", subtitle ? `<p class="subtitle">${htmlEscape(subtitle)}</p>` : ""],
    ["__SUMMARY__", htmlEscape(textAt(spec, "summary"))],
    ["__SOURCE__", source ? `<p class="source">Source: ${htmlEscape(source)}</p>` : ""],
    ["__TABLE__", table],
    ["__DATA__", pyDumps(data, false).replaceAll("</", "<\\/")],
    ["__HEIGHT__", String(HEIGHTS[chart])],
  ];
  let page = template;
  for (const [token, value] of replacements) page = page.split(token).join(value);
  writeFileSync(values.out as string, page, "utf-8");
  console.log(`wrote ${values.out}`);
  return 0;
}

if (import.meta.main) process.exit(main(process.argv.slice(2)));
