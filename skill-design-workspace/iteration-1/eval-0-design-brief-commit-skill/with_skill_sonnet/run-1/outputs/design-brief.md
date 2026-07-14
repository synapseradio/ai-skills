# Design brief: commit-message skill for `ai-skills`

Mode: Design (skill-design, per `skills/skill-design/SKILL.md`). No SKILL.md
exists yet for this task; this brief is the exit artifact that a build step
(skill-creator or hand-authoring) works from.

The user who requested this skill was unavailable for follow-up during
design. Every place this brief would normally confirm a choice with them
instead states the working assumption and repeats the question in Open
Questions, so the build does not inherit a silent guess.

## Intent

**Task region.** Given a set of staged changes in the `ai-skills` repo, draft
a Conventional Commits header (and body) that (a) passes the repo's existing
`commitlint` gate on the first try, and (b) picks a `scope` that matches the
repo's actual, evidenced convention — not merely a scope commitlint accepts,
since commitlint's active config does not constrain scope values at all (see
Sources of Truth). The stated problem is specifically about scopes coming out
wrong even when the message otherwise looks fine, so the skill's core value
is the scope decision, not header formatting in general.

**Trigger phrasings (positive).** "commit this," "write a commit message for
these changes," "help me commit what's staged," "draft a conventional commit
for this diff," or the moment a teammate is about to run `git commit` and
wants the message written for them.

**Near misses that must not trigger (negative).**

- "squash my last three commits," "clean up this branch's history," "how do
  I resolve this rebase conflict" — commit *structure*/history hygiene, not
  message wording. This is the declared territory of the environment's
  existing `software:git` skill (see below); this new skill should not
  absorb it.
- "write the PR description" — a different artifact with different content
  rules (no header/scope format at all).
- "what's a good example of a conventional commit" as a generic, non-repo
  question — no staged diff in view, nothing repo-specific to derive.

These need user confirmation (I could not verify actual trigger behavior
without a running eval harness — see Checks and Open Question 6).

## Floor

**Working assumption:** declare the floor at whatever is the weakest model a
teammate might have configured in Claude Code day to day, since this skill
ships to "the whole team" rather than to one power user. I did not learn the
team's actual model mix, so I cannot name the floor with confidence — see
Open Question 1. Until confirmed, design to a conservative floor (a small,
fast model) rather than to the capability of whichever model designs or
builds the skill.

**Why this matters here specifically:** the scope decision (below) is not a
simple lookup — it has one clean rule (the generator) plus several enumerated
edge cases that a weak executor is more likely to skip or pattern-match past.
That is exactly what the mandatory verification gate (Structure sketch,
Checks) is for: it does not raise the floor executor's judgment, but it
catches the mechanical half of the failure (header shape) deterministically
regardless of which model is running, leaving only the scope-choice judgment
exposed to floor risk.

## Sources of truth

