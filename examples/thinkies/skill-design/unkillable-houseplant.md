# skill-design: a skill for picking a houseplant you will not kill

- skill: skill-design, from commit 0c9258f
- subject: Design an Agent Skill that helps someone pick a houseplant they will not kill.
- kind: staged conversation (the user side played by a second agent)

## Prompt

/skill-design Design an Agent Skill that helps someone pick a houseplant they will not kill.

## Run

**Skill:** **Mode.** No SKILL.md exists yet and the request is an idea to turn into a skill, so this is Design mode. Design ends at a design brief that whoever runs skill-creator next can build from. It never includes the SKILL.md itself. Move 1 of 6 is under way: surface the intent, then confirm it with you before moving on.

**Move 1: the intent, as I currently read it.** This is a proposal for you to correct, not a decision.

Tasks where invoking the skill helps:

- Someone standing in a nursery, a store, or a plant-swap asks what to buy, and wants a plant that survives their habits.
- Someone who has killed plants before wants to know which plant fits how they actually live: how much light their room gets, how often they are home, how often they remember to water.
- Someone is choosing between two or three specific plants and wants to know which one is more forgiving for them.

Trigger phrasings the description should catch:

- "what houseplant can't I kill"
- "I kill every plant I own, what should I get"
- "best low-maintenance plant for my apartment"
- "help me pick a plant for a dark room"
- "which of these plants is easier"

Near misses that must not trigger:

- Rescuing a plant that is already dying ("my pothos has yellow leaves"). That is diagnosis of a live plant, a different job from choosing one.
- Outdoor gardening, vegetable growing, or landscaping.
- Identifying an unknown plant from a photo.
- General plant-care schedules for a plant the person already chose.

The design question underneath: the skill has to turn "a plant I will not kill" into something an executor can decide. The candidate generator is that plants die from a mismatch between what the plant needs (light, water interval, humidity, temperature) and what the person's home and habits supply. Every recommendation then follows from two facts the skill collects: what the space gives, and how the person behaves. The skill would collect those facts and match them, rather than hand out a fixed list of "hardy plants".

**The question I need answered before Move 2 (reading what exists).** The intent above rests on one reading of "will not kill" that only you can settle. I see two readings, and they build different skills.

1. **Match the plant to the home and habits.** The skill asks a few questions (window direction, hours of light, how long the person is away, whether they tend to overwater or forget, pets or small children) and recommends plants whose needs sit inside what that person supplies. It builds a short intake, a matching rule, and a reference of plants with their needs. It expects the user to answer honestly about their own habits. That expectation is implicit today, and the skill has to state it.
2. **Name the most forgiving plants, with no intake.** The skill hands over a ranked short list of tolerant plants (the kind that survive low light and missed waterings) with one line on each. It builds a single reference and no questions. It expects nothing of the user beyond reading, and it fails for anyone whose home falls outside what those plants tolerate, such as a windowless room.

I recommend reading 1. The ground: the skill's stated purpose is a plant the person will not kill, and survival depends on the match between plant and person, so a fixed list fails exactly the people who killed a "hardy" plant before. Reading 2 is cheaper to build and easier to keep correct, and it is the right choice if you want the skill to stay a single lookup.

Also confirm or correct the rest of the intent:

- Are the tasks, trigger phrasings, and near misses above the right edges? In particular, should rescuing a dying plant stay out, as proposed?
- Should pet safety be part of the choice (some common houseplants are toxic to cats and dogs), or is that outside this skill?

Your answer on the reading decides the structure sketch, the floor, and what the brief marks as fixed, so I have stopped here. Moves 2 through 6 (read what exists, research if you ask for it, choose the floor, decide what stays fixed, write the design brief) wait on your answer, and no design brief or skill files have been written.

**User (played):** Yes to option 1, and yes, those edges sound right: no rescuing dying plants. Pet safety should definitely be part of the choice, since I have a cat. Beyond that, you decide.

**Skill:** Intent confirmed: reading 1, pet safety in, rescue of a dying plant out. I searched the skills installed here and found none about houseplants or plant care, so there is no overlap to narrow, extend, or replace.

Next is the ground the skill will stand on. The matching rule needs facts about plants: light needs, how long each tolerates dry soil, which are toxic to cats. I can research those now and bring sourced findings plus a list of what stayed unverified into the brief. Or I can skip research, and then every plant fact stays marked unverified in the brief's open questions, and whoever builds the skill must verify them before encoding any. Research costs more time now. Skipping leaves the plant reference unbuildable until someone does it, and a wrong toxicity claim reaches a real cat.

