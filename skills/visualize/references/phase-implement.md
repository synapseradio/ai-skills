# Phase 3: Build

Build the visualization across five subtasks. Each subtask is gated: it names one
mode reference that you must read, and a reference-derived output that proves you
read it. You cannot produce that output from memory — the principles inlined in
`SKILL.md` tell you WHAT is good, the mode doc tells you HOW, and the gate output
is the HOW made visible. A subtask whose gate output is missing is incomplete, and
the build does not advance past it.

## Entry Conditions

Phase 2 (Research) complete with user approval:

- Encoding table (with units)
- Selected engine and template. This phase covers the Vega and D3 build paths; for
  the Markdown/mermaid engine, build from [markdown-patterns.md](markdown-patterns.md).
- Ordered transformation plan

## Engine Paths

**Vega:** Define data transforms, signals, scales, axes, marks in the fragment's
inline Vega spec, at `assets/vega/fragments/<category>/<name>.frag.html`. Read
[base-vega-wrapper.md](base-vega-wrapper.md) for the fragment contract and
[vega-patterns.md](vega-patterns.md) for the spec patterns before writing it.

**D3:** Implement scales, axes, marks, and interaction in the fragment's chart-js
section, at `assets/d3/fragments/<category>/<name>.frag.html`. Read
[base-template.md](base-template.md) for the fragment contract and
[d3-patterns.md](d3-patterns.md) for the drawing patterns before writing it.

**Read the pattern doc for your chosen engine, and only that one** — reading the
other engine's doc is wasted context, not a safe default.

## Subtask Dependency Graph

```
encode → compose → ┬─ narrate ─┐→ access-audit
                    └─ interact ─┘
```

Narrate and interact run in parallel. Access-audit runs after both complete.

## Subtasks

### 1. Encode — Scales, Marks, Data

Apply the encoding table from Phase 2.

1. Apply the transformation plan (pivot, aggregate, derive, coerce, filter)
2. Define scales: domain from data extent, range from layout. Use `"nice": true`.
3. Define marks matching the encoding table
4. Generate axes with labels that include units
5. Apply OpenColors palette. Verify no red-green pairs without redundant encoding.

**Color accessibility during encoding:**

- Verify palette uses OpenColors colorblind-safe combinations
- If custom colors needed, verify no distinction depends on color alone
- Check contrast: graphical objects ≥ 3:1 against adjacent colors in the code

**Gate — read [mode-encode.md](mode-encode.md).** Produce the encoding table: each
variable mapped to a visual channel **with that channel's effectiveness rank** (1–6,
from the channel-effectiveness ranking in the reference) and its typical error. You
cannot rank the channels reliably from memory — the ranked table is the proof the
reference was read. An encoding table without ranks is an incomplete subtask.

### 2. Compose — Layout and Hierarchy

Arrange encoded elements into a coherent spatial layout.

1. Set margins: top 60px (title), right 40px, bottom 50px (axis), left 60px (axis). Adjust for content.
2. Apply visual hierarchy: primary data prominent, secondary lighter, tertiary near-invisible
3. Position axes, legends, controls. Prefer direct labels over legends.
4. Group related elements with proximity. Separate groups with whitespace.
5. For Vega: add `"role": "img"` and `"aria-labelledby"` on SVG root via config
6. For D3: add semantic SVG roles (`role="img"`, `aria-labelledby`, group data with `role="list"`)

**Gate — read [mode-compose.md](mode-compose.md).** Produce the three-level weight
assignment: name the primary, secondary, and tertiary elements, and for each name the
specific visual-weight move (size, contrast, position, or isolation) that places it at
that level. The named hierarchy with its weight moves is the proof the reference was
read. "Everything looks balanced" is not a hierarchy.

### 3. Narrate — Titles, Annotations, Story (parallel with interact)

1. Write title stating the takeaway (not the topic). 5-10 words.
2. Write subtitle with context: time range, data source, units
3. Annotate key insights: outliers, inflection points, comparisons. Use "30% higher than 2019" not just "45%".
4. For Vega: `text` marks for labels, `rule` marks for reference lines
5. For D3: positioned annotations with leader lines, collision avoidance
6. Write `<title>` and `<desc>` SVG elements describing the insight
7. Create data table fallback in `<details>` / `<summary>`

**What NOT to attempt:** scrollytelling, slide shows, animated revelation sequences.
The output format is standalone HTML — narrative works through title, annotations, and tooltips.

**Gate — read [mode-narrate.md](mode-narrate.md).** Produce the takeaway title (states
the insight, not the topic), the context subtitle, and the annotation list pairing each
flagged insight with its annotation text. The insight-bearing title and the annotation
list are the proof the reference was read. A topic title ("Revenue by Region") means the
gate is not met.

**Skip condition:** Dashboard component where narration lives in surrounding UI. Still write alt text.

### 4. Interact — Tooltips, Filters, Response (parallel with narrate)

1. Tooltips: show details on hover, position near but not obscuring the element. Include units.
2. Selection/brushing if exploration is needed (Vega signals, D3 event listeners)
3. Filtering controls if data density requires subsetting
4. Responsive layout: Vega `autosize`, D3 `viewBox`
5. Temporal states: loading skeleton, error display, empty state

**Gate — read [mode-interact.md](mode-interact.md).** Produce the interaction plan: the
tooltip fields (with units), the selection or brushing behavior if exploration is needed,
and the responsive-sizing approach — or state the explicit skip condition (static medium:
print, slide, PDF). The interaction plan or the stated skip condition is the proof the
reference was read.

**Skip condition:** Static medium (print, slide, PDF).

### 5. Access Audit — Integration Check

Verify accessibility holds together across all subtasks.

**Structural checks (verify by reading the code):**

- [ ] Palette uses OpenColors colorblind-safe combinations
- [ ] Contrast values in code meet 3:1 for graphical objects, 4.5:1 for text
- [ ] SVG has `<title>` and `<desc>` elements
- [ ] Data table fallback exists in `<details>` block
- [ ] Units present on all axes and tooltips
- [ ] Redundant encoding present (color + shape, or color + label)

**D3 additional checks:**

- [ ] `tabindex` and `keydown` handlers present for interactive elements
- [ ] Focus indicators: 2px solid outline, visible on all backgrounds
- [ ] `aria-label` on data groups
- [ ] Tab order follows visual scanning pattern

**Vega limitations (honest):** Vega renders its own SVG — you cannot add ARIA roles to
individual marks, implement keyboard navigation of data points, or manage focus. The data
table fallback and SVG `<title>`/`<desc>` are the primary accessible paths for Vega charts.

**Gate — read [mode-access.md](mode-access.md).** Complete the access-audit checklist
above (the structural checks, plus the D3-additional checks when the engine is D3). The
completed checklist, every box accounted for, is the proof the reference was read. An
unfilled checklist is an incomplete subtask.

## Exit

Proceed to **Phase 4: Verify** with a complete draft HTML file.
