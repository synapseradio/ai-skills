// Tests for the scripts in `scripts/`, driven through their command lines.
//
// Run from the repository root:
//
//     bun test skills/visualize/evals/scripts.test.ts

import { afterEach, beforeEach, describe, expect, test } from "bun:test";
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";

const EVALS = import.meta.dir;
const SCRIPTS = resolve(EVALS, "..", "scripts");
const FIXTURES = join(EVALS, "fixtures");
const BUN_CACHE = mkdtempSync(join(tmpdir(), "viz-bun-cache-"));

type Result = { code: number; stdout: string; stderr: string };

function run(script: string, ...args: (string | number)[]): Result {
  const proc = Bun.spawnSync(
    ["bun", "--install=fallback", join(SCRIPTS, `${script}.ts`), ...args.map(String)],
    { env: { ...process.env, BUN_INSTALL_CACHE_DIR: BUN_CACHE } },
  );
  return { code: proc.exitCode, stdout: proc.stdout.toString(), stderr: proc.stderr.toString() };
}

/** The problem or defect codes a script printed, one per reported line. */
function codes(result: Result): Set<string> {
  const found = new Set<string>();
  for (const line of result.stdout.split("\n")) {
    const match = /^(?:problem|.+?\.(?:html|md)): ([a-z-]+): /.exec(line);
    if (match?.[1]) found.add(match[1]);
  }
  return found;
}

const readText = (path: string) => readFileSync(path, "utf-8");
const readJson = (path: string) => JSON.parse(readText(path));
const fixture = (name: string) => join(FIXTURES, name);

let dir = "";
beforeEach(() => {
  dir = mkdtempSync(join(tmpdir(), "viz-test-"));
});
afterEach(() => {
  rmSync(dir, { recursive: true, force: true });
});

function write(name: string, text: string): string {
  const path = join(dir, name);
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, text, "utf-8");
  return path;
}

function preparedCoffee(): string {
  const out = join(dir, "rows.json");
  const result = run(
    "prepare_data",
    fixture("coffee.csv"),
    "--x",
    "day",
    "--y",
    "cups",
    "--series",
    "person",
    "--out",
    out,
  );
  expect(result.code, result.stdout + result.stderr).toBe(0);
  return out;
}

function coffeePage(): string {
  const page = join(dir, "coffee.html");
  const result = run(
    "build_page",
    fixture("coffee.spec.json"),
    "--data",
    preparedCoffee(),
    "--out",
    page,
  );
  expect(result.code, result.stdout + result.stderr).toBe(0);
  return page;
}

function editedPage(old: string, replacement: string): string {
  const text = readText(coffeePage());
  expect(text).toContain(old);
  return write("edited.html", text.replace(old, () => replacement));
}

describe("PreparingData", () => {
  test("rows come out typed and complete", () => {
    const prepared = readJson(preparedCoffee());
    expect(prepared.xType).toBe("date");
    expect(prepared.seriesValues).toEqual(["Ana", "Ben"]);
    expect(prepared.rows[0]).toEqual({ day: "2026-11-09", cups: 2, person: "Ana" });
    expect(prepared.rows.length).toBe(6);
  });

  test("a measure that is not a number stops the run and writes nothing", () => {
    const source = write("bad.csv", "day,cups\n2026-11-09,2\n2026-11-10,three\n");
    const out = join(dir, "rows.json");
    const result = run("prepare_data", source, "--x", "day", "--y", "cups", "--out", out);
    expect(result.code).toBe(1);
    expect(codes(result)).toEqual(new Set(["not-a-number"]));
    expect(existsSync(out)).toBe(false);
  });

  test("two rows for one position stop the run", () => {
    const source = write("dup.csv", "day,cups\n2026-11-09,2\n2026-11-09,5\n");
    const result = run(
      "prepare_data",
      source,
      "--x",
      "day",
      "--y",
      "cups",
      "--out",
      join(dir, "rows.json"),
    );
    expect(result.code).toBe(1);
    expect(codes(result)).toEqual(new Set(["duplicate-key"]));
  });

  test("a missing value stops the run unless dropping is asked for", () => {
    const source = write("gap.csv", "day,cups\n2026-11-09,2\n2026-11-10,\n2026-11-11,4\n");
    const out = join(dir, "rows.json");
    const refused = run("prepare_data", source, "--x", "day", "--y", "cups", "--out", out);
    expect(codes(refused)).toEqual(new Set(["missing-value"]));
    const dropped = run(
      "prepare_data",
      source,
      "--x",
      "day",
      "--y",
      "cups",
      "--drop-missing",
      "--out",
      out,
    );
    expect(dropped.code).toBe(0);
    expect(readJson(out).rows.length).toBe(2);
  });
});

