# Signal Confidence

Match certainty language to evidence strength, signaling what you know, how you know it, and what would increase confidence.

## Diagnostic Question

Ask: For each claim, what is the evidence foundation—verified, inferred, speculated?
Does the certainty language reflect that foundation? Where does absolute language describe inferred content? Where does hedging obscure solid evidence?

## Instructions

1. **Assess evidence foundation** - Examine what each claim rests on: verified documentation, direct observation, current measurement, reliable inference from data, reasoning from partial information, or speculation by analogy.

2. **Use evidence-matched qualifiers** - State documented facts and verified observations directly. Use "likely" or "appears to" for strong inferences from data. Use "possibly" or "might" for reasoning from partial information. Use "one possibility" or "speculatively" for analogical thinking.

3. **Calibrate absolute language** - Find where absolute terms describe inferred or remembered content. Transform "this framework lacks feature X" to "this framework lacked X in version 3.2, but current versions may differ" when certainty comes from outdated memory.

4. **Strengthen well-supported claims** - Detect rhetorical hedging on solid evidence. When data supports a claim directly, state it directly. Transform "perhaps we could consider denormalizing this table" to "denormalize this table" when measurements show 90% of queries would benefit.

5. **Separate mixed-certainty components** - Split complex claims where different parts carry different evidence. State "Error X occurs in middleware Y (confirmed from logs). The pattern suggests edge case Z triggers it, though the exact condition remains unidentified" rather than hedging all components uniformly.

6. **Make uncertainty actionable** - Express uncertainty by stating boundaries: what is known, what remains unknown, why uncertainty exists, what would resolve it. Transform "uncertainty about scaling" to "This handles current 100-user load (tested). Whether it scales to 10K users is uncertain without load testing that workload."

## Examples

### Calibrating outdated certainty

**Draft**: "This library doesn't support async callbacks in version 3.x."

**Evidence check**: Memory from working with version 3.2 six months ago. The library is actively maintained.

**Revised**: "I recall this library lacking async callback support in version 3.2. Current versions may have added this feature—verification against recent documentation would confirm."

The revision signals: I have relevant experience (past tense), current state is uncertain (modal verbs), verification would resolve it (explicit path).

### Strengthening well-supported claims

**Draft**: "It might perhaps be worth considering that we could possibly benefit from denormalizing the user preferences table."

**Evidence check**: Query patterns show 90% of user preference access occurs during profile loads. Denormalizing eliminates a join on every profile page load. This is measured data, not speculation.

**Revised**: "Denormalize the user preferences table. Query measurements show 90% of preference access occurs during profile loads—denormalizing eliminates this join and reduces page load time."

The hedging (might, perhaps, possibly) was rhetorical habit, not epistemic uncertainty.

### Making uncertainty actionable

**Draft**: "I'm not sure if that will help."

**Revised**: "This optimization reduces memory allocations, which appear in our profiles. Whether allocation is the primary bottleneck or a minor factor remains uncertain without benchmarking. A benchmark against the current hot path would show whether the magnitude of improvement justifies the effort."

Actionable uncertainty states: what's certain (mechanism), what's uncertain (magnitude), why (no measurement), resolution (benchmark).
