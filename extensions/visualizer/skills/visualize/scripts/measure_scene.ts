/**
 * Measure the drawing of a chart page without a browser.
 *
 * `check_output.ts` imports `measurePage`. A TanStack page is compiled to a scene
 * by `createChartScene`; a hand-written page (`"shape": "custom"`) supplies its own
 * scene through the `viz-layout` script. Both scenes are measured as numbers.
 */

import { CDN_BASE, MAP_URLS } from "./build_page.ts";

export type Defect = { code: string; message: string };
export type Measurement = {
  views: number;
  points: number;
  defects: Defect[];
  colors: string[];
};

// Scenes and page data are untyped JSON.
type Json = any;
type Box = { x1: number; y1: number; x2: number; y2: number };

const TANSTACK_SPECIFIER = "@tanstack/charts@1.5.0";
const SCENE_SIZE = { width: 720 };
const CUSTOM_WIDTH = 1200;
const OUT_OF_BOUNDS_TOLERANCE = 1;
const DEFAULT_FONT_SIZE = 12;
const LABEL_SLACK = 0.3;
const MAX_REPORTED = 5;
const HEX = /^#[0-9a-fA-F]{6}$/;

/** Text width and height in pixels, estimated from the font size and the character count. */
export function measureText(text: string, fontSize = DEFAULT_FONT_SIZE): { width: number; height: number } {
  return { width: 0.6 * fontSize * [...text].length, height: 1.2 * fontSize };
}

function scriptBody(html: string, attribute: string): string | null {
  const pattern = new RegExp(`<script\\b[^>]*\\bid=["']${attribute}["'][^>]*>([\\s\\S]*?)</script>`, "i");
  return pattern.exec(html)?.[1] ?? null;
}

