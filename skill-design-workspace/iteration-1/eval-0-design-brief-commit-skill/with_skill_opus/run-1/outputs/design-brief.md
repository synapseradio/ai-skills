# Design Brief: A Conventional-Commit Skill for `ai-skills`

This brief designs a skill, not a SKILL.md. It is the input a build step
(skill-creator or hand-authoring) works from. It follows the design-mode
structure in the `skill-design` skill: Intent, Floor, Sources of truth,
Structure sketch, Fixed decisions, Checks, Open questions.

## The finding that shapes everything

The team's stated pain is "scopes come out wrong." The repo's commit gate
cannot be the thing catching or preventing that. `commitlint.config.js`
extends `@commitlint/config-conventional` and nothing else, and that config
constrains the **type** (an eleven-value enum: `build`, `chore`, `ci`,
`docs`, `feat`, `fix`, `perf`, `refactor`, `revert`, `style`, `test`) plus
header length, subject case, and a few structural rules — but it places **no
constraint on scope whatsoever** (read from
`node_modules/@commitlint/config-conventional/lib/index.js`).

So a wrong scope is never a lint error. It is a semantic mismatch against a
convention that lives only in the repo's directory layout and its commit
history — a source Claude has no reason to consult unless a skill routes it
there. That reframes the whole task. The skill's central job is not "obey
commitlint" (the hook already enforces what commitlint covers); it is
**making scope decidable from a source that actually encodes the answer.**
Everything below follows from that.

## Intent

**Task region.** Authoring the commit message for a staged change in this
repository so it passes the `commit-msg` commitlint hook on the first attempt
and carries the scope the repo's convention expects. The skill covers: choosing
the type, deriving the scope, and phrasing the subject and body to the rules
`config-conventional` enforces. It runs at the moment of committing, after the
change is written and staged.

**Trigger phrasings.** "commit this," "write a commit message," "commit these
changes," "what's the commit message for this," "commit," used while inside
this repository with staged or unstaged changes present.

**Near misses that must not trigger.**

- "How should I split this work into commits?" / "what belongs in this
  commit?" — that is decomposition, owned by the `software:git` skill (its
  Commit Strategy and Selective Stage references). This skill assumes the
  decomposition is already decided and phrases the message for one commit.
- "Rebase this" / "clean up my branch history" / "resolve this conflict" —
  history surgery, also `software:git`. Rewording old commits sits at the
  edge; treat a bulk history reword as out of scope unless the user names it.

The boundary to state in the description: this skill writes the message for a
commit whose contents are already chosen; it does not decide what goes into a
commit or restructure history.

## Floor

**Declared floor: the weakest model any teammate runs in Claude Code**, which
in practice means plan for Haiku-class execution, not Opus. The task ships to
"the whole team," and the team member composition and model choice are not
controllable from the skill. The `skill-design` principles cite measured
evidence that a weak executor loses far more compliance to instruction
phrasing than a strong one (IFEval++ reports small models shedding up to 61.8%
of compliance under paraphrase where the strongest loses 18.3%
— `skills/skill-design/references/principles.md`, "Declare the floor").

This choice has one dominant consequence, developed under Structure sketch and
Checks: **scope derivation is a filesystem lookup, and a weak floor will not
perform a filesystem lookup reliably from prose plus a lookup table.** That
pushes the scope operation toward a script rather than instructions. Naming
the floor as Haiku is what forces that call; naming it as Opus would let the
design get away with prose and then fail in exactly the sessions the team
complained about.

## Sources of truth

Each fact the skill needs already has a home. The skill routes over these
homes and copies none of them, per the "route, don't hold" principle.

**Type vocabulary and subject rules → `commitlint.config.js` /
`config-conventional`.** The eleven-value type enum, the 100-character header
limit, lowercase type, no-trailing-period subject, and the forbidden subject
cases are all enforced there and re-checked by the `commit-msg` hook
(`lefthook.yml`). The skill must not restate the type list as its own
authority; it points at the config and treats the hook as the check. If the
repo ever adds a custom rule, the config changes and the skill inherits it for
free.

