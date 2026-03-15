# Refine Mode

Improve visualizations in progress through principled iteration.

## When to Use

- Improving an existing chart
- Iterating on a visualization design
- Responding to "what's wrong with this"
- Making a visualization clearer
- Simplifying a graph
- Cleaning up visual clutter
- When "something feels off" about a visualization

## Applicability Check

**In comprehensive mode**: Always runs—every visualization benefits from a refinement pass.

**Quick check**: Does a visualization draft exist? If yes → run this mode.

## The Refinement Stance

Refinement is not critique alone. Critique identifies problems; refinement solves them. The goal is not to enumerate what's wrong but to transform what exists into something that works better for readers.

Tufte's principle applies: erase non-data-ink. Every pixel that doesn't reveal data, explain data, or orient the reader to data is a candidate for removal. But the inverse also matters: every aspect of the data that matters should find visual expression. Refinement moves in both directions.

See the visualization fresh. Resist the pull toward the first chart type that came to mind. The default choice (bar chart, line chart, pie chart) may be correct, but only if it survives examination. Ask whether this encoding truly matches what matters in the data.

## Instructions

### 1. Establish What Exists

Before refining, understand what you're refining:

**Identify the current state.** What visualization exists? Describe it without judgment first: chart type, encoding channels used, data represented, labels and annotations present, color choices made.

**Identify the intended purpose.** What question should this visualization answer? What comparison should it enable? What pattern should it reveal? If purpose is unclear, ask before proceeding.

**Identify the audience.** Who will read this? What do they already know? What decisions will this visualization inform? Refinement for an executive dashboard differs from refinement for a technical appendix.

### 2. Audit for Structural Integrity

Check whether the visualization's structure serves its purpose:

**Encoding appropriateness.** Examine whether visual channels match data types:

- Position and length for quantities readers need to compare precisely
- Color saturation or area for quantities readers need to perceive relatively
- Hue for categorical distinctions (with colorblind-safe palette)
- Shape for categorical backup when color is already committed

If a quantity is encoded as area or volume, flag it. Human perception of area is nonlinear and imprecise. Consider whether position or length would serve better.

**Axis integrity.** Check whether axes mislead:

- Bar charts with non-zero baselines exaggerate differences
- Dual y-axes with different scales invite false comparisons
- Truncated axes hide context
- Non-linear scales (log, sqrt) may be justified but must be labeled

If an axis choice distorts perception, note the specific distortion and propose correction.

**Aggregation honesty.** Check whether summary statistics hide relevant variation:

- Means without distributions hide spread
- Totals without breakdowns hide composition
- Time aggregations may smooth away significant events

When aggregation obscures, consider showing distributions (box plots, violin plots, jittered points) or adding summary statistics (mean with confidence interval, sample size annotation).

### 3. Audit for Visual Clarity

Check whether visual choices help or hinder comprehension:

**Data-ink ratio.** For each visual element, ask: does this reveal data? If not, does it orient the reader? If neither, it's a removal candidate:

- Gridlines that don't aid reading values
- Borders and boxes that don't separate meaningful regions
- Legends that could be replaced with direct labels
- 3D effects that add nothing but distortion

**Color economy.** Check color usage:

- Rainbow colormaps destroy ordinal perception and fail for colorblind readers
- Too many categorical colors overwhelm (limit to 5-8 distinguishable hues)
- Color meaning should be consistent across a document
- Sequential data needs sequential palette (single hue varying in lightness)
- Diverging data needs diverging palette (two hues with neutral midpoint)

**Typography clarity.** Check whether text elements work:

- Axis labels should be horizontal when possible
- Titles should state the takeaway, not just the topic
- Annotations should point to specific data features worth noting
- Font sizes should create visual hierarchy (title > labels > annotations)

### 4. Audit for Perceptual Effectiveness

Check whether the visualization works with human perception:

**Preattentive detection.** Important features should pop out without search. If readers must hunt for the pattern, the encoding is working against perception. Consider:

- Stronger contrast for important comparisons
- Color to highlight what matters, not to decorate
- Size and position for what readers should notice first

**Comparison support.** If the visualization asks readers to compare values:

- Adjacent positioning beats distant positioning
- Common baselines beat floating comparisons
- Small multiples beat overloaded single charts
- Explicit difference encoding beats mental arithmetic

**Gestalt grouping.** Check whether visual groupings match conceptual groupings:

- Things that should be compared should be visually similar
- Things that differ conceptually should differ visually
- Proximity, similarity, and enclosure should reinforce meaning

### 5. Audit for Editorial Integrity

Check whether simplification choices serve clarity or comfort:

**Threshold audit.** If the visualization uses categorical thresholds:

- Who set them? When, relative to data collection?
- Are criteria transparent to the viewer?
- Can the user reach the underlying evidence in one click?

**Inclusion audit.** What data was excluded?

- Would exclusion still happen if the data supported the preferred conclusion?
- Does the simplification serve comprehension or organizational narrative?

**Three conditions for legitimate simplification:**

1. Criteria pre-committed (before data arrives)
2. Ground truth reachable (one deliberate click)
3. User can verify (methodology visible)

If any condition fails, the simplification is editorial, not clarifying.

### 6. Question Default Choices

Default chart types often hide better alternatives:

**Pie charts.** Ask whether the comparison is about parts of a whole where exact precision doesn't matter. If precision matters, horizontal bars ordered by value work better. If there are more than 5-7 slices, consider alternatives.

**Line charts for categories.** Lines imply continuity. If the x-axis is categorical (countries, products, teams), lines suggest a relationship that doesn't exist. Use bars or dots instead.