describe("BuildingPages", () => {
  test("a built page passes the output check", () => {
    const result = run("check_output", coffeePage());
    expect(result.code, result.stdout).toBe(0);
    expect(codes(result)).toEqual(new Set());
  });

  test("a line over unordered categories is refused", () => {
    const source = write("teams.csv", "team,points\nRed,3\nBlue,5\nGreen,4\n");
    const rows = join(dir, "teams.json");
    run("prepare_data", source, "--x", "team", "--y", "points", "--out", rows);
    const spec = write(
      "spec.json",
      JSON.stringify({
        title: "Blue leads",
        summary: "Blue has 5 points.",
        chart: "line",
        x: { label: "Team" },
        y: { label: "Score", unit: "points" },
      }),
    );
    const page = join(dir, "teams.html");
    const result = run("build_page", spec, "--data", rows, "--out", page);
    expect(result.code).toBe(1);
    expect(codes(result)).toEqual(new Set(["chart-data-mismatch"]));
    expect(existsSync(page)).toBe(false);
  });

  test("a spec without a unit is refused", () => {
    const spec = readJson(fixture("coffee.spec.json"));
    delete spec.y.unit;
    const result = run(
      "build_page",
      write("spec.json", JSON.stringify(spec)),
      "--data",
      preparedCoffee(),
      "--out",
      join(dir, "page.html"),
    );
    expect(codes(result)).toEqual(new Set(["spec-missing"]));
  });
});

describe("CheckingPages", () => {
  test("a second library is reported", () => {
    const page = editedPage(
      "const data =",
      "await import('https://esm.sh/lodash-es@4.17.21')\nconst data =",
    );
    expect(codes(run("check_output", page))).toEqual(new Set(["foreign-import"]));
  });

  test("an unpinned chart library is reported", () => {
    const page = editedPage("@tanstack/charts@1.5.0/dom", "@tanstack/charts/dom");
    expect(codes(run("check_output", page))).toEqual(new Set(["unpinned-import"]));
  });

  test("a table that lost a row is reported", () => {
    const page = editedPage(
      '<tr><td>2026-11-09</td><td>Ana</td><td class="num">2</td></tr>\n',
      "",
    );
    expect(codes(run("check_output", page))).toEqual(new Set(["table-row-mismatch"]));
  });

  test("two series colours a reader cannot tell apart are reported", () => {
    const page = editedPage('"colors": ["#0072b2", "#d55e00"]', '"colors": ["#0072b2", "#0072b3"]');
    expect(codes(run("check_output", page))).toEqual(new Set(["color-confusable"]));
  });

  test("a series colour too pale for its background is reported", () => {
    const page = editedPage('"colors": ["#0072b2", "#d55e00"]', '"colors": ["#0072b2", "#ffff00"]');
    expect(codes(run("check_output", page))).toEqual(new Set(["color-low-contrast"]));
  });

  test("a page without a text summary is reported", () => {
    const page = editedPage(
      "Ben rose from 3 to 4 cups a day. Ana stayed between 1 and 3.</p>",
      "</p>",
    );
    expect(codes(run("check_output", page)).has("no-summary")).toBe(true);
  });
});