**Scope vocabulary → the repository directory layout, computed live.** The
de-facto scope for a change is the area it touches, and the areas are the
repo's own directories. A change under `skills/<name>/` takes scope `<name>`;
a change under `ideas/` takes `ideas`; under `extensions/` takes `extensions`;
root-level tooling takes `repo`. This is not written down anywhere in the repo
today — it exists only as a pattern in the commit history. The mined evidence,
the exact derivation rule, and the anomalies that violate it are recorded in
the companion file `scope-vocabulary.md`. The critical design decision:
**derive the scope set from the filesystem at commit time (glob `skills/*`,
read the touched paths), never freeze it as a static enum** — because the repo
adds a new skill, and therefore a new valid scope, roughly every few commits.

**Commit-format conventions → the user's global `commit-format.md` rule.** That
rule already states the Conventional Commits shape, "the repository wins," and
the content bans (no co-author trailers, etc.). This skill is the
repo-specific operationalization of that rule, not a competitor to it. It
should cite the rule for the general shape and add only what is
`ai-skills`-specific: the scope-derivation mechanism and the repo's
type-per-area micro-conventions.

## Structure sketch

Justified by principle 1 (schedule the workspace): description at startup, body
on activation, references and scripts on demand.

**Description (~100 tokens, always loaded).** Carries triggering and the one
boundary that prevents mis-fire: writes the commit message for an
already-staged, already-decomposed change in this repo; defers commit
splitting and history rewriting to `software:git`. Names the concrete triggers
("commit this," "write a commit message").

**Body (loaded on activation).** The orchestration, kept short:

1. Read the staged files (`git diff --cached --name-only`).
2. Derive the scope by running the scope script (below), which returns one of:
   a single scope, `no-scope` (multi-area or repo-root only), or a short
   ranked candidate list for the executor to choose from with a stated
   tie-break rule.
3. Choose the type from what the diff does, pointing at the
   `config-conventional` type meanings rather than re-listing them.
4. Phrase subject and body to the enforced rules; cite `commit-format.md` for
   the general shape.
5. Note that the `commit-msg` hook is the check — if it rejects, the rejection
   is the next task (never `--no-verify`).

**Reference: `scope-vocabulary.md` (loaded on demand).** The area→scope map,
the derivation rule in full, the type-per-area micro-conventions the history
shows (`docs(ideas): add <x> idea`, `test(<skill>): add ...`,
`feat(<skill>)`), and the known anomalies to *not* imitate.

**Script: the scope deriver (the load-bearing artifact).** Principle 7 — where
an operation must not vary, ship a script. Scope derivation is a deterministic
function of the staged paths and the live directory layout, so it is exactly
the operation to remove from probabilistic prose. Given the staged file list,
it emits the derived scope (or `no-scope`, or an ambiguous-candidate list) by
mapping each path to its area and applying the tie-break. This is what makes
"right on the first try" reachable at the Haiku floor: a weak model that would
fumble a filesystem-plus-table lookup instead runs code and reads a single
answer. Recommended, not merely optional — the floor choice is the argument
for it.

## Fixed decisions

**Frozen (hard-coded for every session):**

- The commit format is Conventional Commits; the source of the type enum and
  subject rules is `config-conventional`, consulted, never copied.
- Scope is derived from the area the change touches, by the path→area rule in
  `scope-vocabulary.md`.
- Commit decomposition and history rewriting are out of scope and defer to
  `software:git`.
- The `commit-msg` hook is the acceptance check; its rejection is a failure to
  fix, never bypassed.

**Left open (decided per session):**

- The type, when a diff genuinely spans kinds (a `feat` that also touches
  docs) — the executor judges from the dominant change.
- The subject wording and whether a body is warranted.
- The scope when a commit spans multiple areas — resolved by the house rule
  the team still needs to set (see Open questions).

**The frozen decision most likely to need revisiting, and its sign.** The
scope vocabulary. It is the whole point of the skill and it is the thing that
changes most often, because every new skill directory mints a new valid scope.
The design already mitigates this by computing the scope set from the
filesystem rather than freezing an enum — so the revisit sign is not "a new
skill appeared" (that is handled) but rather **the path→area derivation rule
itself stops matching how the repo is organized**: a new top-level directory
that is not `skills/`, `ideas/`, `extensions/`, `packaged/`, `agents/`, or
`examples/`, or a second level of skill grouping that the rule does not
account for. When a maintainer sees commits landing with `repo` scope that
should have had a real area, the derivation rule is the thing to reopen.

