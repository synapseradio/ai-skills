# Grounding Principles for Expression Skills

Synthesized from a 3-round discussion among skill-analyst, culture-researcher, and writing-scholar.
All principles are grounded in cross-tradition research: Arabic, French, Japanese, Latin American, African,
and Anglo-American writing traditions, with evidence from writers (Achebe, Adichie, Bolano, Ernaux,
Luiselli, Mahfouz, Murakami, Ngugi, Ogawa, Poniatowska, Saunders, al-Shaykh, Yourcenar) and
cross-cultural linguistics research (Boroditsky, Garcia & Li Wei, Hall, Hofstede, Kaplan, Saigo).

---

## Consensus

**Technique library: 17 → 21, with tradition as lens.**
Three agents agreed on three new techniques (omit, position, tradition) and a fourth (ground/situate).
Established which 7 survive unchanged, which 6 need diagnostic revision, and which 4 need structural
revision. `technique-tradition` operates as a lens/modifier that changes how all other diagnostics fire,
not as a standalone Connection technique.

**Shared references at plugin root.**
All technique files move to `plugins/expression/references/` — shared infrastructure for all skills.

**Composition is a distinct activity from editing.**
`/writing` fills a structural gap: the current plugin is entirely reactive (improve existing prose).
`/writing` is generative (create prose from intent). The workflow must be recursive, not linear —
Draft → discover → loop back to Frame — because drafting often reveals the real argument.

**"Why must this be written?" precedes all other questions.**
This is the first diagnostic question in any writing workflow, not just `/writing`. Purpose grounded
in necessity is the generative force that shapes all subsequent decisions.

**Help-me-say = ontology bridging, not lightweight composition.**
A point-of-need tool for articulating a thought that resists expression because the idea lives in a
different conceptual framework than the target language. Pairs with `/writing` (structural decisions),
`help-me-say` (L1 concept bridging mid-draft), and `proofread`/`refine` (cross-culturally-aware editing).

**The hedging split is non-negotiable.**
Hedging-as-cushioning (universally low-value) vs. hedging-as-calibration (legitimately cross-cultural)
must be distinguished in every skill that touches `strengthen` or `signal-confidence`.

## Disagreements (Unresolved for Ideation)

**How heavy is `tradition` as a lens?**
Skill-analyst favors ambient context (identify tradition once at session start, carry as lightweight
orientation). Culture-researcher favors explicit modification rules for each downstream diagnostic.
Resolution needed: does tradition load once per session or per-technique?

**`ground`/`situate` vs. expanded `illustrate`.**
Distinction: `illustrate` grounds claims in examples (about content); `situate` grounds voice in lived
experience (about speaker). The boundary with `position` also needs to be sharp — "who speaks from where"
(position) vs. "has the speaker actually been here" (situate).

**Skill count.**
`/feedback` and `/tone-match` from the skill-analyst's initial 7 candidates were not pressure-tested
in this discussion. Both may reduce to modes within `/expression` library and `/refine` respectively.

**Writing-as-resistance propagation beyond `/writing`.**
When `/proofread` encounters prose that deliberately breaks clarity rules for political or cultural
reasons, it must recognize that resistance, not correct it. How this propagates to skills without
a Frame phase needs resolution — the group's candidate: `technique-tradition` as lens provides it.

## Key Evidence

From the skill-analyst: Only the Clarity category has a true dependency chain (structural → voice →
language). The other 4 technique categories are reach-for-as-needed libraries. This means the new
skill structure should have few workflow skills (proofread, refine, writing) and let the remaining
17+ techniques live as a browsable library.

From the culture-researcher: Every current diagnostic question encodes Anglo-American rhetorical
preference as cognitive law. Specific examples: "Can a reader follow linearly?" fails for Arabic
parallel-restatement and French dialectical structure. "Does language commit or cushion?" fails for
Japanese kana (epistemic sophistication) and Spanish estar (emotion precision). Japanese passive,
Arabic agentless constructions, and French subordinate clause accumulation are all "errors" by
current diagnostics that are legitimate rhetorical choices in their traditions.

