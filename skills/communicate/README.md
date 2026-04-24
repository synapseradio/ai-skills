# communicate

Improve, compose, and adapt written prose. The skill provides 16 techniques organized into 5 workflows — from quick proofreading to full multi-pass refinement to blank-page composition. Every route begins by identifying the rhetorical tradition of the text, so Anglo-American conventions do not operate as an invisible default.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/communicate/` into `~/.claude/skills/communicate/`.

## Usage

Apply specific techniques to existing prose:

```
/communicate improve this paragraph — fix the passive voice and strengthen the hedging
```

Proofread a draft before sending:

```
/communicate proofread this draft before I send it
```

Full refinement — run every technique until the prose stabilizes:

```
/communicate make this as good as it can be
```

Write from scratch:

```
/communicate help me write an introduction for this proposal
```

Adapt prose for a different audience or rhetorical tradition:

```
/communicate adapt this for a US business audience
```

Express a thought that resists translation:

```
/communicate in Spanish we say "tengo miedo" — how do I express that in English?
```

## How it works

The skill detects your intent and routes to the appropriate workflow:

- **Ad-hoc** — apply individual techniques (activate passive voice, strengthen hedging, tighten rhythm) via diagnostic question tables
- **Clarify** — four-phase clarity audit: orient, diagnose, repair, verify
- **Redraft** — five-pass cascade across all 16 techniques, repeating until the prose stops changing
- **Compose** — recursive generative workflow: frame, structure, compose, discover, polish
- **Structure** — five-phase tradition adaptation: identify source tradition, identify target, map divergence, adapt, annotate
- **Bridge** — four-phase ontology bridging for multilingual thinkers: receive, identify gap, bridge, offer a third option

## Why use this instead of prompting?

A plain "improve my writing" prompt applies a generic English style — usually informal American business prose. This skill starts by identifying where the writing comes from (its rhetorical tradition) and where it needs to land. It also works in passes rather than a single rewrite, so structural issues are fixed before surface polish, and earlier changes inform later ones.

The 16 techniques address specific dimensions of prose quality — clarity, integrity, shape, depth, connection — rather than applying a vague notion of "better."

## When to use this

Use it when writing matters: proposals, documentation, anything that will be read more than once or by someone outside your team. Also useful when writing in English from a non-English thinking language, or adapting prose across cultural contexts.

For throwaway messages or internal notes, just write.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`communicate.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/communicate.skill)

## License

[EUPL-1.2](/LICENSE)
