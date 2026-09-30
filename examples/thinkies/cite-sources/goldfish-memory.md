# cite-sources: goldfish and the three-second memory

- skill: cite-sources, from commit 0c9258f
- subject: Find and validate sources for the claim "goldfish have a three-second memory."
- kind: single run

## Prompt

/cite-sources Find and validate sources for the claim "goldfish have a three-second memory."

## Run

Format: technical discussion, so simple references with working URLs. Each URL below was retrieved and read this task. Sources are listed with what came from each one and which claim depends on it. Analysis is marked separately.

### Claim under test

"Goldfish have a three-second memory."

### Sources consulted

**1. Live Science, "Do goldfish really have a 3-second memory?"**
<https://www.livescience.com/goldfish-memory.html>
Resolves (HTTP 200); full text extracted and read.

- Information taken: The article calls the three-second figure "a complete myth" and quotes Culum Brown, a fish-cognition researcher at Macquarie University, saying goldfish memory spans "weeks, months and even years" and that the science has existed "since the '50s and '60s." Brown also says the myth's number varies by place ("In some places, it's 2 seconds, and in others, it's 10"), and describes food-conditioning experiments in which goldfish learned to stay at the feeding side of a tank and to prefer a rewarded paddle colour "long after the experiment is finished."
- Claims that depend on it: the three-second figure is unsupported; goldfish memory lasts at least days to weeks; the figure has no single origin in the literature.
- Kind of source: news article quoting one named expert. It reports experiments; it does not present them.

