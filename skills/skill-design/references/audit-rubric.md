# Audit Rubric

One entry per principle. For each: ask the question, collect the evidence,
decide. Three verdicts exist — **pass**, **fail**, and **not checkable
today**. A not-checkable verdict names the check that would decide it, so the
gap gets scheduled instead of dropped. Cite every piece of evidence by file
and line. Full principle statements and their sources live in
[principles.md](./principles.md); consult them when a verdict feels close.

## 1. Schedule the workspace

Question: does read cost scale with the task rather than with the corpus?

Collect: approximate token counts for the description, the body, and each
reference; the body's pointers to references, and whether each pointer says
when to read the target.

Decide: pass when the description alone carries the selection information,
the body stays near or under the recommended 5,000 tokens, and detail lives
in references behind read conditions. Fail when the body inlines what a
reference should hold, or when the skill tells its executor to load
references unconditionally.

## 2. Route, don't hold

Question: does any fact live in two homes?

Collect: candidate duplicated facts — one rule stated in two passages, one
table in two files; the declared sources of truth, and what the skill says to
do when it disagrees with a source.

Decide: pass when each fact keeps one home and every other occurrence
points there. Fail on a duplicated fact that could drift. Duplication decides
mechanically only where the fact has an executable form (a doctest, a
contract test); prose duplication decides by inspection.

## 3. Make every delegated decision decidable

Question: for each decision the skill hands its executor, does the skill
provide what decides it?

Collect: the decision inventory — invocation (the description), every phase
or mode exit, every routing point, every place a red result re-enters the
flow — and, for each, the decision basis the skill provides.

Decide: pass when every inventoried decision names its basis. Fail on any
exit or route that needs information the skill neither provides nor tells the
executor to fetch. A flattened rule ("always do X") that decides everything
while fitting little counts as fail, not pass.

Harness: trigger rate over about 20 labeled queries decides invocation; run
variance decides exits. Without the harness, mark those two aspects not
checkable today and decide the rest by inspection.

## 4. Declare the floor, and write to it

Question: which executor anchors the `compatibility` declaration, and can
that executor act on every abstract term in the body?

Collect: the `compatibility` field; each abstract term, and whether it
grounds in a runnable referent (domain skill) or a worked move (method
skill).

Decide: pass when a floor stands declared and every term grounds. Fail when
no floor exists, or when a term assumes derivation the floor may not perform.
Compliance measurement across a capability range stays not checkable today
without a multi-model harness; name that in the report.

## 5. State the generator, and bound the enumeration

Question: where several rules share a cause, does the skill state the cause —
and still enumerate the load-bearing cases?

Collect: rule clusters; candidate generator sentences; for each candidate,
run the reconstruction test — handed the sentence and a concrete case, but
not the rule, could the executor rebuild the rule?

Decide: pass when each cluster carries a generator that survives
reconstruction plus a bounded enumeration of the cases that matter. Fail on
either half missing: a rule pile with no stated cause, or a lone generator
with no cases for the floor.

## 6. Type every rule by its check

Question: does each rule read as an invariant, an obligation, or a
preference, and does it sit beside the check its kind names?

Collect: every rule — the MUSTs, NEVERs, SHOULDs, and bare imperatives;
classify each; flag mixed buckets, such as a single NEVER list folding
in-task invariants together with artifact obligations.

Decide: pass when kinds stay separated and each rule pairs with its check.
Fail on a mixed bucket or a rule with no assigned check.

## 7. Expect probability, and buy certainty with artifacts

Question: which operations must not vary, and does an executed artifact cover
each one?

Collect: operations where variance costs — exact formats, arithmetic,
mechanical transforms; the `scripts/` directory; wording strength against how
much each rule matters.

Decide: pass when every must-not-vary operation routes to a script or other
executed artifact, and wording strength tracks importance. Fail when a
deterministic need rests on prose alone. Where the eval harness exists, run
variance measures a rule's actual strength.

## 8. Verify each claim in the mode its kind admits

Question: does every empirical claim resolve to an artifact or source a
reader could reach, and does the skill name what no check covers?

Collect: each empirical claim — numbers, API behaviors, performance
statements — and its source; claims inherited from other documents, and
whether they got rechecked; unverified claims, and whether they carry a mark.

Decide: pass when claims resolve or carry an explicit unverified mark. Fail
on a bare magnitude, or an inherited claim with no reachable source.

## 9. Freeze deliberately

Question: are the skill's fixed decisions written down where a maintainer
will read them — what it hard-codes, what it leaves open to each session,
and what sign says to revisit?

Collect: the skill's README, design brief, or maintainer notes; also any
body text that describes the skill to itself rather than instructing the
agent running it.

Decide: pass when a maintainer-facing artifact carries the three statements;
fail when nothing does. Body text that observes the skill ("this skill
fixes...") spends the executor's context without directing action — count it
against principle 1, never as satisfying this one. This principle rests on a
working guideline, so inspection carries the whole verdict — say so in the
report.

## 10. Make the skill observable

Question: could this skill's effect be measured tomorrow morning?

Collect: an `evals/` directory or equivalent; baseline runs; whether each
expected effect pairs with a check or with an admitted gap.

Decide: pass when evals exist, or when the skill names which checks apply and
what stays unmeasurable. Fail when no path to measurement exists and the gap
goes unnamed.

## Report format

For each principle: the verdict, a one-line reason, and the evidence
citations (file and line). Close with the two costliest failures and the
refactor move each one suggests. Audit changes nothing; every fix routes
through Refactor mode with this report as its evidence base.
