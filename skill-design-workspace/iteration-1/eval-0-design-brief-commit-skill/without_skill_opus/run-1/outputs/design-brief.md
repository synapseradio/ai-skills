# Design brief: a commit-message skill for `ai-skills`

## What we're actually solving

The request describes two symptoms — hand-writing conventional commits is tedious, and teammates using Claude get scopes wrong "half the time." Those are not the same problem, and only one of them is invisible today. Getting the design right depends on separating them.

I read the repo's commit tooling before designing anything. `commitlint.config.js` is a single line: it extends `@commitlint/config-conventional` with nothing added. That preset enforces the type vocabulary (`build`, `chore`, `ci`, `docs`, `feat`, `fix`, `perf`, `refactor`, `revert`, `style`, `test`), a lowercase type, a non-empty subject that isn't sentence/start/pascal/upper case, no trailing period on the subject, and 100-character limits on the header and on body and footer lines. It runs at three gates: the `commit-msg` hook, the `pre-push` hook, and again in CI-style form via `bunx commitlint --from origin/main --to HEAD` (all three are wired in `lefthook.yml`).

Here is the load-bearing fact: **`config-conventional` has no rule about scopes at all.** There is no `scope-enum`, no `scope-empty`, nothing. A commit can carry any scope, a wrong one, or none, and every one of those three gates passes it. (Verified by reading `node_modules/@commitlint/config-conventional/lib/index.js` — the `rules` block contains no `scope-*` key.)

That reframes the whole task:

- **Formatting mistakes** (capitalized subject, trailing period, wrong type, over-long header) already bounce at the `commit-msg` hook. They're annoying and cost a retry, but they're self-correcting — the commit literally will not land until they're fixed. A skill helps here by avoiding the bounce, but it isn't fixing anything the team can't already see.
- **Wrong scopes** are the opposite. Nothing catches them. They pass every gate, merge, and sit in the history permanently. This is why "half the scopes come out wrong" is a real, accumulating problem and not just a friction complaint: the tooling is structurally blind to exactly this failure.

So the skill's highest-value job is the one thing the linter cannot do — **pick the scope the team would have picked** — and its secondary job is to pre-format everything else so commits never bounce. A design that treats these as equal weight, or that leans on "just follow conventional commits," misses the point: conventional-commits compliance is already enforced; scope correctness is the gap.

## Where the "right" scope comes from

Scopes in this repo aren't arbitrary. Reading the last 300 commits and the directory tree, the convention is consistent even though it is written down nowhere:

- A change inside one skill uses that skill's name as the scope: `feat(what-if)`, `refactor(communicate)`, `feat(waypoint)`, `feat(surface-intent)`. The scope equals the directory name under `skills/`, which also equals the `name:` field in that skill's `SKILL.md`.
- Changes to non-skill top-level areas use the area's directory name: `docs(ideas)` (18 of the sampled commits), `chore(openspec)`, `feat(extensions)`, `docs(license)` (for `LICENSE`), and `chore(repo)` for root-level config.
- A change spanning two skills has been written both ways: `feat(runbook,shape-up)` (comma-joined) and `feat(skills)` (collapsed to the umbrella). The history is not self-consistent here.
- Grouped skills are ambiguous. `skills/thinkies/` holds ~37 leaf skills, each with its own `SKILL.md` name (`decompose`, `ideate`, …). The commit `feat(thinkies): rework decompose relations and joints` used the **group** name as the scope, not the leaf. But `CLAUDE.md` explicitly says the group name "does not appear in the skill's `name` frontmatter — it is purely organizational." So there is a genuine unresolved question about whether a change to `skills/thinkies/decompose/` should be scoped `decompose` or `thinkies`.

The reason teammates (and Claude) get this wrong is that the vocabulary is real but undocumented, and it changes every time a skill is added. You cannot memorize it and you cannot hardcode it — the correct answer is a function of the current tree and of which files are staged. That is the insight the design has to be built around.

## The design

A Claude Code skill that triggers when the user is about to commit, and that produces a ready-to-commit message by deriving the parts mechanically wherever they can be derived and reserving human judgment for the parts that genuinely need it.