| Fact | Home | How the skill should reference it |
|---|---|---|
| Valid commit `type` values (11: build, chore, ci, docs, feat, fix, perf, refactor, revert, style, test) and their meanings | `commitlint.config.js` → `@commitlint/config-conventional` (installed in `node_modules`) | Point to the config file; do not copy the list into the skill body as a second, driftable copy. If the config ever adds a project override, the skill should read the live config, not a snapshot. |
| Header ≤100 chars, body/footer lines ≤100 chars, subject not sentence/start/pascal/upper-case, subject has no trailing period, type is lower-case | Same config, inherited from `@commitlint/config-conventional`'s default rule set (verified by reading `node_modules/@commitlint/config-conventional/lib/index.js`) | Same as above — pointer, not copy. |
| **Scope taxonomy** — which string is the "right" scope for a given set of changed paths | **No existing written home.** It is not in `commitlint.config.js` (no `scope-enum` rule is configured — confirmed by reading the installed config-conventional source, which defines no such rule, and the repo's own config only does `extends: ['@commitlint/config-conventional']` with no additions). It is not documented in `README.md`, `CLAUDE.md`, or any CONTRIBUTING file. It exists only as tribal precedent, reconstructible from `git log` and from `CLAUDE.md`'s Layout section describing the directory structure. | This brief's appendix (`appendix-scope-evidence.md`) is the first written record of this fact. The skill body should hold the compact generator + case table (it is the load-bearing content the executor needs every run); the appendix carries the raw evidence (commit hashes, diffstats) a maintainer can recheck later — route the "why," don't copy the raw evidence into the skill body. |
| Verification oracle for whether a drafted message is well-formed | The installed `commitlint` CLI itself (`bunx commitlint`), already wired into `lefthook.yml`'s `commit-msg` and `pre-push` hooks | The skill routes to this tool by running it against the draft (`echo "<message>" \| bunx commitlint`, confirmed working during research — exit 0 on a passing message, exit 1 with itemized rule failures on a failing one) rather than re-deriving compliance from restated rules. |
| Commit body voice/conventions (imperative mood, no attribution trailers, no BREAKING CHANGE footers observed) | Only visible as a pattern across the 157-commit history — **not stated as policy anywhere** | Kept as an inferred pattern, not frozen as a rule — see Open Question 2. |

## Structure sketch

Previewed for the build step, not authored here:

- **Description:** the trigger phrasings and near-miss exclusions above, tight
  enough that "commit this" fires and "let's rebase" does not.
- **Body (small, loads every run):**
  1. Read the staged diff (`git diff --cached --name-only` /
     `git diff --cached`) — an actual command, not a remembered assumption
     about what's staged.
  2. Derive `type` from what the diff *does*, judged from the diff itself,
     using the 11-value enum's stated meanings as the generator (a new
     capability is `feat`, a defect correction is `fix`, a docs-only change
     is `docs`, and so on) — not from how the user phrased the request.
  3. Derive `scope` using the generator in the appendix: name the smallest
     directory the team already treats as one unit (a skill, an extension
     bundle, a top-level area); if the change is *adding a new member* to
     such a collection, name the collection, not the new member; if it
     touches a small number of existing units for one coherent reason, list
     them comma-separated; if it touches many units for one structural
     reason, or is genuinely diffuse across unrelated files, collapse to the
     collection name or omit scope entirely (both are attested in history).
  4. Draft the header and, where warranted, a body (imperative mood, blank
     line after the subject, wrapped well under the 100-char limit).
  5. **Run the draft through `bunx commitlint`** before presenting it.
     Iterate until it passes — this is the certainty-buying step (principle
     7): it turns "I believe this is well-formed" into a ground-truth check
     that already exists in the repo's own tooling, at zero new-dependency
     cost.
  6. Present the message (and, if the scope choice used a fuzzy case — see
     Open Question 3 — say so briefly, so the teammate can override it).
- **References:** the scope-evidence appendix (raw git history citations),
  loaded only if a maintainer or a skeptical teammate wants to recheck the
  generator's basis — not needed on a normal run.
- **Script:** none new. Step 5 above is a single existing CLI invocation
  (`bunx commitlint`), not a script this skill needs to ship.

## Fixed decisions

**Fixed for every session:**

- The type-enum and formatting rules are read from `commitlint.config.js`,
  never restated as a hardcoded copy.
- The scope-derivation generator (unit-naming, collection-collapse-on-add,
  comma-list-for-a-few, collapse-or-omit-for-many/diffuse) is fixed as the
  skill's core mechanism — it is reconstructed from real history, not
  invented, and is the direct answer to "teammates' scopes come out wrong."
- The commitlint verification gate (step 5) is mandatory, not optional. It is
  cheap, already installed, and deterministic; skipping it would leave the
  skill's only checkable claim unchecked.

**Left open to each session:**

- All substantive wording (subject, body content).
- Whether to name 2–3 units individually vs. collapse to the collection
  scope, at the fuzzy boundary — the evidence bounds this loosely (2 units
  stayed named in the sample; 10 collapsed) but does not pin an exact
  cutover. The skill should make this judgment call visibly rather than
  silently, per the "present with reasoning" step above.
- Whether to attach any trailer/footer content — no policy found; default to
  omitting, matching every commit observed, but this is a lean, not a rule.

**Decision most likely to need revisiting:** the scope-derivation case table.
It was built from the directory kinds that exist in the repo today (`skills/`,
`skills/<group>/<name>/`, `extensions/<name>/`, `packaged/`, and a handful of
root-level areas). **Revisit sign:** the day the team adds a new top-level
directory kind (e.g., a `services/` or `apps/` tree) or changes
`CLAUDE.md`'s Layout section, the case table stops covering the new shape and
needs a matching addition — it will not fail loudly, it will just produce a
scope guess with no precedent behind it, which is exactly the failure mode
this skill exists to prevent.

