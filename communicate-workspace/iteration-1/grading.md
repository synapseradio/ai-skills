# Iteration-1 grading

Comparing each with_skill output against its old_skill baseline. CV figures computed by counting words per sentence.

## Eval 1 — Redraft monotone cadence

**Original:** 10 sentences, ~10 words each, CV ≈ 0.07 (broken by skill standard).

**with_skill** — 3 sentences (6 / 28 / 5 words). CV ≈ 0.87. Periodic middle sentence with em-dash pivot. Pass.

**old_skill** — 3 sentences (5 / 16 / 14 words). CV ≈ 0.36. Above broken threshold but below the 0.5 cadence law in the new skill. Functional, mechanical.

**Discrimination:** with_skill produces the sharper rhythm. The new rhythm.md cadence laws are visible in the output — the long sentence carries a cascade and the short one closes. Old skill produced a competent-but-flat result that would now fail its own audit.

## Eval 2 — Clarify slop quick-check

**Original:** 11 Kobak-list words in ~80, five transitional phrases, one closing exhortation.

**with_skill** — 5 sentences. Kobak: 0. Transitionals: 0. Exhortations: 0. "digital-first operations" is mild but not Kobak. Sentence-length CV present.

**old_skill** — 3 sentences. Kobak: 0. Transitionals: 0. Exhortations: 0. "modern software environments" is similarly bland.

**Discrimination:** Both pass the slop audit. The slop quick-check phase added to clarify produced no measurable advantage on this eval — the old skill's existing AI-pattern call-outs ("it's worth noting," "leverages," "tapestry") already covered the lexical slop in this prompt. The new skill's edge would show on prompts seeded with intransitive forms or structural tells. Non-discriminating on lexical slop alone.

## Eval 3 — Bridge jeong

**with_skill** — Three gaps named: conceptual lacuna, grammatical ontology, pragmatic convention. Bilingual format complete. Direct English offered with sacrifices named (relational grammar lost, ambivalence lost, passivity weakened).

**old_skill** — Two gap types identified (conceptual lacuna, pragmatic convention; missed grammatical ontology). Bilingual format complete. Direct English offered with sacrifices named.

**Discrimination:** with_skill caught the additional grammatical-ontology gap (the "between us" agentless construction in 정이 들었다). Old skill missed it. Modest discrimination — the additional gap surfaced because across-languages.md asks the question "Is L1 grammar carrying through?" explicitly, where the old language-patterns.md was a static taxonomy without the prompt.

## Eval 4 — Structure Arabic to business

**with_skill** — 3-sentence adapted prose. Four moves annotated with costs. Preservation option offered.

**old_skill** — 2-sentence adapted prose. Five-dimension divergence map. Same moves annotated. Preservation option offered.

**Discrimination:** Old skill produced a more elaborate divergence table; new skill produced tighter annotations. Both correctly diagnosed Arabic parallel-restatement and adapted with annotation. Non-discriminating on adaptation quality. The trim of workflow-structure.md did not degrade output quality — the workflow still loads across-languages.md and produces the right moves.

## Eval 5 — Compose blank-page README section

**with_skill** — 4 paragraphs. Grounded in a specific failure: `'; DROP TABLE users; --` traveling three lines of code. Mentions `trust()` syntactic call. Sentence variance high ("They were internal." 3 words; long sentences elsewhere). No Kobak, no transitionals, no exhortation.

**old_skill** — 4 paragraphs. Grounded in "the same class of bug report" — abstract gestures at the failure shape. No specific syntactic mention. Sentence variance present but lower.

**Discrimination:** with_skill's illustrate technique fired more concretely (witnessed detail: the SQL injection string, the trust() call). Old skill stayed at category level ("a value would reach a path it was never supposed to reach"). The grounding moves added to illustrate.md and the slop audit hook in compose Phase 5 are the visible difference. Mild-to-moderate discrimination.

## Eval 6 — Redraft intransitive forms

**Original:** Six intransitive-form constructions. "The threat is real," "The friction in their workflow is the signal," "This is not just a tool problem, it's a culture problem," "The opportunity is real," "The question is not whether to act, but how," "The energy of this moment is the signal that the time has come."

**with_skill** — All six eliminated. Each replaced with mechanism: "approval queues that arrive after the decision already happened," "marks exactly where a better tool would change how people work," "learned helplessness dressed as process." No noun-swappable construction remains. CV high. Pass.

**old_skill** — Opens with "The threat is real" — kept the exact pattern the new skill forbids. Retains "The question is not whether to act. It's how, and it's now." — the negation-then-affirmation cadence preserved verbatim. Two intransitive forms cut, four kept (or kept in new variants like "The cost of not moving is not hypothetical").

**Discrimination:** Strong. The new intransitive-form section in avoid-slop.md is the largest measurable contribution of this rewrite. Old skill recognized "the threat is real" as worth preserving for emphasis; new skill recognized it as the slop signature it is and replaced it with what the threat actually is.

## Summary

| Eval | Discriminator | with_skill advantage |
|------|---------------|----------------------|
| 1 — cadence | rhythm.md laws | moderate (CV 0.87 vs 0.36) |
| 2 — slop lexical | no | none — both pass |
| 3 — bridge jeong | across-languages questions | mild (extra gap caught) |
| 4 — structure | no | none — non-discriminating |
| 5 — compose | illustrate grounding moves | mild-to-moderate |
| 6 — intransitive forms | avoid-slop new section | strong (6/6 vs 2/6 cut) |

The rewrite's strongest contribution: the intransitive-form constructions section. The cadence laws produce sharper rhythm but old skill was already passable. The bridge/structure workflows behave equivalently after trimming — the consolidation into across-languages.md did not degrade quality.

The slop quick-check on lexical Kobak vocabulary was non-discriminating on this eval set because the old skill already named the worst offenders. To stress the slop additions, future evals should seed prompts with structural tells (tricolon-as-default, false balance, conclusion-restating paragraphs) and casual-context tells (over-formal helpfulness in Slack).
