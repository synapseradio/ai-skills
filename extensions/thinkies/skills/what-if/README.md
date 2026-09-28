# what-if

Play out possible futures from a sparse question. Finds the unknowns that would change a decision, tiles one coherent future per combination, traces consequences and watchpoints between them, and walks its reasoning out loud before ending on a reasoned recommendation plus the conditions that would flip it.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/what-if/` into `~/.claude/skills/what-if/`.

## Usage

```
/what-if <a decision, hypothetical, or idea whose future is uncertain>
```

## Sources

- Yao et al., "Tree of Thoughts" (arXiv:2305.10601) — propose candidates together to avoid duplication; triage states as sure/likely/impossible via lookahead; breadth limits; backtracking.
- Besta et al., "Graph of Thoughts" (arXiv:2308.09687) — aggregation merges convergent reasoning paths into one node; refinement loops a thought once through improvement.
- Weimer-Jehle's cross-impact balance analysis (properties in arXiv:0912.5352) — promote/restrict judgments between outcomes; a scenario stays consistent only when each of its outcomes holds against the combined impacts of the others.
- Peter Schwartz, "The Art of the Long View" — scenario planning, predetermined elements, critical uncertainties.
- Fritz Zwicky — morphological analysis and cross-consistency assessment.
- Jerome Glenn, early 1970s — the futures wheel.
- Winston, Chaffin & Herrmann (1987), "A Taxonomy of Part-Whole Relations," Cognitive Science 11(4), 417-444 — the relation types behind Q1, Q2, and the link-typing discipline.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`what-if.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/what-if.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