const SHAPED: Record<string, string[]> = {
  flow: ["--shape", "sankey", "--source", "from", "--target", "to", "--value", "visits"],
  calls: [
    "--shape",
    "network",
    "--source",
    "caller",
    "--target",
    "callee",
    "--value",
    "calls",
    "--nodes",
    fixture("services.csv"),
    "--node-group",
    "team",
  ],
  internet: ["--shape", "choropleth", "--region", "country", "--value", "share"],
  wards: [
    "--shape",
    "choropleth",
    "--region",
    "ward",
    "--value",
    "trees",
    "--geojson",
    fixture("wards.geojson"),
    "--feature-id",
    "code",
    "--feature-name",
    "name",
  ],
};

function prepare(source: string, ...args: string[]): Result {
  return run("prepare_data", source, ...args, "--out", join(dir, "prepared.json"));
}

function prepared(name: string): string {
  const result = prepare(fixture(`${name}.csv`), ...(SHAPED[name] ?? []));
  expect(result.code, result.stdout + result.stderr).toBe(0);
  return join(dir, "prepared.json");
}

function build(spec: string, data: string): Result {
  return run("build_page", spec, "--data", data, "--out", join(dir, "page.html"));
}

function page(name: string): string {
  const result = build(fixture(`${name}.spec.json`), prepared(name));
  expect(result.code, result.stdout + result.stderr).toBe(0);
  return join(dir, "page.html");
}

function edited(name: string, old: string, replacement: string): string {
  const text = readText(page(name));
  expect(text).toContain(old);
  return write("edited.html", text.replace(old, () => replacement));
}

function specWithout(name: string, section: string, key: string): string {
  const spec = readJson(fixture(`${name}.spec.json`));
  delete spec[section][key];
  return write("spec.json", JSON.stringify(spec));
}

describe("PreparingFlowsAndNetworks", () => {
  test("a balanced flow comes out as nodes and links", () => {
    const out = readJson(prepared("flow"));
    expect(out.nodes.length).toBe(5);
    expect(out.links.length).toBe(6);
    expect(out.links[0]).toEqual({ source: "Landing", target: "Sign-up", value: 620 });
  });

  test("a stage that sends out less than it takes in stops the run", () => {
    const source = write("leak.csv", "from,to,visits\nA,B,10\nB,C,7\n");
    const result = prepare(source, ...(SHAPED.flow ?? []));
    expect(result.code).toBe(1);
    expect(codes(result)).toEqual(new Set(["unbalanced-node"]));
    expect(existsSync(join(dir, "prepared.json"))).toBe(false);
  });

  test("a flow that loops back stops the run", () => {
    const source = write("loop.csv", "from,to,visits\nA,B,5\nB,C,5\nC,A,5\n");
    expect(codes(prepare(source, ...(SHAPED.flow ?? [])))).toEqual(new Set(["cycle"]));
  });

  test("a flow of zero stops the run", () => {
    const source = write("zero.csv", "from,to,visits\nA,B,0\n");
    expect(codes(prepare(source, ...(SHAPED.flow ?? [])))).toEqual(new Set(["not-positive"]));
  });

  test("a link to a node the nodes file lacks stops the run", () => {
    const source = write("calls.csv", "caller,callee,calls\nweb,api,9\napi,cache,4\n");
    const result = prepare(source, ...(SHAPED.calls ?? []));
    expect(result.code).toBe(1);
    expect(codes(result)).toEqual(new Set(["unknown-node"]));
  });

  test("the same pair linked in both directions stops a network", () => {
    const source = write("calls.csv", "caller,callee,calls\nweb,api,9\napi,web,4\n");
    expect(codes(prepare(source, ...(SHAPED.calls ?? [])))).toEqual(new Set(["duplicate-key"]));
  });

  test("a node linked to itself stops a network", () => {
    const source = write("calls.csv", "caller,callee,calls\nweb,web,9\n");
    expect(codes(prepare(source, ...(SHAPED.calls ?? [])))).toEqual(new Set(["self-link"]));
  });

  test("network nodes keep their group", () => {
    const out = readJson(prepared("calls"));
    expect(out.groupValues).toEqual(["Front", "Platform", "Commerce"]);
    expect(out.nodes[0]).toEqual({ id: "web", label: "web", group: "Front" });
  });
});

