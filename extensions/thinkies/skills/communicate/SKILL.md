---
name: communicate
description: >-
  Communicate ideas and information with purpose, clarity, and integrity, in any form or tradition and at any length, to an audience of one or many, addressed or not. Works out with the user who the piece is for, what brought it on, and where it should take its audience, then drafts and checks the piece against that, keeping the user's meaning theirs. Use when the user asks for help with writing, commentary, or communication; when they point out AI slop; when they ask things like "help me say", "write for [a specific audience or context]", "polish [comments, sentences, artifacts]", "write something for the poster", "help me write a novel, a handbook, or a long report", "keep this long piece consistent across chapters", or the like.
compatibility: >-
  Any agent that can read files on demand, create and keep files between
  turns (an alignment file, a ledger, and drafts for each piece), ask the
  user questions and wait for the answers, keep a short ranked list in its
  working notes, and answer explicit questions about a draft by pointing
  to it.
---

# Communicate

Help the user make a piece that takes its audience where the user means it to go, in any form or tradition and at any scale: choosing one word, polishing a sentence, drafting a contract clause, or writing a novel across many sittings. Work in one loop: diagnose the request, align with the user, build a rubric, draft, score the draft, and revise with the user.

## Where the work is kept

Keep each piece's alignment file, its ledger for long work, and its drafts in `${CLAUDE_PLUGIN_DATA}/communicate/<piece-slug>/`. Where that path is not absolute, ask the user once where to keep them. The finished artifact goes where the user names. [align](references/align.md) holds the details.

## The loop

### 1. Diagnose

Read [align](references/align.md), open the piece's alignment file or start one from [align-template](assets/align-template.md), and infer every ring of the wheel the request and any text in hand answer.

Then name the risks ring by ring: for each ring, the ways this piece could fail its audience there, given what the alignment file holds and what it leaves open. Beside them, name the authorship risks: the user's words, facts, and chosen patterns the draft must carry; the intent, stance, and promises it must keep; the choices the user has not made that would steer it. Rank the risks, most damaging first, and write the list down; for larger tasks, show it during alignment.

Name the live rungs too: the levels of unit this request touches, in the form's own names, such as sentence and paragraph for a polish, clause and article for a contract, or scene, chapter, and whole for a novel.

When the user points out AI slop, or prose that reads as machine-made, rank the voice-ring risks first.

Then read [index.md](references/index.md) whole, and read every reference whose `Fits when` condition holds for this piece, whatever ring its risks sit on. The risk list sets the order of reading; the conditions set which files are read. A quick change reads fewer references, never none.

### 2. Align

Run the alignment conversation in [align](references/align.md): one question per message, from the outermost open ring, then from the open choices that would steer the draft; each ring the user's words already answer stated back in one line inside the next question. Where the user cannot answer, lead with contrasting readings, an example, or what should happen after; never guess on their behalf.

The form ring holds the tradition the piece works in, and the period's or house's conventions it carries. Take them from the user's words, the form they named included, or ask when the form ring's turn comes; never assign a tradition from the language the user or the audience speaks.

Take from the user's words how much they want to hear about changes to their words. Where they give no sign, give a short summary, and name every change of meaning.

Match the depth of this conversation to the size of the task. For a quick change to text in hand, infer the rings from the text, choose references silently, and state every inferred ring, one short clause each, and what you checked in the closing line; where the two-sketch test splits, ask about each split alongside the change, one question each. For a substantial piece, show the user the risk list, the rubric, and the questions step 3 dropped beside the first question, and take their reply as agreement or correction on all three before drafting. For work that runs past one sitting, name the live rungs to the user, agree on the skeleton, and start the ledger, as [units-and-ledger](references/units-and-ledger.md) describes.

### 3. Build the rubric

A rubric is the list of questions you will answer about the draft. Copy every numbered question in [baseline](references/baseline.md). Then copy from [rubric-questions](references/rubric-questions.md) the section for each ring where Diagnose found risks. Take rubric questions from these two files only; read the other references for their technique, and leave their own question lists where they are. Stop adding questions at the point where you could no longer answer each one by pointing to the draft: a single word supports a few questions; a chapter supports many, revisited across drafts.

