# The Segel-Heer Narrative Visualization Spectrum

This reference expands on the author-driven to reader-driven spectrum introduced by Segel and Heer in their foundational 2010 paper "Narrative Visualization: Telling Stories with Data."

## The Core Framework

Segel and Heer observed that narrative visualizations vary along a spectrum defined by who controls the viewing experience:

**Author-driven** (one extreme): The author determines sequence, pacing, and attention. Viewers follow a prescribed path. Messaging is controlled; insights are delivered.

**Reader-driven** (other extreme): Viewers choose their own path. Authors provide tools and data; viewers discover their own insights. Exploration replaces narration.

Most effective visualizations fall somewhere between these extremes, combining authored guidance with viewer agency.

## Spectrum Dimensions

Three dimensions define position on the spectrum:

### 1. Ordering

**Author-controlled ordering**: Viewers encounter content in a fixed sequence. First this, then that. The order itself carries meaning—what comes before contextualizes what comes after.

Techniques:

- Linear scrolling (content appears as viewer scrolls down)
- Slideshow progression (explicit "next" actions)
- Animated sequences (time controls ordering)
- Guided tours (prescribed navigation path)

**Reader-controlled ordering**: Viewers choose what to examine first, second, third. Each viewer creates their own sequence based on interest, expertise, or task.

Techniques:

- Dashboard layouts (all visualizations simultaneously visible)
- Tab interfaces (viewer chooses which view to open)
- Linked views (clicking one view updates others)
- Search and filter (viewer defines subset of interest)

### 2. Interactivity

**Low interactivity**: Viewers observe but don't manipulate. They receive what the author prepared. Interaction is limited to navigation (scrolling, clicking through).

Techniques:

- Static charts
- Non-interactive animations
- Print graphics
- Video walkthroughs

**High interactivity**: Viewers manipulate the visualization. They filter, zoom, select, highlight, compare. The visualization responds to their questions.

Techniques:

- Brushing and linking (select in one view, highlight in another)
- Tooltips (hover reveals detail)
- Filter controls (checkboxes, sliders, dropdowns)
- Zoom and pan (explore at different scales)
- Detail on demand (click to expand)

### 3. Messaging

**Heavy messaging**: Text and annotations carry the narrative. The author's voice is present throughout. Insights are stated explicitly.

Techniques:

- Annotated callouts
- Narrative text blocks
- Insight-revealing titles
- Voice-over narration (in video/audio formats)

**Light messaging**: Minimal text. The visualization speaks for itself. Viewers draw their own conclusions.

Techniques:

- Descriptive-only titles
- Minimal axis labels
- No annotations
- Legend without interpretation

## Genre Positions

Segel and Heer identified seven genres of narrative visualization, each occupying a characteristic position on the spectrum:

### Author-Driven Genres

**Magazine style**: Static visualization with heavy annotation. Single image communicates complete story. No interactivity; all messaging explicit. Example: New York Times print graphics.

Position: Maximum author control, minimum viewer agency.

**Annotated chart**: Single visualization with targeted callouts. Author highlights specific insights while leaving broader exploration to viewer. Example: Economist data graphics.

Position: Author controls messaging; viewer controls attention duration.

**Partitioned poster**: Multiple linked visualizations on single canvas. Author determines layout and relationships; viewer chooses reading order. Example: Information graphics, infographics.

Position: Author controls structure; viewer controls sequence.

### Hybrid Genres

**Flow chart**: Sequential but branching. Author defines possible paths; viewer chooses among them. Example: Decision trees, branching narratives.

Position: Constrained choice—author limits options but doesn't force sequence.

**Slide show**: Author-controlled sequence with interaction at each stop. Viewer progresses at own pace but follows prescribed order. Example: Data-driven presentations.

Position: Author controls macro-sequence; viewer controls micro-pacing.

**Martini glass**: Author-driven introduction (the stem) opens into reader-driven exploration (the bowl). Structured onboarding leads to free exploration. Example: Many NYT interactive features.

