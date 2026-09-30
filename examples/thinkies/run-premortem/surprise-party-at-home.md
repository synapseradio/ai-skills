# run-premortem: surprise 70th birthday party at Grandpa's house

- skill: run-premortem, from commit 0c9258f
- subject: A surprise 70th birthday party for Grandpa, held in Grandpa's own house, while Grandpa is supposedly out at the barber for an hour.
- kind: single run

## Prompt

/run-premortem A surprise 70th birthday party for Grandpa, held in Grandpa's own house, while Grandpa is supposedly out at the barber for an hour.

## Run

The plan as stated has four parts: the party happens in Grandpa's house, guests arrive and set up while he is away, the barber trip is the cover story and lasts an hour, and Grandpa comes home to a surprise. Nothing else is stated, so anything beyond those four parts counts as not addressed by the current plan.

### 1. Assume failure

It is the evening after the party. The plan was carried out and failed catastrophically. The headline:

**"70th Birthday Surprise Ends in Ambulance: Grandpa, Home Early From Barber, Finds Twenty Strangers' Cars Blocking His Drive and a Crowd in His Dark Living Room"**

The failure has two layers. The surprise did not work, and something worse than a failed surprise happened, because the house was Grandpa's, the crowd was in it, and he is seventy.

### 2. Work backwards

What went wrong, walking back from the headline:

- Grandpa came home to a house full of people he had not expected, and the shock hurt him or upset him badly.
- He came home early, or he never left, or he came back in the middle of setup, so the moment he walked in was not the planned one.
- He had warning: he saw the cars, heard something, or was told by a guest, so the moment of surprise never came and the party started flat.
- The party ran over the hour, and the barber trip turned out to be the weakest part of the plan, because a haircut ends when the barber decides it ends.
- The guests were the wrong ones, or too many, or arrived in the wrong order, and the house could not hold them.
- The surprise landed, and it was unwelcome: he wanted to be at his own birthday quietly, not have his house taken over.

Each of these traces back to the plan resting on one uncontrolled event, the length and outcome of a haircut, and one unexamined place, a home he lives in and knows in detail.

### 3. Generate failure modes

Listed without censoring, by dimension.

**Technical**

- The barber runs ahead of schedule. Grandpa is done in thirty minutes.
- The barber is closed, fully booked, or shut that day, and Grandpa learns the barber trip was never real.
- Grandpa's phone rings with a guest calling or texting him, and the phone shows the party's group thread.
- A group chat notification or a photo is posted where he can see it, on a shared family tablet or a shared account.
- The doorbell camera, a smart speaker, or a neighbor's camera shows him or a family member the party gathering.
- Balloons, banners, or a cake are visible through the windows from the street.
- The house alarm or a smoke alarm goes off from cooking or candles, and the alarm company calls Grandpa.
- The house lacks the power, fridge space, or seating for the food and guests.
- A guest cannot get in: Grandpa's spare key is on his own keyring, and he took it to the barber.

**Human**

- A guest lets the secret slip to Grandpa in advance, out of excitement or a sense that a surprise might be unkind.
- A grandchild tells him. A child cannot keep a secret for a week.
- A guest arrives late, at the moment Grandpa arrives, and walks in behind him, or opens the door to him.
- A guest who does not know about the plan calls, visits, or drops by, and finds the house full.
- Grandpa's heart, blood pressure, or hearing makes a sudden loud "surprise" dangerous. A person recently unwell, on medication, or with an anxious condition reacts badly to a crowd shouting at him in his own home.
- Grandpa dislikes surprises, dislikes being the center of attention, or dislikes people going through his home.
- A relative he has a quarrel with attends, or a relative he wanted there is absent.
- Guests move, open, or break things in his house. Someone uses his bathroom, his kitchen, or his study, and something is damaged or found that he did not want found.
- A guest with an allergy, a dietary restriction, a mobility need, or a young child with a nap schedule has no plan made for them.
- Someone drinks and drives home.
- The barber, told of the plan, mentions it to Grandpa in the chair, or lets slip something like "Big day today."

**Process**

