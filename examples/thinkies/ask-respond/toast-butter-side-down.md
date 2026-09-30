# ask-respond: Why does toast always land butter-side down?

- skill: ask-respond, from commit 0c9258f
- subject: Why does toast always land butter-side down?
- kind: single run

## Prompt

/ask-respond Why does toast always land butter-side down?

## Run

I was handed a question, not a question set, so the skill's output mode is "write the question set, then answer it."

**Subject:** The final orientation of a slice of buttered toast that falls from a table or plate to the floor, and whether and why that orientation is usually butter-side down.

**Given:**

- The toast is buttered on one face and starts butter-side up (implied by the question; the asker did not state it)
- The toast falls from ordinary table height, about 76 cm, not from a hand or a countertop (assumed; the asker did not state it)
- "Always" is the asker's word and may overstate the pattern (my reading of the question)

**Questions:**

1. Why does a slice of buttered toast that falls from a table to the floor land butter-side down?
2. Which assumptions does that question carry, and which sub-questions must be answered first: whether butter-side down is in fact the usual result, what motion the falling toast makes, and what fixes how far it turns before it lands?
3. What does each of those sub-questions' answers rest on: direct observation, documentation, inference, or assumption without evidence, and where are the gaps?
4. What is the answer, at the strength the evidence supports, to why buttered toast falling from a table lands butter-side down?
5. Does the question about buttered toast falling from a table imply a request for action, and if so, what course should be proposed?

---

**Subject:** The final orientation of a slice of buttered toast that falls from a table or plate to the floor, and whether and why that orientation is usually butter-side down.

1. Why does a slice of buttered toast that falls from a table to the floor land butter-side down?

   Because a slice that slides off a table edge starts to tip as it goes, turns about half a revolution during the fall, and lands with the face that began up now facing down. The fall from table height takes too little time for a second half-turn to finish. The rotation is a property of the table edge and the slice, not of the butter, so the same reasoning gives a butter-side-up landing for any toast that started butter-side down.

2. Which assumptions does that question carry, and which sub-questions must be answered first: whether butter-side down is in fact the usual result, what motion the falling toast makes, and what fixes how far it turns before it lands?

   The question carries three assumptions and needs three sub-questions answered.

   Assumptions:

   - "Always" holds. It probably does not, because some starting conditions give the opposite result.
   - The toast starts butter-side up. A slice dropped butter-side down gets a different landing.
   - The fall is from table height. A fall from a hand, or a shelf, changes the number of turns.

   Sub-questions:

   - Is butter-side down in fact the usual result, and if so, by how much?
   - What motion does a slice make as it goes off an edge?
   - What fixes how far the slice turns before it lands, and does the butter matter?

