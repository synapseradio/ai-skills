# Definitions and Evidence

This file holds the shared vocabulary and the evidence behind the practices
in [principles.md](./principles.md). Section names quoted below ("Expect
probability", "Declare the floor", and kin) refer to the principles in that
file.

## Definitions

A **skill** instructs an agent — it loads into a working session and directs
what the agent reads, in what order, and how the work closes — in order to
shape the session's workspace: what becomes expressible and routable in the
context. The workspace lives in the session, so executors that lack internal
workspace machinery still run skills; for the weakest of them, the context
window supplies the only workspace there is.

A **source of truth** holds the knowledge a skill routes over. The skill and
its source stay distinct entities, whatever container the source lives in —
the skill's own reference files, a codebase, a documentation corpus.

An **executor** runs the session: a model plus its harness, stochastic in
behavior, varying in capability across deployments. The **floor** names the
weakest executor in the skill's declared deployment set.

An **intent**, or context of utility, names the region of task space where
invoking the skill helps.

An **expression space** is the set of outputs an executor could produce in a
session — a property of the executor, not the skill. A skill does not add to
or remove from this set; it shifts the probability distribution over it (see
"What the evidence shows"). That shift arrives in stages, tracking how the
runtime loads the skill. While only the name and description sit in context,
the skill shifts one narrow region of the distribution — the chance the
executor invokes it — and conditions the rest only incidentally. On
invocation the body enters context and shifts the distribution over the
task's outputs directly; references shift it further as they load. Presence
and invocation are therefore not two spaces but two interventions on one,
and the presence intervention matters mostly through whether it leads to
invocation.

A **generator**, relative to a set of rules, names a stated fact with three
properties held jointly: each rule in the set follows from the fact plus
ordinary background knowledge; a case outside the set can be decided from the
fact alone; and one edit to the fact updates or invalidates every consequence
together. The reconstruction test checks the name: an executor handed the
fact and a concrete case, but not the rule, can rebuild the rule. A sentence
that compresses rules without deciding new cases merely summarizes. The same
relation, one level up, connects the evidence below to the principles.

## What the evidence shows

Each fact below carries its evidence and names the principles that stand on
it. Where a principle cannot be traced cleanly to this evidence, the gap is
stated in its own section rather than hidden.

**Executors respond stochastically.** An instruction intervenes on a
distribution over behaviors. Evidence: the compliance, paraphrase, and
position measurements cited under "Expect probability" and "Declare the
floor". Generates: type every rule by its check (the preference kind), expect
probability, verify each claim, make the skill observable.

**The workspace has bounds.** Everything that loads competes for finite
context, and position within it carries weight. Evidence: the staged loading
described under "Schedule the workspace" exists precisely to ration this
budget, and the position sensitivity cited under "Expect probability" shows
the budget has geometry as well as size. Generates: schedule the workspace.

**Capability varies, and the floor caps compliance.** The same instruction
moves different executors by different amounts, and abilities like overriding
priors and deriving from stated rules emerge with scale, per the evidence
cited under "Declare the floor" and "State the generator". Generates: declare
the floor; state the generator, bound the enumeration.

**Encoding amplifies.** An encoded instruction re-executes across every
session that loads it, compounding truth and error alike. Official sources
state the reuse premise and stay silent on the compounding of error
([equipping agents](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills));
the corollary follows from reuse directly. Generates: verify each claim,
freeze deliberately.

**Copies drift.** Two homes for one fact diverge from the first
unsynchronized update. Evidence: the duplications and the conforming
architecture cited under "Route, don't hold". Generates: route, don't hold.

**Alignment shows up as decidability.** When a skill shapes the expression
space to fit its intent, decisions fall out unambiguously; ambiguity anywhere
evidences misfit. Alignment stays latent; decidability operationalizes it —
turns a fit no check reaches directly into a gauge a check can read — and the
trigger-rate check reads that gauge at selection time. Like any proxy, the
gauge can be gamed; the rule against flattening under "Make every delegated
decision decidable" covers this. Generates: make every delegated decision
decidable.

## Checks you can run today

Each check below exists as a working tool, with its source. Together they
carry every "Check:" line in [principles.md](./principles.md) that names a
measurement.

| Check | Measures | Source |
|---|---|---|
| Trigger rate over labeled queries | Invocation decidability of a description | [optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) |
| Assertion pass rate, with and without the skill | Task completion attributable to the skill | [evaluating skills](https://agentskills.io/skill-creation/evaluating-skills) |
| Run variance (mean and standard deviation over repeats) | Probabilistic strength of a rule; exit decidability | skill-creator harness |
| Iteration regression (re-run per edit, diff against prior) | Effect of a change across reuse | skill-creator harness |
| Tokens and duration per run | Workspace spend per task | [evaluating skills](https://agentskills.io/skill-creation/evaluating-skills) |
