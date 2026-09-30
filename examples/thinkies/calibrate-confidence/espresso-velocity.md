# calibrate-confidence: the espresso machine and team velocity

- skill: calibrate-confidence, from commit 0c9258f
- subject: "The new espresso machine is why the team ships faster." (Since it arrived three weeks ago, the team closed 30% more tickets; a new hire also started that month.)
- kind: single run

## Prompt

/calibrate-confidence "The new espresso machine is why the team ships faster." (Since it arrived three weeks ago, the team closed 30% more tickets; a new hire also started that month.)

## Run

### 1. Identify the claim

The claim is causal: the espresso machine is the reason, or the main reason, the team ships faster. It has two parts that carry different weight:

- Part A, the observation: the team closed 30% more tickets in the three weeks since the machine arrived than before.
- Part B, the attribution: the machine caused that rise.

The word "why" makes Part B the claim. Part A is only the evidence offered for it.

### 2. Name confidence explicitly

- Part A, that the count rose 30%: moderately confident (60-80%), because it is a reported figure I have not seen the counting behind.
- Part A read as "the team shipped faster": uncertain (40-60%). Tickets closed is a count of closures, and closures can rise while shipped value stays flat (smaller tickets, split tickets, a backlog cleanup).
- Part B, that the machine is why: low confidence (below 40%). My honest figure is about 5-10% that the machine is the main cause, and somewhat higher, perhaps 20-25%, that it contributes something measurable.

The confidence is not uniform, so I report it in those three pieces and not as one number.

### 3. Inventory the evidence

- Direct observation: none of mine. Everything reaches me as a report in the prompt.
- Documentation or authoritative sources: none. No ticket export, no period definition, no baseline series.
- Logical reasoning from established facts: one valid step. If tickets closed rose after the machine arrived, then the machine's arrival is compatible with the rise. Compatibility is all the timing establishes.
- Inference or analogy: the rest. "Came after, so caused by" is inference from sequence alone.
- Assumption without evidence: that three weeks is a representative window, that "more tickets" tracks "faster shipping", that no other cause was at work.

The evidence-backed share is small: one reported number and one timing fact. The assumption share is large, and it carries the causal step.

A competing cause sits in the prompt itself: a new hire started the same month. That is a second candidate that arrived in the same window, and the data as given cannot separate the two. Other candidates the prompt does not mention but that fit the same window include a sprint boundary or release deadline, a quarter-end push, a change in how tickets are sized or split, seasonal workload, and ordinary week-to-week variation, which for a small team over three weeks can easily be 30% by chance.

Mechanism plausibility also matters and is weak here. A machine could raise output through less time away from the desk, a social hub, or a mood lift. Each is possible and small, and none by itself predicts a 30% step within three weeks. A new person doing tickets predicts a rise directly, in the same direction, on the same timescale, though a new hire usually costs the team throughput at first through onboarding and review load, so that story is also not clean.

### 4. Check for overconfidence

The original sentence commits it. Its markers:

- A definitive "is why" on limited data: one team, one three-week window, one before-and-after comparison, no control.
- Uncertainty suppressed to sound authoritative: the sentence carries no hedge, and the new hire, which the speaker knows, is left out of the sentence and mentioned only in brackets.
- Sequence presented as mechanism: "since it arrived" turns temporal order into cause.

No "obviously" or "clearly" appears, but the flat declarative does the same job.

In my own reasoning, one pull toward overconfidence: the machine story is fun and easy to picture, and vividness raises felt confidence without adding evidence. I set that aside.

### 5. Check for underconfidence

Care in the other direction. The correct reading is not "we know nothing".

- The rise, if real, is real. A 30% change is large enough that dismissing it as noise would be habit, not judgment, though three weeks of a small team's counts is a noisy series.
- The machine is not ruled out. Cheap small comforts do sometimes shift a team's output, and I would not give it 0%. I hold it as a contributor with a low, nonzero weight.
- The new hire being a candidate does not make them the answer either. Two candidates does not mean each has 50%.

So I keep the low confidence in Part B because the causal step has nothing under it, and I keep the moderate confidence in Part A because a report of a number is worth something. I am not hedging Part A out of habit.

### 6. Test calibration

Betting test. What odds would I accept?

- On "the machine is the main cause": I would take a bet paying 15 to 1 against it, and decline one paying 5 to 1. That places my credence between roughly 6% and 17%, consistent with the 5-10% figure, drifting up if the machine is the only change nobody has controlled for.
- On "the rise persists at 30% over the next six weeks": near even, perhaps 35-45%, since early jumps after a change often regress toward the earlier level.
- On "the count has risen at all, by a margin beyond usual weekly variation": about 65%, pending the baseline.

What would change the level:

- Upward on the machine: the rise is spread across everyone including people who do not drink coffee, the rise began within days of the machine and not of the hire, an earlier period with a comparable ticket count and no rise, or a reversal if the machine is removed.
- Upward on the hire: the new hire's own closed tickets account for most of the delta. That is checkable directly from the tracker, and it is the single fastest test available.
- Downward on both: ticket-size or splitting changes, a sprint boundary inside the window, a release deadline, or a prior period showing similar swings without any cause.
- Downward on Part A: a different definition of "closed" (auto-closed stale tickets, bulk closures) in the recent period.

Track record: claims of the form "X happened, then Y improved, so X caused Y" resolve against the claim more often than for. Post-hoc attributions about team performance in particular run overconfident, and I adjust for that by staying below 10% on the machine as the main cause.

### 7. Communicate uncertainty

What I would say in place of the original sentence:

> The team closed about 30% more tickets in the three weeks since the machine arrived, if the figure holds up. A new hire also started that month, and the machine and the hire cannot be told apart from this data. I would put the machine as the main cause at roughly 5-10%, and as a small contributor somewhat higher. The claim that it is why the team ships faster is not supported yet.

Where certainty ends and speculation begins:

- Reasonably firm: a rise in tickets closed was reported, and the machine and the hire both arrived inside the window.
- Uncertain but checkable: whether the rise is real beyond normal variation, and whether "closed tickets" tracks "shipping faster". A tracker export answers both within an hour.
- Speculation: that the machine drives the rise. This is a hypothesis with no test run yet.

Personal ignorance versus collective uncertainty:

- Personal ignorance, closable by looking: the baseline series, how tickets are sized, who closed the extra tickets, whether the hire's tickets explain the gap, and what happened at the sprint boundary. I do not have these; the team does.
- Collective uncertainty, not closable by looking: whether a coffee machine can move team throughput at all, and by how much. Even with perfect tracker data, one team and one event give a correlation, and a cause needs a comparison: another team without the machine, or the same team before and after with the hire's effect removed.

Cheapest next step: split the tickets closed in the window by who closed them, and compare the same weeks for the previous two quarters. If the delta sits mostly with the new hire or is inside the usual weekly swing, drop the machine explanation. If the delta is broad across the team and the historical series is flat, the machine moves up, though still not to certainty.
