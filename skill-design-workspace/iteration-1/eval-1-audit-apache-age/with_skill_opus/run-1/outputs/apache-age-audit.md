# Audit — `skills/apache-age`

Mode: Audit (skill-design). Nothing was changed. Every verdict cites file and
line. Verdicts are one of **pass**, **fail**, or **not checkable today**,
following `skill-design/references/audit-rubric.md`.

## Bottom line

This is a well-researched, well-organized domain skill with a genuinely strong
spine — five generator sentences, each with its own reference — and unusually
disciplined sourcing (most AGE-specific claims cite a GitHub issue, PR, or
discussion number). It is let down in two ways that matter for a *reference*
skill, where the whole value proposition is being right: a handful of facts live
in two homes and have already drifted into contradiction, and a few load-bearing
claims are unsourced or self-contradictory. It also skips the skill-as-artifact
scaffolding — no `compatibility` floor, no maintainer-facing freeze record, no
evals.

Four principles pass, five fail, one is partly not-checkable without a harness.

## Per-principle verdicts

### 1. Schedule the workspace — **pass**

The description alone carries selection information (SKILL.md:3). The body is
~910 words / roughly 1,200-1,400 tokens, comfortably under the 5,000-token
guideline. Detail lives in five references, each gated by an explicit "When to
Load" column plus a "Do NOT load" list (SKILL.md:24-36). Reference sizes are
reasonable (1,300-2,300 words each).

One caveat, not enough to fail: three references are marked **MANDATORY**, and
`hybrid-is-the-point.md` is "MANDATORY before writing any SQL+Cypher query"
(SKILL.md:28). Because every AGE query is a SQL-wrapped Cypher call (the skill's
own generator, SKILL.md:46), that condition fires on nearly every task — it
approaches "load unconditionally," which is the failure mode this principle
warns against. The condition is at least stated, so the read cost still nominally
tracks the task.

### 2. Route, don't hold — **fail**

Several facts have two homes, and at least one pair has already drifted into a
contradiction:

- **`graphid` uniqueness — direct contradiction.** `schema-is-storage.md:44`
  states `id` is "system-assigned, globally unique." `the-wrapper-contract.md:247-249`
  states the opposite: "graphid is not globally unique across graphs… IDs are
  unique within a graph, not across graphs" (also line 172). A reader who loads
  one reference gets the inverse rule from the other. At least one is wrong (see
  principle 8).
- **agtype→SQL casting table duplicated in full.** The same table appears in
  `agtype-is-everything.md:232-240` and `hybrid-is-the-point.md:401-408`,
  including the identical "the only string cast that works" cell. Two homes, no
  pointer; the next correction to one will silently diverge.
- **Single-label rule stated four times with drifted wording.**
  `the-wrapper-contract.md:173` says "exactly one label per vertex," while
  `agtype-is-everything.md:96` and `SKILL.md:110` say "zero or one." A
  label-less vertex is legal in AGE (`agtype-is-everything.md:110` notes the
  label "may be empty"), so "exactly one" is the inaccurate copy.

Some repetition here is legitimate routing — the `search_path` and AS-column-list
gotchas recur across four files as a body summary plus reference detail, which is
fine. The three items above are not that: they are the same fact re-stated as
fact, and they can (and do) drift.

### 3. Make every delegated decision decidable — **pass (invocation not checkable today)**

The routing decisions are decidable by inspection: which reference to load has a
"When to Load" basis and a "Do NOT load" exclusion list (SKILL.md:24-36), and how
tightly to follow a rule is given by the Low/Medium/High "Freedom calibration"
(SKILL.md:38-42). No routing point is left without a basis.

The one decision this skill cannot self-evidence is **invocation** — whether the
description triggers on the right prompts and stays quiet on near misses. That
needs the trigger-rate harness (about 20 labeled prompts, three runs). No such
data ships. Per the rubric, this aspect is **not checkable today**; the rest
passes by inspection.

### 4. Declare the floor, and write to it — **fail**

