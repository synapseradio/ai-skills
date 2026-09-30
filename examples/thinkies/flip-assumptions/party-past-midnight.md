# flip-assumptions: fun parties and midnight

- skill: flip-assumptions, from commit 0c9258f
- subject: "If the party is fun, people stay past midnight."
- kind: single run

## Prompt

/flip-assumptions "If the party is fun, people stay past midnight."

## Run

### 1. Identify the claim

The claim is "If the party is fun, people stay past midnight." It came in as the argument, so there is no need to look to the surrounding context.

### 2. Identify the conditional structure

The claim is already written as an explicit conditional, with one loose word to pin down.

- P: the party is fun.
- Q: people stay past midnight.

Made explicit: if P, then Q. Two words carry hidden quantifiers. "People" could mean every guest, most guests, or at least one guest. "The party" could mean any party or one particular party. I read it in the strongest natural form, which is also the form people say aloud: for any party, if it is fun, then guests remain after midnight.

### 3. Form the contrapositive

Negate both parts and reverse them.

- not-Q: nobody stays past midnight; the room is empty by twelve.
- not-P: the party is not fun.

Contrapositive: if everyone has left by midnight, then the party was not fun.

This says exactly what the original says. If a party emptied before midnight and was fun, the original is false. The same party is the counterexample to both forms.

The trap in this step is the converse, "if people stay past midnight, the party is fun". That is a different claim. It is not equivalent, and it is not what the subject said. I keep it out of the analysis except where it explains why the original sounds truer than it is.

### 4. Compare verification difficulty

The original needs P, and P is "fun". Fun is felt by each guest privately, differs from guest to guest, and can only be measured through proxies. The likely proxies are laughter, dancing, and guests saying they had a good time. One of the common proxies for fun is guests staying late, which is Q. Testing the original with that proxy means testing Q against Q, so the test cannot fail.

The contrapositive needs not-Q, which is a headcount at midnight. Anyone with a clock and a doorway can observe it, and two observers will agree. It also needs not-P, "the party was not fun", but that only arrives after not-Q is observed, and the claim asks us to accept it.

Which form is easier to test? The contrapositive. The way to test it is to find a party where the room emptied before midnight and ask whether it was fun by a measure independent of departure time: guests' accounts the next day, whether they came back for the next party, what they were doing at ten o'clock. One countable observation (the emptied room) leads to a question about fun that can be asked separately.

### 5. Surface hidden assumptions

The contrapositive puts the load on "left by midnight" and makes each reason for leaving visible. The original hid them behind "if the party is fun".

- Guests are free to stay. Babysitters, last trains, early shifts, and rides that leave at eleven all remove people from the room without touching how much they enjoyed it.
- Midnight is reachable. A party that starts at eleven at night, or one held at a venue that closes at eleven, cannot pass the test however fun it is.
- Fun is the only force acting on departure. The contrapositive reads "everyone left" as evidence against fun, which assumes nothing else pushes people out.
- The guests are the kind who stay late for anyone's party. A gathering of parents with young children or of people up at five the next morning empties early whatever happens.
- Staying is voluntary. In the original, "people stay" sounds like a choice. Without a ride home, a guest can stay past midnight at a dull party, which is the converse problem; it does not damage the original but it damages the proxy in step 4.
- The claim is much stronger than it sounded. Spoken aloud it is a rule of thumb ("good parties run late"). Written as a conditional it is a sufficiency claim: fun alone guarantees late staying. The contrapositive reads it as a necessity claim: an early exit rules out fun. That is far more than a rule of thumb can carry.

### 6. Test both directions

Original: fun party, so people stay past midnight. Evidence in favor: the common experience of a good night running long. Evidence against: any fun party held for people with constraints. A child's birthday party is often at its happiest at four in the afternoon and over by six. A wedding with grandparents present often loses its older guests by ten, with the dance floor still full. A weeknight dinner party can be excellent and end at half past ten because Tuesday exists.

Contrapositive: nobody stayed past midnight, so the party was not fun. Evidence in favor: a party that empties early because the music died, the food ran out, and the conversation stalled. Evidence against: the same three parties above. Each one emptied before midnight, and by the measure in step 4 (guests' accounts, return visits) each was fun.

The contrapositive is plainly false for the child's birthday party. The skill's rule applies: since the contrapositive fails, the original fails, and here it failed faster. "That party was over by six and nobody remembers it as anything but a great day" settles the matter in one sentence, where refuting the original directly meant hunting for a fun party that ended early.

What survives is a weaker claim. "Among parties where guests are free to stay and midnight lies inside the party's hours, fun raises the chance that some guests stay past midnight." That statement carries every hidden assumption from step 5 as a stated condition, and it is a probabilistic claim rather than a guarantee. The original, as a universal conditional, does not hold.