From the writing-scholar: Writers across every tradition describe writing as discovery, not
transmission. AI writing lacks seven specific things — most actionable for skills: no strategic
silence (subtractive craft), no position/accountability, no writing-as-thinking. Concrete AI-isms
to prevent: filling intentional gaps, smoothing productive friction, defaulting to disclosure over
restraint, substituting category for experience, simulating position without stakes, treating all
hedging as weakness, resolving tension prematurely.

## Recommendation

The following 10 principles — Principle 0 through Principle 9 — should ground all expression skills.
Every proposed skill is evaluated against them. A skill that violates any of them has a design flaw,
not a feature.

---

## The 10 Grounding Principles

### Principle 0 — Necessity (the ground)

Writing exists because something must not be lost. The question "why must this be written?" is not
a planning step but the generative force that shapes all subsequent decisions. Writing driven by
necessity produces different work than writing driven by efficiency or instruction. Without necessity,
there is only content production.

This principle is what separates writing assistance from content generation. Skills should honor it
by asking for necessity before prescribing method, and by recognizing when prose is doing preservation
work that looks like inefficiency.

*Cross-tradition evidence:* Achebe's tortoise marks survival into the record. Poniatowska records
voices official history erases. Ngugi writes on toilet paper in prison. Ogawa says writing is "facing
death." Al-Shaykh began writing "as a way of being sure of her own existence."

### Principle 1 — Purpose

Every piece of writing serves a purpose the writer must be able to name. But that purpose may be
discovered through drafting, not known in advance. The skill's job is to help the writer surface the
purpose, not impose one.

Skills should ask: what must this piece accomplish, and for whom? But they should also allow the
Frame phase to be revisited after drafting — discovery is not failure.

*Cross-tradition evidence:* The Arabic *maqsad* (intent), French *problématique*, and Japanese
*mondai-ishiki* (problem-consciousness) all begin with explicit purpose-framing. Murakami discovers
his novels' purposes by writing them. These are not contradictory — they are different entry points
into the same necessity.

### Principle 2 — Tradition-aware, not tradition-bound

All writing operates within rhetorical conventions. Identify which conventions are active before
evaluating structure, and never treat one tradition's conventions as the unmarked default.
Anglo-American linear-deductive organization is one rhetorical tradition — not the tradition.

*Stated explicitly as the design claim:* The expression plugin's diagnostics evaluate prose against
its own rhetorical logic, not against an invisible Anglo-American baseline. Prose that follows a
different organizational logic is not "unclear" — it is operating within a different system.

*Cross-tradition evidence:* Arabic parallel-restatement builds meaning through accumulation, not
progression. French academic writing holds contradiction before synthesis. Japanese prose moves
through indirection toward implication. Latin American narrative uses ecosystem metaphor over linear
argument. Circular and spiral structures are legitimate organizational strategies in many oral
traditions.

*Implementation:* `technique-tradition` operates as a lens that modifies how all other diagnostics
fire. It contains: a taxonomy of rhetorical traditions with structural signatures, diagnostic questions
to identify which tradition is operating, and explicit modification rules for each downstream technique.

### Principle 3 — Position

Writing comes from somewhere. Every skill surfaces whose perspective is speaking, what authority
grounds it, what the writer's relationship to the subject is, and what they are unable to see from
where they stand. Generic prose is not neutral — it is a specific cultural register with its own
assumptions.

Three questions for any writer: What is my relationship to this subject? What can I legitimately
claim? What am I unable to see from where I stand?

*Cross-tradition evidence:* Ngugi's choice to write in Gikuyu was an ontological commitment, not a
style preference. Luiselli insists on "recognizing the limitations of the position that we occupy
in society." Ernaux treats the self as data with "ethnology of myself" — not authority but method.
Achebe writes from the position of a people whose story was being told by others.

*Note on voice:* The `voice` technique revision must extend consistency to include position — not
just "does this sound like one person wrote it?" but "does that person speak from a position?"
Generic unmarked voice defaults to dominant-culture register; skills must make that visible.

### Principle 4 — Subtraction

What the text refuses to say is as meaningful as what it says. Deliberate omission, strategic
silence, and restraint are craft tools equal in value to addition, elaboration, and explanation.

Two dimensions:

- **Literary craft**: The refusal to say something is a positive rhetorical act. "Is this gap doing
  work?" not "What needs to be added here?"
- **Cultural calibration**: High-context writing leaves out what the reader is trusted to supply.
  Over-explicitness reads as clumsy or insulting. Explicitness is a cultural parameter, not a
  universal virtue.