- No one is assigned to delay him. The person who took him to the barber has no instruction for what to do if the haircut ends early.
- No signal exists between the barber's shop and the house for "he's leaving now."
- No single person owns the schedule. Setup, cake, guests, and delaying tactics each have separate people.
- Setup takes longer than the hour, because nobody timed it, and food that needs cooking or a cake that needs collecting is not done.
- Guests arrive all at once, cars fill the street and drive, and setup is still going.
- Where guests park, hide, and wait is not decided.
- No plan exists for the moment of entry: who opens the door, where everyone stands, what happens if he walks in through the back door or the garage.
- No fallback exists if the surprise is spoiled, so the party goes on as a second-best version of itself, with everyone visibly disappointed.
- No one has asked Grandpa's household, a spouse or a live-in relative for one, whether the house may be used.
- The cleanup nobody planned falls on Grandpa the next morning.

**External**

- Weather delays or cancels the barber's appointment, or brings rain that puts guests and their wet coats indoors earlier than planned.
- Traffic delays a guest who is carrying the cake, or Grandpa's ride home takes a different route and passes guests arriving.
- A neighbor, seeing the cars, greets Grandpa in the street on his way in.
- A delivery arrives, or a meter reader, a salesperson, or a friend of his knocks on the door mid-party.
- Noise draws a complaint or a call to the authorities.
- A guest gets ill, or has an accident, at the house, in front of others.

**Timing**

- One hour is short for setup by a group and long for a barber trip that Grandpa might extend to chat or shop. The two estimates are independent, and the plan needs the first to be shorter than the second.
- The barber trip is the only thing with a start and end time; the guests' arrival times are unstated.
- The party happens at the hour of his usual nap, medication, or meal.
- The window is a fixed hour but Grandpa's return time is not fixed. Errands on the way back stretch or shrink it.
- Seventieth birthday falls on a date the day of which Grandpa already has plans, a call, or a visit.
- Guests need to leave before dark, or have a long trip, and the party's length is fixed by them.

### 4. Surface hidden assumptions

What the plan takes for granted, and the dependencies it does not show:

- **Grandpa wants a surprise.** The plan assumes he will be delighted and not distressed, and that surprise is the right form of the gift. Nothing in the plan says anyone asked how he feels about surprises.
- **Grandpa is well enough to be startled by a crowd.** The plan assumes his health can take a sudden entry.
- **The barber trip is a real appointment that takes one hour.** In fact the plan depends on a third party, the barber, whose timing and cooperation no one has secured.
- **Grandpa goes alone and comes straight back.** He may take a friend, run an errand, stop for a coffee, or walk.
- **He goes at all.** The plan assumes Grandpa needs a haircut and will keep the appointment.
- **The house is available and suitable.** It is assumed that its size, layout, parking, bathrooms, and chairs work for the guest list, and that Grandpa (and anyone he lives with) is fine with people in it.
- **Guests can enter.** Keys, a code, or someone inside at the door: none is stated.
- **Everybody can keep a secret for the whole lead-up.** The number of people who know is the number of chances it leaks.
- **He cannot see it coming.** The plan assumes windows, phones, neighbors, cameras, and familiar routine give nothing away.
- **The hour is enough.** The setup, guests' arrival, and hiding all fit inside the one hour, and Grandpa's return is not earlier.
- **The invisible dependency is the person with the delay tool.** Someone must be able to reach Grandpa, or the barber, or the house, in real time. The plan has no such person named.
- **The surprise, once landed, produces a good party.** Food, drink, seating, and speech are assumed to be there.

### 5. Group by theme

The failure modes cluster into six themes.

1. **Detection before the moment (the secret leaks).** Slips by guests, children, and the barber; phone and chat traces; visible cars and decorations; doorbell and neighbor sightings.
2. **Timing of Grandpa's return.** An early haircut, an errand, a route home, a missed appointment, and setup that runs over the hour.
3. **The moment of entry.** Guests arriving late or at the same moment, an unplanned door, no signal, and no plan for who stands where.
4. **Grandpa himself: health and preference.** Startle risk, dislike of surprises, and dislike of crowds in his home.
5. **The house as a venue.** Access, capacity, power, parking, damage, private rooms and belongings, and cleanup.
6. **Guests and logistics.** Allergies, mobility, alcohol, late arrivals, food and cake, and the people not invited or not told.