There is no `compatibility` field in the frontmatter (SKILL.md:1-4 contains only
`name` and `description`). The floor — the weakest executor this skill is written
for — is undeclared, so "correctness judged at the floor" has no anchor. The
rubric fails this on "no floor exists."

Mitigating fact: the body largely does write to a low floor anyway. Abstract
terms ground in runnable, copy-paste SQL, and the "Think in AGE" generators are
concrete. So the *prose* is floor-friendly; the *declaration surface* is empty.
Adding a `compatibility` string is a one-line fix.

### 5. State the generator, and bound the enumeration — **pass (strongest principle)**

This is the skill's best feature. "Think in AGE" states five true generators —
"Every Cypher query is a SQL function call," "agtype is the only type that
crosses the boundary," "Graphs are PostgreSQL schemas," "Nothing exists until you
create it," "Hybrid is the value proposition" (SKILL.md:46-50). Each survives the
reconstruction test (this is the same shape as principles.md's own exemplar,
"Every value AGE returns is agtype"), and each has a whole reference named after
it. The enumeration is also present and bounded: Critical Gotchas (SKILL.md:53-99),
the NEVER list (SKILL.md:101-112), and Common Recipes (SKILL.md:114-159) carry
the load-bearing concrete cases the floor may not derive.

### 6. Type every rule by its check — **fail**

The NEVER list (SKILL.md:101-112) is a single bucket mixing rule kinds:

- per-query obligations — "NEVER omit the AS column list" (line 103)
- schema-design invariants — "NEVER use multiple labels on one vertex" (line 110)
- performance/query-writing rules — "NEVER use unbounded `[:REL*]`" (line 106),
  "NEVER assume indexes exist" (line 107)
- a hard limit — "NEVER build maps with 50+ fields" (line 111)

An agent doing schema design wades through query-writing and performance rules to
find the one that applies, which is exactly the misapplication this principle
warns about. The "Freedom calibration" block (SKILL.md:38-42) does type rules by
strength and is a real strength — but the NEVER list itself stays undifferentiated
and unpartitioned by the moment each rule is checked.

### 7. Expect probability, and buy certainty with artifacts — **pass (with one candidate)**

There is no `scripts/` directory. For this skill that is defensible: the
must-not-vary operations here (the AS column list, index DDL) are all
schema-dependent, so no context-free operation exists that a standalone script
could pin. The deterministic content ships as copy-paste-correct SQL templates,
which is the right artifact form for a knowledge skill, and wording strength
tracks importance (NEVER / MANDATORY / Low-freedom for the rigid parts).

One candidate worth flagging for a future refactor: the single-key BTREE index
DDL, `agtype_access_operator(VARIADIC ARRAY[properties, '"email"'::agtype])`
(nothing-is-automatic.md:85-87, schema-is-storage.md:507-509), is exact,
error-prone, and repeated verbatim — a small generator snippet parameterized by
key name would remove a transcription hazard. Not a fail; a note.

### 8. Verify each claim in the mode its kind admits — **fail**

Sourcing discipline is mostly excellent — issues #315, #195, #1225, #1996, #1840,

# 1956, #1303, #2194, discussion #109, PR #1431 are all cited at their claims

That makes the exceptions stand out:

- **Unsourced magnitude.** "Published benchmark: 725K vertices + 2.8M edges
  loaded in ~83 seconds" (nothing-is-automatic.md:353) names no resolvable
  source. It is the exact "bare magnitude" the rubric fails on — unrecheckable
  when AGEFreighter's numbers change.
- **Unsourced, likely-suspect API claim.** The "AGE extended form" edge syntax
  `-[:KNOWS]->>(b)` and `<<-[:KNOWS]-(b)` (the-wrapper-contract.md:108-114) is
  the only AGE-specific behavioral claim in the file that carries **no** issue
  citation, in a file that otherwise cites everything. `->>` collides with
  PostgreSQL's JSON operator, which makes it worth doubting. I cannot confirm it
  is wrong from the files alone, so I mark it unverified rather than false [?] —
  but it violates the skill's own sourcing convention and should be checked
  against AGE's grammar before it ships.