describe("PreparingRegions", () => {
  test("a country code and a country name both join the atlas", () => {
    const out = readJson(prepared("internet"));
    const keys = new Set(out.regions.map((region: { key: string }) => region.key));
    expect(keys.has("United States of America")).toBe(true);
    expect(keys.has("Norway")).toBe(true);
    expect(out.regions.length).toBe(9);
  });

  test("a region the atlas lacks stops the run", () => {
    const source = write("bad.csv", "country,share\nNorway,99\nAtlantis,50\n");
    const result = prepare(source, ...(SHAPED.internet ?? []));
    expect(result.code).toBe(1);
    expect(codes(result)).toEqual(new Set(["unknown-region"]));
  });

  test("one country given by name and by code stops the run", () => {
    const source = write("twice.csv", "country,share\nNorway,99\n578,98\n");
    expect(codes(prepare(source, ...(SHAPED.internet ?? [])))).toEqual(new Set(["duplicate-key"]));
  });

  test("a region the geojson lacks stops the run", () => {
    const source = write("bad.csv", "ward,trees\nN,410\nQ,5\n");
    expect(codes(prepare(source, ...(SHAPED.wards ?? [])))).toEqual(new Set(["unknown-region"]));
  });

  test("counterclockwise rings come out clockwise", () => {
    const given = readJson(fixture("wards.geojson"));
    const out = readJson(prepared("wards"));
    const ring = given.features[0].geometry.coordinates[0];
    expect(out.features[0].geometry.coordinates[0]).toEqual([...ring].reverse());
  });

  test("a geojson point stops the run", () => {
    const geojson = readJson(fixture("wards.geojson"));
    geojson.features[0].geometry = { type: "Point", coordinates: [13.3, 52.5] };
    const args = [...(SHAPED.wards ?? [])];
    args[args.indexOf("--geojson") + 1] = write("points.geojson", JSON.stringify(geojson));
    const source = write("wards.csv", "ward,trees\nS,265\nE,120\n");
    expect(codes(prepare(source, ...args))).toEqual(new Set(["not-a-region"]));
  });
});

