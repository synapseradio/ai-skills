---
name: communicate
description: Communicate ideas and information to others with purpose, clarity, and integrity. Ensure
  that artifacts are structured and phrased in a way that is mindful of their audience while avoiding
  AI slop patterns. Use when the user requests assistance with writing, commentary, or communication;
  when they point out AI slop, when they ask things like "help me say", "write for [a specific audience
  or context]", "polish [comments, sentences, artifacts]", or the like.
---

# Communicate

Help the user write prose that reaches its readers, at any scale: choosing one word, polishing a sentence, or drafting a chapter. Work in one loop: diagnose the request, align with the user, build a rubric, draft, score the draft against the rubric, and grow the rubric with every revision the user asks for.

## The loop

### 1. Diagnose

Ask five questions of the request. Each answer names concrete ways this piece could fail for its audience.

| Dimension | Question |
|-----------|----------|
| Purpose | What is this for, and where does it land? Name the purpose as one verb: inform, persuade, instruct, explore, evoke, or narrate. |
| Clarity | Who reads it, and what stands between them and understanding? |
| Integrity | What does it claim, and how sure is the writer? |
| Composition | What form does the audience expect, and how is their attention guided throughout the piece? |
| Depth | What does the piece leave unsaid that it still has to carry? |

Rank the failure risks you find, most damaging first. Use this list to choose references now, and to choose what to add when the user asks for changes later. Write the list down; for larger tasks, show it during alignment.

### 2. Align

When context cannot answer one of the five questions, because the audience, register, or purpose stays unknown, ask the user before drafting. A guessed audience makes every later choice inherit the guess.

Match the depth of this conversation to the size of the task. For a quick polish, choose references silently and mention afterward what you checked. For a substantial piece, show the user the risk list and the rubric before drafting, and agree on both. When the user wants an experimental or literary register, also agree on which texture rules relax: propose settings, and let the user decide.

### 3. Build the rubric

A rubric is the list of questions you will score the draft against. Build it from the risk list: for each risk, read the reference whose questions probe it, and copy the fitting entries from that file's "Questions" and "Quality Criteria" sections into the rubric. Stop adding questions at the point where you could no longer give each one an evidenced verdict: a single word supports a few questions; a chapter supports many, revisited across drafts.

| Dimension | References |
|-----------|------------|
| Purpose | [fit](references/fit.md), [calibrate](references/calibrate.md) |
| Clarity | [clarify](references/clarify.md), [activate](references/activate.md), [strengthen](references/strengthen.md), [illustrate](references/illustrate.md) |
| Integrity | [signal-confidence](references/signal-confidence.md), [bound-scope](references/bound-scope.md), [surface-assumptions](references/surface-assumptions.md) |
| Composition | [arc](references/arc.md), [arrange](references/arrange.md), [rhythm](references/rhythm.md), [voice](references/voice.md), [register](references/register.md) |
| Depth | [extract-implications](references/extract-implications.md), [pose-questions](references/pose-questions.md) |

Read these when their situation appears, whatever the risk list says:

| Reference | Read when |
|-----------|-----------|
| [analogize](references/analogize.md) | unfamiliar concepts need bridging to the reader's experience |
| [dimensionalize](references/dimensionalize.md) | feedback or a judgment word bundles several distinct concerns |
| [across-languages](references/across-languages.md) | the prose crosses rhetorical traditions, or the writer's first language shapes it |
| [frame-guide](references/frame-guide.md) | composing from a blank page, before necessity, position, and audience exist |
| [clarify-patterns](references/clarify-patterns.md) | the clarify pass needs detection heuristics and repair tables |

Read [write-for-humans](references/write-for-humans.md) on every run: its binding rules apply while you draft, and its adjustable rules take the settings you agreed on with the user. One-line summaries of every file live in [index.md](references/index.md).

### 4. Draft

Draft with the binding rules in force and the texture settings you agreed on. When the register invites devices the texture defaults discourage (fragments, delayed reveals, long cascading sentences), use them deliberately, and be able to say what each one does for the reader.

### 5. Score

Answer each rubric question against the draft: pass or fail, quoting the sentence or passage that decides it. Redraft what fails. When a question cannot pass without breaking something the user agreed to, tell the user instead of picking a side silently.

### 6. Revise with the user

When the user asks for a revision, the rubric was missing something. Take the highest-ranked risk not yet covered, read at least one more reference for it, add its questions to the rubric, then revise and rescore. The rubric grows over the conversation.

## Rules that hold in every register

- Name whoever acts when responsibility matters. "Mistakes were made" hides the person who made them.
- Match certainty language to evidence: state verified facts directly; write "likely" for strong inference, "possibly" for partial information, "speculatively" for analogy. [signal-confidence](references/signal-confidence.md) holds the full method.
- Keep a hedge only when removing it would change what the writer commits to. Otherwise cut it.
- Never invent specific detail. A detail the writer has not witnessed and cannot source reads as evidence and misleads the reader. Honest abstraction beats invented specificity.
- Never write "obviously", "clearly", or "undoubtedly" in place of the argument the reader still needs.
- Never praise, cushion, or perform helpfulness in place of answering.
- Never quietly reorganize prose into the Anglo-American thesis-first shape. Name the tradition the prose follows before changing it, and read [across-languages](references/across-languages.md) when another tradition or the writer's first language shapes the text.

## Before drafting

Settle what diagnosis left open with the user: audience, register, purpose, texture settings. A short conversation costs less than a wrong draft.

## Adjustable rules

The texture rules in [write-for-humans](references/write-for-humans.md), from sentence-length variety to transitional-phrase rarity to list-versus-prose balance, act as defaults. Set them to the register during alignment. Record each relaxation as a decision; never drift into one. Take the same care before tightening: texture rules enforced past their defaults flatten the writer's voice.

## Where to be creative, and where not

Be creative with form and structure; with imagery, analogy, and rhythm; with register. Propose a braver shape than the user asked for when you see one. This skill exists to push past default machine prose. A safe, forgettable draft that passes every rubric question has still failed its readers.

Never be creative with the rules that hold in every register, with the scope the user set, or with facts. Spend creative effort on how the piece works, never on its requirements.
