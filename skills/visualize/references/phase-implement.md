# Phase 3: Implementation

Build the visualization across five subtasks with dependency-aware ordering and parallelism where possible. These patterns synthesize established visualization practice. Primary sources are cited where available.

## Entry Conditions

Phase 2 (Research) complete with user approval. The following are confirmed:

- Encoding table (data attributes → visual channels → VL/Vega encoding types or D3 scales)
- Selected engine (Vega-Lite, Vega, or D3) and template
- Ordered transformation plan

## Engine-Specific Implementation Paths

The subtask structure adapts based on the engine selected in Phase 2:

**If Vega-Lite:**
- **Encode** = build the `encoding` block (`"x"`, `"y"`, `"color"`, etc. with field types)
- **Compose** = configure `width`/`height`/composition operators (`layer`, `concat`, `facet`)
- **Narrate** = VL `title`/`description` properties + `text` mark layers for annotations
- **Interact** = `params`/`selection` with `bind` for filters, tooltips via `tooltip` encoding
- **Access** = verify SVG a11y + data table fallback
- Note: VL collapses encode + compose into a single spec-building step since the encoding block implicitly defines marks and layout. Treat them as one pass when building the spec, but validate each concern separately.

**If full Vega:**
- **Encode** = define `signals`, `data` transforms, and `scales`
- **Compose** = configure `marks`, `axes`, `legends`, and layout groups
- **Interact** = signal-driven interactions (drag, hover, zoom via `events` and `update` expressions)
- **Access** = same SVG a11y approach as VL

**If D3 (sankey only):**
- Follow the existing D3 workflow described below

## Subtask Dependency Graph

```
encode (+ color access) → compose (+ semantic SVG) → ┬─ narrate (+ text alt) ─┐→ access-audit
                                                      └─ interact              ─┘
```

- **Encode** must complete before compose (marks must exist before layout)
- **Compose** must complete before narrate and interact (layout must exist before annotations/behavior)
- **Narrate** and **interact** run in parallel (independent concerns)
- **Access-audit** runs after both narrate and interact complete (final integration check)

## Subtask Instructions

### Encode — Implement Scales and Marks

Create the visual encoding: data transforms, scales, axes, and marks.

**Weave in color accessibility during encoding:**

- Select colorblind-safe palette (viridis, Okabe-Ito, or ColorBrewer safe options)
- Run colorblind simulation on the chosen palette — if distinctions disappear, add redundant encoding (shape, pattern, direct label)
- Verify contrast ratios: graphical objects ≥ 3:1 against adjacent colors

**Steps (vary by engine):**

1. Apply the transformation plan from Phase 2 — pivot, aggregate, derive, coerce, filter
2. **Vega-Lite:** Build the `encoding` block with field names, types (`quantitative`, `nominal`, `temporal`, `ordinal`), and scale/axis configuration
3. **Vega:** Define explicit `scales` (domain from data extent, range from layout), `axes`, and `marks` arrays
4. **D3:** Implement D3 scales matching the encoding table — domain from data extent, range from layout dimensions; create marks with correct channel mappings
5. Generate axes with appropriate ticks, labels, and formatting
6. Apply color palette with colorblind safety verified
7. For quantitative scales: VL/Vega use `"nice": true`; D3 uses `.nice()`

**Cross-reference:** `mode-encode.md`, `vega-lite-patterns.md`, `vega-patterns.md`, `d3-patterns.md`, `chart-patterns.md`, `base-template.md`

**Special cases:** `canvas-patterns.md` (>1000 elements), `network-patterns.md` (force-directed graphs)

### Compose — Arrange with Visual Hierarchy

Arrange encoded elements into a coherent spatial layout.

**Weave in semantic SVG structure during composition:**

- Apply `role="img"` on the SVG root with `aria-labelledby` referencing title and description
- Group related elements with `role="list"` / `role="listitem"` for data series
- Mark decorative elements with `aria-hidden="true"`

**Steps:**

1. Establish margins, drawing area, and responsive viewBox dimensions
2. Apply visual hierarchy — primary data at center or top, secondary at edges
3. Position axes, legends, and controls
4. Apply Gestalt grouping: proximity for related items, similarity for comparable items, enclosure for categorical groups
5. Verify whitespace separates without wasting — margins guide the eye, not fill the page
6. Add semantic SVG roles and grouping to all element groups

**Cross-reference:** `mode-compose.md`, `gestalt.md`, `hierarchy.md`

### Narrate — Add Annotations and Storytelling (parallel with interact)

Add titles, annotations, and guided revelation that make the visualization self-explanatory.

**Weave in text alternatives during narration:**

- Write `<title>` and `<desc>` elements that describe the insight, not the implementation
- Provide a data table fallback in `<details>` for screen reader users
- Layer descriptions: brief title → summary takeaway → detailed data on demand

**Steps:**

1. Write a title that states the takeaway, not just the topic
2. Add subtitle with context (time range, data source, methodology)
3. Annotate key data features — outliers, inflection points, comparison reference lines
4. Choose revelation strategy from Segel-Heer framework: author-driven (fixed narrative) vs. reader-driven (exploratory) vs. hybrid (guided exploration)
5. Write alt text at all three levels: title, summary, detail
6. Create data table fallback with `<details>` / `<summary>` structure

