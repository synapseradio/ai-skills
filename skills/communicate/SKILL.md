---
name: communicate
description: >-
  Communicate ideas and information to others with purpose, clarity, and integrity. Ensure that artifacts are structured and phrased in a way that is mindful of their audience while avoiding AI slop patterns. Use when the user requests assistance with writing, commentary, or communication; when they point out AI slop, when they ask things like "help me say", "write for [a specific audience or context]", "polish [comments, sentences, artifacts]", or the like.
metadata:
  context: fork
---

# Communicate

Write prose for others that has purpose, clarity, integrity, and depth. Structure and phrase communication appropriate in context, mindful of linguistic tradition and how people actually speak to each other.

This skill includes reference files grouped under five dimensions: Purpose, Clarity, Integrity, Shape, and Depth. You do not pick from them at random or by instinct. You earn the selection by interrogating the request first.

## Pre-flight: interrogate the request, then choose

Before you draft a word, you cannot know which techniques this piece needs. The request has to tell you. Run the diagnostic below. Each dimension poses one question to *this* request, and the answer names the reference within that dimension you will load. Commit to at least one reference per dimension before writing — five applicable references, each chosen because the diagnostic pointed at it.

When a dimension's question has no answer you can find in context, that absence is your cue to ask the user. A reference chosen on a guessed answer is a guess wearing a citation.

| Dimension | Ask of this request | Load the most fitting |
|-----------|---------------------|-----------------------|
| Purpose | What is this for, and where does it land? | fit, calibrate, or analogize |
| Clarity | Who reads it, and what stands between them and understanding? | clarify, activate, strengthen, or illustrate |
| Integrity | What does it claim, and how sure am I? | signal-confidence, bound-scope, or surface-assumptions |
| Shape | What form does the audience expect, and what carries attention through it? | arc, arrange, rhythm, voice, or register |
| Depth | What does the piece leave unsaid that it still has to carry? | extract-implications, dimensionalize, or pose-questions |

Two files are read every time, on top of those five. [across-languages](./references/across-languages.md) keeps the message intact for a reader who does not share your first language. [avoid-slop](./references/avoid-slop.md) is the final revision pass before anything ships.

Record the five selections as todos at the start, each paired with the one-line answer that chose it. Five is the floor. A heavier piece pulls in more references per dimension as the drafts develop.

When a dimension's question does not by itself decide which of its candidates to load, read the one-line technique summaries in [index.md](./references/index.md) — the single home for what each reference does — and pick from those. The dimension sections below elaborate each candidate with its link.

## Questions you need answers for any piece of writing are headings below

Try to infer them from context. Ask the user if you cannot be certain.

### Always read (every piece, independent of dimension)

These two are not dimension picks — they load on every piece, per the pre-flight note above.

[Ensure the message survives transition across language and rhetorical tradition.](./references/across-languages.md)

[Run avoid-slop as the final revision pass before anything ships.](./references/avoid-slop.md)

### Purpose: What is the purpose of the piece?

[Your output should fit into its destination. Here is the manual.](./references/fit.md)

[After fitting, calibrate output by asking a few important questions.](./references/calibrate.md)

[When explaining, reach for analogy per the manual.](./references/analogize.md)

### Clarity: can the audience understand it?

[Begin by understanding what makes your output clear to others.](./references/clarify.md)

[Ensure your output may be activated in their minds.](./references/activate.md)

[When information is hedged, padded, or hidden in verbs within abstract nouns, make it concrete with the instructions in the strengthen reference.](./references/strengthen.md)

[Ground information with specificity for others to integrate it with their own experience.](./references/illustrate.md)

### Integrity: does tone match evidence?

[Signal confidence appropriately and methodically.](./references/signal-confidence.md), [and remember to bound scope to what you claim.](./references/bound-scope.md).

[Assumptions should always be surfaced transparently.](./references/surface-assumptions.md).

### Shape: does this shape conform to audience expectations?

[What you communicate must be observed, and to engage attention, the arc of change must be understood.](./references/arc.md)

[Arrange statements in complimentary, cohesive style.](./references/arrange.md)
[Pay attention to the rhythm implied by your output.](./references/rhythm.md)
[Write in distinctive voice by asking these leading questions.](./references/voice.md)
[Register your words to their context.](./references/register.md)

### Depth: does this piece have the necessary depth to transmit its message?

[Take a moment to understand the implications of what it is you are writing.](./references/extract-implications.md)

[When more than one subject is present, the contrast creates dimensionality that is essential to be aware of.](./references/dimensionalize.md)

[Lead your writing process by posing questions of the space. This mandatory guide will help you.](./references/pose-questions.md)

## Invariants — hold on every run

Set up todos when this skill is invoked, without exception. The pre-flight diagnostic runs every time, and every time it yields at least five applicable references — one per dimension — alongside the two always-read files. This floor holds even for a quick "how do I say this" question: a short ask still has a purpose, an audience, a claim, a shape, and a depth, so the five questions still have answers. Drafting scales with the task. Diagnosis stays fixed. A one-line rewrite may need a single draft where an artifact needs several, but both pass through the same five questions first.

## Obligations — discharge before you start

Work with the user to de-blur and align intention before you start. Trust the user, and don't be afraid to have a conversation with them to get things right.

## Preferences — the revision pass before you ship

Every word must earn its place in service of concept, construction, or narrative. Output only what is worth disturbance to natural quietude, such that concept, construction, and narrative survive transit in clarity. Cataphora belongs to the avoid-slop pass — [avoid-slop](./references/avoid-slop.md) is where it is caught. Omit post-hoc explanation.