AI's default is to add. Skills must counterbalance this default. The diagnostic before any addition
suggestion: is this gap intentional?

*Cross-tradition evidence:* Japanese *ma* (negative space as meaning). French litotes (affirmation
through understatement). Arabic *tawriya* (double meaning through deliberate ambiguity). Al-Shaykh's
characters achieve power through what they avoid saying. Ernaux: some things are more faithfully
represented by absence than description.

### Principle 5 — Difficulty from subject, not expression

When prose is hard to parse, the writer has shifted cognitive work to the reader. But when ideas
are genuinely complex, simplification is dishonest. Skills distinguish between accidental complexity
(poor expression) and essential complexity (the subject demands it), and preserve the latter while
eliminating the former.

Further: productive friction — irregular rhythm, unresolved tension, deliberate register shifts —
may be the writing working correctly, not failing. Smoothing friction without asking whether it is
intentional is an AI-ism.

*Implementation:* `clarify`'s load-type distinction (extraneous vs. intrinsic vs. germane cognitive
load) is the existing mechanism. Skills should explicitly ask whether difficulty is the subject
asserting itself before flagging it as a clarity problem.

### Principle 6 — Discovery

Writing is a thinking process, not a transmission process. The act of writing changes what the
writer knows. Skills must allow — and in `/writing`, actively encourage — the possibility that
drafting reveals the real argument, that structure emerges from material, and that the first frame
may not survive contact with the prose.

*Implementation for `/writing`:* Draft phase explicitly invites exploratory prose. Self-audit
includes: "Did this draft teach you something you didn't know when you started? If so, does your
Frame still hold?" This creates a loop: Draft can send the writer back to Frame. The skill names
this loop and normalizes it — not as failure to plan but as the writing working.

*Cross-tradition evidence:* Murakami enters novels without a plan. Ernaux calls her method
"an ethnology of myself" — studying experience to surface what she didn't know was there. Saunders
describes losing the self entirely in revision: "all of my energy is being used to try to figure
out how to make the story better." Writing-as-discovery is consistent across every tradition studied.

### Principle 7 — Epistemic honesty (the floor)

Claims must be calibrated to evidence. Uncertainty must be named as uncertainty. Scope boundaries
must be stated. Assumptions must be surfaced. No expression skill produces or encourages prose that
claims more than it knows, hides uncertainty behind confident language, or flattens genuine complexity
into false simplicity.

This is non-negotiable. It is never traded off against clarity, persuasiveness, or narrative craft.

*The hedging split:* Hedging performs two distinct functions — epistemic calibration (legitimate,
preserve) and habitual cushioning (low-value, cut). The diagnostic must distinguish. Different
traditions signal certainty through different mechanisms; the goal is calibration within the
writer's system, not conversion to a single register.

### Principle 8 — Grammar as philosophy

Different languages grammaticize different philosophical distinctions. Moving between languages
is not just translating words — it is navigating between ontologies. When L1 grammatical structures
surface in English prose, diagnose whether they carry intended precision before treating them as error.

Spanish `tener miedo` treats emotion as carried, not identity — this is philosophical precision.
Japanese sentence-final particles encode epistemic stance that English can only approximate.
Arabic agentless constructions may encode divine or natural causation deliberately. These are not
errors to be corrected; they are meanings to be understood.

*Implementation:* `help-me-say` is the primary site for this principle. But it applies to every skill
when working with multilingual writers — `activate`, `strengthen`, `clarify`, and `voice` all have
culturally-situated defaults that can misread L1-inflected English as error.

### Principle 9 — Reader as participant

Writing invites the reader into cognitive and emotional work. A piece of writing creates a relationship
between writer and reader that requires something of both parties. Optimizing for frictionless
comprehension can destroy the space where meaning happens.

The reader is not an obstacle to overcome; the reader is a collaborator the writer has chosen to
address. Skills should ask: what does this piece require of the reader, and does the writer intend
to require it?

*Implementation:* This principle modifies `calibrate` (which currently measures what the audience
knows — not what the writer is asking them to do) and `bridge` (which currently explains unfamiliar
concepts — but sometimes the refusal to bridge is the invitation to the reader). It also grounds the
`pose-questions` technique, which exists specifically to open rather than close inquiry.

