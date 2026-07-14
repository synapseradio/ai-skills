# Scope Vocabulary and Derivation Rule

Companion to `design-brief.md`. This file records the source of truth for
scope in `ai-skills`: what the convention actually is, mined from the repo,
and the derivation rule a skill (or its script) applies. The scope convention
is written down **nowhere in the repo** — it exists only in the directory
layout and the commit history. This file makes it legible; the skill routes
over it rather than copying it.

## What commitlint enforces about scope

Nothing. `commitlint.config.js` extends only `@commitlint/config-conventional`,
whose `rules` block (read from
`node_modules/@commitlint/config-conventional/lib/index.js`) contains
`type-enum`, `type-case`, `type-empty`, `subject-case`, `subject-empty`,
`subject-full-stop`, `header-max-length` (100), `header-trim`, and the
`body`/`footer` blank-and-length rules — and **no `scope-enum`, `scope-case`,
or `scope-empty` rule.** Any scope, or none, passes the gate. Scope
correctness is therefore a convention, not a constraint.

## Type enum (the enforced part, for reference)

From `config-conventional`, `type-enum` (error): `build`, `chore`, `ci`,
`docs`, `feat`, `fix`, `perf`, `refactor`, `revert`, `style`, `test`. Type is
also lowercase (`type-case`) and required (`type-empty`). The skill points
here; it does not re-own this list.

## Mined scope frequency (last 400 commits)

From `git log -n 400 --pretty=format:'%s'`, scopes by frequency:

| Scope | Count | Area it maps to |
|---|---|---|
| `ideas` | 18 | `ideas/` directory |
| `what-if` | 15 | `skills/what-if/` |
| `skills` | 8 | multiple/general skills work |
| `communicate` | 3 | `skills/communicate/` |
| `waypoint` | 2 | `skills/waypoint/` |
| `visualize` | 2 | `skills/visualize/` |
| `thinkies` | 2 | `skills/thinkies/` (a group) |
| `prompt` | 2 | `skills/prompt/` |
| `openspec` | 2 | `openspec/` |
| `ask-questions` | 2 | `skills/ask-questions/` |
| `ts-typeclasses`, `surface-intent`, `ponder`, `decision-analysis`, `create-skill`, `cli-development`, `bash-scaffold`, `runbook` | 1 each | `skills/<name>/` |
| `extensions` | 1 | `extensions/` |
| `license` | 1 | `LICENSE` |
| `repo` | 1 | root-level repo config |

Type frequency over the same window: `docs` 29, `feat` 27, `refactor` 9,
`test` 7, `chore` 6, `fix` 3, `style` 1, `build` 1 (plus one invalid `update`).

The dominant pattern is unmistakable: **the scope is the name of the skill or
top-level area the change touches**, and that name is a directory in the repo.

## The derivation rule

Given the staged file paths, derive the scope:

1. Map each staged path to an **area**:
   - `skills/<name>/...` → area `<name>`.
   - `skills/<group>/<name>/...` (one level of grouping, e.g.
     `skills/thinkies/argue-opposite/`) → area `<name>` for a change to that
     specific skill; area `<group>` (e.g. `thinkies`) for a change spanning
     several skills in the group. CLAUDE.md documents that the group name is
     organizational and does not appear in the skill's own `name` frontmatter,
     so both `thinkies` and the leaf skill name occur legitimately as scopes;
     the choice is "which level did the change actually touch."
   - `ideas/...` → `ideas`.
   - `extensions/...` → `extensions`.
   - `packaged/...` → the scope of the skill it mirrors (packaged is a build
     artifact of a source skill) — in practice packaged changes ride along
     with the source-skill commit and take that skill's scope.
   - `agents/...` → `agents`. `examples/...` → `examples`.
   - Root-level config/tooling (`lefthook.yml`, `biome.jsonc`, `package.json`,
     `commitlint.config.js`, `README.md`, `CLAUDE.md`, etc.) → `repo`
     (pending Open question 2, which may prefer no scope here).
2. Collapse to the set of distinct areas touched.
3. If exactly one area → that is the scope.
4. If more than one area → the multi-area case, resolved by the house rule the
   team still owes an answer on (Open question 1 in the brief): omit scope,
   pick the dominant area, or comma-list. Until decided, the script should
   return `ambiguous` with the candidate list rather than guess.
5. If only root-level tooling → `repo` (or `no-scope`, per Open question 2).

The set of valid single-area scopes is **whatever the filesystem holds at
commit time**, not a frozen list. Globbing `skills/*` (and the one grouping
level) yields the current skill scopes; the top-level directories yield the
rest. This is why the brief insists the vocabulary be computed live: the repo
adds a skill, and thus a scope, every few commits.

## Type-per-area micro-conventions (observed, not enforced)

The history shows consistent type+scope+subject shapes worth encoding as
guidance (the team decides in Open question 5 whether to enforce the subject
wording):

- New idea document: `docs(ideas): add <name> idea` (18 instances follow this
  exact shape).
- Eval/fixture additions for a skill: `test(<skill>): add <description>`
  (e.g. `test(what-if): add iteration-5 eval runs`).
- New skill capability or a new skill: `feat(<skill>): ...` or
  `feat(skills): ...` for cross-cutting.
- Skill edits that neither add nor fix behavior: `refactor(<skill>): ...`.

## Known anomalies — patterns to NOT imitate

These appear in history and violate the convention; the skill should treat
them as counter-examples, and the eval's negative expectations can use them:

- `feat(runbook,shape-up)` — comma-joined multi-scope. Permitted by
  config-conventional, but it is the unresolved multi-area case (Open
  question 1), not a settled pattern.
- Scopes containing spaces, e.g. `(as-is port from seed)` — not a valid scope;
  a subject fragment leaked into the scope slot.
- PR numbers as scope, e.g. `(#1)`, `(#2)`, `(#3)` — a scope should be an
  area, not an identifier.
- Non-enum type `update` (`update communicate`, `Update ... README.md`) — not
  in the type enum; would fail `type-enum` if it reached the hook, and the
  capitalized `Update` also violates `type-case`. These predate or bypassed
  the gate.

## For the build

The future skill's scope script implements steps 1–5 above against the live
filesystem and the staged path list. Its contract (what it returns for the
multi-area case) is blocked on Open question 1. Everything else here is
directly implementable and verifiable: each mapping can be checked by running
the script on a fixture path set and comparing to the expected scope.
