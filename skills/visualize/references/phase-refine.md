# Phase 4: Refinement

Audit the draft visualization for structural integrity, perceptual effectiveness, and editorial clarity.

## Entry Conditions

Phase 3 (Implementation) complete. A draft HTML visualization exists with encoded marks, composed layout, annotations (unless skipped), interactions (unless skipped), and accessibility layers.

## Three-Audit Procedure

```
┬─ structural-audit ─┐→ clarity-audit → glance-test
└─ perceptual-audit ─┘
```

Structural audit and perceptual audit run in parallel. Clarity audit depends on both being resolved first. Load `mode-refine.md` for the full audit methodology — the sections below are checklists, not the methodology itself.

### Structural Audit (parallel with perceptual)

> **Vega/VL:** Inspect the `"encoding"` and `"mark"` fields directly — the declarative spec makes encoding decisions auditable without reading imperative code.

- [ ] Visual channels match data types (no hue for quantities, no length for nominals)
- [ ] Magnitude channels anchored at meaningful baselines (bars start at zero)
- [ ] No dual y-axes with manufactured correlation
- [ ] Means shown with distribution context; aggregations don't smooth away significant events
- [ ] Data-ink ratio: remove non-data gridlines, borders, 3D effects; replace legends with direct labels where possible

### Perceptual Audit (parallel with structural)

- [ ] Important features pop out without conscious search (pre-attentive detection)
- [ ] Adjacent positioning for things that need comparing; common baselines over floating comparisons
- [ ] Visual groupings match conceptual groupings (Gestalt alignment)
- [ ] Colorblind re-simulation passes on final rendered output

### Clarity Audit (after both above)

- [ ] Title states the takeaway, not just the topic
- [ ] Annotations point to specific data features; no orphaned annotations
- [ ] Guided reading path matches the argument
- [ ] Threshold criteria transparent; excluded data acknowledged

## Fix Priority

1. **Misleading elements first** — truncated axes, dual-axis abuse, 3D distortion
2. **Encoding mismatches second** — channel doesn't match data type
3. **Clarity improvements third** — remove chartjunk, improve labels, adjust colors
4. **Polish last** — alignment, spacing, font consistency

## Glance Test

**5-second test:** What do you notice first? Is that what should be noticed first?

**Distracted-glance test** (dashboards): Does the critical signal survive 3 seconds of divided attention? Critical states must be categorically distinct from normal states — not a color change, a categorical disruption.

## Regression Check

After applying fixes, verify: color accessibility not broken, semantic SVG intact, alt text still accurate, keyboard navigation still functional.

## Exit

- **Passing** → Phase 5: Present
- **Structural issues** → Phase 3 (specific subtask) with targeted fixes
- **Encoding fundamentally wrong** → Phase 2 for re-planning

Cross-references: `mode-refine.md` (full methodology), `common-pitfalls.md`, `cleveland-mcgill.md`, `iteration-workflow.md`
