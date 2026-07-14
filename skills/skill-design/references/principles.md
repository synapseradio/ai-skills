# The Principles

This file holds the canonical statements of the skill-design principles: what
makes an Agent Skill genuinely useful across the widest space of contexts,
from a domain reference to a metacognitive method. Each principle states a
practice, the reason it holds, and the way to check it. The shared vocabulary
and the measured evidence behind each practice live in
[evidence.md](./evidence.md), cited where they stand. Each principle closes
with a Check line naming how to verify it — a measurement where one exists,
inspection where none reaches the claim yet. A principle checked only by
inspection stands as a working guideline, and its Check line says so.

## Schedule the workspace

A skill spends its executor's bounded workspace and earns its place by
scheduling that spend. The runtime loads skills in three stages: name and
description at startup (about 100 tokens), the body on activation (under
5,000 tokens recommended), reference files on demand ([Agent Skills
specification](https://agentskills.io/specification)). Design against the
stages — the description carries the sole information the executor has
available when deciding whether to use the skill, the body carries
orchestration, references carry detail — and read cost then scales with the
task rather than with the corpus.

Check: the standard harness captures tokens per task and assertion pass rate
together ([evaluating skills](https://agentskills.io/skill-creation/evaluating-skills));
a skill that violates the stages raises the first without raising the second.

## Route, don't hold

A skill differs from its content. It routes an executor over a source of
truth. Give every fact one home and make every other occurrence a pointer,
because two copies of a fact drift apart from the first unsynchronized
update. When a pointer cannot do the work, move the affordance — the check,
the script, the table — to the fact's home rather than copying the fact to
the work. When the skill and the source it serves disagree, the source wins,
and the skill directs its executor to surface the disagreement.

Both sides show up in practice. A domain skill that states one rule — say,
that a write operation replaces every property rather than merging — in two
separate passages will drift the moment one copy is updated and the other is
not, while a skill that keeps its structure in a single manifest and derives
the rest stays consistent by construction.

Check: by inspection for prose — no pass/fail check exists for the same fact
restated in two passages, only static heuristics or advisory comparison.
Where the duplicated fact has a machine-checkable form, that form makes
drift measurable: a doctest fails when a shown output stops matching real
behavior, and contract tests (Dredd, Schemathesis, Pact) fail when a spec
and its implementation disagree.

## Make every delegated decision decidable

Every decision a skill hands its executor must be decidable from what the
skill provides. Invocation decides from the description alone — the only text
present at selection time. A process skill names each phase's object and exit
condition; a reference skill names which page serves which task; both name
where a red result re-enters the flow. Ambiguity anywhere signals that the
way the skill shapes the expression space does not fit its intent, and
decidability serves as the observable face of that fit.

Decidability can rise two ways, and only one counts. Clarity raises it
through the fit itself: surface the decision factors and sharpen the stated
intent, and decisions fall out because the fit improved. Flattening raises it
without touching the fit: "always do X" decides everything and fits almost
nothing ([Goodhart's law](https://en.wikipedia.org/wiki/Goodhart%27s_law)).
Buy decidability with clarity, never with flattened decisions.

Check: the description harness measures mis-triggering directly — about 20
labeled prompts, three runs each, trigger rate against a 0.5 threshold
([optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions))
— and an undecidable exit shows up as divergent executions across repeated
runs, which run variance captures. A description that fires on "any moment
you are adding to a system you have not fully read," for instance, triggers
on nearly every write action — an over-firing the trigger-rate check would
expose. Running trigger rate beside assertion pass rate tells a clarity gain
from a flattened one: clarity moves the first without costing the second,
where flattening buys the first at the second's expense.

## Declare the floor, and write to it

Every skill has a floor: the weakest executor in its declared deployment set,
with the specification's `compatibility` field as the declaration surface.
Correctness gets judged at the floor, and every abstract term costs grounding
there — ground each term in referents the floor executor can act on, which
means runnable code in a domain skill and worked moves in a method skill. The
evidence for taking the floor seriously: the same instruction shifts weak
executors far less than strong ones (constraint satisfaction of 47.0% on
Qwen2-7B against 79.0% on Qwen2-72B — [SysBench](https://arxiv.org/abs/2408.10943)),
and paraphrasing an instruction costs small models up to 61.8% of their
compliance where the strongest model loses 18.3%
([IFEval++](https://arxiv.org/abs/2512.14754)). Weakest means least compliant
on the task, not smallest: a larger model is not automatically a more
compliant one, so identify the floor by measured compliance, not by parameter
count.

Official guidance agrees in spirit — "What works perfectly for Opus might
need more detail for Haiku. If you plan to use your Skill across multiple
models, aim for instructions that work well with all of them"
([best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices))
— while its conciseness baseline assumes a capable executor; declaring the
deployment set reconciles the two.

Check: by inspection, until a harness runs. No turnkey check takes an
arbitrary skill and reports its compliance across a capability range, but
the measurement is established for fixed instruction sets — one benchmark
sweeps a single instruction structure across twenty models and reports where
compliance decays ([IFScale](https://arxiv.org/abs/2507.11538)) — and it can
be assembled for a given skill from a multi-model harness plus a compliance
rubric.

## State the generator, and bound the enumeration

Where several rules share a cause, state the cause as a generator — a fact
from which the rules can be reconstructed (see Definitions in
[evidence.md](./evidence.md)). The reconstruction test decides whether a
sentence deserves the name: hand the executor the stated fact and a concrete
case, but not the rule, and ask whether it can rebuild the rule. "Every value
AGE returns is agtype" passes, because the casting rules follow from it. "Be
careful with AGE syntax" fails: it compresses the rules but decides nothing.
A generator pays twice: the maintainer edits one sentence when reality
changes instead of chasing every consequence, and a capable executor extends
it to cases the author never listed.

Then enumerate the load-bearing concrete cases anyway, because the floor may
not derive. Overriding pretraining priors in favor of a stated fact emerges
with scale ([Wei et al. 2023](https://arxiv.org/abs/2303.03846)), and
deriving multi-step consequences from a stated principle emerges only around
a hundred billion parameters ([Wei et al. 2022](https://arxiv.org/abs/2201.11903))
— a floor executor handed only the generator tends to pattern-match past it.
Enumeration offers no refuge on its own: compliance degrades as enumerated
constraints densify, with the best frontier models reaching 68% accuracy at
500 simultaneous instructions ([IFScale](https://arxiv.org/abs/2507.11538)),
and even simple explicit rules break under pressure
([RuLES](https://arxiv.org/abs/2311.04235)). So bound the enumeration to the
cases that carry the skill's weight — the concrete output specification does
the load-bearing work in an instruction
([Yin et al. 2023](https://aclanthology.org/2023.acl-long.172/)).

Check: compare two formulations of the same skill — generator alone against
generator plus bounded cases — on assertion pass rate at the floor; the
harness that compares runs with and without a skill resolves the comparison.

## Type every rule by its check

A rule has a kind, and its kind names the check that verifies it. An
invariant holds at every moment and gets checked by inspection, matching the
class invariant of Design by Contract
([Meyer](https://en.wikipedia.org/wiki/Design_by_contract)) and the safety
property of the formal literature
([Lamport 1977](https://lamport.azurewebsites.net/pubs/proving.pdf)). An
obligation discharges at a task boundary and gets checked there, matching
pre- and postconditions. A preference admits degrees (a SHOULD, in RFC terms)
and gets checked as a distribution over runs, matching the soft constraint of
the optimization literature. Place each rule beside its check. This typology
deliberately covers hard and graded rules; obligations of the form
"eventually" (liveness, in [Alpern and Schneider's](https://www.cs.cornell.edu/fbs/publications/RecSafeLive.pdf)
exhaustive partition) admit no finite check and stay outside it, named here
so the exclusion reads as a choice.

Mixing kinds in one bucket produces misapplication: an executor doing schema
design wades through rules meant for query writing and applies one at the
wrong moment. A single NEVER list that folds invariants together with
task-boundary obligations invites this; separating the rules that constrain
actions during the task from the rules that constrain the finished artifact
prevents it.

Check: by inspection — classify every rule (the MUSTs, NEVERs, SHOULDs, and
bare imperatives), flag any bucket that mixes kinds, and confirm each rule
sits beside the check its kind names.

## Expect probability, and buy certainty with artifacts

An in-skill rule shifts the probability of a behavior and never pins it. The
best measured full-session compliance with system instructions reaches 54.4%
([SysBench](https://arxiv.org/abs/2408.10943)); moving the same content to
the middle of a long context costs over 30%
([Liu et al. 2024](https://arxiv.org/abs/2307.03172)); performance drops an
average of 39% in multi-turn conversation against single-turn
([Laban et al. 2025](https://arxiv.org/abs/2505.06120)). Write rules with
this in view: calibrate wording strength to how much a rule matters, and
where an operation must not vary, ship a script and route the executor to it,
because executed code behaves deterministically where generated behavior does
not ([equipping agents](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)).
Official guidance operates this same dial as "degrees of freedom" —
specificity matched to the task's fragility
([best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices));
the mechanism underneath that dial is what this section describes.

Check: run variance measures a rule's actual strength — any prose rule
complies below 1.0, while a rule backed by an executed artifact approaches
determinism. One caution before treating such measurements as settled: part
of published phrasing sensitivity traces to lenient or brittle scoring
([Hua et al.](https://arxiv.org/abs/2509.01790)), so they need reliable
scoring before they count as confirmed or refuted.

## Verify each claim in the mode its kind admits

Whatever a skill states re-executes in every session that loads it, so a
wrong claim compounds at the rate of the skill's own reuse. That makes
verification before encoding a consequence of reuse itself: check each
empirical claim against the artifact it describes — the wiring, the script,
the config — and give claims inherited from existing documents the same
check, because encoding launders them. Craft claims admit no artifact; type
them as preferences and assess them by their evaluation distributions. A
claim with no check available yet is named as unverified, and the skill
states what no check covers — voice, altitude, placement — routing that
remainder to review so unverifiable work gets scheduled instead of dropped.

A skill that anchors a performance claim to a resolvable issue number can be
rechecked when the facts change; a skill that states a bare magnitude with no
source a reader could reach cannot, and the unsourced number rots silently as
reality moves on.

Check: by inspection — trace each empirical claim to a source a reader could
reach, or to an explicit unverified mark; a bare magnitude with neither
fails.

## Freeze deliberately

Every skill freezes decisions about what it serves — scope, naming,
placement, process shape — and replays them in every session that loads it.
Freezing does the work and carries the risk, so make it explicit: state what
the skill fixes, what it leaves to the session, and which frozen decision to
revisit when the skill misfires. Make that declaration where a maintainer
reads — a README, a design brief — never as self-description in the skill
body, which spends the executor's workspace without directing its action.

Check: by inspection only — a maintainer-facing artifact carries the three
statements, or nothing does. This principle rests on reasoning from
amplification alone (see "Encoding amplifies" in
[evidence.md](./evidence.md)), with no measurement behind it yet; treat it as
a working guideline, not a tested claim.

## Make the skill observable

Evaluations serve as the source of truth
([best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)):
build them before the skill, baseline the task without it, then iterate on
observed behavior rather than on intuition. Observability is a property the
author designs in — every rule is typed by the check that verifies it, every
fact keeps a single home, every empirical claim resolves to a source, and
every expected effect is paired with the check that would confirm or refute
it, or the gap is admitted. A skill whose effect cannot be measured cannot be
improved; where a claim outruns every available check, say so and route the
remainder to review, so unobservable work gets scheduled instead of assumed.

Check: by inspection — evals exist and each expected effect pairs with a
check, or the skill names which checks apply and what stays unmeasurable.
