# detect-diminishing-returns: ninth draft of a best-man speech

- skill: detect-diminishing-returns, from commit 0c9258f
- subject: I'm rewriting my best-man speech for the ninth time. Draft 1 took an hour and got the structure; drafts 2–4 added three jokes and cut two minutes; drafts 5–8 swapped single words back and forth; draft 9 moved one joke from the end to the middle and back. The wedding is Saturday.
- kind: single run

## Prompt

/detect-diminishing-returns I'm rewriting my best-man speech for the ninth time. Draft 1 took an hour and got the structure; drafts 2–4 added three jokes and cut two minutes; drafts 5–8 swapped single words back and forth; draft 9 moved one joke from the end to the middle and back. The wedding is Saturday.

## Run

What I have is your description of each draft, not the drafts themselves. Everything below is read from that description. Where a step needs a fact the description does not give, I say so.

### 1. Track pattern emergence

Each theme, and the draft where it first appeared:

| Draft | What entered | Kind of change |
|---|---|---|
| 1 | The structure of the speech | Structural: the shape everything else hangs on |
| 2–4 | Three jokes | Content: new material |
| 2–4 | Two minutes cut | Length: a new dimension, the running time |
| 5–8 | Single-word swaps, back and forth | Wording: a dimension, but one whose changes reverse |
| 9 | One joke moved end to middle and back | Order: a dimension, but the change reversed |

Four dimensions have appeared: structure, content, length, and wording, with order as a fifth that appeared only as a move and its reversal. Structure arrived in draft 1, content and length by draft 4. After draft 4, no new dimension arrived. Drafts 5 through 9 reinforce what was known, or return to where they started.

### 2. Test predictive power

The test: predict what draft N+1 will contain, then compare it with what happened.

- After draft 4, the prediction "the next drafts will swap words, not add material" would have been right for drafts 5, 6, 7, and 8: four hits in four.
- After draft 8, the prediction "draft 9 will make another small change and leave the speech as it was" was right. Moving a joke and moving it back leaves the speech unchanged.
- Looking forward: draft 10 is predicted to be another small reversible change, with the speech unchanged at the end of it.

The model anticipates reality for five drafts running. Drafts 5–9 have no surprises left, which is the sign the process has stopped producing information. The early drafts were the opposite: from the outside, no one could have predicted that draft 2 would add a joke or that draft 4 would cut two minutes.

### 3. Measure theme stability

Compare the early definitions of the speech's themes with the current ones.

- Structure: defined in draft 1, unchanged since. Nine drafts have not reshaped it.
- Length: reduced by two minutes in drafts 2–4, unchanged since, as far as the description says.
- The three jokes: added in drafts 2–4. The description mentions no joke being cut, so all three appear to have survived five drafts.
- Wording: this is the one unstable element, and its instability is the signal. Words swapped back and forth are words with no settled answer. The ear cannot tell the two versions apart.
- Joke order: moved and restored, so the settled state is the state before the move.

The core has held since draft 4. The only things still moving are the ones that return to where they started.

### 4. Count novel information

A change counts as novel where it leaves the speech different from every earlier draft. A change that restores an earlier draft counts as zero.

| Drafts | Changes made | Novel (net change) | Novelty share |
|---|---|---|---|
| 1 | The whole structure | 1 | all of it |
| 2–4 | 3 jokes added, 2 minutes cut | 4 (3 additions, 1 cut) | all of it |
| 5–8 | Word swaps, back and forth | 0 net | none |
| 9 | Joke moved to the middle and back | 0 net | none |

Count by draft: draft 1 carried one novel change, drafts 2 through 4 carried four between them, and drafts 5 through 9 carried none. Novelty fell from 100% of the changes to 0% and has stayed there for five consecutive drafts. Five drafts of work produced a speech identical to what it would have been after draft 4, plus the time it took to write them.

### 5. Check boundary conditions

The question in this step is which edge cases the drafts have not touched. Do the existing patterns explain them, or do they expose gaps?

Edge cases that would test the speech, none of which appear in the description of drafts 1–9:

- **Read aloud, against a clock.** Every change so far is a change on the page. A speech is delivered by voice. Whether the word swaps matter, and whether the joke belongs at the end or in the middle, are questions the ear answers and the page cannot. Nothing in the description says a draft was read aloud.
- **The target length.** Two minutes were cut, and the description does not say to what. Whether the speech now fits the slot is unknown to me.
- **A listener.** No draft is described as heard by anyone. Whether the three jokes land is untested.
- **The room.** Whether the humor suits the guests, including the couple's families, is a fact only the speaker holds. The drafts add nothing to it.
- **The opening and the last line.** The joke that travelled from the end to the middle and back shows that the ending is the place where the speech is least settled. It is where the decision, if there is one left, actually sits.

These gaps are not filled by more drafts. The existing pattern, small reversible edits to the text, explains none of them. It tells us nothing about them, because none of the nine drafts was a test of the speech in the medium where it will be used. The text has converged. The speech's effectiveness has not been measured at all.

### 6. Declare convergence

**What has stabilized:** the structure (since draft 1), the length (since draft 4), and the set of three jokes (since draft 4). The text is at a fixed point: the last five drafts left it where it was.

**What confidence the synthesis supports:**

- High confidence that further redrafting on the page has reached zero marginal value. Five drafts with zero net novelty and five correct predictions in a row support this well.
- No confidence, in either direction, about whether the speech is good. The drafts contain no measurement of that. Convergence of the text shows the writing has stopped changing, and does not show the speech works.

**What further exploration would add:**

- Draft 10 and later, on the page: about nothing, by the prediction in step 2.
- One read-aloud with a timer: a lot. It is the first test of length, wording by ear, and joke order in the medium where they matter. It is the one action on this list that can produce a surprise.
- One listener, once, on the jokes and the last line: some value, and it costs a few minutes.

**Recommended stopping rule, given that the wedding is Saturday:** stop drafting. Read the speech aloud once against a clock. If the running time fits the slot, choose the joke position that felt right aloud, and settle every remaining word swap by which version was easier to say. If it does not fit, cut the joke you would miss least and stop. Then use the days left for rehearsal, which improves delivery, and not for drafts, which have stopped improving the text.
