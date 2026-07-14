# The Principles

A skill should give the sessions that load it more than it takes from
them. Ten practices serve that end. This file holds each in full — the
practice, the reason behind it, and the way to check it — along with
the vocabulary the statements share. Read it before design or refactor
work; during an audit, walk the principles with the user as lenses.

The established practice behind these statements lives on two pages:
the [Agent Skills specification](https://agentskills.io/specification)
and Anthropic's [skill best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
Each link below sits where its claim stands.

## Vocabulary

A **skill**: instructions an agent loads into a working session — what
to read, in what order, and how the work closes.

A **source of truth**: the knowledge behind a skill — the skill's own
reference files, a codebase, a documentation corpus. Skill and source
stay distinct.

An **executor**: the agent running the session, a model plus its
harness, varying in capability across deployments. The **floor**: the
weakest executor the author commits the skill to work on. Weakest
means least compliant on the task, never smallest — a larger model
does not automatically follow instructions better.

**Intent**: what the user wants when they reach for the skill. A
well-stated intent lets you tell, for any request, whether it falls
inside the tasks the skill exists for or just nearby.

A **generator**, relative to a set of rules: a stated fact the rules
follow from. Hand an executor the fact and a concrete case, but not
the rule, and it can rebuild the rule; one edit to the fact updates
every consequence together. If no executor can decide a new case from
the fact, the sentence only summarizes.

## 1. Schedule the workspace

Everything loaded from a skill takes up the same finite context. The
runtime loads a skill in stages — name and description at startup,
body on activation, references on demand
([specification](https://agentskills.io/specification)) — so put
selection information in the description, orchestration in the body,
and detail in references behind clear read conditions. What the
executor must read then scales with the task at hand, never with how
much the skill contains.

Check: pick a small task the skill exists for and list what the
executor must load to finish it. Detail loaded but never touched means
the staging failed. skill-creator's harness reports tokens per task
next to pass rate; a body that inlines what references should hold
shows up there as tokens rising while pass rates stay flat.

## 2. Route, don't hold

Treat a skill as a map of its source of truth, never as a second copy.
Give every fact one home and make every other occurrence a pointer,
because two copies of a fact drift apart from the first update that
reaches only one of them. Where a pointer alone falls short, move the
check or the script to the fact's home rather than copying the fact to
the work. Where the skill contradicts its source, trust the source —
and write the skill so its executor surfaces the contradiction to the
user.

Check: by inspection — hunt for one rule stated in two passages, one
table in two files. Where a duplicated fact takes an executable form,
a doctest or contract test makes the drift visible.

## 3. Make every delegated decision decidable

Every decision delegated to the executor must close from what the
skill provides. The executor decides invocation from the description
alone, because only the description sits in context at selection time.
Name each phase's exit condition, and name where the work resumes
after a failed check. You can raise decidability two ways, and only
one counts: sharpen the fit between skill and intent, and the executor
decides without guessing; flatten the rules ("always do X"), and the
executor reaches the same answer whether the rule fits the case or
not. Buy decidability by sharpening, never by flattening.

Check: inventory the decisions — invocation, every exit, every routing
point — and ask, for each, where the executor gets its answer.
skill-creator's description optimizer measures whether the description
triggers on the right requests.

## 4. Declare the floor, and write to it

Every skill has a floor: the weakest executor it must work on. Declare
it in the `compatibility` field and judge correctness there, because
an instruction that works on the strongest model can quietly fail
below it — "What works perfectly for Opus might need more detail for
Haiku"
([best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)).
Ground every abstract term in something the floor can act on: runnable
code in a domain skill, a worked move in a method skill.

Check: read each abstract term and say what the declared floor would
do with it. If acting on a term takes reasoning the floor may not
perform, the term fails the check.

## 5. State the generator, and bound the enumeration

Where several rules share a cause, state the cause. "Every value AGE
returns is agtype" passes the generator test: an executor can rebuild
the casting rules from it and extend them to cases the author never
listed. "Be careful with AGE syntax" fails the same test — no executor
can rebuild a single rule from it. Then enumerate the cases that carry
the skill's weight anyway, because the floor may not manage the
derivation — and stop at those, because the more rules you add, the
less of the executor's attention each one gets.

Check: run the reconstruction test on each candidate generator — given
the fact and a concrete case, but not the rule, can the executor
rebuild the rule? To weigh the halves, compare the skill with the
generator alone against the skill with generator plus cases, on
skill-creator's harness.

## 6. Type every rule by its check

Every rule has a kind; match the check to the kind. An invariant holds
at every moment — inspect for it. An obligation falls due at a task
boundary — check it there. A preference admits degrees — watch it
across repeated runs. Place each rule beside its check. Fold
invariants and obligations into one NEVER list and you set up
misapplication: an executor doing schema design wades through rules
meant for query writing and applies one at the wrong moment.

Check: classify every MUST, NEVER, SHOULD, and bare imperative; flag
any bucket that mixes kinds; confirm each rule sits beside the check
matched to its kind.

## 7. Expect probability, and buy certainty with artifacts

A prose rule shifts the odds of a behavior; it cannot pin them,
because the executor generates its behavior rather than executing the
rule. Match wording strength to how much each rule matters. Where an
operation must not vary — an exact format, arithmetic, a mechanical
transform — ship a script and route the executor to it, because
executed code behaves the same on every run
([equipping agents](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)).
Anthropic calls the same dial "degrees of freedom": match specificity
to how much damage variation would cause
([best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)).

Check: measure a rule's real strength with repeated runs. A rule
backed by an executed artifact approaches determinism; any prose rule
sits below that.

## 8. Verify each claim in the mode its kind admits

Every claim written into a skill re-executes in every session that
loads it, so a wrong claim compounds at the rate of reuse. Before
encoding a claim, check it against the artifact: run the command, call
the API, read the schema. Give claims inherited from existing
documents the same check, because once a claim appears in a skill,
readers stop asking where it came from. A claim you cannot check yet
stays out of the skill; record it as an open question where a
maintainer reads — the design brief, the README, a scratchpad — so
verification gets scheduled instead of skipped.

Check: trace each claim in the skill to a source a reader could reach.
A bare magnitude with no reachable source fails.

## 9. Freeze deliberately

A skill helps because its author decided things once — scope, naming,
process shape — and every executor that loads it inherits those
decisions instead of re-making them. Ask what would keep a misfiring
skill misfiring: decisions nobody can see. The API changes, the team
renames things, the process shrinks — and the skill keeps replaying
the old decision. No executor questions it, because inside a session a
frozen decision just looks like how the skill works. The maintainer
could question it, but finds no record of which decisions the author
fixed, which they left open, or what a stale one looks like. So write
exactly that down where a maintainer reads, in a README or a design
brief: what the author fixed, what stays open to each session, and
what sign would show that a frozen decision needs revisiting. Never
write it inside the skill's own content — self-description there takes
up the executor's context and gives it nothing to do.

Check: by inspection — an artifact a maintainer reads holds the three
statements, or nothing does.

## 10. Make the skill observable

Build the checks before the skill, baseline the task without it, and
iterate on observed behavior rather than on intuition
([best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)).
Pair every expected effect with the check that would confirm or refute
it — without one, you cannot tell whether a change to the skill
helped. State the effect you expect before committing the change, so
the check tests a prediction made in advance rather than a description
written after. When an effect has no check yet, record the gap where a
maintainer reads — the README, a scratchpad — never in the skill's own
content, so the gap gets scheduled without costing the executor
anything. The harness — evals, trigger measurement, benchmarks — lives
with skill-creator; from this skill, you decide what deserves
measuring.

Check: every expected effect has a named check, or the maintainer
artifact records the gap.