Then, for each question in the rubric, ask whether the form or tradition recorded already answers it. Where it does, drop the question and write one line naming the part of the form that answers it. Where one feature of the form answers several questions for the same reason, one line may cover the group: it names the feature and lists each question it covers.

**Contrast: a drop-reason line that names the form**

- antipattern: "dropped “How does the draft's vocabulary stand beside the audience's own?”: not needed here."
- pattern: "dropped “How does the draft's vocabulary stand beside the audience's own?”: the contract defines its terms in its definitions article."
- observe: the pattern lets the user check the drop against the form; the antipattern asks for trust.
- shared: the same dropped question, in the same one-line shape.
- contrast: a reason that names a feature of the form against a reason that names none.
- look for: a reason line that names no feature of the form or tradition.

Never drop the baseline's authorship questions.

### 4. Draft

Draft with the authorship line in [baseline](references/baseline.md) in force, the rubric in view, and the technique of each reference you read at hand. Use any device the form calls for, such as fragments, delayed reveals, long cascading sentences, or repetition, and be able to say what each one does for the audience. The conventions of the recorded form that the user's text follows count among the user's chosen patterns: an edit keeps them.

The artifact carries no scaffolding of yours: no gap, bracket, placeholder, or note, short pieces included. What the user wrote stays theirs, their own notes included. Before a choice the user has not made enters the draft, run the two-sketch test in [align](references/align.md). Where it splits, ask, and hold the choice in the alignment file or the ledger until the user answers; the draft waits for the answer.

Keep the user in the loop: show each draft, or each unit in long work, before the next, with every decision it holds. Never draft past a unit the user has not seen. Where a ledger exists, read it whole before drafting a unit, and update it after.

### 5. Score

Answer the ring questions, then the authorship questions, each in your own words, pointing to the draft. Set each answer beside the alignment file. Where they differ, redraft; where the difference touches authorship, take it to the user. After every redraft, answer the authorship questions again, starting from what they pointed to on the last pass: where each passage stands now, or that it was cut. When an answer cannot match the alignment file without breaking something the user agreed to, tell the user instead of picking a side silently.

### 6. Revise with the user

A revision request updates the alignment file: record every ring it touches. Then reread [index.md](references/index.md) against the updated state, read at least one fitting reference not yet read this run, add the rubric-questions section for any ring where a risk now shows, and revise and rescore. The rubric grows over the conversation. Where a ledger exists, attach each new question to the rung where the risk it probes shows.

### Report

Report each change at the detail the user asked for: a short summary to a user who says "just fix it", each change to a user who asks what changed. Where the reply names an edit to the user's words, quote their words beside yours. Name every change of meaning, every fact you invented at the user's word, and every ring you inferred and have not yet stated back.

## The line that holds in every form

The user authors the meaning. Authorship is no ring of the wheel; it runs across the whole loop, in four parts.

- Given: the user's words, facts, and chosen patterns. Score checks them with the authorship questions.
- Meant: the user's intent, stance, promises, and subtext. Score checks them with the authorship questions.
- Undecided: the choices the user has not made that would steer the piece. Align settles them. Where the user hands you an invention, that handing over is their decision; name each invented fact back to them.
- Shown: every change reaches the user at the detail they asked for, and a change of meaning is never silent.

The skill guards authorship only. Whether a piece is true, a story, satire, or a lie told on purpose is set in the form ring, and every step takes it from there. Before changing the structure of prose that a tradition or the user's first language shapes, read [across-languages](references/across-languages.md).

## Where to be creative, and where not

Be creative with form and structure; with imagery, analogy, and rhythm; with register. Where the form rewards invention, propose a braver shape than the user asked for; where it rewards convention, keep to the convention. A draft whose answers all match the alignment file and still leaves the audience short of the point has failed its audience.

Never be creative with the user's meaning or with the scope the user set. Spend creative effort on how the piece works, never on its requirements.
