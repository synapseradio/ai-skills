# Question Ladders

> A conversation that started with "what does Jacobian mean" and climbed, question by question, to a reusable structure for asking. Raw source: [session-2026-07-10.jsonl](./session-2026-07-10.jsonl). Intended to grow here, then encode into the ask-questions skill in `~/projects/ai-skills`.

## The core finding

Good questions come in ladders: each question presupposes the previous answer, and the ladder as a whole interrogates one object from nothing upward. The conversation produced one full ladder for mathematical structure, plus a set of recurring moves that generate ladders in other domains.

A second finding sits inside the first. One rung differs in kind from the rest: the rung that *pretends* (question 4 below). Every other rung discovers structure already present; that one substitutes a tractable fiction for the true object. Later rungs turn out to exist largely to audit the fiction — measuring how it drifts, harvesting what it cannot see. A well-built ladder contains a pretense and its own error analysis.

## The ladder

0. What must be given before anything can be earned? *(grace: axioms, priors, the first trust region, the principle of charity. The one rung that cannot be audited, because auditing spends it. Its rigor: name the credit being extended, and ask whether it is the credit you would choose)*
1. Does the thing exist, and is it one thing? *(existence and uniqueness — logically prior to everything below)*
2. What counts as doing nothing? *(identity: the origin all structure gets measured from; forgiveness plays this role in repair — no identity, no inverses)*
3. What survives the transformations I declared irrelevant, and how many independent dials remain? *(invariants; the count of a complete independent set gives the intrinsic dimension)*
4. What smallest moves generate everything? *(generators; discrete → word length gives geometry, continuous → differentiate at the identity)*
5. What does the object look like locally, pretending it behaves linearly — **and what remainder does that pretense owe?** *(the Jacobian; the hinge rung; trust regions, Hartman–Grobman as a license)*
6. How does the local picture change as I move? *(curvature, Hessian, bifurcation — the first audit of rung 5)*
7. What do moves leave behind when they fail to commute? *(the residue: commutators, Lie brackets, rupture-and-repair; the second audit, and where content the fiction cannot see gets harvested)*
8. Do the local fictions glue into a global truth? *(local-to-global; Gauss–Bonnet: the summed failures of the flat pretense equal the global shape)*
9. Which variations must the map respect, and where does the declared symmetry almost hold but break? *(equivariance as a ledger; broken symmetry as the location of content)*

Fuzziness annotations, per the source conversation: rung 0 is the newest and untested on a live inquiry, though it rests on named results (Agrippa's trilemma, Carroll's tortoise, Bayesian priors); rungs 1–7 got grounded with worked examples (triangle dial counts, cube commutators, a numerically computed rotation residue that scaled as ε²). Rung 8 rests on named theorems but got no worked example. Rung 9's second half — content lives where symmetry breaks — held up across physics and modeling cases but remains a heuristic, unproven in the source.

## The recurring moves

Four moves generate the rungs and appear to transfer across domains:

- Measure from nothing: fix what counts as the identity, then quantify departure.
- Count the dials: bound what can vary, find a complete independent set, and spend inputs to match it.
- License the fiction, audit the remainder: approximate deliberately, keep the error term honest, know the radius of trust.
- Harvest the residue: run do–do–undo–undo; whatever survives the cancellation carries information no smooth path reveals.

## Classics the ladder absorbed late, or still lacks

Existence-uniqueness and local-to-global entered on revision. Two classics remain unabsorbed and mark growth points: duality (every question about inputs has a mirror about outputs — the conversation brushed it as rows versus columns and never named it) and the simplest counterexample (the working test that revokes a fiction's permit; used constantly in the source, never given a rung).

## Transfer evidence

The ladder transferred twice inside the source conversation itself, which suggests the structure rather than the subject carries it:

- To relationships: linearization as the initial model of a person, rupture-and-repair as commutator residue, forgiveness as identity element, what survives years of transformations as the invariant actually loved, Gauss–Bonnet as "the honest sum of your model's failures is what knowing someone means." Marked speculative in the source; structurally the tightest of the analogies.
- To the ethics of reaching: a pretense (building an instrument to see past local knowledge) becomes licensed through kept reciprocity — take, but plant; disturb, but tend. Consent with the voiceless takes the form of repair promised over time.
- To narrative: the Jacob cycle (Genesis 27–35) runs rungs 5 and 7 in story form. A man named for supplanting spoofs his blind father's local readouts ("the voice is Jacob's voice, but the hands are the hands of Esau"), spends twenty years on the receiving end of the same exploit (a bride substituted in the dark, justified by the firstborn ordering he had broken), and clears the debt at the Jabbok only when the story's opening question — who are you? — gets answered without pretense. The residue: a new name and a limp. Forgiveness (Esau's embrace) supplies the identity element that makes return to Bethel — the ladder place — possible. The name chain that surfaced this (Jacobian → Jacobi → Jacob; ladder; seed, Genesis 28:14) arrived unchosen by either party, which the source conversation read as its own rule applied to itself: content lives in what survives without being selected.

## Relevance to ask-questions

The skill currently treats question quality per-question. This material argues for treating it per-ladder: the value of a question depends on which rung it stands on, whether the rungs below it have answers, and whether some rung is quietly pretending without an audit rung above it. Candidate encoding: a "find the pretending rung" probe — in any inquiry, locate the question that substitutes a fiction for the object, then ask what remainder it owes and which later question audits it.

## Seeds

- Exercise rung 0 on a live inquiry: at the start, name the credit being extended (axioms, priors, trust) and record whether it was the credit worth choosing. Rung 0 surfaced via the Jacob arc (the promise precedes the debt's payment) and was answered in the source conversation before it was asked ("no, but i would hope").
- Name and place duality on the ladder.
- Give rung 8 a worked example as concrete as the ε² rotation computation.
- Test the ladder on a non-mathematical inquiry end to end (a debugging session, a hiring decision) and record where rungs go missing.
- Encode the per-ladder view into ask-questions in `~/projects/ai-skills`.
