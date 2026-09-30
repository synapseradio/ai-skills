# research-and-teach: why onions make you cry

- skill: research-and-teach, from commit 0c9258f
- subject: Why do onions make you cry?
- kind: staged conversation (the user side played by a second agent)

## Prompt

/research-and-teach Why do onions make you cry?

## Run

### Step 1, Scope

**Skill:** Before I start: what do you want to be able to do or explain after this, and how much chemistry do you have to lean on? Different answers change where I begin.

**User (played):** I want to actually understand why it happens, not just be told "it's the sulfur." And ideally I'd stop dreading it. I've got nothing past secondary school chemistry: I remember atoms and molecules, but not much about reactions.

Target: a working explanation of the cause, for a home cook with secondary-school chemistry, that ends in something usable at the chopping board.

Components, foundational first:

1. An intact onion holds no tear gas; it holds ingredients kept apart (foundational).
2. Cutting mixes them, and enzymes convert one ingredient into an airborne molecule.
3. The conversion has two enzyme steps with a fork between flavour and tears.
4. The molecule reaches the eye and triggers nerves, and tears follow.
5. Each stage is a place to interfere, in the kitchen or in plant breeding.

Known versus to research. Known from general knowledge: the culprit is a sulfur compound, enzymes are involved, cutting matters. Needed research: the exact chemical steps, whether a second enzyme is involved, how the eye detects the molecule, and whether kitchen tricks have evidence behind them.

Curiosity questions: Why would a plant build a tear-gas factory? Why does the gas form only after cutting? Why do some onions and spring onions sting less? Is the tear reflex protective or accidental? Does any trick measurably work?

### Step 2, Research

Searches and fetches ran through the Tavily command line. What each source settled, with its rung on the source ladder (artifact and publisher rungs are primary; the rest are leads):

- Imai et al., Nature 2002. The irritant was presumed to form spontaneously after alliinase acts; the paper shows it is made by a separate enzyme, lachrymatory-factor synthase. Publisher rung, abstract only (paywalled). <https://www.nature.com/articles/419685a>
- Silvaroli et al. 2017, crystal structure of the synthase. Alliinase cleaves S-alk(en)yl cysteine sulfoxides to sulfenic acids, which condense into thiosulfinates; alternatively the synthase converts the sulfenic acid into (Z)-propanethial S-oxide, the lachrymatory factor. The abstract calls the whole pathway part of the plant's "chemical warfare against microbes and animals". Publisher rung. <https://pmc.ncbi.nlm.nih.gov/articles/PMC5693239>
- Kato et al., Scientific Reports 2016. Tearless, non-pungent onions made without transgenes by irradiating seeds with neon ions; about 7.5-fold lower lachrymatory factor, traced to under 1 percent of normal alliinase messenger RNA, no tears or pungency among 20 sensory panelists. Publisher rung. <https://www.nature.com/articles/srep23779>
- Salazar et al. 2008, channel study. Onion and garlic extracts, and allicin, activate the sensory channel TRPV1 by covalent modification of a cysteine; the same compounds are known to activate TRPA1. Publisher rung. The experiments used extracts and allicin, not purified lachrymatory factor. <https://pmc.ncbi.nlm.nih.gov/articles/PMC4370189>
- Royal Society of Chemistry, Magnificent Molecules. Names the two-step process, says the molecule reacts with water on the eye to make an acid, and offers cooling, a sharp knife, contact lenses and goggles as advice. Practitioner rung. <https://edu.rsc.org/magnificent-molecules/propanethial-s-oxide/3010038.article>
- The Conversation. Names the precursor PRENCSO, explains that suppressing the synthase could shift the balance toward thiosulfinate. Practitioner rung. <https://theconversation.com/why-onions-make-us-cry-and-why-some-dont-84486>

Validation by explaining simply. The one gap this exposed: the eye step. Two accounts circulate, "the molecule becomes an acid on the eye" and "it switches on nerve channels". The channel experiments I found used extracts and allicin, not the purified molecule, so the receptor step is likely, not established. I found no measured comparison of the kitchen tricks; they follow from the mechanism and appear as advice in sources. One source I opened (a cookbook excerpt) calls the irritant "sulfuric acid"; the primary papers name sulfenic acid, so I set that framing aside.

Framings gathered: a glow stick (two chemicals kept apart until broken), a two-key lock, a fork in a road (flavour or tears).

### Step 3, Structure

- Layer 1: an intact onion holds ingredients apart; the knife mixes them; a gas forms; the eye reacts; tears wash it off.
- Layer 2: two enzymes, a snip and a rearrangement, with a fork between flavour and tears.
- Layer 3: how the eye detects it, what the evidence does and does not settle, and where each trick interrupts the chain.
- Anchor for this learner: cooking and kitchen practice, the glow stick, the fridge.

### Step 4, Teach

**Skill:** Thanks. Here is the simplest true version. An intact onion holds no tear gas. It keeps two things in separate compartments inside its cells: a sulfur-bearing compound it drew up from the soil, and enzymes (proteins that speed up one specific reaction). Your knife breaks the compartments, the two meet, and the enzymes turn the compound into a small, light molecule that evaporates into the air. That gas reaches your eyes and irritates the nerve endings on their surface, and your brain answers by making tears to wash it off. So the crying is a defence: the onion arms itself only when something bites it.

