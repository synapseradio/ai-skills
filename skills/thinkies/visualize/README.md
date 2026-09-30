# visualize

Create data visualizations for the surface where they will actually be read. Three engines, weighed as equals with no default: **Vega** (declarative, concise, for standard static browser charts), **D3** (imperative, full control, for custom interactivity and sankey), and **Markdown** (tables, unicode bars, sparklines, mermaid diagrams that drop into pull requests, READMEs, tickets, and Slack posts). Every browser output is a standalone HTML file — no build step, no server. The workflow is principles-first: find the claim before touching data.

## Worth running when

- You have numbers and a hunch, and need a chart that says one thing a reader can check.
- The chart has to live where it's read: a pull request, a ticket, a chat message, or a page in the browser.
- You want the chart to show what cuts against your framing, not only what supports it.

## What a run looks like

It starts by finishing the sentence "This visualization shows that ___" and checking that sentence against the data. It stops twice for you: once to approve the plan, and once to see the chart before it's saved. In between it drafts, then verifies a second draft by reading its own source.

Trimmed from a staged conversation on a household of three's coffee across a week, Monday to Sunday: 9, 7, 8, 11, 6, 3, 4 cups, with Monday's "spike" blamed on a Sunday-night "just one episode" habit ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/visualize/household-coffee-week.md)). A second agent played one of the housemates:

> - You called Monday's count a spike, but Thursday's 11 is higher than Monday's 9. Monday is the second-highest day, not the peak.
> - Monday is the first row of the week, so the Sunday before it is not in the data. The Sunday shown (4) comes at the end of the week. Comparing Monday's 9 with Sunday's 4 assumes the Sunday before was also about 4.
>
> […]
>
> # Monday Runs High at 9 Cups, but Thursday Peaks at 11
>
> […]
>
> Mon  █████████     9 cups  ◀ Monday, after the Sunday-night episode habit (reported, not measured here)

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/visualize/` into `~/.claude/skills/visualize/`.

## Usage

Full visualization workflow:

```
/visualize create a bar chart showing quarterly revenue by region
```

Targeted entry — jump into a specific phase:

```
/visualize make this chart accessible
/visualize refine this visualization
/visualize what chart type should I use for this time series data?
```

Visualization management (requires Python 3):

```
"save this visualization"    → registers in ~/.visualizations/
"list my charts"             → shows all stored visualizations
"search for revenue"         → finds matching visualizations
```

Storage moved from `~/.visualizer-skill/visualizations/` to `~/.visualizations/`. The new layout is flat (no chart-type subdirectories) and accepts both `.html` and `.md` outputs. To migrate prior data manually:

```bash
mkdir -p ~/.visualizations
find ~/.visualizer-skill/visualizations -name '*.html' -exec mv {} ~/.visualizations/ \;
```

## Why use this instead of prompting?

A plain prompt will produce a chart, but it skips the work that makes a chart good — identifying what claim the visualization supports, choosing encodings that match the data's structure, adding units and context, checking accessibility. This skill enforces a six-phase workflow (context, research, implement, refine, present, save) so the output communicates clearly, not just renders correctly.

## Templates

| Category      | Charts                                                        | Vega          | D3   | Markdown                                |
| ------------- | ------------------------------------------------------------- | ------------- | ---- | --------------------------------------- |
| Comparisons   | bar, grouped-bar, stacked-bar, dot-plot, dumbbell             | Yes           | Yes  | unicode-bar-chart, comparison-table, ranked-list |
| Compositions  | pie, sunburst, treemap, waffle                                | Yes           | Yes  | comparison-table, ascii-tree, emoji-heatmap |
| Distributions | histogram, box-plot, violin-plot                              | Yes           | Yes  | unicode-bar-chart, comparison-table     |
| Geographic    | choropleth                                                    | Yes           | Yes  | —                                       |
| Hierarchical  | tree-diagram                                                  | Yes           | Yes  | ascii-tree                              |
| Networks      | force-graph, sankey                                           | force-graph only | Yes (sankey D3-only) | —                            |
| Process/flow  | flowchart, sequence, gantt                                    | —             | —    | mermaid-flowchart / mermaid-sequence / mermaid-gantt |
| Relationships | scatter-plot, heatmap, bubble-chart, parallel-coords, radar   | Yes           | Yes  | emoji-heatmap (heatmap)                 |
| Temporal      | line-chart, area-chart, candlestick, slope, sparkline         | Yes           | Yes  | sparkline-row, comparison-table         |

## Design system

- **Palette**: OpenColors (colorblind-safe combinations)
- **Spacing**: Generous margins (40px body, 32px container, adequate internal padding)
- **Units**: Mandatory on all axes, tooltips, and annotations
- **Accessibility**: WCAG AA contrast, redundant encoding, data table fallback, keyboard navigation (D3)

## Prerequisites

- **Required**: None
- **Optional**: Python 3.6+ (for visualization management CLI)

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`visualize.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/visualize.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
