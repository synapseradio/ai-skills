# visualize

Turn numbers, a comparison, a flow, or a structure into one chart or diagram that says one thing a reader can check. You get either a single HTML page that opens in a browser, or Markdown that renders in a pull request, README, ticket, or chat. Before handing either over, the skill validates the data and checks its own output.

## Worth running when

- You have numbers and a hunch, and need a chart that says one thing a reader can check.
- The chart has to live where it's read: a pull request, a ticket, a chat message, or a page in the browser.
- You want the chart to show what cuts against your framing as well as what supports it.

## What a run looks like

It starts by finishing the sentence "This shows that ___" from your data, and that sentence becomes the title. It asks you only where the data leaves a choice open: how duplicate rows combine, whether a gap means zero, where the result will be read. Then it prepares the rows, picks the chart, builds the output, and checks it before handing it over.

Trimmed from a staged conversation, run with an earlier version of the skill, on a household of three's coffee across a week, Monday to Sunday: 9, 7, 8, 11, 6, 3, 4 cups, with Monday's "spike" blamed on a Sunday-night "just one episode" habit ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/visualize/household-coffee-week.md)). A second agent played one of the housemates:

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

```text
/visualize show weekly signups by channel from signups.csv
/visualize which chart fits cups of coffee per person per day?
/visualize draw the checkout flow for the README
```

## What it produces

| Where it is read | Output |
| --- | --- |
| A browser | One HTML file holding a bar, line, area, or scatter chart |
| A pull request, README, ticket, wiki, or chat | Markdown: a Mermaid flowchart, sequence diagram, or schedule; a table; text bars; a ranked list; an indented tree |

### The HTML page, top to bottom

1. A title that states the claim, such as "Ben drank more coffee each day while Ana held steady".
2. A subtitle giving the scope and period.
3. The chart, with units on its axes, a legend for its series, and keyboard focus on its points.
4. A text summary carrying the numbers behind the claim, for a reader who never sees the chart.
5. The source of the data.
6. A table of every value, folded closed until opened.

The page is one file. It needs no install and no `package.json`, and opens straight from disk.

### What the page needs

The chart is drawn by [TanStack Charts](https://github.com/TanStack/charts), which the page fetches over https from the `esm.sh` module host when it opens, fixed at version 1.5.0. Drawing the chart therefore needs network access. Without it, the page shows its data table and says why the chart is missing.

TanStack Charts is the only library a page names. That library depends on D3 modules, which the same host serves alongside it, some at version ranges resolved when the page loads.

### Limits

- The build script draws four chart kinds: bar (plain, grouped, or stacked), line, area, and scatter. For another kind the agent writes the chart code by hand against the same page.
- A chart holds five series at most, the number of colours that passed the colour checks below.
- Colour encodes categories only. A continuous colour scale, as in a heatmap, is outside what the skill draws.
- Mermaid diagrams render on GitHub, GitLab, Notion, and Obsidian. Elsewhere the skill uses a table, a list, or a tree.

## How an output is prepared

1. **Data.** `scripts/prepare_data.py` converts each value to its type and sorts dates and numbers. It stops, and the agent asks you, on a missing value, a value that is not a number, or two rows for one position.
2. **Chart.** The agent picks the chart from the question the reader asks. The build refuses a chart the data does not fit, such as a line joining categories that have no order.
3. **Labels.** The build requires a title, axis labels, a unit, and a text summary, and writes the data table itself.
4. **Colour.** Each series colour has at least 3:1 contrast with the page background. Each pair stays distinct under simulations of the three main kinds of colour blindness (protanopia, deuteranopia, tritanopia).
5. **Check.** `scripts/check_output.py` reads the finished file and lists each defect: a missing summary or table, a second library or an unfixed version, colours a reader cannot tell apart, a text bar out of proportion to its value, a malformed Mermaid block.

## Prerequisites

- Python 3.9 or later, run through `uv` where it exists. The scripts use the standard library only.
- A browser with network access to draw the HTML chart.

## Sources

- TanStack Charts 1.5.0 documentation, the API the pages and `references/charts.md` use: <https://github.com/TanStack/charts/tree/v1.5.0/docs>
- npm registry entry for `@tanstack/charts`, the source of the pinned version: <https://registry.npmjs.org/@tanstack/charts>
- Machado, Oliveira, and Fernandes, "A Physiologically-based Model for Simulation of Color Vision Deficiency", the simulation matrices in `scripts/check_output.py`: <https://www.inf.ufrgs.br/~oliveira/pubs_files/CVD_Simulation/CVD_Simulation.html>
- WCAG 2.2, the contrast ratio formula and the 3:1 minimum for graphical objects: <https://www.w3.org/TR/WCAG22/#non-text-contrast>

The distance of 12 that the check requires between two series colours is this skill's own threshold, set below the closest pair in its palette (17.0) and above a red and green pair (`#d62728`, `#2ca02c`) that simulated colour blindness brings to 7.3.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`visualize.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/visualize.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