Underneath all six sits one shared root: the plan has one fixed event (one hour) resting on one variable (Grandpa's schedule) that nobody controls, and nobody has asked the person it is for.

### 6. Find the unaddressed

Measured against the four parts of the plan as stated, the following are not addressed. The four parts do address the cover story (the barber) and the venue choice (his house). Beyond those, everything below is open.

| Theme | Addressed by the current plan? | What is missing |
| --- | --- | --- |
| Detection before the moment | Partly: the cover story hides the setup | No rule about phones, chats, or who may know; no plan for cars or decorations; no plan for the barber |
| Timing of return | Barely: it names one hour and stops | No timing test of setup, no buffer, no live signal from the shop, no delay person |
| The moment of entry | No | No door plan, no signal, no rule for late guests |
| Grandpa's health and preference | No | No one has checked either |
| The house as a venue | Only by choosing it | No access plan, capacity check, parking plan, room boundaries, or cleanup |
| Guests and logistics | No | No guest list limits, dietary and access needs, alcohol plan, or food schedule |

Ranking by danger, meaning how likely it is and how bad the result:

1. **Grandpa's health and preference.** Unaddressed, and the worst outcome is harm to him. It costs one conversation with someone who knows him to check.
2. **Timing of return.** Unaddressed, very likely (a haircut ending early is ordinary), and the result is the exact scene in the headline.
3. **The moment of entry.** Unaddressed, and it decides whether the surprise works even if timing holds.
4. **Detection before the moment.** Partly addressed, and likely with many guests.
5. **The house as a venue.** Unaddressed but survivable.
6. **Guests and logistics.** Unaddressed but survivable.

### 7. Design interventions

Interventions for the most dangerous, each tied to the failure it prevents.

**Against harm and unwelcome surprise (theme 4)**

- Before anything else, ask one person close to Grandpa, a spouse, child, or doctor-aware relative, whether a surprise of this size is safe and welcome for him. If the answer is no or unsure, change the form: a small group, a warned "there's a dinner at your house tonight," or a party where he knows it is coming but not who is there.
- Cut the shout. Guests greet him quietly, or one at a time, or he is met at the door by one person he knows who walks him in. This removes the startle without removing the surprise.
- Choose a seat for him, a quiet room he can step into, and a person who is assigned to sit near him.

**Against the early return (theme 2)**

- Give the plan a delay person: one named relative or friend who goes with Grandpa or meets him after the barber, and has a second errand ready (a coffee, a stop at a shop, a "let me show you something") that adds thirty minutes.
- Tell the barber. The barber becomes an ally, holds the appointment slot, and sends a text to one named person the moment Grandpa is in the chair and again when he stands up.
- Set setup to finish thirty minutes before the earliest plausible return. Time it: a dry run of the setup, with a stopwatch, tells the real number. Then plan the party start around that.
- Move the guests' arrival before Grandpa leaves for the barber or use a different place for guests to wait: guests wait at a neighbor's house or a car park nearby, and come in only after the signal.

**Against the botched entry (theme 3)**

- Name one host at the door with a signal chain: barber text to a lookout at the window, lookout to the host, host to the room. Agree one word for "he is on the street."
- Write down the door plan: which door he uses, who opens it, where everyone stands, and what the lookout does if he comes by the garage or the back.
- Decide the fallback if the surprise is spoiled: the party turns into a warm "we could not keep it from you," with a line ready and a person to say it. The party never has to be a failure if the surprise is.

**Against the leak (theme 1)**

- Cap who knows, and tell the people who know only what they need. Children get a job (hide the cake) and a reason ("it's a secret game") and are told late.
- Take the planning off any thread Grandpa can see. Use a separate chat, and a cover name for the party.
- Park cars away from the house (a neighbor's drive, the next street), keep the curtains as they normally are, and put decorations up last.
- Tell the neighbors, so none greets him with "big party tonight!"

**Cheaper items for the remaining themes, done in one afternoon before the day**

- Find out how Guests get in (a spare key held by the host, not on Grandpa's keyring).
- Ask about dietary needs and mobility in the invitation.
- Name a person responsible for cleanup and for driving anyone who drinks.
- Close the doors of rooms guests should not enter, and put away anything private.

### Result

The plan as stated fails most likely where it is thinnest: it relies on a one-hour haircut that no one controls, and on a surprise that no one has checked with the person it is for. The two interventions that change the most are the first conversation, whether Grandpa can and would want this, and the delay person with a live signal from the barber. Everything else in the list makes the day smoother; those two decide whether it is a good day at all.