**2. Gee, Stephenson and Wright (1994), "Temporal discrimination learning of operant feeding in goldfish (Carassius auratus)," Journal of the Experimental Analysis of Behavior 62(1), 1-13**
<https://researchportal.plymouth.ac.uk/en/publications/temporal-discrimination-learning-of-operant-feeding-in-goldfish-c>
Resolves (HTTP 200); abstract read. The DOI link (<https://doi.org/10.1901/jeab.1994.62-1>) returned HTTP 403 to a scripted request, so the university record is the citation I am relying on.

- Information taken: Eight goldfish were trained to press a lever that released food. The feeding window was narrowed until food was available one hour in every 24, and that schedule held for 4 weeks. When the dispensers were switched off, the fish's responding still anticipated the feeding time, and the pattern "persisted for a limited number of days" during 6 days of extinction. A second experiment found the same timing under continuous light.
- Claims that depend on it: goldfish retain a learned association over weeks and act on a time of day.
- Kind of source: the peer-reviewed abstract. I read the abstract only, not the full paper.

**3. The Times, "Goldfish pass memory test"**
<https://www.thetimes.com/travel/destinations/uk-travel/england/london-travel/goldfish-pass-memory-test-p830bt00sh7>
Resolves (HTTP 200); article text extracted and read.

- Information taken: Press coverage of the Plymouth work says scientists "claimed not only that goldfish have a memory span of up to three months, but that they can also tell the time," and describes the fish as "previously believed to have a memory of just a few seconds."
- Claims that depend on it: the "up to three months" figure, and that the three-second belief predates the research.
- Kind of source: newspaper report. The page carries no date in the extracted text.

**4. A student science-fair study in the American Museum of Natural History's Young Naturalist Awards, "Goldfish as a Model for Understanding Learning and Memory: More Complex Than You Think"**
<https://www.amnh.org/learn-teach/curriculum-collections/young-naturalist-awards/goldfish-as-a-model-for-understanding-learning-and-memory-more-complex-than-you-think>
Resolves for a browser-style extraction tool (full text read). A plain scripted request returned HTTP 403, which reads as bot blocking rather than a dead page.

- Information taken: Goldfish were trained to find food in a maze, then retested after absences. Average times to find the food were 189.58 seconds at one month and 36.35, 32.00, 29.85 and 12.82 seconds at two, three, four and six months, against 410.05 seconds on the first training day (all improvements reported at p < 0.0005). The author also notes that the literature review turned up goldfish memory "frequently and often deridingly characterized as lasting three seconds."
- Claims that depend on it: recall after months is measurable in a simple maze.
- Kind of source: an award-winning student project published by a museum. It is a small study and is not peer reviewed.

**5. Shinozuka, Ono and Watanabe (2013), "Reinforcing and discriminative stimulus properties of music in goldfish," Behavioural Processes 99, 26-33, as quoted in the Annals of Improbable Research newsletter**
<https://improbable.com/wp-content/uploads/2024/10/Ig-and-beyond-20-4.pdf>
Resolves for an extraction tool (text read); a plain scripted request returned HTTP 403. The publisher page (<https://www.sciencedirect.com/science/article/abs/pii/S0376635713001228>) returned HTTP 403 to a scripted request and to the extraction tool, so it is not cited as a validated source.

- Information taken: The newsletter quotes the authors' abstract. Goldfish "were successfully trained to discriminate between two pieces of music," Bach's Toccata and Fugue in D minor and Stravinsky's The Rite of Spring. In a second experiment the goldfish "did not show consistent preferences for music."
- Claims that depend on it: goldfish can learn and act on a fine auditory discrimination.
- Kind of source: a secondary reprint of the abstract. I did not open the journal article.

### Source material against synthesis

**What the sources state.**

- According to Live Science, the three-second figure is a myth, and goldfish memory runs to weeks, months and years.
- According to the Plymouth abstract, goldfish fed for one hour a day over 4 weeks anticipated the feeding time, and kept doing so for several days after the food stopped.
- According to the Times, the Plymouth researchers reported a memory span of up to three months.
- According to the museum-hosted student study, fish retested after six months found food faster than on their first training day.
- According to the quoted abstract, goldfish learned to tell Bach from Stravinsky.

**What I conclude.**

- These sources agree that "goldfish have a three-second memory" is false. The claim contradicts sources 1 to 5 and none supports it.
- The strongest support comes from source 2, the only peer-reviewed abstract I read directly. It shows retention across days and weeks. It does not report three months.
- The three-month figure rests on source 3, a press report, and it is not in the Plymouth abstract I read. I would repeat "up to three months" only with that attribution.
- The six-month result (source 4) is consistent with long retention and is the longest interval in this list. It is a small student study, so I would cite it as illustration and not as proof.
- I found no source that traces where the three-second number began. Source 1 says only that the number varies by region. This run therefore cannot say who first claimed three seconds.
- Source 5 shows discrimination learning and says nothing about how long the memory lasts. I have cited it for the ability alone.

### Citations

Sources are listed in the order above, each with its validation status.

1. Live Science. "Do goldfish really have a 3-second memory?" <https://www.livescience.com/goldfish-memory.html> (validated, HTTP 200)
2. Gee, P., Stephenson, D., and Wright, D. E. (1994). Temporal discrimination learning of operant feeding in goldfish (Carassius auratus). Journal of the Experimental Analysis of Behavior, 62(1), 1-13. <https://researchportal.plymouth.ac.uk/en/publications/temporal-discrimination-learning-of-operant-feeding-in-goldfish-c> (validated, HTTP 200; abstract only)
3. The Times. "Goldfish pass memory test." <https://www.thetimes.com/travel/destinations/uk-travel/england/london-travel/goldfish-pass-memory-test-p830bt00sh7> (validated, HTTP 200)
4. American Museum of Natural History, Young Naturalist Awards. "Goldfish as a Model for Understanding Learning and Memory: More Complex Than You Think." <https://www.amnh.org/learn-teach/curriculum-collections/young-naturalist-awards/goldfish-as-a-model-for-understanding-learning-and-memory-more-complex-than-you-think> (validated through extraction; HTTP 403 to a plain request)
5. Shinozuka, K., Ono, H., and Watanabe, S. (2013). Reinforcing and discriminative stimulus properties of music in goldfish. Behavioural Processes, 99, 26-33. Quoted at <https://improbable.com/wp-content/uploads/2024/10/Ig-and-beyond-20-4.pdf> (validated through extraction; HTTP 403 to a plain request; journal page not validated and not cited)

### Not cited

- The journal page for Shinozuka et al. and the DOI link for Gee et al., because neither could be retrieved by any tool I used.
- A review of fish cognition (<https://abel.mcmaster.ca/publications/pdfs/Salena2021_Article_UnderstandingFishCognitionARev.pdf>) that resolved but says nothing about goldfish memory duration. It reports retention of up to 11 months for a different species, the rainbowfish, so it does not bear on this claim.
- Background knowledge about goldfish, which was not retrieved this task and is not cited.
