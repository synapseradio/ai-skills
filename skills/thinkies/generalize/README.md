# generalize

Find the class a case belongs to and carry back what holds for every member: drop the case's particulars one at a time while its parts, relations, and goal stay the same, name the class that is left, list what is known for every member of that class, apply to the case each item no dropped particular voids, and climb to a wider class while it still predicts something about the case.

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