I recommend researching, at least the cat-toxicity facts, since a wrong claim there does harm. Should I research, and if so, everything or only the pet-safety facts?

**User (played):** Yes, research it. Do everything, not just the pet-safety facts, since I'd rather the plant reference be right the first time. If you have to choose, do the cat toxicity first.

**Skill:** Research bound: the questions I must answer to fill the brief are (a) which plants are both forgiving and cat-safe, from the authority on cat toxicity; (b) what light and watering tolerance each candidate has, from a university extension source; (c) the live home of each fact. I read the artifacts, not summaries of them, and stopped once those three were answered.

### Research findings

Cat toxicity, from the ASPCA plant pages (the authority; the executor points at them and never restates them from memory):

- Spider plant, Chlorophytum comosum: "Non-Toxic to Dogs, Non-Toxic to Cats". <https://www.aspca.org/pet-care/aspca-poison-control/toxic-and-non-toxic-plants/chlorophytum>
- Cast iron plant, Aspidistra elatior: "Non-Toxic to Dogs, Non-Toxic to Cats, Non-Toxic to Horses". <https://www.aspca.org/pet-care/aspca-poison-control/toxic-and-non-toxic-plants/cast-iron-plant>
- Snake plant, Sansevieria trifasciata: "Toxic to Dogs, Toxic to Cats" (toxic principle: saponins). <https://www.aspca.org/pet-care/aspca-poison-control/toxic-and-non-toxic-plants/snake-plant>
- ZZ plant, pothos, peace lily, and philodendron: listed by the ASPCA among houseplants that can cause trouble for pets. <https://www.aspca.org/news/these-houseplants-can-cause-trouble-your-pets>
- The ASPCA's per-species cat list is the live home for every other plant: <https://www.aspca.org/pet-care/animal-poison-control/cats-plant-list>