*Cross-tradition evidence:* Saunders: "you can know my mind and I can know your mind, which is a
vastly consoling idea." Adichie: fiction takes us "into the lives and motivations of other people."
Murakami wants to "open a window in their souls." The reader is present in every writer's description
of why they write.

---

## The Hierarchy

```
Principle 0: Necessity ── the ground beneath everything
    │
    ▼
Principle 1: Purpose ── what must this accomplish?
    │
    ▼
Principles 2+3: Tradition + Position ── the lens through which all craft operates
    │
    ▼
Principles 4+5: Subtraction + Difficulty ── constraints on method
    │
    ▼
Principle 6: Discovery ── shapes the process
    │
    ▼
Principles 7+8: Epistemic honesty + Grammar as philosophy ── the floor
    │
    ▼
Principle 9: Reader as participant ── the destination
```

No principle below this line is traded off against a principle above it.

---

## Application to Skills

Each proposed expression skill must be evaluated against all 10 principles:

| Principle | `/composition` | `help-me-say` | `/clarify` | `/redraft` | `/expression` library |
|-----------|-----------|--------------|-------------|----------|----------------------|
| 0 Necessity | Frame phase | User's felt need | "why does this exist?" before what's wrong | cascade guards against loss | available as technique |
| 1 Purpose | Frame phase (recursive) | articulating a specific intent | scope-check before editing | convergence check | diagnostic routing |
| 2 Tradition | Structure phase: identify before drafting | L1 tradition identified | tradition lens before diagnostics | tradition modifies all 5 passes | tradition is the first lookup |
| 3 Position | Structure: positional questions mandatory | L1 speaker's position named | voice audit includes position | position technique in Pass 3 | position technique available |
| 4 Subtraction | Draft: practice leaving things out | annotate what was compressed | streamline audit, gap-check | omit technique in Pass 3 | omit technique available |
| 5 Difficulty | Draft: follow the surprising sentence | compression is sometimes loss | preserve intrinsic load | load-type preserved across passes | clarify load-type distinction |
| 6 Discovery | Draft → Self-audit → Frame loop | skill reveals what user didn't know they meant | post-edit: what survived reveals purpose | cascade is multiplicative discovery | ad-hoc use reveals hidden issues |
| 7 Epistemic honesty | Self-audit: calibrate claims | annotate where meaning shifted | strengthen split: calibration vs. cushioning | Integrity is Pass 2, mandatory before Narrative | signal-confidence available |
| 8 Grammar | Frame: L1 framing preserved if meaningful | core mechanism | L1 structures diagnosed not corrected | tradition lens in Pass 1 | tradition + activate revised |
| 9 Reader | Polish: who receives this? | the user's reader named | audience + purpose before edits | calibrate/bridge in Pass 5 | calibrate + bridge available |

---

## Anti-AI-ism Commitments

All expression skills share these specific commitments to prevent AI-isms and foster genuine human
connection. These are concrete behavioral requirements, not general principles.

1. **Do not fill intentional gaps.** Before suggesting additions, ask whether the gap is doing
   rhetorical work. Relevant: `omit`, `tradition`.

2. **Do not smooth productive friction.** Do not regularize rhythm, eliminate repetition, or
   normalize register shifts without asking whether the irregularity is intentional.
   Relevant: `rhythm`, `diction`, `tradition`.

3. **Do not default to disclosure over restraint.** Do not add topic sentences, transitions, or
   explanatory frames when the rhetorical tradition achieves power through implication.
   Relevant: `omit`, `tradition`, `bridge`.

4. **Do not substitute category for experience.** Do not replace specific, situated detail with
   clearer generalizations. Do not optimize for abstraction. Relevant: `ground`/`situate`.

5. **Do not simulate position without stakes.** If the writer hasn't specified their relationship
   to the subject, ask — do not invent a position. Relevant: `position`.

6. **Do not treat all hedging as weakness.** Distinguish epistemic calibration from habitual
   cushioning. Relevant: `strengthen`, `signal-confidence`, `tradition`.

7. **Do not resolve tension prematurely.** Do not offer conclusions or syntheses the draft has not
   earned. Unresolved contradiction may be the point. Relevant: `pose-questions`, `bound-scope`, `omit`.
