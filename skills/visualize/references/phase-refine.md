# Phase 4: Refinement

Audit the draft visualization for structural integrity, perceptual effectiveness, and editorial clarity.

## Entry Conditions

Phase 3 (Implementation) complete. A draft HTML visualization exists with:

- Encoded marks and scales
- Composed layout
- Annotations (unless narrate was skipped)
- Interactions (unless interact was skipped)
- Accessibility layers woven in

## Refinement Stance

Tufte's principle applies: erase non-data-ink. Every pixel that doesn't reveal data, explain data, or orient the reader is a removal candidate. But the inverse also matters: every aspect of data that matters should find visual expression. Refinement moves in both directions.

See the visualization fresh. Resist the pull toward the first chart type. Ask whether this encoding truly matches what matters in the data.

Load `mode-refine.md` for the complete refinement methodology.

## Three-Audit Procedure

```
┬─ structural-audit ─┐→ clarity-audit → glance-test
└─ perceptual-audit ─┘
```

Structural audit and perceptual audit examine different aspects and run in parallel. Clarity audit depends on both being resolved first.

### Structural Audit (parallel with perceptual)

Check whether the visualization's structure serves its purpose.

**Encoding appropriateness:**

- Do visual channels match data types? (No hue for quantities, no length for nominals)
- Are magnitude channels anchored at meaningful baselines?
- Would a different chart type serve the argument better?

**Axis integrity:**

- Bar charts start at zero (or use dot plot if zero is meaningless)
- No dual y-axes with manufactured correlation
- Non-linear scales (log, sqrt) are labeled and justified

**Aggregation honesty:**

- Means shown with distribution context (box plot, confidence interval, jittered points)
- Totals include composition visibility
- Time aggregations don't smooth away significant events

**Data-ink ratio:**

- Remove gridlines that don't aid value reading
- Remove borders and boxes that don't separate meaningful regions
- Replace legends with direct labels where possible
- Strip 3D effects, gradients, shadows

Load: `mode-refine.md` (sections 2–3), `common-pitfalls.md`

### Perceptual Audit (parallel with structural)

Check whether the visualization works with human perception.

**Pre-attentive detection:**

- Important features pop out without conscious search
- Anomalies use categorical disruption (not subtle hue shift)
- Color highlights what matters, not decorates

**Comparison support:**

- Adjacent positioning for things that need comparing
- Common baselines over floating comparisons
- Explicit difference encoding over mental arithmetic
- Small multiples over overloaded single charts when needed

**Gestalt alignment:**

- Visual groupings match conceptual groupings
- Proximity, similarity, and enclosure reinforce meaning
- Things that differ conceptually differ visually

**Colorblind re-simulation:**

- Run final rendered output through protanopia and deuteranopia simulation
- Verify redundant encoding holds after all modifications

Load: `mode-refine.md` (section 4), `cleveland-mcgill.md`

### Clarity Audit (after both above)

Check editorial quality and storytelling integrity.

**Label quality:**

- Title states the takeaway, not just the topic
- Axis labels are horizontal when possible
- Font sizes create visual hierarchy (title > labels > annotations > footnotes)

**Annotation coherence:**

- Annotations point to specific data features worth noting
- No orphaned annotations pointing at empty space
- Annotation density does not obscure data

**Storytelling:**

- Guided reading path matches the argument
- Revelation strategy is consistent (author-driven, reader-driven, or hybrid)

**Editorial integrity:**

- Threshold criteria are transparent
- Excluded data is acknowledged
- Simplification serves comprehension, not convenience

Load: `mode-refine.md` (section 5), `iteration-workflow.md`

## Fix Priority

Apply fixes in this order:

1. **Misleading elements first** — truncated axes, dual-axis abuse, 3D distortion. Accuracy precedes aesthetics.
2. **Encoding mismatches second** — channel doesn't match data type. The visualization isn't communicating.
3. **Clarity improvements third** — remove chartjunk, improve labels, adjust colors. Correct visualization becomes easier to read.
4. **Polish last** — alignment, spacing, font consistency. Professional appearance, not comprehension.

## Glance Test

**5-second test:** Look at the visualization for 5 seconds. What do you notice first? Is that what should be noticed first?

**Distracted-glance test** (for dashboards): Does the critical signal survive 3 seconds of divided attention? Dashboard users operate in ambient mode — peripheral awareness with brief focal glances. Critical states must be categorically distinct from normal states. Not a color change — a categorical disruption.

## Regression Check

After applying refinement fixes, verify:

- Color accessibility not broken by palette changes
- Semantic SVG structure intact after layout adjustments
- Alt text still accurate after data or encoding changes
- Keyboard navigation still functional after interaction modifications

## Exit

- **Passing** → proceed to Phase 5: Present
- **Structural issues found** → return to Phase 3 (specific subtask) with targeted fixes
- **Encoding fundamentally wrong** → return to Phase 2 for re-planning
