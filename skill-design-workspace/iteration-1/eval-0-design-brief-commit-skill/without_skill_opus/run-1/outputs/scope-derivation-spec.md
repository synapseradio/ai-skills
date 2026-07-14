# Scope-derivation spec

The technical core of the skill. This is the part that must be deterministic, because it fixes the failure the linter can't see. It's written here as an algorithm so it can become a script and an eval, independent of how the SKILL.md eventually wraps it.

Everything below is grounded in the repo as it stands: the `skills/` tree layout described in `CLAUDE.md`, the scope patterns in the last 300 commits, and the `@commitlint/config-conventional` rule set read from `node_modules`. Where the repo doesn't settle a decision, the step says so and points to the matching open question in `design-brief.md`.

## Input

The staged file list, and only that:

```
git diff --cached --name-only
```

If nothing is staged, the skill stops and says so rather than guessing from the working tree. Scope is a property of the commit, and the commit is what's staged.

## Step 1 — Build the scope vocabulary from the live tree

Do not hardcode scope names. Compute them each run so the vocabulary tracks the tree.

**Skill scopes** come from the tree under `skills/`:

- Flat skills: each directory `skills/<name>/` that contains a `SKILL.md` contributes the scope `<name>`.
- Grouped skills: each directory `skills/<group>/<leaf>/` that contains a `SKILL.md` contributes a leaf scope `<leaf>` and belongs to group `<group>`.

The directory name equals the `name:` field in that skill's `SKILL.md` (verified on `what-if`, `communicate`, and others), so the directory name is a safe scope token without parsing YAML. Parsing `name:` is a belt-and-suspenders option if you want to detect a drifted directory.

**Area scopes** come from a small map of non-skill top-level directories to scope names. Observed in history: `ideas/ → ideas`, `openspec/ → openspec`, `extensions/ → extensions`, `LICENSE → license`. Root-level config files (`commitlint.config.js`, `lefthook.yml`, `package.json`, `biome.jsonc`, dotfiles) map to `repo`. The remaining top-level dirs — `agents/`, `bin/`, `plugins/`, `packaged/` — are unconfirmed; see design-brief open question 3. Until confirmed, treat them as `repo` and flag for the user rather than inventing a scope.

## Step 2 — Map each staged path to a scope token

For each staged path, match longest-prefix-first against the vocabulary:

1. `skills/<group>/<leaf>/...` → the grouped-skill token (see Step 4 for group-vs-leaf).
2. `skills/<name>/...` → skill token `<name>`.
3. `packaged/<name>.skill` or `packaged/<group>/<name>.skill` → the same token as the corresponding source skill (packaging mirrors source). Open question 4.
4. `extensions/<plugin>/...` → for a single-skill plugin bundle, the wrapped skill's token; otherwise `extensions`. Open question 3/7.
5. A recognized area directory → its area token.
6. Anything unmatched → `repo`, and flag the path so the user sees what fell through.

The result is a multiset of scope tokens, one per staged path.

## Step 3 — Reduce the token set to one scope

Collapse the distinct tokens:

- **Exactly one distinct token** → that token is the scope. This is the overwhelmingly common case and it is unambiguous.
- **Several tokens, all skills** → comma-join in the order the files appear, or collapse to `skills` past a threshold. History contains both `feat(runbook,shape-up)` and `feat(skills)`, so this rule is genuinely unsettled — design-brief open question 2. The algorithm should expose the threshold as a single named constant so the decision is one edit, not a rewrite.
- **Several tokens, all under one group** → the group token, or the comma-joined leaves — tied to the same group-vs-leaf decision as Step 4, open question 1.
- **Mixed skills and areas, or several areas** → collapse to the broadest single token that covers them: `skills` if it's skills plus their own packaged/extension artifacts, otherwise `repo`. Flag mixed commits to the user, since a commit that spans a skill and unrelated root config is often two commits wearing one hat.

## Step 4 — The grouped-skill decision (blocked)

This step cannot be finalized without the user. A change confined to `skills/thinkies/decompose/` is either scope `decompose` (the leaf's own `name`) or scope `thinkies` (the organizational group). History used the group name for a cross-group edit; the single-leaf case is undocumented, and `CLAUDE.md` calls the group purely organizational. See design-brief open question 1.

Until it's answered, the algorithm should implement the leaf-name reading (it's the more specific, more information-preserving choice and matches the flat-skill rule that scope = the skill's own name) **and** surface the alternative to the user on grouped-skill commits, rather than silently committing to one. This is the one place the skill should show its work instead of just emitting an answer.

## Step 5 — Infer the type

Type is not fully mechanical, so the skill proposes and the human confirms. Heuristics, in priority order, grounded in the observed history:

- A staged path that is a newly added `SKILL.md` (a skill that didn't exist before) → `feat`. (`feat(surface-intent)`, `feat(waypoint)`.)
- Only `*.md` prose content changed, no behavior → `docs`. (`docs(ideas)`, `docs(license)`.)
- Only eval/fixture/test files under a skill changed → `test`. (`test(what-if): add iteration-5 eval runs`.)
- Only tooling/config changed (`lefthook.yml`, `commitlint.config.js`, linter configs, `openspec/` housekeeping) → `chore`, or `build`/`ci` when it's specifically dependency or pipeline machinery. (`chore(openspec)`, `chore(repo)`.)
- Behavior change to an existing skill → `feat` (adds capability), `fix` (corrects wrong behavior), or `refactor` (restructures without behavior change). The diff can't reliably distinguish these three; this is where the human's intent is required. Propose the most likely from the diff shape and let them override.

The type must be lowercase and one of the eleven `config-conventional` types. That set is fixed by the preset, so the skill can validate the type against it mechanically even though choosing it is semantic.

## Step 6 — Draft the subject

Model's job, constrained by what the linter enforces:

- Imperative mood, describing the change ("add", "rework", "replace", matching the verbs in history).
- First word lowercase — `config-conventional` forbids sentence/start/pascal/upper subject case, so a lowercase imperative is the safe form.
- No trailing period.
- Length such that the full header `type(scope): subject` is ≤ 100 characters. Compute the budget as `100 − len("type(scope): ")` and hold the subject under it.

## Step 7 — Validate before presenting

Two layers, cheap first:

1. **Internal mirror.** Check the draft against the enforced rules directly: type in the enum, type lowercase, subject non-empty and not in a forbidden case, no trailing period, header ≤ 100, and — if a body is present — a leading blank line and each line ≤ 100. Catches the common mistakes without spawning a process.
2. **The real linter.** Write the drafted message to a temp file and run `bunx commitlint --edit <file>` (or call the config's API). The repo's config is the source of truth; if it changes, this catches what the mirror doesn't yet know about. Only present the message once this passes clean.

If either layer fails, the skill fixes the draft and re-validates rather than handing the user something that will bounce at the `commit-msg` hook.

## What this makes testable

Because the derivation is a pure function from staged paths to a scope, it can be checked against real history without a model in the loop:

```
for each of the last N commits C:
    paths   = files C touched          # git show --name-only C
    derived = derive_scope(paths)      # steps 1–3
    actual  = scope parsed from C's subject
    record (C, derived, actual, match?)
```

The output is an accuracy number and, more valuably, the exact set of commits where derivation and history disagree. Each disagreement is either an algorithm bug or a genuine inconsistency in the history (the `runbook,shape-up` vs `skills` split will show up here). That list is the concrete artifact to take back to the user — it turns the fuzzy "half the scopes are wrong" into a specific, reviewable set of cases, and it's how the open questions above get answered with evidence instead of opinion.