**Cross-reference:** `mode-narrate.md`, `segel-heer.md`, `annotation-patterns.md`

**Skip condition:** Omit visible annotations if the visualization is a dashboard component where narration lives in surrounding UI context. Still write alt text even when skipping visible annotations.

### Interact — Add Dynamic Behavior (parallel with narrate)

Add tooltips, brushing, filtering, transitions, and responsive behavior.

**Steps:**

1. Implement hover tooltips with details-on-demand (position near but not obscuring the element)
2. Add click selection or brushing if exploration is needed
3. Implement filtering controls (legend toggles, sliders, dropdowns) if data density requires subsetting
4. Add transitions for data updates and state changes (exit → update → enter sequence)
5. Handle responsive layout — recalculate scales on resize, use viewBox for SVG scaling
6. Ensure touch-friendly targets (44px minimum) for mobile
7. Manage temporal states: loading skeleton, error display, empty state, partial data, staleness indicators

**Cross-reference:** `mode-interact.md`

**Skip condition:** Omit if the medium is static (print, slide deck, static report). Document the skip decision in the task tree.

### Access Audit — Final Integration Check

Verify that accessibility holds together across all subtasks. This is not a full accessibility implementation — color access, semantic SVG, and text alternatives were woven into earlier subtasks. This is integration verification plus keyboard/ARIA implementation.

**Audit by layer:**

| Layer | Implemented During | Verify Now |
|-------|--------------------|------------|
| Color accessibility | Encode | Palette survives colorblind simulation at final render |
| Semantic structure | Compose | SVG roles and groups correct after all modifications |
| Text alternatives | Narrate | Alt text accurately describes the final visualization |
| Keyboard + ARIA | Access audit (now) | Implement and verify focus management, tab order, live regions |

**Steps:**

1. Implement keyboard navigation — tab order follows visual scanning pattern (title → legend → data → controls), arrow keys within data series
2. Add visible focus indicators (3:1 contrast, outline + offset, not color-alone)
3. Add ARIA live regions for dynamic content (filter results, tooltip announcements)
4. Test complete keyboard-only workflow: can a user reach all data and controls without a mouse?
5. Verify contrast ratios on the final rendered output (not just the planned palette)
6. Check zoom behavior at 200% and 400% — no horizontal scrolling, text remains legible
7. Re-run colorblind simulation on the complete visualization

**Cross-reference:** `mode-access.md`, `color-accessibility.md`, `assistive-tech.md`

## Parallel Execution

When creating tasks for Phase 3 subtasks:

- **Narrate** and **interact** share the same `addBlockedBy` (compose) but do not block each other
- An agent working on narrate does not need to wait for interact, and vice versa
- **Access-audit** uses `addBlockedBy` referencing both narrate and interact tasks
- If interact is skipped, access-audit only blocks on narrate

Mark parallel tasks in the task tree:

```
[Phase 3: narrate] Add annotations for Q4 anomaly        ← parallel with next
[Phase 3: interact] Add tooltip and filter controls       ← parallel with above
```

## Skip Conditions

| Subtask | Skip When | Still Do |
|---------|-----------|----------|
| Narrate | Dashboard component with external narration | Write alt text |
| Interact | Static medium (print, slide, PDF) | Document the skip |
| Access audit | Never skip | — |

## Targeted Entry

When entering Phase 3 at a specific subtask (via signal detection or Phase 5 feedback):

1. Verify the subtask's prerequisites are met:
   - Compose requires encode output
   - Narrate and interact require compose output
   - Access-audit requires narrate and interact output (or documented skips)
2. If prerequisites are missing, scaffold from available state — ask user for existing HTML or code
3. Load the relevant subtask instructions and proceed

## Subtask Feedback Loops

When a later subtask reveals issues in an earlier one:

- **Access audit reveals encoding issues** (palette fails colorblind simulation after modifications) → return to encode, fix, re-verify downstream
- **Narrate reveals layout issues** (annotations collide with data marks) → return to compose to adjust layout
- **Interact reveals encoding issues** (hover targets too small, canvas needed for performance) → return to encode

Create a new task for the revisit rather than reopening the completed task.

## Exit

Proceed to **Phase 4: Refinement** with a complete draft:

- **Vega-Lite / Vega:** Standalone HTML (wrapper template + injected JSON spec) containing encoded marks, composed layout, annotations (or skip), interactions (or skip), and accessibility layers
- **D3:** Standalone HTML with ESM imports containing encoded marks, composed layout, annotations (or skip), interactions (or skip), and accessibility layers

## Sources

- Vega-Lite documentation — https://vega.github.io/vega-lite/
- Vega documentation — https://vega.github.io/vega/
- D3.js documentation — https://d3js.org/getting-started
- WCAG 2.2 Quick Reference — https://www.w3.org/WAI/WCAG22/quickref/
- WAI-ARIA 1.2 specification — https://www.w3.org/TR/wai-aria-1.2/
- Segel, E. and Heer, J. (2010). "Narrative Visualization." https://vis.stanford.edu/papers/narrative
