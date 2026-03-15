---
name: visualize
description: >
  Transform data into browser-runnable D3.js visualizations through principled
  intent framing, encoding, composition, narration, accessibility, interaction, and refinement.
  This skill should be used when the user asks to "create a visualization",
  "make a chart", "graph this data", "show this visually", "visualize this",
  "encode data", "design a layout", "annotate my chart", "make this accessible",
  "add interactivity", or "refine this visualization". Also triggers on broader
  queries: "data viz help", "chart question", "D3.js", "how should I display this",
  "best chart type for", "what visualization", "plot this", "diagram this data".
context: fork
user-invocable: true
disable-model-invocation: true
---

# Visualize

Transform data into browser-runnable D3.js visualizations that communicate insight effectively. Proceed through six phases — from establishing intent to delivering a polished, accessible artifact.

## Phases

| Phase | Purpose | Checkpoint | Reference |
|-------|---------|------------|-----------|
| 1. Context | Establish argument, viewer, cognitive mode, constraints | — | `references/phase-context.md` |
| 2. Research | Assess data, plan encoding, select template | User review | `references/phase-research.md` |
| 3. Implement | Build across encode, compose, narrate, interact, access | — | `references/phase-implement.md` |
| 4. Refine | Audit structural integrity, perception, clarity | — | `references/phase-refine.md` |
| 5. Present | Output final HTML, collect feedback | User review | `references/phase-present.md` |
| 6. Complete | Persist visualization (optional, requires Python 3) | — | `references/phase-present.md` |

## Phase Flow

```
Phase 1        Phase 2         Phase 3            Phase 4        Phase 5       Phase 6
Context   →   Research   →   Implement   →   Refine   →   Present   →   Complete
              [checkpoint]                                [checkpoint]
                  ↑               ↑                           │
                  └───────────────┴───── feedback loops ──────┘
```

Feedback loops: user review at Phase 5 may route back — "change chart type" → Phase 2, "fix layout" → Phase 3:compose, "something feels off" → Phase 4.

## Signal Detection → Phase Routing

| Signal | Route To |
|--------|----------|
| "visualize this data", "create a chart", "make a graph" | Phase 1 (full workflow) |
| "what chart type", "encode", "bar vs line", "represent" | Phase 2: plan-encoding |
| "layout", "arrange", "hierarchy", "whitespace", "grid" | Phase 3: compose |
| "annotate", "title", "story", "explain", "highlight" | Phase 3: narrate |
| "accessible", "WCAG", "colorblind", "screen reader", "ARIA" | Phase 3: access-audit |
| "interactive", "filter", "zoom", "hover", "brush", "animate" | Phase 3: interact |
| "improve", "refine", "what's wrong", "simplify", "clearer" | Phase 4 |
| "network", "graph", "nodes", "force-directed" | Phase 2 + `network-patterns.md` |
| "large dataset", "100k", "millions", "performance" | Phase 2 + `canvas-patterns.md` |
| "why visualize", "what's the point", "who is this for" | Phase 1 |

## Targeted Entry

When the user enters with a specific need rather than a full visualization request:

1. Identify the target phase and subtask from signal detection
2. Verify prerequisites exist (argument, encoding plan, draft HTML — whatever the target phase requires)
3. If prerequisites are missing, gather them through focused questions — do not run earlier phases in full
4. Load the target phase reference and proceed

Example: "make this chart accessible" → Phase 3: access-audit. Verify draft HTML exists; if not, ask for it. Load `phase-implement.md` and jump to the access-audit subtask.

## Anti-Patterns

| Never Do | Because | Instead |
|----------|---------|---------|
| Rainbow or jet colormaps | Perceptually non-uniform — distorts magnitude, creates false boundaries | Sequential single-hue or diverging palette (viridis, Tableau10) |
| 3D charts for 2D data | Occlusion hides data, perspective distorts area/length | 2D equivalent with opacity or faceting |
| Pie charts with >7 slices or small differences | Angle comparison ranks low on Cleveland-McGill | Bar chart (length encodes more accurately) |
| Truncated y-axis on bar charts | Bar length encodes magnitude from zero — truncation breaks that | Start at zero, or use dot plot |
| Color as sole differentiator | ~8% of males have color vision deficiency | Pair with shape, pattern, or direct label |
| Dual y-axes without labeling each series | Readers misattribute correlation between unrelated scales | Two aligned charts sharing x-axis |
| Decorative chartjunk | Violates data-ink ratio — non-data pixels compete for attention | Strip to data-ink; whitespace for separation |
| Default fonts below 11px on dense charts | Legibility collapses; labels become decoration | Minimum 12px; rotate or abbreviate if cramped |
| Treating accessibility as final-pass check | Encoding dependencies go unnoticed until too late | Weave color access into encode, semantic SVG into compose, text alternatives into narrate |

