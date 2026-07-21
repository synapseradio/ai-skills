# Phase 4: Verify

Mandatory second draft. Every visualization gets two render-free verification
passes, a fix pass, and re-verification before presenting to the user. No pass
opens a browser or captures the screen — both read the source.

## Entry Conditions

Phase 3 (Build) complete. A draft HTML visualization exists.

## Verification Protocol (both paths, consensus required)

### Path A: Structural Verification

Read back the generated HTML file. Check:

- [ ] Vega spec is valid JSON (or D3 code has no syntax errors)
- [ ] Data fields in the spec match the encoding table from Phase 2
- [ ] Units present on all axis labels and tooltips
- [ ] OpenColors palette used (verify hex values)
- [ ] Title states the insight, not the topic
- [ ] Bar charts start at zero
- [ ] Categories sorted by value, not alphabetically
- [ ] No dual y-axes
- [ ] Redundant encoding for accessibility (color + shape or color + label)
- [ ] SVG `<title>` and `<desc>` elements present
- [ ] Data table fallback in `<details>` block

### Path B: Render Inference

Predict what the source will draw, without running it. Every check reads the spec
or HTML — there is no browser, no screen capture, and no browser MCP. Each item
below is a defect a screenshot used to catch, recovered as something the source
already tells you.

- [ ] Overflow / clipping — mark and label extents fit the declared `width`/`height`/viewBox and margins
- [ ] Label collision — tick count times estimated label length fits the available axis span
- [ ] Axis domain / zero baseline — length encodings start at zero; the quantitative domain is correct
- [ ] Encoding vs. data — every encoded field exists in the bound data rows
- [ ] Mark count — declared mark count is consistent with data length (no empty or partial chart)
- [ ] Legend wiring — the legend is bound to the same field and scale as the series
- [ ] Engine wiring — required CDN scripts and the render call are present; JSON is well-formed
- [ ] Scroll containment — no wheel/zoom handler and no `overflow`/`100vh` lets the chart capture the page's scroll
- [ ] Keyboard-interaction wiring — interactive marks carry `tabindex`, key handlers, and focus styles

Scroll hijacking and unwired keyboard interaction are exactly the defects the
mandatory second draft was created to catch. A screenshot never showed either: a
still image cannot reveal that the wheel is trapped or that Tab reaches nothing.
The source can.

### Consensus

Both passes must agree the chart is correct. They are distinct on purpose.
Structural read-back proves the code is correct; render inference reasons forward
from that code to what it will draw. When they disagree, treat the disagreement
itself as a defect: re-read the source until you can explain why one pass saw
what the other missed, then fix.

Fix all issues found by either pass.

### Optional accelerator (never a gate)

A stdlib-only static-analysis script can mechanically flag render-blocking defects
across all three engines, as a fast first sweep before the Path B reasoning:

```bash
python3 scripts/check_render.py <path> [<path> ...]
```

It prints each defect with file and cause and exits non-zero on a render-blocking
defect. It accelerates render inference; it never replaces it and never blocks
presenting. If Python is unavailable, the script is missing, or it errors, the two
prose passes stand on their own and verification proceeds unchanged.

## Editorial Integrity Check

After structural and visual checks, load [mode-refine.md](mode-refine.md) for the full audit:

- **Threshold-based pre-interpretation:** Did you choose breakpoints that support the narrative?
- **Metric selection bias:** Would this metric be included if it showed the opposite trend?
- **Designer's epistemic commitment:** Are contradictory findings suppressed while "interesting"
  findings get prominence?

## Fix Priority

1. **Misleading** — truncated axes, hidden distribution, cherry-picked windows
2. **Encoding mismatches** — wrong channel for data type, missing units
3. **Clarity** — weak title, missing annotations, poor hierarchy
4. **Polish** — alignment, spacing, font consistency

## Second Draft

After fixing, produce a second draft and re-verify both passes. Run a style pass on the
second draft against the Core Principles — composition, color, spacing, simplicity. Those
principles are inlined in `SKILL.md` and detailed in [mode-compose.md](mode-compose.md) and
[mode-narrate.md](mode-narrate.md); the skill carries its own style standard and depends on
no other skill. Only proceed to Phase 5 after the second draft passes.

## Regression Check

After fixes: color accessibility intact? Annotations accurate? Layout balanced? Units present?

## Exit

- **Passing** → Phase 5: Present
- **Structural issues** → Phase 3 (specific subtask)
- **Encoding fundamentally wrong** → Phase 2 for re-planning
