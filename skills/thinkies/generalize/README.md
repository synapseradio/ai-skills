# generalize

Find the class a case belongs to and carry back what holds for every member: drop the case's particulars one at a time while its parts, relations, and goal stay the same, name the class that is left, list what is known for every member of that class, apply to the case each item no dropped particular voids, and climb to a wider class while it still predicts something about the case.

## Try it when

- Something works, or fails, in one place and you want to know what it is an instance of.
- You suspect your problem is an old one in new clothes and want what is already known about it.
- A single case has you fascinated and you want predictions from it, not just admiration.

## What a run looks like

A question set about your case, then its answers: which details can go and which must stay, the class that is left and its other members, what holds for every member, which of those apply to your case (and, for each that doesn't, the dropped detail that voids it), and whether a wider class still predicts anything.

From a run on the one bus driver on route 12 who waves at every passenger, and whose bus everyone waits for even when another comes first ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/generalize/waving-bus-driver.md)), trimmed:

> The class: one server, among servers who otherwise do the same job, gives every recipient a small discretionary act of personal regard, and recipients pay a real cost to be served by that one. A short name for it is "the unrequired acknowledgment that people pay to receive."
>
> […]
>
> - "The server can turn the preference into a price." A barista can charge more or sell more. A transit fare is set by the agency, so the driver captures nothing. The dropped domain voids it.
>
> […]
>
> They predict two things the narrower class did not: riders at the stop probably wave and speak to each other and to the driver, and the preference survives the driver's occasional bad day but not the discovery of a motive. Neither prediction is checked against route 12 here.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/generalize/` into `~/.claude/skills/generalize/`.

## Usage

```
/generalize <case to examine>
```

## Sources

- Zheng et al. (2023). Step-back prompting. [arXiv:2310.06117](https://arxiv.org/abs/2310.06117).
- Tversky, B. (1989). [Parts, partonomies, and taxonomies](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/1989_Tversky_Partspartonomiesandtaxonomies.pdf).
- Rosch, E., et al. (1976). Basic objects in natural categories. [doi:10.1016/0010-0285(76)90013-X](https://doi.org/10.1016/0010-0285%2876%2990013-X).
- Rasmussen, J. (1985). The role of hierarchical knowledge representation in decisionmaking and system management. *IEEE Transactions on Systems, Man, and Cybernetics*, SMC-15(2), 234–243. [doi:10.1109/TSMC.1985.6313353](https://doi.org/10.1109/TSMC.1985.6313353). Pages below count article pages; the [DTU PDF](https://backend.orbit.dtu.dk/ws/files/158019622/HISMC.PDF) opens with a cover sheet, so its page number is one higher. Art. p. 3 (PDF p. 4): "transfer of knowledge from previously experienced cases".

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`generalize.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/generalize.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