**It operates on staged files, not the working tree.** The first action is `git diff --cached --name-only`. The scope of a commit is a property of what's being committed, so the skill reads what's staged and never re-stages or expands the selection on its own. (This also keeps it aligned with the repo rule that staged files are verified before committing.)

**It derives the scope vocabulary from the live tree, not a fixed list.** At commit time it enumerates `skills/*/` (flat skills) and `skills/*/*/` (grouped leaves) to build the set of valid skill scopes, and maps known top-level directories to area scopes. This is the property that makes it stay correct as skills are added and removed — a hardcoded scope list would rot on the next new skill. The full algorithm lives in the companion file `scope-derivation-spec.md`.

**It splits the work by what can be mechanized:**

- *Scope* — fully mechanical. Path prefixes map to scope tokens; the token set reduces to a final scope by deterministic rules. This is where the skill earns its keep, so this part should be deterministic and testable, not left to model judgment each time.
- *Type* — partly mechanical, genuinely semantic at the edges. New skill directory → `feat`; docs-only prose edit → `docs`; eval/fixture files → `test`; tooling and config → `chore`/`build`/`ci`. But `feat` vs `fix` vs `refactor` on an existing skill depends on intent, which the diff alone doesn't reveal. The skill proposes a type and lets the human confirm or override.
- *Subject* — the model's job: imperative mood, lowercase first word, no trailing period, short enough that `type(scope): subject` fits in 100 characters.