## Checks

**Eval assertions to build first** (each pairs a labeled staged-diff fixture
with an expected scope or type):

1. A diff touching only files inside one existing skill's directory → scope
   equals that skill's directory name.
2. A diff that is the *first* commit for a brand-new skill (new `SKILL.md`,
   `README.md`, `packaged/*.skill`, plus the root `README.md` link) → scope
   is the collection name (`skills`), not the new skill's own name. This is
   the single highest-value assertion: it is the exact shape of error a
   naive "scope = affected folder" heuristic gets backwards, and it is
   directly evidenced in history (see appendix, cases 2–3).
3. A diff touching exactly two existing skills for one coherent reason →
   scope is the comma-separated pair.
4. A diff touching many (repo's evidence: ten or more) existing skills for
   one structural, repo-wide reason → scope collapses to the collection name.
5. **Every drafted message passes `bunx commitlint --edit` (or the stdin
   equivalent) with exit code 0.** This is the headline, cheapest, most
   deterministic check and should gate the skill's own release, not only run
   inside it.
6. A small labeled set (aim for enough to see a pattern, not a fixed count)
   of type-selection fixtures spanning feat/fix/docs/chore/refactor, checked
   against the type each should produce.
7. A trigger-rate harness: labeled positive prompts (commit-shaped requests)
   against labeled near-miss prompts (git-workflow-shaped requests that
   belong to `software:git` instead), per principle 3's mis-triggering check.

**Operation that must be a script/executed step, not prose:** the commitlint
verification gate (check 5). Everything upstream of it (type and scope
choice) is inherently a judgment call and stays probabilistic; this one step
is not, and there is no reason to leave it to chance when the exact tool
already exists in the repo.

## Open questions

Recorded here in place of a conversation the user was unavailable for.

1. **Floor executor.** Which model(s) do teammates actually run in Claude
   Code for everyday commits? This decides how much the generator's case
   table needs to be spelled out versus how much can be left to inference.
2. **Trailers/attribution.** Should "no `Co-authored-by`, no attribution
   trailers" be encoded as a hard rule, or left as an unstated default? The
   full 157-commit history shows zero instances, but that is an absence, not
   a written policy — it could be one author's habit rather than team intent.
3. **The comma-list vs. collection-collapse threshold.** History bounds it
   loosely (2 units named individually in one case; 10+ collapsed in
   another) but no commit in the sample pins the exact cutover (3? 4? 5
   units?). Worth either picking a number deliberately or explicitly leaving
   it to judgment — right now it is a working heuristic, not a frozen rule.
4. **Scope of the skill itself.** The stated complaint is specifically about
   scopes. Should this skill also draft the commit *body* (multi-line
   rationale), or stay narrowly focused on the header line (type + scope +
   subject)? A narrower skill is smaller to verify and faster to trust; a
   broader one covers more of what a teammate would otherwise hand-write.
5. **Pairing with a deterministic repo-side gate.** Right now, correctness
   depends on a teammate remembering to invoke the skill — the skill itself
   only shifts a probability (principle 7). Is there appetite for also
   adding a `scope-enum` rule to `commitlint.config.js` (mechanically listing
   the current skill/extension names) or a commit-msg hook addition, so
   scope correctness is caught even without the skill running? That is a
   repo-tooling change, outside a skill's own footprint — flagging rather
   than deciding it, since scope of work belongs to the user.
6. **Invocation model.** Should the skill fire automatically whenever a
   teammate runs `git commit` through Claude Code, or only on an explicit
   ask ("commit this")? Automatic firing removes reliance on remembering to
   invoke it, but raises the cost of a false trigger on unrelated git
   commands — this needs the trigger-rate harness (Checks, item 7) run
   before deciding, not a guess now.
7. **Overlap with the environment's `software:git` skill.** That skill
   already covers "structuring commits for review, deciding what belongs in
   a commit... git strategy, commit discipline." This design deliberately
   stays narrower — deriving the message for a diff that is already staged,
   not deciding what should be staged. Confirm the team wants these to
   coexist as separate, composable skills rather than merged into one.

## Evidence appendix

The scope-derivation generator's full case-by-case evidence (commit hashes,
diffstats, and the reasoning drawn from each) lives in
`appendix-scope-evidence.md`, alongside this brief.