Light and watering tolerance, from Iowa State University Extension, "Easy Low-Maintenance Houseplants" (<https://yardandgarden.extension.iastate.edu/how-to/easy-low-maintenance-houseplants>). The page chooses plants that tolerate a wide range of light, inconsistent watering with dry soil, and low humidity:

- Snake plant: "Grow in low to direct light"; allow soil to dry between waterings; "The only way to kill this plant is to overwater it!"
- ZZ plant: "do exceptionally well in low light"; "very tolerant of dry conditions and low humidity".
- Spider plant: "adaptable to various environmental conditions but prefers indirect light, average moisture".
- Pothos: low to moderate light; allow soil to dry moderately between waterings.
- Cast iron plant: listed as tough. The passage on its light and water needs was cut off in my extract.
- Peperomia: tolerates neglect but rots if overwatered. Ponytail palm: tolerates dry conditions, avoid overwatering. Peace lily: keep soil moist; wilts when dry, revives after watering.

What the findings change about the design:

- Two of the three plants most lists call "unkillable" for low light and missed watering, snake plant and ZZ plant, are cat-toxic per the ASPCA. For a cat owner, the fixed-list reading (option 2) would have recommended a toxic plant. This confirms reading 1 and makes pet safety a hard filter applied before any matching, not a preference.
- The failure mode named for the most forgiving plants is overwatering. A person who kills plants by attention, not neglect, needs the intake to ask about that habit, and the reference to state each plant's overwater risk.

### Claims kept but unverified

- Cat toxicity of ZZ plant, pothos, peace lily, and philodendron: I saw them named in the ASPCA houseplant news list, and did not open each species page for the exact toxicity wording.
- Cat toxicity of peperomia, ponytail palm, and dragon tree: not checked.
- Cast iron plant light and water needs: extract truncated, so only the ASPCA safety line is verified.
- Spider plant's stated tolerance (indirect light, average moisture) is narrower than the tolerance of snake plant or ZZ, so whether it suits a dark north-facing room is not established by this source.
- The Agent Skills specification and Anthropic's skill best practices, cited in the skill's own principles, were not re-read in this run.
- The extension source is one page from one university. No second source corroborates the light and water figures.

### Questions I could not answer

- Where should the plant table's toxicity column live: stored in the skill with a source link per row, or looked up at run time from the ASPCA list?
- How many plants must the reference hold before the matching rule has real choices in a dark room and for a person who overwaters?

### Moves 4 and 5, decided

**Floor (move 4).** The weakest executor the skill must work on can ask the user questions one at a time, read a reference table, and apply a stated exclusion before ranking. It cannot be assumed to browse the web. That choice shapes the design: toxicity has to sit in the reference, with its source link per row, because a floor with no web access cannot look it up at run time.

**Fixed and open (move 5).**

- Fixed: reading 1, an intake followed by a match. Pet safety as a hard exclusion applied first. Rescue of a dying plant, outdoor gardening, and photo identification out of scope.
- Fixed: the intake asks what the space supplies and how the person behaves, including whether they tend to overwater or forget, and the executor is told the answers are the person's own report of habits.
- Open to each session: which two to five plants to recommend, their order, and the wording to the person.
- The fixed decision most likely to need revisiting: storing cat toxicity in the skill's reference. The sign that would show it: the ASPCA changes or corrects a listing, or a maintainer finds a stored row that disagrees with the live page.

### The design brief

**Intent**

- Tasks served: choosing a houseplant to buy for a home and habits the person describes, including comparing two or three named candidates, and including a household with a cat or dog.
- Trigger phrasings: "what houseplant can't I kill", "I kill every plant I own, what should I get", "best low-maintenance plant for my apartment", "help me pick a plant for a dark room", "which of these plants is easier", "a plant that is safe for my cat".
- Near misses that must not trigger: rescuing a plant that is already dying, outdoor gardening or vegetables, identifying a plant from a photo, care schedules for a plant already chosen.

**Floor**

The weakest declared executor asks one question at a time, reads a reference table, quotes a row, and applies a stated exclusion before ranking. It has no guaranteed web access. Reasoning: the intake, the exclusion, and the ranking are each a step the floor can walk from a table without deriving anything, and the one fact that harms if wrong (toxicity) must not depend on a lookup the floor may not be able to make.

**Sources of truth**

- Cat and dog toxicity: the ASPCA plant pages, with the per-species cat list as the live home (<https://www.aspca.org/pet-care/animal-poison-control/cats-plant-list>). Each reference row carries its species page link. Where the skill and the page disagree, trust the page and say so to the person.
- Light, watering, and humidity tolerance: Iowa State University Extension (<https://yardandgarden.extension.iastate.edu/how-to/easy-low-maintenance-houseplants>) for the plants it covers. Each fact has one home, the reference table. The body points at the table and never restates a row.
- The person's own home and habits: collected in the intake and never assumed.

**Structure sketch**

- Description: what the skill does, the trigger phrasings, and the near misses (rescue, outdoor, identification), because selection happens from the description alone (principle 1, schedule the workspace).
- Body: the flow, in order. Intake, apply the pet exclusion, match on light and watering, recommend two to five plants with the reason each fits, state the exit (the person has a short list and knows what each asks of them). A pointer to the reference and the reading condition for it.
- Reference, plants: one row per plant with light range, dry-soil tolerance, overwater risk, cat and dog toxicity, and the ASPCA page link. Loaded only at the match step.
- Reference, intake: the questions, each with what the answer excludes or changes. Loaded at the start.
- Scripts: none proposed. The pet exclusion and the light and water filter are a table lookup the floor can do; a script would help only if the table grows large enough that the executor drops rows (an open question below).

**Fixed decisions**

- Fixed: the six items under "Fixed and open" above, and the floor.
- Open to each session: the number of plants recommended, their order, the person's wording.
- Revisit sign: the stored toxicity column disagrees with the live ASPCA page, or a new listing appears for a plant in the table.

**Checks**

- Cat-safety exclusion: a case with a cat and a dark room must never return snake plant, ZZ plant, or pothos. This is an invariant, so inspect it on every run of a fixed set of pet cases, and it belongs beside a check, not in a shared list of rules.
- Fit: for a person who overwaters, the recommendation must name the overwater risk of each plant. This is an obligation at the recommendation step.
- Trigger: the description must fire on the five phrasings and stay silent on the four near misses. Trigger queries and the harness belong with skill-creator.
- Ranking order and wording: preferences; watch across repeated runs.

**Open questions**

- Cat toxicity of ZZ plant, pothos, peace lily, philodendron, peperomia, ponytail palm, and dragon tree needs the individual species page opened before any row is written.
- Cast iron plant light and water needs need a re-read of the source page.
- One extension page is the only source for light and water figures; a second source would corroborate them.
- The Agent Skills specification and best practices pages were not re-read; the builder should confirm frontmatter constraints against them.
- Whether toxicity stays stored in the skill or moves to a run-time lookup depends on whether the target deployments give the executor web access.
- Dog toxicity is covered only where a source above states it; a household with a dog needs the same per-row verification.
- The size of the plant table that keeps matching useful, and the point where a script replaces prose filtering.

The brief is the exit artifact for Design mode, and it holds every field the mode specifies. Whoever runs skill-creator next can answer its intake questions from it. No SKILL.md was written, by design.
