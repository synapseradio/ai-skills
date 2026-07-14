# Design Brief: Commit Message Skill for `ai-skills`

This brief works out the design before any `SKILL.md` gets written. It is grounded in what the repo's own commitlint config and git history actually show, not in assumptions about conventional commits in general. The evidence is here so the design can be checked against it.

## The problem, restated against evidence

The stated symptom is that teammates using Claude Code get commit scopes wrong about half the time, even though commitlint is already configured. Reading `commitlint.config.js` explains why lint isn't catching it:

```js
module.exports = { extends: ['@commitlint/config-conventional'] }
```

`@commitlint/config-conventional` enforces `type-enum` (the standard `feat`/`fix`/`docs`/... list) and header shape rules, but it does not set a `scope-enum`. Scope is free text as far as commitlint is concerned. The `commit-msg` and pre-push hooks in `lefthook.yml` both run `commitlint`, but neither can catch a wrong scope — there is nothing to catch it against. A commit like `feat(waypiont): ...` or `feat(the-wrong-skill): ...` sails through every gate in the repo today.

So the actual problem isn't "Claude doesn't know conventional commits." It's that this repo has a real, consistent scope convention that lives only in git history and nowhere else — no `CONTRIBUTING.md`, no scope documentation, no `scope-enum`, nothing in `CLAUDE.md`. Anyone (human or Claude) has to reverse-engineer it from `git log`, and the mapping from "which files changed" to "the one correct scope token" has more structure than it looks like at first glance.

## The scope convention, as it actually exists

Scanning the last 300ish commit subjects and cross-referencing each against its changed files surfaces a taxonomy that varies by which top-level directory the change lands in — it is not simply "scope = top-level directory name":

| Area touched | Scope convention observed | Evidence |
|---|---|---|
| `skills/<name>/**` (single skill) | the skill's own directory name, e.g. `waypoint`, `what-if`, `visualize` | `feat(waypoint): ...`, `feat(what-if): ...` — dozens of examples |
| `packaged/<name>.skill` alongside its source | inherits the skill's own scope, not `packaged` | `feat(ask-questions): ...` touched both `skills/ask-questions/**` and `packaged/ask-questions.skill` in one commit |
| `extensions/<plugin>/**` alongside its source skill | inherits the skill's own scope, not `extensions` | `feat(extensions): add de-residency Claude Code plugin bundle` is the one counterexample — used when the extension itself, not a specific skill inside it, is the subject |
| Multiple skills, or the `skills/` directory as a concept (e.g. removing dead skills, syncing all packaged artifacts) | literal `skills` | `refactor(skills)`, `chore(skills)`, `feat(skills)`, `docs(skills)` |
| `ideas/<slug>/**` | literal `ideas` — never the slug | `docs(ideas): add waypoint idea` (note: this is a *different* `waypoint` than `skills/waypoint`) |
| `openspec/**` | literal `openspec` | `chore(openspec): archive visualize-improvements` |
| Two related skills in one commit | comma-joined scope | exactly one precedent: `feat(runbook,shape-up): ...` |
| Repo-wide files (`CLAUDE.md`, `README.md`, `lefthook.yml`, license, tooling) | no scope, or occasionally `repo`/`license` | `docs: ...`, `chore: gitignore local notes/ directory`, one `chore(repo)` |

Two things stand out. First, `ideas/waypoint/` and `skills/waypoint/` are both real paths in this repo, and they take opposite scope treatments — `ideas` for one, `waypoint` for the other. A path-name heuristic that just grabs "the directory after the top-level one" would get this exactly backwards for `ideas/`. Second, of 82 recent commits, 66 carry a scope and 16 don't; nearly all of the unscoped ones predate `lefthook.yml` (added mid-June), i.e., from before commitlint was even enforced. Once the hook existed, scoping got consistent — which is more evidence that the humans writing these by hand already internalized the convention; Claude doesn't have access to that internalized knowledge unless it's given the taxonomy explicitly.

### Gaps with no precedent yet

`agents/`, `bin/`, `plugins/`, `notes/`, `examples/`, and this very `skill-design-workspace/` directory have either zero commits or only unscoped/pre-hook commits touching them. There's no established answer for what scope a change to `agents/scout.md` or `bin/jj-push` should carry. This is a real gap in the convention, not something the design can paper over by guessing — it needs a team decision (see open questions below).

## Core design decision: externalize the taxonomy, don't ask the model to remember it

The most direct explanation for "half the scopes come out wrong" is that scope selection is currently an unaided inference task: it asks the model to hold a taxonomy that isn't written down anywhere and reconstruct it fresh, under time pressure, from partial pattern-matching on file paths. That's a task an LLM will get right most of the time and wrong close to half the time, which matches the reported symptom.

The fix that follows from that diagnosis: don't rely on the model's memory of the convention. Write the taxonomy down once, as a structured file the skill reads and a deterministic script applies, and reserve model judgment for the genuinely ambiguous cases the taxonomy doesn't cover. Concretely:

- A taxonomy file (JSON or YAML) mapping path patterns to scope rules — e.g., `skills/*/**` → basename of the immediate skill directory; `packaged/*.skill` and `extensions/*/skills/*/**` → resolve to the matching skill's own scope; `ideas/**` → literal `ideas`; `openspec/**` → literal `openspec`; and so on for each row in the table above.
- A small deterministic script (shell or Python, consistent with this repo's existing `bin/` scripts) that takes `git diff --cached --name-only`, applies the taxonomy, and emits either a single scope, a comma-joined set, "no scope," or "ambiguous — needs a decision," rather than leaving that judgment to the model on every commit.
- The skill's job becomes: run the script, use its output when unambiguous, fall back to asking (the user, or recording a note for the team) only when the script reports ambiguity or an unmapped path, and never silently invent a new scope convention for a path it hasn't seen before.
- Before presenting the drafted message, run it through `bunx commitlint --edit` (or pipe the header through commitlint the way the `commit-msg` hook does) so the skill validates what it drafted against the same gate the repo already enforces, rather than trusting its own judgment about the header shape.

This turns scope selection from "the model guesses from vibes" into "the model runs a lookup and only exercises judgment at the documented edges" — which is where the reliability actually needs to live, and which someone can audit and extend over time without needing an LLM to relearn the convention.

## Open design questions (recorded here in place of asking the user, who is unavailable)

These are genuine forks where the brief doesn't have enough information to decide unilaterally, and guessing would bake an arbitrary answer into the skill:

1. **Grouped skills with no precedent.** `skills/<group>/<name>/` skills exist (e.g., `skills/thinkies/consider-alternatives/`), but every commit touching `thinkies/` so far has used the group scope (`thinkies`) for changes that appear to touch multiple sub-skills at once. There is no commit yet that changes exactly one `thinkies` sub-skill in isolation. Should that get the group scope (`thinkies`) or the sub-skill's own frontmatter name (`thinkies-consider-alternatives`)? The two existing precedents don't disambiguate this.
2. **Uncharted top-level directories.** `agents/`, `bin/`, `plugins/`, `notes/`, `examples/`, and `skill-design-workspace/` have no post-hook scope precedent. Does each get its own literal scope (mirroring how `ideas` and `openspec` work), or do they fall under a generic default, or does the team want to explicitly declare some of them scope-less by convention?
3. **Cross-cutting commits.** There's exactly one precedent for comma-joined scopes (`runbook,shape-up`), from before commitlint was enforced. Is that the sanctioned pattern for a commit touching two unrelated skills, or should such changes be scopeless, or should the skill push back and suggest splitting the commit instead? This is probably the single highest-value question to resolve, since it's the case most likely to keep producing "wrong" scopes if left to guesswork.
4. **Draft-and-confirm vs. auto-commit.** Should the skill hand back a drafted `type(scope): subject` line for the user (or the calling agent) to review before running `git commit`, or is it expected to run the commit itself once it's confident? This changes the interface substantially and should be settled before writing `SKILL.md`.
5. **Failure mode when the taxonomy can't resolve a scope.** Should the skill block and ask a clarifying question, fall back to no scope, or refuse to commit at all until a human decides? Silently guessing is exactly the behavior being fixed, so this needs an explicit answer rather than an implicit default.
6. **Where the taxonomy file lives and who maintains it.** Should it live inside the new skill's own `references/` directory (self-contained, but drifts from reality unless someone remembers to update it when a new top-level directory appears), or should it live at the repo root as a convention document that both humans and the skill read from (visible, but is a new artifact this brief has no mandate to create without being asked)?
7. **Whether a `scope-enum` belongs in `commitlint.config.js` too.** Right now nothing blocks a wrong scope at the commit-msg or pre-push gate. Adding a `scope-enum` rule (even a loose one, or one generated from the taxonomy file) would make the convention enforced rather than merely advisory, and would catch mistakes from anyone — human or any Claude session, whether or not the skill happens to fire. That's a change to `commitlint.config.js` itself, outside a skill's reach, and is flagged here as a complementary fix worth deciding on rather than something this brief decided to add unasked.

## A trigger-reliability concern worth flagging before implementation

A `SKILL.md`'s `description` field triggers the skill semantically — Claude Code decides to invoke it based on matching the current request against that description. That works well when a user explicitly asks "write me a commit message." It's less certain when an agent is mid-task and reaches for `git commit -m "..."` as one step among several, which is the scenario the task description actually describes ("teammates use claude" and scopes come out wrong — implying Claude is already the one running the commit, not being asked to draft one in isolation). A skill that only fires on explicit request may not fire at the moment it's needed most.

Two supplementary mechanisms exist in this harness and are worth deciding between rather than defaulting to one silently: a `PreToolUse` hook on `Bash` matching `git commit` that routes the commit through the taxonomy logic regardless of whether the skill gets semantically triggered, or leaning on the existing `commit-msg` git hook (which already runs commitlint) to also run the scope-resolution script and rewrite or reject the message before it lands. Either supplements the skill; neither replaces the value of writing the taxonomy down. This is flagged as a decision point, not folded into the design, because it changes what gets built (a skill alone, versus a skill plus a hook) and that's the kind of scope call that belongs to the user.

## What this brief recommends, in one paragraph

Treat "the model doesn't know our scope convention" as the root cause, not "the model doesn't know conventional commits" — commitlint already handles the latter. Externalize the convention the git history already shows (the table above) into a taxonomy file plus a small deterministic script that a skill can call, rather than asking the model to reconstruct the mapping from memory on every commit; validate the drafted header against `bunx commitlint --edit` before presenting it, the same way the repo's own hook does; and resolve the seven open questions above — especially the cross-cutting-commit question and the draft-vs-auto-commit question — before writing `SKILL.md`, since each one changes the skill's interface rather than just its internals.