For expanded analysis, load `references/common-pitfalls.md`.

## Workflow Tracking

Create a task for each phase and update status as each completes. Use dependency tracking for sequential phases — parallel tasks share the same blockers but do not block each other.

```
[Phase 1] Context — define argument and viewer for <description>
[Phase 2] Research — assess data and plan encoding
[Phase 2: checkpoint] User review of encoding plan
[Phase 3: encode] Implement D3 scales and marks (+ color access)
[Phase 3: compose] Arrange layout with hierarchy (+ semantic SVG)
[Phase 3: narrate] Add annotations and storytelling        ← parallel with next
[Phase 3: interact] Add tooltip and filter controls        ← parallel with above
[Phase 3: access-audit] ARIA roles, keyboard navigation
[Phase 4: structural] Structural audit                     ← parallel with next
[Phase 4: perceptual] Perceptual audit                     ← parallel with above
[Phase 4: clarity] Clarity audit and glance test
[Phase 5] Present visualization and collect feedback
[Phase 5: checkpoint] User review of final output
[Phase 6] Persist and exit
```

## Browser-Runnable Output

All visualizations produce standalone HTML with ESM imports:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Visualization Title</title>
  <style>/* Styles embedded for portability */</style>
</head>
<body>
  <div id="container"></div>
  <script type="module">
    import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";
    const data = [...]; // Data embedded for standalone operation
  </script>