- **The `graphid` contradiction (from principle 2).** "globally unique"
  (schema-is-storage.md:44) versus "not globally unique across graphs"
  (the-wrapper-contract.md:247). One of these is a wrong claim being replayed
  every session.

### 9. Freeze deliberately — **fail** (checked by inspection; this principle has no measurement)

The only maintainer-facing artifact is `README.md`, and it holds just install
instructions and a license (README.md:1-23). Nowhere does a maintainer-facing
document state what the skill hard-codes (its scope, the five generators, the
naming conventions), what it leaves to each session, or what sign says to revisit
a frozen choice. The "Freedom calibration" and "When to Load" blocks encode some
of this, but they live in the body, addressed to the executor — which this
principle explicitly does not count. There is no design brief or maintainer note.

### 10. Make the skill observable — **fail**

No `evals/` directory exists for this skill and no baseline is referenced. More to
the point, the skill names no gap — it neither ships checks nor admits their
absence. A path to measurement plainly exists (a trigger-rate harness over
labeled AGE prompts; assertion pass rate on the recipes with and without the
skill), which is what makes this a fail rather than "not checkable": the
measurement is available and simply unbuilt and unmentioned.

## The two costliest failures

For a domain-reference skill, correctness of the content dominates, because every
claim re-executes as fact in every session that loads it. So the two failures to
fix first are both about the content being right, not about the skill's
scaffolding:

1. **Principle 8 — factual reliability.** Fix the `graphid` contradiction (decide
   whether it is globally unique or per-graph and state it once), source or drop
   the 83-second benchmark, and verify the `->>` / `<<` "extended form" against
   AGE's actual grammar before shipping it. Refactor move: treat each as a claim
   needing a reachable source; where none exists, mark `[?]` or remove.

2. **Principle 2 — route, don't hold.** Give each drifted fact one home. Put the
   agtype→SQL casting table in `agtype-is-everything.md` and make
   `hybrid-is-the-point.md` point to it; state the single-label rule once with
   accurate wording ("zero or one per vertex; edges require exactly one") and
   reference it elsewhere. This also structurally prevents the principle-8
   contradictions from recurring.

A secondary theme worth one refactor pass: the skill-as-artifact gaps
(principles 4, 9, 10) cluster together and are cheap to close — add a
`compatibility` floor line, add a short maintainer "Fixed decisions / revisit
sign" note (README or design brief), and stand up a minimal eval + trigger-query
set. None changes the content; all three make the skill maintainable and
measurable.

## Open questions for the author

The task author was unavailable, so questions that would normally be asked are
recorded here instead:

1. **Deployment floor.** Which executor is this skill meant to serve at its
   weakest (Haiku-class? a specific harness)? The answer sets the `compatibility`
   string and calibrates how much the enumerations need to spell out.
2. **`->>` / `<<` edge syntax.** Is the "AGE extended form"
   (the-wrapper-contract.md:108-114) real and current AGE grammar, and if so what
   issue/PR/doc supports it? If it cannot be sourced, should it be removed?
3. **`graphid` uniqueness — which is correct?** Resolve globally-unique
   (schema-is-storage.md:44) versus per-graph (the-wrapper-contract.md:247) so
   the fact can be stated once.
4. **Benchmarks.** Is there a citable source for the 725K/2.8M/83s AGEFreighter
   figure, and for the "~15x faster" aggregation number beyond "Issue #2194"?
5. **Intended breadth of "MANDATORY."** Is `hybrid-is-the-point.md` genuinely
   meant to load on essentially every query, or should its trigger be narrowed to
   queries that actually mix SQL and Cypher beyond the bare wrapper?
6. **Scope of any follow-up.** This audit changes nothing. Should the findings
   feed a Refactor pass, and if so, is fixing the content contradictions
   (principles 2 and 8) in scope before the scaffolding gaps (4, 9, 10)?