Position: Shifts from author-driven to reader-driven within single piece.

### Reader-Driven Genres

**Drill-down story**: Entry point leads to depth. Initial view is overview; interactions reveal detail. Example: Many dashboard interfaces.

Position: Author provides structure; viewer controls depth.

**Interactive slideshow**: Multiple possible sequences. Viewer chooses which thread to follow. Example: Exploratory story interfaces.

Position: Author provides threads; viewer weaves path.

## Choosing Spectrum Position

Position on the spectrum should match purpose and audience:

### Choose Author-Driven When

- A specific insight must be communicated
- The audience lacks domain expertise to discover insights independently
- The story has a clear arc that benefits from pacing
- Time is limited (viewers won't explore)
- Persuasion is the goal

### Choose Reader-Driven When

- Multiple valid insights exist depending on viewer interest
- The audience has domain expertise
- Viewers have specific questions the author can't anticipate
- Exploration is more valuable than conclusion
- The visualization will be used repeatedly (reference tool)

### Choose Hybrid When

- Onboarding is needed before exploration
- Core insight should be delivered, but exploration adds value
- Different viewers need different depths
- Time varies (some will skim, some will dive)

## Implementation Considerations

### Martini Glass Pattern (common hybrid)

Structure:

1. **Opening**: Author-driven introduction establishes context
2. **Core insight**: Guided revelation of main finding
3. **Transition**: Explicit handoff ("Explore the data yourself")
4. **Exploration**: Interactive tools for reader-driven discovery

Design principles:

- Opening should be skippable for returning users
- Core insight should be memorable without exploration
- Transition should be visually clear (change in UI, invitation text)
- Exploration tools should be discoverable

### Scrollytelling Pattern (author-driven)

Structure:

1. **Hook**: Opening that creates curiosity
2. **Progressive reveals**: Each scroll position adds information
3. **Climax**: Main insight delivered with emphasis
4. **Denouement**: Resolution, implications, call to action

Design principles:

- Early sections should be short (build momentum)
- Scroll position should feel natural (avoid jarring jumps)
- Each reveal should add value (no filler)
- Provide skip option for impatient readers

### Dashboard Pattern (reader-driven)

Structure:

1. **Overview**: High-level view showing all dimensions
2. **Coordination**: Selecting in one view filters others
3. **Detail**: Drill-down for granular examination
4. **Comparison**: Side-by-side analysis tools

Design principles:

- Overview should be interpretable without interaction
- Coordination should be obvious (visual feedback)
- Detail should be reachable in 1-2 clicks
- Reset should be easy (escape hatches everywhere)

## Common Mistakes

**Mismatch between purpose and position**: Author-driven structure for exploratory purpose (viewers can't find their answers). Reader-driven structure for explanatory purpose (viewers miss the point).

**False reader-drivenness**: Interactive controls that don't change the story. Filters that reveal nothing new. Interactivity as decoration rather than insight tool.

**Incomplete martini glass**: Author-driven opening without the payoff of exploration. Or exploration tools with insufficient onboarding.

**Overwhelming interaction**: Too many controls. Every feature enabled at once. No progressive disclosure of complexity.

## Evaluation Questions

When assessing a narrative visualization's spectrum position:

1. **Whose insight is it?** Author's (author-driven) or viewer's (reader-driven)?

2. **What happens if the viewer only spends 10 seconds?** Author-driven should still communicate. Reader-driven should invite return.

3. **What happens if the viewer spends 10 minutes?** Author-driven should not exhaust. Reader-driven should reveal depth.

4. **Can the viewer get lost?** Author-driven provides rails. Reader-driven provides maps.

5. **Can the viewer disagree?** Author-driven asserts. Reader-driven invites interpretation.

## Source

Segel, E. and Heer, J. (2010). Narrative Visualization: Telling Stories with Data. *IEEE Transactions on Visualization and Computer Graphics*, 16(6), 1139-1148.

The framework has been extended by subsequent research on design patterns, evaluation methods, and applications in data journalism and scientific communication.