</body>
</html>
```

### Persisting Visualizations

**With CLI** (requires Python 3):

Save to `${CLAUDE_PROJECT_DIR}/.claude/visualizations/viz-<timestamp>.html`, then register with the management CLI:

```
python3 scripts/visualizer.py create --file <path>
```

This copies the file to organized storage at `~/.visualizer-skill/visualizations/` grouped by chart type. See `references/base-template.md` for required frontmatter fields.

**Without CLI** (one-off visualizations):

Save directly to `${CLAUDE_PROJECT_DIR}/.claude/visualizations/viz-<timestamp>.html`. Add HTML frontmatter (see `references/base-template.md`) for future discoverability. The visualization is fully functional without CLI registration.

## Templates

Use templates from `assets/d3/templates/` as starting points. 19 templates organized by data relationship — see `references/template-selection.md` for the decision tree. For chart types not covered (radar, chord diagram, parallel coordinates, etc.), follow the Custom Template Workflow below.

## Custom Template Workflow

When the user needs a visualization type not covered by the 19 built-in templates (e.g., radar chart, chord diagram, parallel coordinates, streamgraph, waffle chart):

### 1. Confirm No Existing Template

Check `assets/d3/templates/` — if a template exists for the requested chart type, use it instead.

### 2. Craft the Template

Build a browser-runnable HTML template following `references/base-template.md` structure. The template must meet:

| Requirement | Standard |
|-------------|----------|
| **Correctness** | Renders when opened directly in a browser — no build step, no server |
| **Completeness** | All dependencies via CDN (ESM), sample data embedded, styles inlined |
| **Customizability** | Comments explain where and how to modify for different data |
| **Accessibility** | `role="img"` on SVG, title/description elements, Tableau10 colors, 4.5:1 contrast |
| **Responsiveness** | viewBox-based scaling (not fixed width/height), mobile-friendly touch targets |

Use D3 patterns from `references/chart-patterns.md`. Use `.join()` for data binding, D3 margin convention, ESM imports.

### 3. Quality Checklist

Before completing, verify:

- [ ] Opens and renders in browser without errors
- [ ] Sample data produces visible, meaningful visualization
- [ ] Tooltip appears on hover with correct data
- [ ] SVG has `role="img"`, title, and description elements
- [ ] Color scheme is colorblind-safe (Tableau10 default)
- [ ] Uses viewBox for responsiveness
- [ ] Uses `.join()` for data binding
- [ ] DATA section documents expected format

## CLI Workflows

The visualization management CLI (`scripts/visualizer.py`) is available when Python 3 is installed. These natural language patterns trigger CLI operations:

| User Says | Action |
|-----------|--------|
| "save this visualization", "persist this chart", "store this" | `python3 scripts/visualizer.py create --file <path>` |
| "show my visualizations", "list my charts", "what have I made" | `python3 scripts/visualizer.py list` |
| "show me the bar charts", "list scatter plots" | `python3 scripts/visualizer.py list --type <chart-type>` |
| "find my sales visualizations", "search for revenue" | `python3 scripts/visualizer.py search <term>` |
| "show details for this visualization", "info on this chart" | `python3 scripts/visualizer.py show <id>` |
| "delete this visualization", "remove this chart" | `python3 scripts/visualizer.py delete <id> --force` |

**Before invoking any CLI command**: Check if Python 3 is available by running `python3 --version`. If unavailable, inform the user that the CLI requires Python 3 and offer to save the file directly instead.

## Plan-Aware Execution

If a plan file exists at `.claude/plans/*.md` describing a visualization task:

1. Read the plan file
2. Identify which phases are already resolved
3. Create tasks only for remaining phases
4. Begin from the first unresolved phase

When producing a plan, include: exact data file paths, Frame decisions verbatim, chart type and encoding assignments, selected template, accessibility constraints.

## References

**Phase workflow:**

- **`references/phase-context.md`** — Argument, viewer, cognitive mode, constraints
- **`references/phase-research.md`** — Data assessment, encoding plan, template selection, user checkpoint
- **`references/phase-implement.md`** — Build orchestration across encode, compose, narrate, interact, access
- **`references/phase-refine.md`** — Structural, perceptual, and clarity audits
- **`references/phase-present.md`** — Output, user review, persist, complete

**Mode methodology:**

- **`references/mode-encode.md`** — Cleveland-McGill rankings, channel selection, data type mapping
- **`references/mode-compose.md`** — Gestalt principles, visual hierarchy, whitespace, grid systems
- **`references/mode-narrate.md`** — Segel-Heer framework, annotation patterns, storytelling
- **`references/mode-access.md`** — WCAG compliance, color accessibility, ARIA, keyboard navigation
- **`references/mode-interact.md`** — Brushing, linking, transitions, responsive adaptation
- **`references/mode-refine.md`** — Iteration workflow, common pitfalls, data-ink ratio

**Theory and perceptual science:**

- **`references/cleveland-mcgill.md`** — Perceptual accuracy rankings for visual channels
- **`references/gestalt.md`** — Gestalt grouping principles for layout
- **`references/segel-heer.md`** — Narrative visualization framework
- **`references/hierarchy.md`** — Visual hierarchy and attention flow
- **`references/channel-guide.md`** — Visual channel reference by data type
- **`references/color-accessibility.md`** — Color vision deficiency simulation and safe palettes
- **`references/common-pitfalls.md`** — Frequent visualization mistakes and corrections
- **`references/assistive-tech.md`** — Screen reader, keyboard, and assistive technology patterns

**Implementation patterns:**

- **`references/d3-patterns.md`** — Browser-runnable templates, ESM imports, responsive patterns
- **`references/chart-patterns.md`** — D3 implementation patterns by chart type
- **`references/plot-patterns.md`** — Observable Plot for rapid prototyping
- **`references/network-patterns.md`** — Force-directed graphs, edge visibility, interaction
- **`references/canvas-patterns.md`** — Canvas rendering for large datasets
- **`references/annotation-patterns.md`** — D3 annotation library patterns and positioning

**Workflow:**

- **`references/base-template.md`** — HTML skeleton with frontmatter, ESM imports
- **`references/template-selection.md`** — Template decision tree by data shape and question type
- **`references/data-preparation.md`** — Pivot, aggregate, derive, and clean data
- **`references/iteration-workflow.md`** — Systematic refinement loop and critique framework
