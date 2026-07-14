# Appendix: scope-derivation evidence

Supporting evidence for `design-brief.md`'s scope-taxonomy row and generator.
Every case below was checked against the actual artifact (`git show
--stat <hash>` in the `ai-skills` repo, run during design research on
2026-07-14), not inferred from commit subjects alone. Commit hashes are
resolvable in the repo's own history.

## Why scope needs a generator at all

`commitlint.config.js` reads:

```js
module.exports = { extends: ['@commitlint/config-conventional'] }
```

`@commitlint/config-conventional`'s installed rule set (read from
`node_modules/@commitlint/config-conventional/lib/index.js`) defines
`type-enum`, `type-case`, `subject-case`, `subject-empty`,
`subject-full-stop`, and header/body/footer length limits — but **no
`scope-enum` rule**. Confirmed by running the lint against sample messages:

```
$ echo "feat(skill-design): add a new capability" | bunx commitlint
(exit 0)
$ echo "Feat(skill-design): Add A New Capability." | bunx commitlint
✖ subject must not be sentence-case... [subject-case]
✖ subject may not end with full stop [subject-full-stop]
✖ type must be lower-case [type-case]
✖ type must be one of [...] [type-enum]
(exit 1)
```

Any scope string at all passes commitlint. That means the user's complaint —
"half the scopes come out wrong" — describes messages that pass the lint gate
but still read as wrong to a human reviewer, because the actual convention
lives outside the tooling entirely, in precedent.

## The generator, stated as a fact

**Scope names the smallest directory the team already treats as one unit —
a skill, a grouped skill, an extension bundle, or a top-level area — that
contains every changed path. When a commit's structural role is different
from "edit an existing unit," the scope names that role instead:**

- **Adding a new member to a collection** (the first commit for a brand-new
  skill or extension) scopes to the *collection*, not the new member.
- **Touching a small number of existing units for one coherent reason**
  scopes to a comma-separated list of those units.
- **Touching many units for one structural, repo-wide reason**, or touching
  files with no shared unit at all, scopes to the collection name or omits
  scope entirely — both are attested below.
- **A concept anchored to a single root file or cross-cutting feature**
  (not a skill, not a directory) scopes to that concept's own name.

## Case-by-case evidence

**Case 1 — single-unit edit → unit's own name.**
`82a71c2` (`refactor(prompt): simplify skill...`) and the seven `feat(what-if)`
/ `fix(what-if)` / `test(what-if)` commits, plus single-word scopes like
`ask-questions`, `waypoint`, `ts-typeclasses`, `surface-intent`,
`decision-analysis`, `cli-development`, `bash-scaffold` — each of these
touches only files under `skills/<that-name>/`. This is the baseline case a
naive heuristic would get right.

**Case 2 — new skill addition → collection name, not the new skill's name.**
`1743ce7` (`feat(skills): add prompt skill for EIP-aligned prompt authoring`)
— diffstat shows only new files under `skills/prompt/`
(`SKILL.md`, `README.md`, `evals/evals.json`, five `references/*.md`) plus
`skills/packaged/prompt.skill`. Despite touching only the new `prompt`
skill's own files, the scope used is `skills`, not `prompt`. The very next
commits that *modify* that same skill — `1b42f29`
(`feat(prompt): emit only the prompt artifact...`) and `82a71c2`
(`refactor(prompt): simplify skill...`) — switch to `prompt` as scope. The
distinguishing fact is "this commit is the act of the skill collection
gaining a member," not which files changed.

`d67c4ca` (`feat(skills): add de-residency-advisor and package as .skill`)
confirms the same pattern independently: diffstat is
`README.md` (root) + seven new files under `skills/de-residency-advisor/`

- `skills/packaged/de-residency-advisor.skill` — again scoped `skills`, not
`de-residency-advisor`.

The same pattern holds one level up for extension bundles: `a6d0181`
(`feat(extensions): add de-residency Claude Code plugin bundle`) — "First
inhabitant of extensions/" per its own commit body — scopes to `extensions`
(the collection), not `de-residency` (the new bundle).