## Checks

Per principle 10 — build the evals before the skill and baseline the task
without it.

**Evals: staged-diff fixtures → expected commit header.** Each fixture is a
set of staged paths plus the intended change kind; the assertion pair is
(a) the produced message passes `commitlint --edit`, and (b) the produced
scope equals the scope the derivation rule yields for those paths. Cover:
a single-skill change (`skills/what-if/...` → `what-if`), an ideas doc
(`ideas/foo.md` → `docs(ideas)`), a root-tooling change (`lefthook.yml` →
`repo` or `no-scope` per the house rule), a multi-area change (the ambiguous
case), and a new-skill-directory change whose scope is not yet in any frozen
list (proves the live-derivation requirement). Baseline every fixture with no
skill first, to measure the lift and to confirm the "wrong scope" failure
actually reproduces.

**Trigger queries, both polarities.** Positive: "commit this," "write the
commit message," "commit these changes." Negative: "split this into commits,"
"how should I structure these commits," "rebase onto main," "reword my last
five commits." The negative set guards the `software:git` boundary; a
description that fires on the negatives is over-broad.

**The operation that needs a script, not prose:** scope derivation, for the
reasons under Structure sketch and Floor. Flag for the build: if the build
chooses prose-plus-table over the script, the multi-model eval must
demonstrate the Haiku-floor fixture still passing, or the floor claim is
unmet.

## Open questions

Recorded here because the person who requested this is unavailable. Each is a
decision the skill's correctness depends on and that the design cannot settle
alone.

1. **Multi-area commits: omit the scope, or comma-list it?** The history holds
   one `feat(runbook,shape-up)` (a comma-joined scope, which
   `config-conventional` permits) against many single-scope commits. The team
   needs one house rule: for a commit touching two skills, is the scope
   omitted, set to the dominant area, or comma-listed? The eval's ambiguous
   fixture and the script's `no-scope` behavior both depend on this answer.

2. **Root-level tooling scope: `repo` or no scope?** History shows both a bare
   `chore:` / `docs:` and a `chore(repo)`. Pick one so root changes are
   consistent.

3. **Does the skill produce only the message text, or also run the commit?**
   The repo uses jj alongside git (`jj-config.toml`, a `bin/jj-push` wrapper,
   and `commit-msg` firing only through git). If the skill should drive the
   commit, it must know whether the team commits via `git`, `jj`, or the
   wrapper — and the acceptance check differs (`jj git push` does not fire git
   hooks, which is why the wrapper exists). Recommendation absent an answer:
   produce the message text and let the human or an outer flow commit, keeping
   the skill's surface small and the hook as the real gate.

4. **Distribution shape.** "Drop into Claude Code, whole team" reads as a
   plugin extension under `extensions/`, not a loose `skills/<name>/` source
   or a personal rule — but the choice affects how the skill is installed and
   versioned across the team. Confirm the team wants a plugin bundle.

5. **How prescriptive on subject wording?** History shows tight
   micro-conventions (`docs(ideas): add <x> idea`, `test(<skill>): add <x>
   eval ...`). Should the skill enforce these phrasings, or fix only type and
   scope and leave the subject to the author's voice? Enforcing them raises
   first-try consistency but narrows expression; this is a team-taste call.

6. **Should scope correctness be enforced, not just guided?** commitlint has a
   `scope-enum` rule the repo does not use. The team could make wrong scopes a
   hard failure by generating a `scope-enum` from the filesystem in
   `commitlint.config.js`. That is a repo change beyond this skill, but it
   would move scope from "guided by a skill" to "checked by the gate," which is
   strictly stronger. Flagging it as an option the team may prefer over — or
   alongside — the skill.

## Handoff

When the build runs next (skill-creator or hand-authoring), this brief answers
its intake: the intent and triggers are in Intent, the floor and its
consequence in Floor, the single home for each fact in Sources of truth, the
loading schedule and the required script in Structure sketch, the freeze and
its revisit sign in Fixed decisions, and the evals to build first in Checks.
The scope-derivation detail the build needs is in the companion file
`scope-vocabulary.md`. Do not begin the SKILL.md until Open question 1 (the
multi-area scope rule) has an answer, because the script's contract depends on
it.
