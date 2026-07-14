# Audit: skills/apache-age

Mode: Audit (skill-design). Changes nothing in the target skill. Verdicts are
**pass**, **fail**, or **not checkable today**, each with evidence cited by
file and line. Files read in full: `SKILL.md`, `README.md`, and all five
references (`the-wrapper-contract.md`, `agtype-is-everything.md`,
`hybrid-is-the-point.md`, `schema-is-storage.md`, `nothing-is-automatic.md`).

## Bottom line

The skill is well researched and its factual content is largely accurate —
two of its most load-bearing quantitative claims were spot-checked live
against GitHub and both held up. But structurally it fails half the ten
principles: the same facts live in two or three files at once, one rule of
each of its content documents mixes hard invariants with graded heuristics
in a single undifferentiated list, it names its own "follow exactly"
operations and then backs none of them with a script, it declares no floor
executor, and it carries no evals and no maintainer notes on what it freezes.
None of these are close calls — each has direct textual evidence below.

## Per-principle verdicts

### 1. Schedule the workspace — **pass**

The description (`SKILL.md:3`) alone carries the trigger surface — Cypher
syntax, agtype, hybrid SQL+Cypher, schema modeling, performance — with no
detail deferred to it. The body is ~910 words / 6,213 characters
(~1,500–1,600 tokens by char/4 estimate), comfortably under the 5,000-token
guideline. A reference-loading table (`SKILL.md:24-31`) states an explicit
load condition for each of the five references ("Load when casting agtype to
SQL types...", "MANDATORY before performance work..."), and a "Do NOT load"
section (`SKILL.md:33-36`) actively prunes unneeded reads. Read cost scales
with the task, not the corpus.

Soft spot, not a failing one: three of five references are marked
`MANDATORY` (`SKILL.md:26,28,30`), which narrows how much the conditional
table actually saves in the common case — most real sessions will load most
references anyway.

### 2. Route, don't hold — **fail**

Several facts have more than one home, with measurable drift already visible
between copies:

- **The agtype→SQL casting table is duplicated near-verbatim** between
  `references/agtype-is-everything.md:228-239` and
  `references/hybrid-is-the-point.md:401-408`. Same rows, same target types,
  same Issue citations (#1225, #1996) — but the wording of the `text` row
  already diverges ("**Fails on non-scalars**" vs. "Fails on non-scalar
  agtype... Use `col::varchar` instead"). Two homes for one fact, already
  not word-for-word identical.
- **"cypher() requires an AS column list"** is stated independently in three
  places: `SKILL.md:54-60,103`, `references/the-wrapper-contract.md:26-38,
  221-231`, and `references/hybrid-is-the-point.md:42-48,469-476`.
- **"search_path must include ag_catalog"** appears in `SKILL.md:12-13,94-98`,
  `references/the-wrapper-contract.md:69-81,212-219`, and
  `references/hybrid-is-the-point.md:47`.
- **"CREATE/SET/REMOVE cannot run inside a JOIN"** appears in
  `SKILL.md:83-92,105` and is separately restated three times inside
  `references/hybrid-is-the-point.md` (lines 160, 224-250, 459-467).

No file is marked as the canonical home for any of these facts, and nothing
says "the reference wins on disagreement" — SKILL.md and the references read
as parallel, independently-maintained restatements.

### 3. Make every delegated decision decidable — **pass**, with one harness gap

The reference table ties each load decision to a task shape the executor can
observe directly — "before writing any SQL+Cypher query" (`SKILL.md:28`),
"before performance work" (`SKILL.md:30`) — which is decidable from what the
user is asking for. Two entries lean on inferring user history rather than
the task in front of the executor: "MANDATORY for first-time AGE users"
(`SKILL.md:26`) and "the-wrapper-contract.md for users already familiar with
cypher() mechanics" (`SKILL.md:36`) ask the executor to judge something it
cannot directly observe from context. Narrow, but real.

**Not checkable today:** no `evals/` directory and no trigger-rate or
run-variance harness exist anywhere in the skill or the repo (confirmed with
`find` across both the skill directory and the broader repo). Invocation and
exit decidability stay unmeasured; this is also principle 10's finding.

### 4. Declare the floor, and write to it — **fail**

Frontmatter (`SKILL.md:1-4`) declares only `name` and `description` — no
`compatibility` field exists. No floor executor is named anywhere in the
skill. This also weakens the "Freedom calibration" section
(`SKILL.md:38-42`), whose "adapt to context" / "choose freely" language for
medium/high-freedom items has nothing to ground against once a floor is
named.

### 5. State the generator, and bound the enumeration — **fail** (mixed at the cluster level)

Two clusters carry a genuine generator that survives the reconstruction
test:

- `references/agtype-is-everything.md:9` — "agtype is AGE's single data type
  for all values crossing the SQL↔Cypher boundary" — is exactly the
  generator form the skill-design principle uses as its own passing example,
  and the casting rules, null-handling rules, and comparability notes in
  that file all follow from it.
- `SKILL.md:49` — "Nothing exists until you create it — no default indexes,
  no property constraints, no type enforcement" — explains the indexing
  NEVER, the missing-constraint NEVER, and most of
  `references/nothing-is-automatic.md` in one sentence.

One cluster does not: the JOIN-mutation restriction is restated four times
total (`SKILL.md:83-92,105`; `references/hybrid-is-the-point.md:160,224-250,
459-467`) but its stated cause — "they interact with the PostgreSQL
transaction system in a way that is incompatible" (`hybrid-is-the-point.md:
160`) — is an assertion, not a mechanism. Handed that sentence and a new
concrete case, an executor cannot derive anything further from it; it names
that the restriction exists without stating why, so the rule pile has no
generator to reconstruct from and instead gets repeated by hand at every
occurrence (which is also principle 2's finding for this same cluster).

### 6. Type every rule by its check — **fail**

`SKILL.md:101-112`'s NEVER list is one flat bucket folding together kinds
that need different checks:

- **Invariants**, checkable by inspection because AGE physically enforces
  them — "NEVER use multiple labels on one vertex" (line 110), "NEVER
  compare agtype to SQL types without casting" (line 108).
- **Task-boundary obligations** — "NEVER omit the AS column list" (line
  103), checked at the moment the query is finalized.
- **Scale-dependent heuristics that read as absolute preferences** — "NEVER
  use unbounded `[:REL*]`" (line 106) and "NEVER assume indexes exist" (line
  107) are graded by graph size (fine on a thousand-row demo graph,
  catastrophic at 1.5M vertices per the same line's own citation) but are
  phrased with the same NEVER strength as the true invariants above them.

Nothing in the list's presentation distinguishes these — exactly the
rubric's named failure mode: "a single NEVER list that folds invariants
together with... obligations invites [misapplication]."

### 7. Expect probability, and buy certainty with artifacts — **fail**

The skill names its own must-not-vary operations directly: "**Low freedom**
(follow exactly): cypher() wrapper syntax, AS column lists, search_path,
index DDL, mutation CTE guards" (`SKILL.md:40`). These are precisely the
class of operation the principle asks to be backed by an executed artifact.
The skill directory contains no `scripts/` at all — only `SKILL.md`,
`README.md`, and `references/` (confirmed by directory listing). Every one of
those low-freedom operations is enforced by prose and example code blocks
only; nothing checks, at write time, whether a given query's `AS` column
count matches its `RETURN` count, whether `search_path` is set, or whether a
generated index DDL statement is well-formed.

### 8. Verify each claim in the mode its kind admits — **fail**, with two claims independently confirmed

Two of the skill's most load-bearing quantitative claims were checked live
against GitHub during this audit and both hold up:

- "~15x faster... per Issue #2194" (`SKILL.md:50`;
  `references/nothing-is-automatic.md:423`) matches `apache/age` issue #2194,
  "Major Performance Difference: SQL vs. Cypher for Aggregation/Ordering,"
  opened 2025-07-16, which states Cypher is "over 15x slower" for this
  workload — confirmed via live search.
- "7s → 7min on 1.5M vertices, Issue #195" (`SKILL.md:106`) matches
  `apache/age` issue #195, "Variable Length Edges feature does not scale
  well with the length of the path," opened 2022-03-09 — confirmed to exist
  and match the subject matter; the exact 7s/7min figures were not visible in
  the search snippet, so those specific numbers stay unconfirmed[?] even
  though the underlying issue is real.

One claim does not hold up under the same check: "Published benchmark: 725K
vertices + 2.8M edges loaded in ~83 seconds using `use_copy=True`"
(`references/nothing-is-automatic.md:353`) cites no issue number, PR, or URL.
A search of AGEFreighter's own PyPI pages and GitHub surfaced different
published benchmarks for the same tool (965 million rows via Azure Storage;
512 seconds for a distinct dataset) but not this figure — a bare magnitude
with no reachable source, which is the principle's named failure mode
exactly.

The remaining Issue/Discussion citations in the skill (#1225, #1996, #1840,

# 1956, #1303, #315, #109, #1431) were not independently checked in this

audit — flagged `[?]` rather than asserted as either verified or wrong.

### 9. Freeze deliberately — **fail**

No README, design brief, or maintainer note anywhere states what the skill
hard-codes (e.g., the PascalCase/SCREAMING_SNAKE_CASE/camelCase naming
convention table in `references/schema-is-storage.md:217-224`), what it
leaves to each session, or what sign would prompt a revisit.
`skills/apache-age/README.md` is install/license boilerplate only (23 lines,
confirmed by full read). `git log --oneline -- skills/apache-age` shows only
directory-reorganization and link-fixup commits — no design-brief content
anywhere in history.

### 10. Make the skill observable — **fail**

No `evals/` directory or equivalent exists anywhere in `skills/apache-age`
(confirmed by `find`). A repo-wide search for other `apache-age`-named paths
turned up only the eval workspace currently being used to audit *this very
skill* via skill-design — nothing that measures apache-age's own effect.
Nowhere does the skill admit this gap or name which of its claims would stay
unmeasured even if a harness existed.

## The two costliest failures

**1. Principle 7 — no artifacts back the skill's own "follow exactly" list.**
This is a skill whose failure modes are syntactic and silent: wrong `AS`
column count, `SET n =` instead of `SET n +=` (silently drops every other
property), a missing `search_path`. The skill already tells the reader which
operations must not vary (`SKILL.md:40`) — it has done the hard part of
naming them — but ships nothing that checks them mechanically. A refactor
here doesn't need much: a short script that lints a candidate query for
column-count mismatch against its `RETURN` clause, or one that greps for
bare `SET n = {` where `+=` was probably intended, converts the highest-risk
items on the NEVER list from "hope the executor remembers" to "the tool
catches it."

**2. Principle 2 — the same facts live in multiple files and are already
drifting.** The agtype-casting table is the clearest case: two nearly
identical copies, already worded differently, both dated to the same two
GitHub issues. If AGE ever resolves #1225 or #1996, whoever updates this
skill has to remember there are two tables to fix, not one — and nothing in
either file points to the other as the source of truth. The fix is
mechanical: pick one home per fact (the wrapper mechanics facts belong in
`the-wrapper-contract.md`; the casting table belongs in
`agtype-is-everything.md`; the JOIN/CTE facts belong in
`hybrid-is-the-point.md`) and turn every other occurrence, including the
ones currently in `SKILL.md`'s Critical Gotchas and NEVER list, into a
pointer.

Runners-up, both real but less immediately actionable without more input:
principle 4 (no declared floor — fixable in one line, but the right floor to
declare is a judgment call the user should make, not this audit) and
principle 10 (no evals — the largest fix by effort, but downstream of
everything else being stable first).

## Open questions (for the user, recorded rather than asked)

1. Should `agtype-is-everything.md` own the casting table outright, with
   `hybrid-is-the-point.md` reduced to a one-line pointer plus its own
   hybrid-specific examples? Or is some duplication intentional so each
   reference reads standalone without cross-file hops mid-task?
2. What executor is this skill's actual floor — is it meant to run
   identically well on a smaller/cheaper model, or is Opus-and-up an
   acceptable assumption? That answer determines both the `compatibility`
   field and how much the "Freedom calibration" section needs tightening.
3. Is a lint-style script for `AS` column-count / `SET =` vs `+=` detection
   worth building, or does the team consider prose NEVERs sufficient given
   how AGE errors are usually loud (query fails outright) rather than silent
   — except for the `SET =` case, which is the one genuinely silent failure
   mode on the list?
4. Was the 725K-vertex/83-second AGEFreighter benchmark seen firsthand (a
   specific PR, release note, or blog post), or should it be re-sourced or
   removed?