**Case 3 — a small number of units, one coherent reason → comma list.**
`f23c20e` (`feat(runbook,shape-up): strengthen alignment, encode testing
discipline, add plan mode`) — diffstat touches exactly
`skills/runbook/SKILL.md`, `skills/runbook/references/alignment-guide.md`,
and the equivalent `shape-up` files, for one stated reason ("port high-value
elements from shape-up into runbook's alignment phase"). Two units, named
individually and joined with a comma — not collapsed to `skills`.

**Case 4 — many units, one structural reason → collapse to collection.**
`6c4bc28` (`refactor(skills): move non-spec frontmatter fields under
metadata`) — diffstat touches `SKILL.md` in ten separate skills (`cite`,
`communicate`, `flix`, `ponder`, `rabbit-hole`, `scamper`, `sequencer`,
`team`, `tree-of-thought`, `visualize`). Same structural reason applies to
all ten (spec-compliance migration), and the scope collapses to `skills`
rather than listing ten names.

`5031c05` (`chore(skills): remove deleted skills, sync packaged artifacts`)
— diffstat is 116 files, entirely deletions, across four skill directories
(`sequencer`, `skill-review`, `stax`, `team`). Same pattern: one repo-wide
structural act, collection-level scope.

**Case 5 — diffuse, no shared unit → scope omitted entirely.**
`faed87a` (`docs: replace hard-coded numeric thresholds with qualitative
guidance`) carries no scope at all — the commit body describes changes
"across skill docs and reference files," with no single directory or small
set of directories capturing the intent better than the bare type. Of the
157 commits in history, 57 have no parenthesized scope; this is not
uncommon.

**Case 6 — a root-anchored concept, not a directory → the concept's own
name as scope.**
`fcd27ba` (`feat(marketplace): add ai-skills marketplace manifest`) — adds
`.claude-plugin/marketplace.json` at the repo root; there is no
`marketplace/` directory. The scope names the feature/concept
(`marketplace`), not a path segment.
`1fd8dcf` (`docs(license): use absolute repo URL for LICENSE links in all
READMEs`) — touches `LICENSE`-related links across many README files; no
`license/` directory exists either. Same pattern: `license` names the
concept the change is about.

**Case 7 — non-skill top-level areas follow the same rule.**
The 18 `docs(ideas)` commits scope to `ideas` because every changed path
sits under the root-level `ideas/` directory (per `CLAUDE.md`'s directory
listing at repo root, confirmed by `ls`), independent of the `skills/`
taxonomy. `chore(openspec)` similarly matches the root-level `openspec/`
directory. `docs(examples)` / `feat(examples)` commits (part of a longer
build-out under `examples/visualizer/` and `examples/housing-affordability/`)
confirm the sub-project name under `examples/` is used the same way a skill
name is used under `skills/` — e.g. `d40f3fb`
(`docs(visualizer): expand acronyms on first use across all charts`) touches
only `examples/visualizer/charts/*.html`, and `visualizer` is that
sub-project's actual directory name (distinct from, and not to be confused
with, the unrelated `skills/visualize` skill — checked directly by diffstat
to rule out a typo/inconsistency reading).

## What this does not resolve

The boundary between Case 3 (name a few units) and Case 4 (collapse to the
collection) is bounded only loosely by the sample: 2 units stayed named,
10 units collapsed. No commit in the 157-commit history sits at 3, 4, or 5
touched units under one structural reason, so the exact cutover is
unverified — carried into the design brief's Open Questions rather than
guessed at here.

## Commits predating the convention

The earliest three commits in history (`Add skill-review...`,
`Add sequencer skill...`, `Add lefthook pre-commit hook... (#3)`) use no
type prefix at all and a `(#N)` suffix that is a PR-reference annotation,
not a scope — these predate `commitlint.config.js`'s introduction and are
excluded as counter-evidence.
