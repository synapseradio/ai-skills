# Units and ledger

Fits when: more than two levels of unit are live in the request, or the work runs past one sitting

This keeps a long piece steady in three ways: the same three questions go to every unit at every live level, a ledger holds what one sitting learned for the next, and the user sees each unit before the next one is drafted.

## Rungs

A rung is one level of unit. Each unit sits inside a unit of the rung above it, and the whole sits inside the audience's purpose. The form names its rungs:

| Form | Rungs, smallest to largest |
|------|----------------------------|
| Novel | sentence, paragraph, scene, chapter, part, whole |
| API reference | sentence, entry, section for one resource, reference |
| Contract | sentence, clause, article, agreement |
| Recipe | step, stage, recipe |
| Speech | sentence, passage, speech |
| Lyric poem | line, stanza, poem |
| Ki-shō-ten-ketsu essay | sentence, movement, essay |
| Commit message | subject line, body |

A live rung is one the request touches. Diagnose, step 1 of the loop, names the live rungs. A short form collapses to one or two rungs: a chat message has sentence and message.

Enter at the rung Diagnose names. New work that spans several units has the whole among its live rungs, so it starts with the skeleton. A request about one unit of existing work starts at that unit, and the ledger holds the rungs above it.

## Three questions at every live rung above the sentence

Ask these of each unit at each live rung above the sentence, or above the line in verse: from the paragraph, clause, step, or stanza up to the whole. The sentence rung keeps only the rubric questions attached to it. Answer each in one sentence that quotes or points to the unit.

1. What, if anything, does this unit do for the unit it sits inside?
2. What, if anything, does the audience bring into this unit from the units before it?
3. What, if anything, differs for the audience between the unit's start and its end?

Then ask the engagement question, in two halves:

- At every live rung but the last: What carries the audience from this unit into the next, if anything?
- At the whole's end: Which questions the piece opened close by its end, and which stay open?

"Nothing" is an ordinary answer to each of the three questions and to either half. A unit may pass through a piece without changing what the audience holds, someone who looks up one entry and goes leaves the unit by design, and a question may stay open because the form keeps it open. Record the reason beside the answer.

A unit is done at its rung when each of the three questions and the engagement half that applies has been answered, "nothing" included, each answer quoting or pointing to the unit. Those answers need units to attach to, and the skeleton makes the units.

## Skeleton, from the top down

Before drafting the first unit of work that spans several units, build the skeleton from the whole down to the rung you will draft at.

1. Answer the three questions for the whole. For the whole, question 1 asks what, if anything, it does for the audience's purpose.
2. List the units of the rung below, each with a one-line answer to each of the three questions.
3. Repeat for each rung, down to the rung you draft at. Where the split of a rung waits on an open decision, propose one split for each sketch of that decision, each unit with its three answers, and let the user's answer choose between them.
4. Show the skeleton to the user and agree on it before drafting. Where you cannot tell what a unit should hold, ask the user; write no placeholder in its place.

Keep the agreed skeleton in the ledger, with each unit's status: planned, drafted, or stale.

## Discovery, from the bottom up

Drafting a unit can show that the skeleton is wrong: a thread wants another place, a term needs defining earlier, a party knows something too soon, a step depends on a later one. When it does, change the skeleton, and record the change as a decision. The next section says which units the change reaches.

## After any skeleton change

Record every change to the skeleton or to a committed fact as a decision, whoever asked for it, with the units it makes stale. Where the change reaches the premise or the spine, rewrite them too.

A drafted unit is stale when the change alters what its audience holds at its start, or what it must deliver at its end. Test every drafted unit from the first one the change touches to the last, not only the unit that states the changed fact. A planned unit stays planned; rewrite its question-3 line to match the change.

Before drafting the next new unit:

1. Mark each stale unit stale in the skeleton.
2. Reread each stale unit against its three questions and the changed skeleton. Where a stale unit's text is not in hand, ask the user for it.
3. Revise or confirm it, rewrite its question-3 line, and mark it drafted.

Draft a new unit only when no unit is stale.

## Rubric by rung

Attach each rubric question to the rung where the risk it probes shows:

- a word-choice question to the sentence rung
- a defined-term question to the clause or entry rung
- a question about open threads to the chapter or part rung

Score a unit only on the questions attached to its rung. A question retires for a unit once its answer there matches the alignment record, and returns when that unit changes.

## Reread from the ledger, per rung

When a unit is drafted, reread it holding only what the ledger says the audience holds at its start.

1. Read the ledger's question-3 lines for every unit before it, and what the audience knows by the end of the unit just before it, from the who-knows-what table.
2. Read the unit, and nothing else of the draft.
3. Where the unit rests on something the ledger does not give the audience by then, repair it. Where the cause lies inside the unit, change the unit. Where it comes from the order of units, change the skeleton, as a decision.

The ledger stands in for the units you did not reread. When a whole part can be reread in one sitting, reread the part whole as well.

## The user between units

Show the user each unit once it is drafted, before drafting the next, with every decision it holds: each committed fact it adds, each change to the skeleton, and each invention the user asked for. Never draft past a unit the user has not seen. Mark the date in the skeleton's shown column.

## Unit per sitting

A sitting is one working session. Draft in one sitting the largest unit you can reread whole, beside the ledger, before writing its last sentence. When the unit and the ledger cannot both be reread whole, draft at the rung below.

## Pacing across units

Read the open threads as a series: how many each unit opens, how many it closes. The form decides how long its audience holds a thread. A mystery holds its central question from the first chapter to the last, on purpose. A reference entry holds none, since someone who looks up one entry leaves before a later one could close it.

**Contrast: a thread closed inside the unit that opens it**

- antipattern: "Timeout: see the note on retries in section 7."
- pattern: "Timeout: 30 seconds. Each retry starts a new 30 seconds."
- observe: the pattern answers inside the entry the question the antipattern sends to section 7.
- shared: the same reference entry, on the same setting.
- contrast: a thread held open past the unit against a thread closed within it.
- look for: a pointer forward in a unit its audience reads alone.

Record the form's choice of how long a thread stays open as a decision in the ledger.

## The ledger

- kept for: work that runs past one sitting
- file: `ledger.md`, in the piece's folder beside `align.md`, as the storage section of [align](./align.md) says
- built from: [ledger-template](../assets/ledger-template.md)
- started: in the first sitting, with what the user has given (premise, facts, voice)
- skeleton: added once the user agrees on it
- read: whole, before drafting each unit
- updated: after each unit
- form: key-value lines and tables, one line per item
- closed thread: cut to one line
- fact the user let you invent ("make up the names", "you pick the ending"): invent it within what they handed over, record it as a decision, and name it back to the user when the unit is shown
- any other fact about the piece's world that settles what the piece is about (a reveal, a premise, an ending, a term the agreement turns on): goes to the open decisions table and to the user; no unit that depends on it is drafted until the user answers
- other new fact about the piece's world (a name, a rule, a date, a tool, a procedure that connects units): run the two-sketch test in [align](./align.md); where it splits, it goes to open decisions and to the user; where it does not, it enters as a decision, named to the user when the unit is shown; a fact placed only in the draft stays unseen by the user
- any other fact about the real world: goes to open decisions and to the user; the draft waits for the answer
