# Iteration Workflow

How professional visualization teams refine work from draft to publication. Based on practices documented at The New York Times Graphics team, The Pudding, and FiveThirtyEight. These patterns synthesize established visualization practice. Primary sources are cited where available.

## The Story-First Principle

Professional teams start from the story, not the chart. Before any visual encoding, they answer:

**What should the reader take away?** This isn't "here's some data about climate change." It's "your city will feel like a different city within your lifetime." The takeaway shapes everything.

**What decision or understanding does this serve?** Visualizations exist to change what readers know or do. If the visualization doesn't connect to a decision or insight, question whether it's needed.

**Who is the audience?** General readers need different treatment than domain experts. The same data might become an interactive explainer for public audiences and a dense statistical summary for researchers.

Once the story is clear, encoding choices follow. The chart serves the story; the story doesn't serve the chart.

## The Iteration Cycle

### Phase 1: Exploration (Diverge)

**Multiple sketches before any commitment.** Paper, whiteboard, or rough digital—the medium doesn't matter. Speed matters. Generate 3-5 different approaches before selecting one.

Questions to explore:

- What chart types could work?
- What's the primary comparison? Secondary?
- What would a reader unfamiliar with the data notice first?
- What's the minimum needed to convey the point?

**Low-fidelity is intentional.** Rough sketches discourage premature polish. If a sketch looks too finished, designers become attached. Keep exploration loose.

**Challenge the first instinct.** The first chart type that comes to mind is often a default, not a choice. Deliberately explore alternatives. If your instinct says bar chart, sketch a dot plot, a table, a slope chart. Then return to the bar chart if it's still best.

### Phase 2: Prototype (Converge)

**Build the chosen approach enough to evaluate.** This isn't the final implementation. It's a working version sufficient to reveal problems.

At The Pudding, prototyping typically uses:

- Static mockups for layout and proportion
- Interactive prototypes (D3, Svelte) for testing scrollytelling flow
- Real data, even if incomplete

**Test the prototype with fresh eyes.** Someone who hasn't seen the data should describe what they notice. Their description reveals what the visualization actually communicates, which may differ from intent.

The gap between intent and perception is where refinement happens.

### Phase 3: Critique (Evaluate)

**Systematic evaluation before revision.** Random noticing produces random fixes. Structured critique ensures coverage.

The PDIEC framework provides structure:

1. **Purpose**: Is the intended takeaway clear? Does the title state it?
2. **Data integrity**: Does the visualization accurately represent the data?
3. **Encoding & design**: Do visual channels match data types?
4. **Interpretation**: Can readers draw correct conclusions?
5. **Accessibility & context**: Does it work for all readers? Are sources cited?

**External perspective is essential.** Creators become blind to their own work's problems. The NYT Graphics team regularly circulates work-in-progress for internal critique. Fresh eyes catch what familiarity hides.

**Critique the work, not the worker.** Effective critique focuses on whether the visualization serves readers. It doesn't judge the creator's skill or intentions.

### Phase 4: Revision (Improve)

**Fix systematically, not randomly.** Prioritize:

1. Accuracy problems (lies or misleading elements)
2. Clarity problems (confusion or friction)
3. Polish problems (aesthetics and consistency)

**One round is rarely enough.** Plan for 2-3 revision cycles. Each cycle:

- Addresses critique from previous round
- May introduce new problems worth catching
- Gets closer to final form

**Document decisions.** Why was a color palette chosen? Why were certain data points excluded? These decisions matter for future maintenance and for justifying choices under editorial review.

### Phase 5: Testing (Validate)

**Test with representative readers.** Not colleagues. Not other data visualization people. Actual members of the target audience.

Observe:

- Where do their eyes go first?
- What do they say the chart shows?
- Where do they hesitate or ask questions?
- What do they misunderstand?

**Revise based on observation.** If readers consistently miss the main point, the visualization isn't working, regardless of how well-designed it seems. Reader behavior trumps designer intention.

### Phase 6: Hardening (Finalize)

**Accessibility pass:**

- Colorblind simulation (Coblis, Color Oracle)
- Screen reader compatibility for interactive work
- Alt text for images
- Keyboard navigation for interactives

**Performance pass (for interactive work):**

- Mobile testing (touch, small screens)
- Load time optimization
- Graceful degradation for slow connections

**Editorial review:**

- Source verification
- Methodology documentation
- Headline and caption accuracy
- Legal and sensitivity review where relevant

## Workflow Patterns from Professional Teams

### The Pudding's Approach

The Pudding emphasizes data-driven storytelling with heavy user interactivity. Their documented process:

1. **Editorial question first.** What should the reader learn or feel? The question precedes data collection.

2. **Data cleaning and modeling.** Often extensive Python/Postgres work before any visualization.

3. **Scrollytelling as default.** Stories unfold as users scroll. This requires testing pacing—how much per scroll step? What's the rhythm?

4. **Prototype, test, iterate.** They test with real users and iterate based on observed behavior, not assumptions.

5. **Technical simplicity when possible.** Novel interactions serve the story; they're not added for novelty.

### NYT Graphics Patterns

The New York Times Graphics team operates under deadline pressure with high editorial standards:

1. **Sketch multiple options quickly.** Before committing to implementation, explore alternatives on paper.

2. **Small multiples over complex single charts.** Simpler charts, repeated, often communicate better than one dense chart.

3. **Direct annotation.** Labels point directly at what readers should notice. Don't make them hunt.

4. **Consistent visual language.** Within a story and across the publication, visual conventions remain stable.

### FiveThirtyEight's Statistical Rigor

FiveThirtyEight emphasizes uncertainty and probabilistic thinking:

1. **Show uncertainty explicitly.** Confidence intervals, fan charts, and probability distributions appear prominently.

2. **Distinguish historical from projected.** Visual encoding clearly separates known past from estimated future.

3. **Methodology accompanies visualization.** Readers can understand how numbers were calculated.

4. **Interactive exploration where useful.** Let readers test scenarios and understand model sensitivity.

## When to Stop Iterating

Refinement could continue indefinitely. Knowing when to stop matters.

**Stop when:**

- The takeaway is clear in 5 seconds
- Fresh readers describe the intended message
- All accuracy issues are resolved
- Accessibility requirements are met
- Deadline demands it

**Don't stop just because:**

- The creator is satisfied
- The chart matches the initial vision
- Polish looks good
- Colleagues approve

Reader understanding, not creator satisfaction, determines completion.

## Adapting to Context

Not every visualization warrants this full process.

**Internal exploratory work:** Rough sketches suffice. Skip formal critique. The goal is understanding, not communication.

**Time-critical decisions:** One or two quick iterations. Good-enough now beats perfect later.

**High-stakes public communication:** Full cycle, possibly multiple times. Errors in major publications damage credibility.

**Ongoing dashboards:** Invest heavily upfront; the work will be viewed repeatedly. Small improvements compound over time.

Match process intensity to stakes and audience.

## Sources

- Tufte, E. (1983). *The Visual Display of Quantitative Information*. Graphics Press.
- The Pudding — https://pudding.cool/
- Segel, E. and Heer, J. (2010). "Narrative Visualization." https://vis.stanford.edu/papers/narrative