describe("BuildingShapedPages", () => {
  test("each kind builds a page that passes the output check", () => {
    for (const name of Object.keys(SHAPED)) {
      const result = run("check_output", page(name));
      expect(result.code, `${name}: ${result.stdout}`).toBe(0);
      expect(codes(result), name).toEqual(new Set());
    }
  });

  test("a chart kind is refused data of another shape", () => {
    for (const [spec, data] of [
      ["flow", "calls"],
      ["calls", "internet"],
      ["internet", "flow"],
    ] as const) {
      const result = build(fixture(`${spec}.spec.json`), prepared(data));
      expect(result.code, `${spec} with ${data}`).toBe(1);
      expect(codes(result), `${spec} with ${data}`).toEqual(new Set(["chart-data-mismatch"]));
      expect(existsSync(join(dir, "page.html")), `${spec} with ${data}`).toBe(false);
    }
  });

  test("a bar chart is refused network data", () => {
    const result = build(fixture("coffee.spec.json"), prepared("calls"));
    expect(codes(result)).toEqual(new Set(["chart-data-mismatch"]));
  });

  test("a flow without a unit is refused", () => {
    const result = build(specWithout("flow", "value", "unit"), prepared("flow"));
    expect(codes(result)).toEqual(new Set(["spec-missing"]));
  });

  test("a map without a unit is refused", () => {
    const spec = specWithout("internet", "value", "unit");
    expect(codes(build(spec, prepared("internet")))).toEqual(new Set(["spec-missing"]));
  });

  test("a network past the readable node count is refused", () => {
    let links = "";
    for (let index = 0; index < 61; index += 1) links += `hub,leaf${index},1\n`;
    const source = write("big.csv", `caller,callee,calls\n${links}`);
    const result = run(
      "prepare_data",
      source,
      "--shape",
      "network",
      "--source",
      "caller",
      "--target",
      "callee",
      "--out",
      join(dir, "prepared.json"),
    );
    expect(result.code, result.stdout).toBe(0);
    const spec = write(
      "spec.json",
      JSON.stringify({ title: "t", summary: "s", chart: "network", nodes: { label: "Service" } }),
    );
    expect(codes(build(spec, join(dir, "prepared.json")))).toEqual(new Set(["too-many-nodes"]));
  });

  test("a map where every region holds one value is refused", () => {
    const source = write("flat.csv", "country,share\nNorway,50\nChad,50\n");
    expect(prepare(source, ...(SHAPED.internet ?? [])).code).toBe(0);
    const result = build(fixture("internet.spec.json"), join(dir, "prepared.json"));
    expect(codes(result)).toEqual(new Set(["constant-values"]));
  });
});

describe("CheckingShapedPages", () => {
  test("a link to a node the page lacks is reported", () => {
    const changed = edited("flow", '"target": "Paid"', '"target": "Refunded"');
    expect(codes(run("check_output", changed))).toEqual(new Set(["link-unknown-node"]));
  });

  test("a network page that lost its link table is reported", () => {
    const text = readText(page("calls"));
    const start = text.indexOf("<table>", text.indexOf("</table>"));
    const end = text.indexOf("</table>", start) + "</table>".length;
    const changed = write("edited.html", text.slice(0, start) + text.slice(end));
    expect(codes(run("check_output", changed)).has("no-table")).toBe(true);
  });

  test("an atlas at another version is reported", () => {
    const changed = edited("internet", "world-atlas@2.0.2", "world-atlas@2.0.1");
    expect(codes(run("check_output", changed))).toEqual(new Set(["foreign-import"]));
  });

  test("a projection import outside a map page is reported", () => {
    const changed = edited(
      "flow",
      "const data =",
      "await import('https://esm.sh/d3-geo@3.1.1')\nconst data =",
    );
    expect(codes(run("check_output", changed))).toEqual(new Set(["foreign-import"]));
  });

  test("a region with no shape on the map is reported", () => {
    const changed = edited("wards", '"key": "N"', '"key": "Q"');
    expect(codes(run("check_output", changed))).toEqual(new Set(["region-unmatched"]));
  });

  test("a ramp too flat to rank regions is reported", () => {
    const changed = edited(
      "internet",
      '"ramp": ["#deebf7", "#08519c"]',
      '"ramp": ["#deebf7", "#c6dbef"]',
    );
    expect(codes(run("check_output", changed))).toEqual(new Set(["ramp-flat"]));
  });
});

describe("CheckingMarkdown", () => {
  test("a well-formed diagram passes", () => {
    expect(run("check_output", fixture("mermaid_good.md")).code).toBe(0);
  });

  test("an unknown diagram type with open brackets is reported", () => {
    const result = run("check_output", fixture("mermaid_broken_source.md"));
    expect(codes(result)).toEqual(new Set(["mermaid-unknown-type", "mermaid-unbalanced"]));
  });

  test("bars in proportion to their values pass", () => {
    expect(run("check_output", fixture("bars_good.md")).code).toBe(0);
  });

  test("a bar drawn longer than its value is reported", () => {
    expect(codes(run("check_output", fixture("bars_broken.md")))).toEqual(
      new Set(["bar-not-proportional"]),
    );
  });
});
