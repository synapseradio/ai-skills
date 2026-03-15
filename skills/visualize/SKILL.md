---
name: visualize
description: >
  Transform data into browser-runnable Vega-Lite and Vega visualizations through principled
  intent framing, encoding, composition, narration, accessibility, interaction, and refinement.
  This skill should be used when the user asks to "create a visualization",
  "make a chart", "graph this data", "show this visually", "visualize this",
  "encode data", "design a layout", "annotate my chart", "make this accessible",
  "add interactivity", or "refine this visualization". Also triggers on broader
  queries: "data viz help", "chart question", "vega-lite", "vega", "D3.js",
  "how should I display this", "best chart type for", "what visualization",
  "plot this", "diagram this data".
context: fork
user-invocable: true
---

# Visualize

Transform data into browser-runnable visualizations using Vega-Lite for standard charts, full Vega for complex charts (force layouts, treemaps, geographic projections), and D3 for sankey diagrams. Proceed through six phases — from establishing intent to delivering a polished, accessible artifact.

## Phases

| Phase | Purpose | Checkpoint | Reference |
|-------|---------|------------|-----------|
| 1. Context | Establish argument, viewer, cognitive mode, constraints | — | `references/phase-context.md` |
| 2. Research | Assess data, plan encoding, select engine and template | User review | `references/phase-research.md` |
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

| Never Do | Instead |
|----------|---------|
| Rainbow colormaps | Sequential single-hue or diverging palette (viridis, Tableau10) |
| 3D charts for 2D data | 2D equivalent with opacity or faceting |
| Pie charts with >7 slices | Bar chart (length encodes more accurately) |
| Truncated y-axis on bar charts | Start at zero, or use dot plot |
| Color as sole differentiator | Pair with shape, pattern, or direct label |
| Full Vega when Vega-Lite suffices | Check `engine-selection.md` — VL first, Vega only when transforms require it |

For the full list with rationale, load `references/common-pitfalls.md`.

## Workflow Tracking

Create a task for each phase and update status as each completes. Use dependency tracking for sequential phases — parallel tasks share the same blockers but do not block each other.

```
[Phase 1] Context — define argument and viewer for <description>
[Phase 2] Research — assess data, select engine, plan encoding
[Phase 2: checkpoint] User review of engine choice and encoding plan
[Phase 3: encode] Implement VL/Vega spec or D3 scales and marks (+ color access)
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

All visualizations produce standalone HTML files that open directly in a browser with no build step.

**Vega/VL charts** (18 templates): Copy `assets/vega/wrapper.html`, inject the JSON spec, fill in frontmatter and title. The wrapper loads Vega stack from CDN, renders via `vegaEmbed`, and auto-generates an accessibility data table. See `references/base-vega-wrapper.md`.

**D3 charts** (sankey only): Generate standalone HTML with ESM imports from CDN. See `references/base-template.md`.

### Persisting Visualizations

Save to `${CLAUDE_PROJECT_DIR}/.claude/visualizations/viz-<timestamp>.html`. If Python 3 is available, register with `python3 scripts/visualizer.py create --file <path>` for organized storage. See `references/phase-present.md` for the full persist workflow.

## Templates

12 Vega-Lite specs + 6 Vega specs + 1 D3 template across 8 categories. Use `references/engine-selection.md` to choose the engine, then select the template from `assets/vega/templates/` (VL/Vega) or `assets/d3/templates/` (sankey only). See `references/template-selection.md` for the full decision tree. For chart types not covered (radar, chord diagram, parallel coordinates, etc.), follow the Custom Template Workflow below.

## Custom Template Workflow

When the user needs a visualization type not covered by the 19 built-in templates (e.g., radar chart, chord diagram, parallel coordinates, streamgraph, waffle chart):

### 1. Confirm No Existing Template

Check `assets/vega/templates/` and `assets/d3/templates/` — if a template exists for the requested chart type, use it instead.

### 2. Craft the Template

Prefer Vega-Lite or Vega specs when possible. Use D3 HTML only for chart types neither can express (like sankey). Follow `references/base-vega-wrapper.md` (Vega/VL) or `references/base-template.md` (D3).

| Requirement | Standard |
|-------------|----------|
| **Correctness** | Renders when opened directly in a browser — no build step, no server |
| **Completeness** | All dependencies via CDN, sample data embedded, styles inlined |
| **Customizability** | `_metadata` block documents data format and customization points (VL/Vega) or inline comments (D3) |
| **Accessibility** | SVG title/description, Tableau10 colors, 4.5:1 contrast, data table fallback |
| **Responsiveness** | `width: "container"` (VL) or viewBox-based scaling (D3) |

For VL/Vega specs, use patterns from `references/vega-lite-patterns.md` and `references/vega-patterns.md`. For D3, use patterns from `references/chart-patterns.md`.

### 3. Quality Checklist

Before completing, verify:

- [ ] Opens and renders in browser without errors
- [ ] Sample data produces visible, meaningful visualization
- [ ] Tooltip appears on hover with correct data
- [ ] SVG has title and description elements
- [ ] Color scheme is colorblind-safe (Tableau10 default)
- [ ] Responsive sizing (`width: "container"` for VL, viewBox for D3)
- [ ] `_metadata` block documents data format (VL/Vega) or DATA section (D3)
- [ ] Data table fallback renders in `<details>` block

## CLI Workflows

The visualization management CLI (`scripts/visualizer.py`) requires Python 3. Check availability with `python3 --version` before use. Commands: `create --file <path>`, `list [--type <chart-type>]`, `search <term>`, `show <id>`, `delete <id> --force`. See `references/phase-present.md` for natural language routing.

## Plan-Aware Execution

If a plan file exists at `.claude/plans/*.md` describing a visualization task:

1. Read the plan file
2. Identify which phases are already resolved
3. Create tasks only for remaining phases
4. Begin from the first unresolved phase

When producing a plan, include: exact data file paths, Frame decisions verbatim, chart type and encoding assignments, selected template, accessibility constraints.

## References

**Mode methodology** (loaded during Phase 3 implementation):

| Mode | Reference | Purpose |
|------|-----------|---------|
| Encode | `references/mode-encode.md` | Cleveland-McGill rankings, channel selection, data type mapping |
| Compose | `references/mode-compose.md` | Gestalt principles, visual hierarchy, layout |
| Narrate | `references/mode-narrate.md` | Segel-Heer framework, annotation patterns |
| Access | `references/mode-access.md` | WCAG compliance, color accessibility, ARIA |
| Interact | `references/mode-interact.md` | Selections, brushing, linking, transitions |
| Refine | `references/mode-refine.md` | Iteration workflow, common pitfalls |

**Implementation patterns:**

| Topic | Reference |
|-------|-----------|
| Vega-Lite specs | `references/vega-lite-patterns.md` |
| Full Vega specs | `references/vega-patterns.md` |
| Engine selection | `references/engine-selection.md` |
| Template selection | `references/template-selection.md` |
| VL/Vega HTML wrapper | `references/base-vega-wrapper.md` |
| D3 HTML skeleton | `references/base-template.md` |
| D3 patterns (sankey) | `references/d3-patterns.md`, `references/chart-patterns.md` |
| Data transforms | `references/data-preparation.md` |
| Networks | `references/network-patterns.md` |
| Large datasets | `references/canvas-patterns.md` |

**Theory** (cross-referenced from mode docs): `cleveland-mcgill.md`, `gestalt.md`, `segel-heer.md`, `hierarchy.md`, `channel-guide.md`, `color-accessibility.md`, `common-pitfalls.md`, `assistive-tech.md`, `annotation-patterns.md`, `iteration-workflow.md`