**It validates before presenting.** The skill checks its draft against a local mirror of the enforced rules, and — because the real linter is the source of truth — runs the draft through `bunx commitlint` (via `--edit` on a temp file, or the config's own API) as a dry check before showing the message. If the repo's config ever changes, the live linter catches it even if the skill's internal mirror lags.

### Should the mechanical part be a committed script?

I recommend yes: extract the scope/vocabulary derivation into a small committed script (`scripts/suggest-commit-scope` or similar) that reads staged files and prints the suggested `type(scope):` prefix. Three reasons. It makes the deterministic part actually deterministic and unit-testable instead of re-derived by model judgment every run. It lets non-Claude teammates — the other half of the stated problem — run the same logic by hand or from a `prepare-commit-msg` hook. And it gives the eval (below) something concrete to measure. The SKILL.md then wraps this script with the semantic layer (type confirmation, subject drafting) that a model does better than a shell script. This is a recommendation, not a settled decision — see open question 5.

## Alternatives I considered, and why the skill still wins

The request asks for a skill, and a skill is the right primary answer, but it is worth being honest that a skill only ever helps people who commit through Claude. The strongest alternatives attack the "wrong scope" problem for everyone:

**Dynamic `scope-enum` in `commitlint.config.js`.** The config is code, so it can build a `scope-enum` at lint time by reading `skills/` and the known area names. This would turn an invented or misspelled scope into a hard failure at every gate, for every committer, Claude or not. It is the most robust available fix for one specific failure mode — but only that mode. `scope-enum` can only reject scopes *outside* the vocabulary; it cannot tell that a change to `skills/A` was mislabeled with the valid scope of `skills/B`. Mis-attribution — arguably the more common "wrong scope" — sails straight through. So this is a strong complement, not a replacement. My recommendation is to propose it to the team alongside the skill: it makes out-of-vocabulary scopes impossible for everyone, and the skill remains the thing that gets attribution right. (Flagged as open question 6, because adding it means changing enforced tooling, which is the team's call.)

**A commitizen (`cz`) prompt with a custom scope list.** Interactive, works outside Claude, but adds friction to every commit and still needs the dynamic vocabulary to avoid rot. It doesn't infer scope from staged files — it asks. That's a step backward from a skill that already knows the answer from the diff.

**A `prepare-commit-msg` hook that prefills the prefix.** The script above, wired as a git hook, would prefill `type(scope):` into the editor for everyone. Deterministic and Claude-independent, but it can only prefill the mechanical prefix; it can't draft the subject, and its type inference is weaker without a model. Good as a fallback layer, not as the whole answer.

The shape I recommend: **the skill as the primary deliverable, its mechanical core as a committed script, and a proposal to the team to add a dynamic `scope-enum` as a hard gate.** The skill gets attribution right for Claude users; the script makes that logic reusable and testable; the enum (if the team accepts it) closes the out-of-vocabulary hole for everyone.

## How we'd know it works

"Right on the first try" is measurable, and the measurement should be built before the SKILL.md, so we're optimizing against a number rather than a vibe:

1. **Zero-bounce.** Every message the skill produces passes `bunx commitlint --edit` with no errors. This is mechanically checkable and should be a hard gate on the skill itself.
2. **Scope matches derivation.** The scope in the message equals what the deterministic algorithm produces for the same staged paths. Also mechanically checkable.
3. **Reproduces real history.** This is the real test. For the last N real commits, reconstruct the staged diff (`git show --name-only`), run the derivation, and compare the derived scope to the scope the human actually used. That yields a concrete accuracy percentage and, more usefully, a list of the specific commits where they disagree — each of which is either a bug in the algorithm or an inconsistency in the history (like the `runbook,shape-up` vs `skills` split). Both are worth surfacing. The disagreements are how we discover the convention's real edges instead of guessing them.

A caveat on criterion 3: the history is the ground truth we're trying to match, but the history is itself inconsistent (documented above). So we should expect and *want* some disagreements — the goal is not 100% match, it's understanding every mismatch. A skill that reproduced a self-contradictory history perfectly would be suspicious.

## Open questions for the user

These are the decisions I could not make from the repo alone. I've recorded them rather than guessing, because each one changes the algorithm's output and the wrong default would bake a wrong convention into every future commit.

1. **Grouped-skill scope.** For a change confined to `skills/thinkies/decompose/`, is the scope `decompose` (the leaf skill's own name) or `thinkies` (the organizational group)? History shows `thinkies` used for a cross-group change, but the single-leaf case is undocumented, and `CLAUDE.md` says the group name is purely organizational and absent from the skill's `name`.

2. **Multi-skill scope.** When a commit touches more than one skill, comma-join the scopes (`feat(runbook,shape-up)`) or collapse to the umbrella `feat(skills)`? Both exist in history. If comma-joining, is there a count past which it collapses to `skills`?

3. **Canonical area names.** Confirm the scope names for non-skill areas. Observed: `ideas`, `openspec`, `extensions`, `license` (for `LICENSE`), `repo` (for root config). Unconfirmed dirs that could also be touched: `agents/`, `bin/`, `plugins/`, `packaged/`. What scope should each carry?

4. **`packaged/` artifacts.** A change to `packaged/<name>.skill` — does it ride under the source skill's scope (since packaging is regenerated from the source), or get its own scope? The repo convention is to commit source + packaged + extension together, which suggests the skill's scope, but please confirm.

5. **Script or prose.** Should the mechanical scope/vocabulary derivation ship as a committed, testable script (my recommendation — reusable by non-Claude teammates), or live entirely as prose instructions inside the SKILL.md?

6. **Complementary hard gate.** Do you want the dynamic `commitlint` `scope-enum` proposed here, accepting that it only rejects out-of-vocabulary scopes (typos, invented names) and cannot catch mis-attribution to a valid-but-wrong scope? It changes enforced tooling for the whole team, so it's your call, not the skill's.

7. **The "commit all four" case.** `CLAUDE.md` says adding a skill means committing source, packaged artifact, README footer, and extension bundle in one change. That single commit spans `skills/<name>/`, `packaged/<name>.skill`, and `extensions/.../`. I assume the scope is the skill's name. Confirm.

8. **Body policy.** Most current history is subject-only. Should the skill propose a body (leading blank line, wrapped at 100 per the preset) for `feat`/`fix`, or stay subject-only unless the user asks?

9. **Staging boundary.** I've designed the skill to draft a message for already-staged changes and never stage files itself. Confirm that's the desired boundary, versus a skill that also decides what to stage.