**Stacked areas.** The middle layers float on unstable baselines, making their heights hard to read. Consider whether small multiples, or just highlighting one series at a time, would work better.

**Dual y-axes.** Two y-axes with different scales invite readers to perceive correlations that are artifacts of scale choice. Consider indexing both series to 100 at a common start, or using two vertically aligned panels with aligned x-axes.

### 7. Apply Fixes in Priority Order

Not all problems are equal. Fix in this order:

1. **Misleading elements first.** If something creates false impressions (truncated axis, dual-axis abuse, 3D distortion), fix it before anything else. Accuracy precedes aesthetics.

2. **Encoding mismatches second.** If a visual channel doesn't match its data type, the visualization isn't communicating. Fix position-for-category and color-for-quantity errors.

3. **Clarity improvements third.** Remove chart junk, improve labels, adjust colors. These make a correct visualization easier to read.

4. **Polish last.** Alignment, spacing, font consistency. These matter for professional appearance but not for comprehension.

### 8. Test the Revision

After making changes, verify improvement:

**State the takeaway aloud.** Can you describe in one sentence what the visualization shows? If you struggle, readers will too.

**Find the story in 5 seconds.** Glance at the visualization. What do you notice first? Is that what should be noticed first?

**Survive the distracted glance.** For monitoring dashboards: does the critical signal
survive 3 seconds of divided attention? Dashboard users operate in ambient mode —
peripheral awareness with brief focal glances. Anomalies encoded in channels requiring
focal attention (subtle hue shift, small positional difference) will be invisible to
the ambient viewer. Critical states must be categorically distinct from normal states.
Not a color change — a categorical disruption.

**Check for introduced problems.** Sometimes fixes create new issues. Did removing a legend make categories impossible to identify? Did changing the color palette break colorblind accessibility?

**Compare before and after.** If possible, view them side by side. The improvement should be visible, not just arguable.

### 9. Document the Rationale

Refinement creates knowledge worth preserving:

**Note what changed and why.** Future iterations benefit from understanding the reasoning behind current choices.

**Note what was preserved and why.** Sometimes complexity earns its place. Document why an apparently complex element serves the visualization's purpose.

**Note alternatives considered.** Recording rejected options saves future refiners from re-exploring dead ends.

## Iteration Workflow

Professional teams refine through cycles:

**Sketch phase.** Multiple quick explorations of different approaches. Don't commit to one encoding until alternatives have been tried. Paper sketches or rough digital drafts both work.

**Critique phase.** Systematic examination using the audits above. Fresh eyes help; if possible, get someone unfamiliar with the data to describe what they see.

**Revision phase.** Apply fixes based on critique. One round rarely suffices. Plan for 2-3 revision cycles for anything important.

**Testing phase.** Show to representative readers. Watch where they look. Listen to what they say. Revise based on actual reader behavior, not assumptions about it.

## Examples

### Overloaded bar chart with too many categories

**Problem identified:** A horizontal bar chart shows 25 product categories, all in different colors, with a legend requiring cross-referencing. The bars are sorted alphabetically.

**Refinement applied:**

1. Sort by value (descending) to create visual ranking
2. Highlight top 5 categories with a single emphasis color; gray the rest
3. Remove legend; use direct labels at bar ends
4. Group remaining 20 categories into "Other" with option to expand

**Result:** Reader immediately sees the important categories. The 20 minor categories are acknowledged but don't compete for attention.

### Line chart hiding uncertainty

**Problem identified:** A projection line extends into the future with the same solid line treatment as historical data. Readers can't distinguish known from estimated.

**Refinement applied:**

1. Dash the projected portion to distinguish it from historical
2. Add a 95% confidence band around projection
3. Add vertical annotation line at "Today" to mark the boundary
4. Adjust title from "Revenue Trend" to "Revenue History and Projection"

**Result:** Readers can instantly see where certainty ends and estimation begins. The confidence band communicates that the projection is not a single fate but a range of possibilities.

### Dual-axis chart creating false correlation

**Problem identified:** Temperature and ice cream sales share a dual-axis line chart. The scales are chosen to make the lines overlap, suggesting causation through visual correlation.

**Refinement applied:**

1. Split into two vertically stacked panels with shared x-axis
2. Or: normalize both to percent-of-maximum for fair visual comparison
3. Remove the implicit causation claim; let readers draw their own conclusions
4. Add honest title acknowledging correlation without claiming cause

**Result:** The data is shown without the chart arguing a conclusion. Readers can see the relationship but aren't manipulated by scale alignment.

## When Not to Over-Refine

Some contexts warrant restraint:

**Exploratory analysis.** When the goal is finding patterns rather than communicating them, quick and rough visualization serves better than polished work. Don't refine exploration into communication prematurely.

**Internal working documents.** Polish has diminishing returns for audiences already familiar with the data and context. Save deep refinement for external communication.

**Speed-critical decisions.** A good-enough chart now beats a perfect chart too late. Match refinement effort to the stakes of the decision.

**Learning contexts.** Sometimes showing the full complexity, even if overwhelming, teaches what summary charts hide. Refinement toward simplicity is not always the goal.

## Further Reading

For deeper guidance on specific refinement topics:

- See `common-pitfalls.md` for anti-patterns organized by damage type (misleading, perceptual, structural, honesty)
- See `iteration-workflow.md` for professional team practices from NYT Graphics, The Pudding, and FiveThirtyEight

## Phase Transition

After refinement, consider:

- **Access** to verify accessibility wasn't broken by changes
- **Encode** if refinement revealed fundamental encoding issues
- Loop back to earlier modes if refinement uncovered deeper problems
