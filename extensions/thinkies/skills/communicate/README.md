# communicate

A writing partner for any piece, at any length, in any form. It works out with you who the piece is for, what brought it on, and where it should leave its audience, then drafts toward that and checks the draft against it. The meaning stays yours throughout.

## Ways to use it

Start from a vague idea. Name the occasion and little else, and it asks what the piece needs, one question at a time:

```
/communicate Can you write something for the poster? It's for Saturday.
/communicate I need a few words for Dad's retirement party, something nice
```

Polish text you already have. It keeps your words, facts, and chosen patterns, and tells you what it changed:

```
/communicate tighten clause 7.2 of our NDA before it goes to the supplier's counsel tomorrow
/communicate check this commit message before I push
```

Adapt a piece for another audience or another tradition. The same news reads differently to a council office and to a neighbour, and a piece built in one rhetorical tradition keeps its structure when you ask it to:

```
/communicate turn this incident report into a note for the customers it affected
/communicate this essay is a ki-sho-ten-ketsu piece on purpose, can you give it a pass?
```

Write something that isn't factual. A story, a poem, a lyric, or satire is its own form, and the skill works inside what that form promises, an unreliable narrator included:

```
/communicate polish this poem, I'm reading it at my aunt's memorial next week
/communicate Arthur lies to his audience the whole way through, draft the next scene
```

Carry long work across sessions. For a novel, a handbook, or a long report, it agrees a skeleton with you, drafts one unit at a time, and keeps a running record of committed facts, threads, and open decisions so chapter nine still agrees with chapter two:

```
/communicate here's the outline and chapter 1 of my novella, draft chapter 2
```

Name what feels wrong. When prose reads as machine-made, say so, and it starts from voice, word choice, and rhythm.

## What you'll get

A few questions first, one per message, with concrete readings to choose between wherever your intent is open. Then a draft with every decision in it named, and a revision that states what changed and whether any meaning moved.

Trimmed from a staged conversation, in which a second agent played the person asking, about a note to an upstairs neighbour who practises tap dancing at 3 a.m. The agent invented the name and flat number that sign the note ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/communicate/upstairs-tap-dancing.md)):

> **Skill:** So it's a first mention, to someone friendly you've only chatted with on the stairs, and I'll write it assuming they probably don't know how far the sound carries. Where should the note leave them? Two possible endings: "Could you keep the tapping to before 11 at night?" asks them to stop at an hour; "Would a mat or soft shoes after midnight be possible?" asks them to change how they practise. Is either close, or is it somewhere else, maybe a knock on your door to talk it over?
>
> **User (played):** The mat or soft shoes one is closer. I don't want to tell them when they can dance, I just need to sleep between about midnight and seven. […]
>
> […]
>
> **Skill:** Both changes are in:
>
> > Hi,
> >
> > I'm Sam from Flat 2, right below you. We've said hello on the stairs a couple of times.
> >
> > Sound carries through the floor more than you'd probably guess. Most nights around 3 a.m. I can hear your tap practice, and it wakes me up.
> >
> > I don't want to tell you when to dance. I just need it quiet from about midnight to seven. Would a mat or soft shoes at those hours be possible? If you'd rather talk it over, knock on my door.
> >
> > Hope the practice is going well.
> >
> > Thanks,
> > Sam, Flat 2

## What you can count on

- **It asks before it assumes.** Where two readings of your request would lead to different pieces, a formal notice or a friendly note, a laugh or a thank-you, it shows you both and lets you choose. What your words already answer, it states back in a line instead of asking again.
- **Your meaning stays yours.** It changes wording freely and meaning never silently. Every change of meaning, and every fact it invented because you asked it to, is named back to you. You set how much detail you want about the rest.
- **The draft carries no placeholders.** What it hands you is the finished piece, with no brackets, gaps, or notes to fill in. Where a choice is still yours to make, the draft waits for your answer.
- **The depth scales to the task.** A one-word fix gets the fix and a line naming what it assumed. A speech gets a short conversation first. A book gets a plan, a record, and a check-in after every unit.
- **It takes risks with form, not with substance.** It will propose a braver shape, image, or rhythm where the form rewards one, and it keeps to the scope and the point you set.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/communicate/` into `~/.claude/skills/communicate/`.

## Where the work is kept

For anything longer than a quick change, the skill keeps a small alignment file for each piece, plus a ledger for long work and the drafts, so a later session picks up where the last one stopped. Loaded from the thinkies Claude Code plugin, these live in the plugin's data folder; anywhere else, it asks you once where to keep them. The finished piece goes wherever you name.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`communicate.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/communicate.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