3. What does each of those sub-questions' answers rest on: direct observation, documentation, inference, or assumption without evidence, and where are the gaps?

   - Is butter-side down usual? Documentation: a 1995 physics paper reports that toast has an inherent tendency to land butter-side down over a wide range of conditions, in contrast to the view that the outcome is a 50/50 split (abstract: <https://iopscience.iop.org/article/10.1088/0143-0807/16/4/005>). A later paper in the American Journal of Physics reports that a board falling from a table 76 cm high lands butter-side down for two ranges of overhang, which implies other ranges exist (search snippet only, page not opened; a copy of the paper is at <https://gwern.net/doc/science/physics/2001-bacon.pdf>). Gap: I read only the abstract of the first and a snippet of the second, and no data on real kitchens.
   - What motion does a slice make? Documentation, and inference from it: the 1995 paper models toast tipping over the table edge and slipping off, with friction limiting how fast it can spin (summary: <https://oikofuge.com/matthews-tumbling-toast>). Gap: I did not open the full paper, so the model's equations are unchecked here.
   - What fixes the number of turns, and does the butter matter? Inference from that model plus one calculation of mine: a fall of 0.76 m takes t = sqrt(2h/g) = sqrt(2 x 0.76 / 9.81), about 0.39 s. A rotation rate set by the edge and friction gives about half a turn in that time. Gap: whether the mass of the butter shifts the result is an assumption without evidence in what I read; I expect it to be small, but I did not check.
   - Is the "always" real? Assumption without evidence: that people remember butter-side down landings and forget butter-side up ones, which would make the pattern look stronger than it is. Gap: no count of remembered versus actual landings.

4. What is the answer, at the strength the evidence supports, to why buttered toast falling from a table lands butter-side down?

   Likely because of the mechanism above. A slice pushed off a table edge tips and spins as it leaves, and the fall from about 76 cm is too short for it to complete more than roughly half a turn. It starts butter-side up, so it ends butter-side down. The published estimate, as quoted in a search snippet of the 1995 paper, is that a table near 3 m high would give the toast time for a further half-turn (<https://www.researchgate.net/publication/230693562_Tumbling_toast_Murphy's_Law_and_the_fundamental_constants>). That figure I did not check against the paper itself.

   "Always" is too strong. The tendency holds for tables of ordinary height and for slices that start butter-side up. Toast that starts butter-side down, that leaves a hand, or that falls from a much greater height lands differently. I am unsure whether the mass of the butter shifts the result, and unsure how much remembering the annoying landings adds.

5. Does the question about buttered toast falling from a table imply a request for action, and if so, what course should be proposed?

   Skipped: The question asks why, not what to do. It names no toast about to fall and no goal such as saving the toast.

---

### ask-respond · toast butter side down · 2026-09-29 23:09 UTC

Not saved: no store here. Keep the record below as `ask-respond_20260929T230917Z_toast-butter-side-down.jsonl`.

**Results**

- Buttered toast falling from a table usually lands butter-side down because it tips off the edge, turns about half a revolution in the 0.39 s fall, and started butter-side up; "always" is too strong.

```jsonl
{"kind": "run", "at": "2026-09-29T23:09:17Z", "skill": "ask-respond", "topic": "toast-butter-side-down", "subject": "Why does toast always land butter-side down?", "project": "", "resumed": false}
{"kind": "given", "at": "2026-09-29T23:09:17Z", "text": "The toast is buttered on one face and starts butter-side up", "source": "implied by the question; the asker did not state it"}
{"kind": "given", "at": "2026-09-29T23:09:17Z", "text": "The toast falls from ordinary table height, about 76 cm", "source": "assumed; the asker did not state it"}
{"kind": "given", "at": "2026-09-29T23:09:17Z", "text": "\"Always\" is the asker's word and may overstate the pattern", "source": "my reading of the question"}
{"kind": "question", "at": "2026-09-29T23:09:17Z", "id": "question-1", "text": "Why does a slice of buttered toast that falls from a table to the floor land butter-side down?"}
{"kind": "question", "at": "2026-09-29T23:09:17Z", "id": "question-2", "text": "Which assumptions does that question carry, and which sub-questions must be answered first: whether butter-side down is in fact the usual result, what motion the falling toast makes, and what fixes how far it turns before it lands?"}
{"kind": "question", "at": "2026-09-29T23:09:17Z", "id": "question-3", "text": "What does each of those sub-questions' answers rest on: direct observation, documentation, inference, or assumption without evidence, and where are the gaps?"}
{"kind": "question", "at": "2026-09-29T23:09:17Z", "id": "question-4", "text": "What is the answer, at the strength the evidence supports, to why buttered toast falling from a table lands butter-side down?"}
{"kind": "question", "at": "2026-09-29T23:09:17Z", "id": "question-5", "text": "Does the question about buttered toast falling from a table imply a request for action, and if so, what course should be proposed?"}
{"kind": "answer", "at": "2026-09-29T23:09:17Z", "q": "question-1", "text": "A slice that slides off a table edge tips as it goes, turns about half a revolution during the fall, and lands with the face that began up now facing down; the fall from table height is too short for a second half-turn.", "by": "the assistant"}
{"kind": "answer", "at": "2026-09-29T23:09:17Z", "q": "question-2", "text": "Assumptions: that \"always\" holds, that the toast starts butter-side up, that the fall is from table height. Sub-questions: whether butter-side down is the usual result, what motion a slice makes off an edge, what fixes the number of turns and whether the butter matters.", "by": "the assistant"}
{"kind": "answer", "at": "2026-09-29T23:09:17Z", "q": "question-3", "text": "Usual result: documentation (1995 Eur. J. Phys. abstract; American Journal of Physics snippet). Motion: documentation summary of the 1995 model, full paper not opened. Number of turns: inference plus a calculation of fall time, about 0.39 s. Butter mass and remembered landings: assumption without evidence.", "by": "the assistant"}
{"kind": "answer", "at": "2026-09-29T23:09:17Z", "q": "question-4", "text": "Likely because the slice tips off the edge, turns about half a revolution in the short fall, and started butter-side up; \"always\" is too strong, and the effect of butter mass and of selective memory is unsettled.", "by": "the assistant"}
{"kind": "skip", "at": "2026-09-29T23:09:17Z", "q": "question-5", "reason": "The question asks why, not what to do, and names no goal such as saving the toast."}
{"kind": "result", "at": "2026-09-29T23:09:17Z", "text": "Buttered toast falling from a table usually lands butter-side down because it tips off the edge, turns about half a revolution in the 0.39 s fall, and started butter-side up; \"always\" is too strong."}
```