Before I add anything, in your own words: why doesn't a whole onion on the counter make you cry, and what does the knife change?

**User (played):** A whole onion doesn't make me cry because the sulfur compound and the enzymes are kept in separate compartments, so they never touch. The knife breaks those compartments open, they mix, and the enzymes turn the compound into a gas that gets into my eyes.

One thing I'm fuzzy on is what "turn the compound into a gas" actually means. Is it like the enzyme snips a piece off the molecule, or does it rearrange it?

**Skill:** Good, that is exactly the right question, and the answer is both, in two steps. Layer 2:

Step 1, a snip. The first enzyme, alliinase, cuts the sulfur compound (S-1-propenyl-L-cysteine sulfoxide) and releases an unstable fragment called 1-propenylsulfenic acid. Left alone, that fragment reacts with itself to form thiosulfinates, the compounds that give a cut onion its sharp flavour.

Step 2, a rearrangement. A second enzyme, lachrymatory-factor synthase, grabs some of that same fragment and reshuffles its atoms into propanethial S-oxide, the small volatile molecule that stings your eyes. Until 2002 people assumed that last step happened by itself; a Japanese team showed it needs its own enzyme.

So one fragment reaches a fork: flavour if it reacts with itself, tears if the second enzyme gets it first.

Check: which step is the snip and which the rearrangement, and what would you predict happens to the onion's flavour and its tears if you could switch the second enzyme off?

**User (played):** The first enzyme does the snip. It cuts the fragment off the sulfur compound. The second enzyme does the rearrangement, reshuffling that fragment into the stinging molecule. If you switched the second enzyme off, I'd guess the fragment would mostly react with itself, so the onion would still taste sharp and might even taste stronger, but the tears would mostly stop.

I'm a bit lost on one word, though. What is a "sulfenic acid", and why is that fragment "unstable"? Is that just a fancy way of saying it can't stay as it is for long?

**Skill:** Your prediction is right, and your reading of "unstable" is right. A sulfenic acid is a carbon chain joined to a sulfur atom that carries an OH group (carbon chain, sulfur, OH). That arrangement is very eager to react, so two fragments meet and join within moments, which is why the fragment cannot be kept in a bottle.

Layer 3, the eye and the kitchen. The stinging molecule is small and light, so it evaporates from the board and drifts up. On your eye it meets the wet surface, and nerve endings there fire. Those nerves carry pain-sensing channel proteins, and onion and garlic extracts are known to switch on two of them, called TRPA1 and TRPV1, by chemically modifying a sulfur-containing part of the channel. Your brain reads the signal as irritation and orders tears to dilute and wash away the irritant. Two honest limits: the channel experiments I found used whole extracts and the related garlic compound allicin, not purified stinging molecule, and older explanations say the molecule turns into an acid on the eye, which sources still repeat. Treat the exact receptor step as likely, not settled.

The three stages give you three places to interfere. Fewer broken cells means less reaction (a sharp knife, slicing without crushing). Cooler onions react and evaporate more slowly (chilling them first). A barrier stops the gas reaching your eye (goggles; one writer finds contact lenses help). These tricks follow from the mechanism; the sources I found offer them as reasoned advice, and I found no measured comparison. And breeders have gone after the chemistry: in 2016 a team made onions with about 7.5 times less of the stinging molecule by lowering the first enzyme, with no tears reported by 20 tasters.

Check: pick one kitchen trick you would actually try and tell me which stage it interrupts and why.

**User (played):** I'd try chilling the onion in the fridge before cutting. That interrupts the reaction stage, where the enzymes turn the compound into the stinging gas. Cold slows the enzymes, and it also slows the gas evaporating off the board, so less of it reaches my eyes.

The sulfenic acid part makes sense now: sulfur with an OH on it, eager to react. What I still don't follow is how the gas irritates my eye. You said it "chemically modifies" part of the nerve channel. Does that mean it actually sticks to the protein and changes its shape, so the channel opens by mistake?

**Skill:** Yes, with one caution about how far the evidence reaches. In the channel experiments, the pungent compound forms a covalent bond, a chemical bond that does not let go, with a sulfur-containing amino acid in the channel called cysteine. For TRPV1, one cysteine near the start of the protein was necessary and sufficient for the effect; TRPA1 has several such sites. Bonding at that site opens the channel, which is what "activated" means here: charged particles flow into the nerve ending, the nerve fires, and you feel the sting. So "it sticks and the channel opens by mistake" is a fair picture. The caution is the one from Layer 3: those results come from onion and garlic extracts and allicin, so for the onion's own stinging molecule the same route is the likely account, not a measured one.

That completes the chain from knife to tear: broken cells, a snip, a rearrangement, an airborne molecule, a bonded nerve channel, and tears. Your fridge plan targets the middle of it, and the sharp knife and goggles target the two ends.

### Step 5, Persist (optional)

**Skill:** Would you like the layered explanation saved as study notes or a one-page reference, with the sources above?