function moduleScripts(html: string): string[] {
  const found: string[] = [];
  for (const match of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)) {
    if (/\btype=["']module["']/i.test(match[1] as string)) found.push(match[2] as string);
  }
  return found;
}

/**
 * The box a label occupies, from the text estimate. The full box spans a line of
 * `1.2 × fontSize`; the core box leaves out the estimate's slack, 15% of the width at
 * each end and 0.2 × fontSize above and below, so a pair counts as overlapping only
 * where the text itself would collide.
 */
function labelBox(node: Json, core = false): Box {
  const size = node.fontSize ?? DEFAULT_FONT_SIZE;
  const estimate = measureText(String(node.text ?? ""), size);
  const width = typeof node.maxWidth === "number" ? Math.min(estimate.width, node.maxWidth) : estimate.width;
  let left = 0;
  if (node.anchor === "middle") left = -width / 2;
  else if (node.anchor === "end") left = -width;
  let top = -size;
  if (node.baseline === "hanging") top = 0;
  else if (node.baseline === "middle") top = -estimate.height / 2;
  const trimX = core ? 0.15 * width : 0;
  const trimY = core ? 0.2 * size : 0;
  const local = {
    x1: left + trimX,
    y1: top + trimY,
    x2: left + width - trimX,
    y2: top + estimate.height - trimY,
  };
  const turn = Number(node.rotate ?? node.rotation ?? 0);
  const angle = (turn * Math.PI) / 180;
  const corners = [
    [local.x1, local.y1],
    [local.x2, local.y1],
    [local.x2, local.y2],
    [local.x1, local.y2],
  ].map(([cx, cy]) => [
    node.x + (cx as number) * Math.cos(angle) - (cy as number) * Math.sin(angle),
    node.y + (cx as number) * Math.sin(angle) + (cy as number) * Math.cos(angle),
  ]);
  return {
    x1: Math.min(...corners.map((corner) => corner[0] as number)),
    y1: Math.min(...corners.map((corner) => corner[1] as number)),
    x2: Math.max(...corners.map((corner) => corner[0] as number)),
    y2: Math.max(...corners.map((corner) => corner[1] as number)),
  };
}

function pathBox(path: string): Box | null {
  const numbers = (path.match(/-?\d*\.?\d+(?:e[+-]?\d+)?/gi) ?? []).map(Number);
  if (numbers.length < 2) return null;
  const xs = numbers.filter((_, index) => index % 2 === 0);
  const ys = numbers.filter((_, index) => index % 2 === 1);
  return { x1: Math.min(...xs), y1: Math.min(...ys), x2: Math.max(...xs), y2: Math.max(...ys) };
}

function pointsBox(points: number[][]): Box | null {
  if (points.length === 0) return null;
  return {
    x1: Math.min(...points.map((point) => point[0] as number)),
    y1: Math.min(...points.map((point) => point[1] as number)),
    x2: Math.max(...points.map((point) => point[0] as number)),
    y2: Math.max(...points.map((point) => point[1] as number)),
  };
}

/** The box a data mark occupies. A dot counts by its centre, since a marker may overhang the plot edge. */
function markBox(node: Json): Box | null {
  switch (node.kind) {
    case "rect":
      return { x1: node.x, y1: node.y, x2: node.x + node.width, y2: node.y + node.height };
    case "dot":
      return { x1: node.x, y1: node.y, x2: node.x, y2: node.y };
    case "rule":
      return {
        x1: Math.min(node.x1, node.x2),
        y1: Math.min(node.y1, node.y2),
        x2: Math.max(node.x1, node.x2),
        y2: Math.max(node.y1, node.y2),
      };
    case "polyline":
    case "area": {
      if (Array.isArray(node.polygons) && node.polygons.length > 0) {
        return pointsBox(node.polygons.flat(2));
      }
      if (Array.isArray(node.points) && node.points.length > 0) return pointsBox(node.points);
      return typeof node.path === "string" ? pathBox(node.path) : null;
    }
    default:
      return null;
  }
}

function describeBox(box: Box): string {
  const round = (value: number) => Math.round(value * 10) / 10;
  return `${round(box.x1)},${round(box.y1)} to ${round(box.x2)},${round(box.y2)}`;
}

function overlaps(a: Box, b: Box): boolean {
  return a.x1 < b.x2 - 0.5 && b.x1 < a.x2 - 0.5 && a.y1 < b.y2 - 0.5 && b.y1 < a.y2 - 0.5;
}

type Walked = { marks: Json[]; labels: Json[] };

function hasMarksGroup(nodes: Json[]): boolean {
  return nodes.some(
    (node) => node.kind === "group" && (node.key === "marks" || hasMarksGroup(node.children ?? [])),
  );
}

function walkScene(scene: Json): Walked {
  const marksGroup = hasMarksGroup(scene.nodes ?? []);
  const marks: Json[] = [];
  const labels: Json[] = [];
  const visit = (nodes: Json[], inMarks: boolean): void => {
    for (const node of nodes) {
      const key = String(node.key ?? "");
      if (node.kind === "group") {
        if (key.startsWith("default-focus")) continue;
        const entering = marksGroup ? inMarks || key === "marks" : !(key === "grid" || key.startsWith("guide"));
        visit(node.children ?? [], entering);
      } else if (node.kind === "label") {
        labels.push(node);
      } else if (inMarks || (!marksGroup && !/^(x|y)-axis|^legend/.test(key))) {
        marks.push(node);
      }
    }
  };
  visit(scene.nodes ?? [], false);
  return { marks, labels };
}

function paintedColors(marks: Json[]): string[] {
  const found = new Set<string>();
  for (const node of marks) {
    for (const paint of [node.style?.fill, node.style?.stroke]) {
      if (typeof paint === "string" && HEX.test(paint)) found.add(paint.toLowerCase());
    }
  }
  return [...found];
}

/** Defects one scene carries, with the geometry the scene reports. */
function measureScene(scene: Json): { defects: Defect[]; colors: string[] } {
  const defects: Defect[] = [];
  const { marks, labels } = walkScene(scene);
  const chart = scene.chart;
  for (const node of marks) {
    const box = markBox(node);
    if (!box) continue;
    const slack = OUT_OF_BOUNDS_TOLERANCE;
    if (![box.x1, box.y1, box.x2, box.y2].every(Number.isFinite)) {
      defects.push({
        code: "mark-out-of-bounds",
        message: `the ${node.kind} ${JSON.stringify(String(node.key))} has no finite position`,
      });
    } else if (
      box.x1 < chart.x - slack ||
      box.y1 < chart.y - slack ||
      box.x2 > chart.x + chart.width + slack ||
      box.y2 > chart.y + chart.height + slack
    ) {
      defects.push({
        code: "mark-out-of-bounds",
        message: `the ${node.kind} ${JSON.stringify(String(node.key))} spans ${describeBox(box)}, outside the plot area ${describeBox({
          x1: chart.x,
          y1: chart.y,
          x2: chart.x + chart.width,
          y2: chart.y + chart.height,
        })}`,
      });
    }
  }
  const boxes = labels.map((node) => ({ node, box: labelBox(node, true), full: labelBox(node) }));
  for (const { node, full: box } of boxes) {
    const slack = LABEL_SLACK * (node.fontSize ?? DEFAULT_FONT_SIZE);
    if (
      box.x1 < -slack ||
      box.y1 < -slack ||
      box.x2 > scene.width + slack ||
      box.y2 > scene.height + slack
    ) {
      defects.push({
        code: "label-out-of-bounds",
        message: `the label ${JSON.stringify(String(node.text))} spans ${describeBox(box)}, outside the ${scene.width} by ${scene.height} drawing`,
      });
    }
  }
  for (let first = 0; first < boxes.length; first += 1) {
    for (let second = first + 1; second < boxes.length; second += 1) {
      const a = boxes[first] as { node: Json; box: Box };
      const b = boxes[second] as { node: Json; box: Box };      if (overlaps(a.box, b.box)) {
        defects.push({
          code: "label-overlap",
          message: `the labels ${JSON.stringify(String(a.node.text))} and ${JSON.stringify(String(b.node.text))} overlap`,
        });
      }
    }
  }
  return { defects, colors: paintedColors(marks) };
}

function normalize(value: unknown): unknown {
  return value instanceof Date ? value.toISOString() : value;
}

function sameValue(wanted: unknown, drawn: unknown): boolean {
  const have = normalize(drawn);
  if (wanted === have) return true;
  return (
    typeof wanted === "string" &&
    typeof have === "string" &&
    /^\d{4}-\d{2}-\d{2}$/.test(wanted) &&
    have.startsWith(`${wanted}T`)
  );
}

function rowMatches(row: Json, candidate: Json): boolean {
  if (!candidate || typeof candidate !== "object") return false;
  const entries = Object.entries(row).filter(([, value]) => value === null || typeof value !== "object");
  return entries.length > 0 && entries.every(([key, value]) => sameValue(value, candidate[key]));
}

function describeRow(row: Json): string {
  const text = JSON.stringify(row);
  return text.length > 80 ? `${text.slice(0, 77)}...` : text;
}

function dataRows(data: Json): Json[] {
  if (data.shape === "sankey" || data.shape === "network") {
    return [...(data.nodes ?? []), ...(data.links ?? [])];
  }
  if (data.shape === "choropleth") return data.regions ?? [];
  return Array.isArray(data.rows) ? data.rows : [];
}

function missingRows(data: Json, drawn: Json[]): Defect[] {
  const defects: Defect[] = [];
  for (const row of dataRows(data)) {
    const found = drawn.some((point) => {
      const datum = point.datum;
      if (data.shape === "choropleth") return datum?.id === row.key || datum?.properties?.name === row.key;
      return rowMatches(row, datum) || rowMatches(row, datum?.data);
    });
    if (!found) {
      defects.push({ code: "row-not-drawn", message: `the data row ${describeRow(row)} has no mark in the drawing` });
    }
  }
  return defects;
}

function limit(defects: Defect[]): Defect[] {
  const counts = new Map<string, number>();
  const kept: Defect[] = [];
  const unique = new Set<string>();
  for (const defect of defects) {
    const identity = `${defect.code}:${defect.message}`;
    if (unique.has(identity)) continue;
    unique.add(identity);
    const count = (counts.get(defect.code) ?? 0) + 1;
    counts.set(defect.code, count);
    if (count <= MAX_REPORTED) kept.push(defect);
  }
  for (const [code, count] of counts) {
    if (count > MAX_REPORTED) {
      kept.push({ code, message: `${count - MAX_REPORTED} more of this kind were left out of the list` });
    }
  }
  return kept;
}

const AsyncFunction = Object.getPrototypeOf(async () => {}).constructor as new (
  ...parts: string[]
) => (...args: unknown[]) => Promise<unknown>;

/** The page's definition code, as text that imports bare pinned specifiers. */
function definitionSource(html: string): string | null {
  for (const script of moduleScripts(html)) {
    const start = script.indexOf("// viz:definition:start");
    const end = script.indexOf("// viz:definition:end");
    if (start === -1 || end === -1 || end < start) continue;
    let code = script.slice(start + "// viz:definition:start".length, end);
    code = code
      .split("\n")
      .filter((line) => !/\bmountChart\b/.test(line))
      .join("\n");
    code = code.replaceAll(CDN_BASE, TANSTACK_SPECIFIER);
    for (const url of Object.values(MAP_URLS)) {
      if (!url.endsWith(".json")) code = code.replaceAll(url, url.replace("https://esm.sh/", ""));
    }
    return code;
  }
  return null;
}

async function measureTanstack(html: string, data: Json): Promise<Measurement> {
  const code = definitionSource(html);
  if (code === null) return { views: 0, points: 0, defects: [], colors: [] };
  const height = typeof data.height === "number" ? data.height : 380;
  let scene: Json;
  try {
    const definition = await new AsyncFunction("data", `${code}\nreturn definition;`)(data);
    const { createChartScene } = await import("@tanstack/charts@1.5.0/scene");
    scene = createChartScene(
      definition as never,
      { width: SCENE_SIZE.width, height },
      { measureText: (text: string, style?: { fontSize?: number }) => measureText(text, style?.fontSize) },
    );
  } catch (error) {
    return {
      views: 0,
      points: 0,
      defects: [{ code: "scene-failed", message: `the chart definition could not be compiled: ${(error as Error).message}` }],
      colors: [],
    };
  }
  const measured = measureScene(scene);
  const defects = [...missingRows(data, scene.points as Json[]), ...measured.defects];
  return { views: 1, points: scene.points.length, defects: limit(defects), colors: measured.colors };
}

type Layout = {
  vizViews: (data: Json) => Json[];
  vizLayout: (data: Json, size: { width: number; height: number }, view: Json, text: typeof measureText) => Json;
};

async function measureCustom(html: string, data: Json): Promise<Measurement> {
  const source = scriptBody(html, "viz-layout");
  if (source === null) return { views: 0, points: 0, defects: [], colors: [] };
  const defects: Defect[] = [];
  const colors = new Set<string>();
  const drawn = new Set<string>();
  let views = 0;
  try {
    const layout = new Function(`${source}\nreturn { vizViews, vizLayout };`)() as Layout;
    const size = { width: CUSTOM_WIDTH, height: Number(data.height) || 380 };
    for (const view of layout.vizViews(data)) {
      views += 1;
      const scene = layout.vizLayout(data, size, view, measureText);
      const measured = measureScene(scene);
      defects.push(...measured.defects);
      for (const color of measured.colors) colors.add(color);
      for (const point of scene.points ?? []) drawn.add(String(point.key));
    }
  } catch (error) {
    defects.push({ code: "scene-failed", message: `the layout could not be computed: ${(error as Error).message}` });
  }
  for (const row of dataRows(data)) {
    if (!drawn.has(String(row.key))) {
      defects.push({ code: "row-not-drawn", message: `the data row ${describeRow(row)} has no mark in any view` });
    }
  }
  return { views, points: drawn.size, defects: limit(defects), colors: [...colors] };
}

/** Measure the drawing of one chart page. Pages with nothing to compile measure as zero views. */
export async function measurePage(html: string): Promise<Measurement> {
  const empty: Measurement = { views: 0, points: 0, defects: [], colors: [] };
  const dataText = scriptBody(html, "viz-data");
  if (dataText === null) return empty;
  let data: Json;
  try {
    data = JSON.parse(dataText);
  } catch {
    return empty;
  }
  if (!data || typeof data !== "object") return empty;
  return data.shape === "custom" ? measureCustom(html, data) : measureTanstack(html, data);
}
