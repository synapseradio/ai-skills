# Skill Design

This document states a theory of skill design: what makes an Agent Skill generically useful across the widest space of contexts, from a domain reference to a metacognitive method. The principles come first; below them, the foundations hold the definitions and axioms behind each principle, with the evidence for each axiom cited where it stands. Where a claim can be measured, a prediction and its instrument sit beside the principle; where no instrument reaches the claim, the principle is a working guideline, checked by inspection and flagged as such in its section.

## The principles

### Schedule the workspace

A skill spends its executor's bounded workspace and earns its place by scheduling that spend. The runtime loads skills in three stages: name and description at startup (about 100 tokens), the body on activation (under 5,000 tokens recommended), reference files on demand ([Agent Skills specification](https://agentskills.io/specification)). Design against the stages — the description carries triggering alone, the body carries orchestration, references carry detail — and read cost then scales with the task rather than with the corpus.

Prediction: a skill that violates the stages raises tokens per task without raising its assertion pass rate. The standard harness captures both quantities ([evaluating skills](https://agentskills.io/skill-creation/evaluating-skills)).

### Route, don't hold

A skill differs from its content. It routes an executor over a source of truth. Give every fact one home and make every other occurrence a pointer, because two copies of a fact drift apart from the first unsynchronized update. When a pointer cannot do the work, move the affordance — the check, the script, the table — to the fact's home rather than copying the fact to the work. When the skill and the source it serves disagree, the source wins, and the skill directs its executor to surface the disagreement.

Both sides show up in practice. A domain skill that states one rule — say, that a write operation replaces every property rather than merging — in two separate passages will drift the moment one copy is updated and the other is not, while a skill that keeps its structure in a single manifest and derives the rest stays consistent by construction. Drift is measurable only where the duplicated fact has a machine-checkable form: a doctest fails when a shown output stops matching real behavior, and contract tests (Dredd, Schemathesis, Pact) fail when a spec and its implementation disagree. For the same fact restated in two prose passages, no pass/fail instrument exists — only static heuristics or advisory comparison — so this principle is checked by inspection.

### Make every delegated decision decidable

Every decision a skill hands its executor must be decidable from what the skill provides. Invocation decides from the description alone — the only text present at selection time. A process skill names each phase's object and exit condition; a reference skill names which page serves which task; both name where a red result re-enters the flow. Ambiguity anywhere signals that the way the skill shapes the expression space does not fit its intent, and decidability serves as the observable face of that fit.

Prediction: an undecidable description mis-triggers at a measurable rate (the description harness computes it: about 20 labeled prompts, three runs each, trigger rate against a 0.5 threshold — [optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)); an undecidable exit produces divergent executions across repeated runs, which the variance instrument captures. A description that fires on "any moment you are adding to a system you have not fully read," for instance, triggers on nearly every write action — an over-firing the trigger-rate instrument would expose.

### Declare the floor, and write to it

Every skill has a floor: the weakest executor in its declared deployment set, with the specification's `compatibility` field as the declaration surface. Correctness gets judged at the floor, and every abstract term costs grounding there — ground each term in referents the floor executor can act on, which means runnable code in a domain skill and worked moves in a method skill. The evidence for taking the floor seriously: the same instruction shifts weak executors far less than strong ones (constraint satisfaction of 47.0% on Qwen2-7B against 79.0% on Qwen2-72B — [SysBench](https://arxiv.org/abs/2408.10943)), and paraphrasing an instruction costs small models up to 61.8% of their compliance where the strongest model loses 18.3% ([IFEval++](https://arxiv.org/abs/2512.14754)). Weakest means least compliant on the task, not smallest: a larger model is not automatically a more compliant one, so identify the floor by measured compliance, not by parameter count.

Official guidance agrees in spirit — "What works perfectly for Opus might need more detail for Haiku. If you plan to use your Skill across multiple models, aim for instructions that work well with all of them" ([best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)) — while its conciseness baseline assumes a capable executor; declaring the deployment set reconciles the two. No turnkey instrument takes an arbitrary skill and reports its compliance across a capability range, but the measurement is established for fixed instruction sets — one benchmark sweeps a single instruction structure across twenty models and reports where compliance decays ([IFScale](https://arxiv.org/abs/2507.11538)) — and it can be assembled for a given skill from a multi-model harness plus a compliance rubric. Until that runs, floor correctness is checked by inspection.

### State the generator, and bound the enumeration

Where several rules share a cause, state the cause as a generator — a fact from which the rules can be reconstructed (see Definitions). The reconstruction test decides whether a sentence deserves the name: hand the executor the stated fact and a concrete case, but not the rule, and ask whether it can rebuild the rule. "Every value AGE returns is agtype" passes, because the casting rules follow from it. "Be careful with AGE syntax" fails: it compresses the rules but decides nothing. A generator pays twice: the maintainer edits one sentence when reality changes instead of chasing every consequence, and a capable executor extends it to cases the author never listed.

Then enumerate the load-bearing concrete cases anyway, because the floor may not derive. Overriding pretraining priors in favor of a stated fact emerges with scale ([Wei et al. 2023](https://arxiv.org/abs/2303.03846)), and deriving multi-step consequences from a stated principle emerges only around a hundred billion parameters ([Wei et al. 2022](https://arxiv.org/abs/2201.11903)) — a floor executor handed only the generator tends to pattern-match past it. Enumeration offers no refuge on its own: compliance degrades as enumerated constraints densify, with the best frontier models reaching 68% accuracy at 500 simultaneous instructions ([IFScale](https://arxiv.org/abs/2507.11538)), and even simple explicit rules break under pressure ([RuLES](https://arxiv.org/abs/2311.04235)). So bound the enumeration to the cases that carry the skill's weight — the concrete output specification does the load-bearing work in an instruction ([Yin et al. 2023](https://aclanthology.org/2023.acl-long.172/)).

Prediction: two formulations of the same skill — generator alone against generator plus bounded cases — differ measurably in assertion pass rate at the floor, and the harness comparing runs with and without the skill resolves the comparison.

### Type every rule by its check

A rule has a kind, and its kind names the check that verifies it. An invariant holds at every moment and gets checked by inspection, matching the class invariant of Design by Contract ([Meyer](https://en.wikipedia.org/wiki/Design_by_contract)) and the safety property of the formal literature ([Lamport 1977](https://lamport.azurewebsites.net/pubs/proving.pdf)). An obligation discharges at a task boundary and gets checked there, matching pre- and postconditions. A preference admits degrees (a SHOULD, in RFC terms) and gets checked as a distribution over runs, matching the soft constraint of the optimization literature. Place each rule beside its check. This typology deliberately covers hard and graded rules; obligations of the form "eventually" (liveness, in [Alpern and Schneider's](https://www.cs.cornell.edu/fbs/publications/RecSafeLive.pdf) exhaustive partition) admit no finite check and stay outside it, named here so the exclusion reads as a choice.

Prediction: a bucket that mixes kinds produces misapplication — an executor doing schema design wades through rules meant for query writing and applies one at the wrong moment. A single NEVER list that folds invariants together with task-boundary obligations invites this; separating the rules that constrain actions during the task from the rules that constrain the finished artifact prevents it.

### Expect probability, and buy certainty with artifacts

An in-skill rule shifts the probability of a behavior and never pins it. The best measured full-session compliance with system instructions reaches 54.4% ([SysBench](https://arxiv.org/abs/2408.10943)); moving the same content to the middle of a long context costs over 30% ([Liu et al. 2024](https://arxiv.org/abs/2307.03172)); performance drops an average of 39% in multi-turn conversation against single-turn ([Laban et al. 2025](https://arxiv.org/abs/2505.06120)). Write rules with this in view: calibrate wording strength to how much a rule matters, and where an operation must not vary, ship a script and route the executor to it, because executed code behaves deterministically where generated behavior does not ([equipping agents](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)). Official guidance operates this same dial as "degrees of freedom" — specificity matched to the task's fragility ([best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)); the mechanism underneath that dial is what this section describes.

Prediction: any prose rule complies below 1.0, measurable as run variance; a rule backed by an executed artifact approaches determinism. One caution applies to these predictions: part of published phrasing sensitivity traces to lenient or brittle scoring ([Hua et al.](https://arxiv.org/abs/2509.01790)), so they need robust scoring before they count as confirmed or refuted.

### Verify each claim in the mode its kind admits

Whatever a skill states re-executes in every session that loads it, so a wrong claim compounds at the rate of the skill's own reuse. That makes verification before encoding a consequence of the amplification axiom: check each empirical claim against the artifact it describes — the wiring, the script, the config — and give claims inherited from existing documents the same check, because encoding launders them. Craft claims admit no artifact; type them as preferences and assess them by their evaluation distributions. A claim with no check available yet is named as unverified, and the skill states what no check covers — voice, altitude, placement — routing that remainder to review so unverifiable work gets scheduled instead of dropped.

A skill that anchors a performance claim to a resolvable issue number can be rechecked when the facts change; a skill that states a bare magnitude with no source a reader could reach cannot, and the unsourced number rots silently as reality moves on.

### Freeze deliberately

Every skill freezes decisions about what it serves — scope, naming, placement, process shape — and replays them in every session that loads it. Freezing does the work and carries the risk, so make it explicit: state what the skill fixes, what it leaves to the session, and which frozen decision to revisit when the skill misfires. This principle rests on reasoning from the amplification axiom (A4), with no measurement behind it yet; it is a working guideline, not a tested claim.

### Make the skill observable

Evaluations serve as the source of truth ([best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)): build them before the skill, baseline the task without it, then iterate on observed behavior rather than on intuition. Observability is a property the author designs in — every rule is typed by the check that verifies it, every fact keeps a single home, every empirical claim resolves to a source, and every prediction is paired with the instrument that would confirm or refute it, or the gap is admitted. A skill whose effect cannot be measured cannot be improved; where a claim outruns every available instrument, say so and route the remainder to review, so unobservable work gets scheduled instead of assumed.

## Foundations

### Definitions

A **skill** instructs an agent — it loads into a working session and directs what the agent reads, in what order, and how the work closes — in order to shape the session's workspace: what becomes expressible and routable in the context. The workspace lives in the session, so executors that lack internal workspace machinery still run skills; for the weakest of them, the context window supplies the only workspace there is.

A **source of truth** holds the knowledge a skill routes over. The skill and its source stay distinct entities, whatever container the source lives in — the skill's own reference files, a codebase, a documentation corpus.

An **executor** runs the session: a model plus its harness, stochastic in behavior, varying in capability across deployments. The **floor** names the weakest executor in the skill's declared deployment set.

An **intent**, or context of utility, names the region of task space where invoking the skill helps.

An **expression space** is the set of outputs an executor could produce in a session — a property of the executor, not the skill. A skill does not add to or remove from this set; it shifts the probability distribution over it (A1). That shift arrives in stages, tracking how the runtime loads the skill. While only the name and description sit in context, the skill shifts one narrow region of the distribution — the chance the executor invokes it — and conditions the rest only incidentally. On invocation the body enters context and shifts the distribution over the task's outputs directly; references shift it further as they load. Presence and invocation are therefore not two spaces but two interventions on one, and the presence intervention matters mostly through whether it leads to invocation.

A **generator**, relative to a set of rules, names a stated fact with three properties held jointly: each rule in the set follows from the fact plus ordinary background knowledge; a case outside the set can be decided from the fact alone; and one edit to the fact updates or invalidates every consequence together. The reconstruction test checks the name: an executor handed the fact and a concrete case, but not the rule, can rebuild the rule. A sentence that compresses rules without deciding new cases merely summarizes. The same relation, one level up, connects the axioms below to the principles above.

### Axioms

Each axiom below is given with its evidence and the principles it generates. Where a principle cannot be derived cleanly, the gap is stated in its section rather than hidden.

**A1 — the executor responds stochastically.** An instruction intervenes on a distribution over behaviors. Evidence: the compliance, paraphrase, and position measurements cited under "Expect probability" and "Declare the floor". Generates: type every rule by its check (the preference kind), expect probability, verify each claim, make the skill observable.

**A2 — the workspace has bounds.** Everything that loads competes for finite context, and position within it carries weight. Evidence: the staged loading described under "Schedule the workspace" exists precisely to ration this budget, and the position sensitivity cited under "Expect probability" shows the budget has geometry as well as size. Generates: schedule the workspace.

**A3 — capability varies, and the floor bites.** The same instruction moves different executors by different amounts, and abilities like overriding priors and deriving from stated rules emerge with scale, per the evidence cited under "Declare the floor" and "State the generator". Generates: declare the floor; state the generator, bound the enumeration.

**A4 — encoding amplifies.** An encoded instruction re-executes across every session that loads it, compounding truth and error alike. Official sources state the reuse premise and stay silent on the compounding of error ([equipping agents](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)); the corollary follows from reuse directly. Generates: verify each claim, freeze deliberately.

**A5 — copies drift.** Two homes for one fact diverge from the first unsynchronized update. Evidence: the duplications and the conforming architecture cited under "Route, don't hold". Generates: route, don't hold.

**A6 — alignment shows up as decidability.** When a skill shapes the expression space to fit its intent, decisions fall out unambiguously; ambiguity anywhere evidences misfit. Alignment stays latent; decidability is its measurable face, and the trigger-rate instrument measures that face at selection time. Generates: make every delegated decision decidable.

### Instruments

The testable core consists of the predictions above that an existing instrument can measure.

| Instrument | Measures | Source |
|---|---|---|
| Trigger rate over labeled queries | Invocation decidability of a description | [optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) |
| Assertion pass rate, with and without the skill | Task completion attributable to the skill | [evaluating skills](https://agentskills.io/skill-creation/evaluating-skills) |
| Run variance (mean and standard deviation over repeats) | Probabilistic strength of a rule; exit decidability | skill-creator harness |
| Iteration regression (re-run per edit, diff against prior) | Effect of a change across reuse | skill-creator harness |
| Tokens and duration per run | Workspace spend per task | [evaluating skills](https://agentskills.io/skill-creation/evaluating-skills) |
