# communicate

Most machine prose reads as if nobody risked anything to write it. This skill raises the stakes: it reads a writing request for the specific ways the piece could fail its audience, builds a rubric of questions aimed at those failures, and scores every draft against that rubric, quoting the line that decides each verdict. A single word or a chapter of a novel: the loop stays the same, and the rigor scales to the work.

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/communicate/` into `~/.claude/skills/communicate/`.

## Usage

The skill triggers on natural language about prose work — composing, proofreading, redrafting, adapting, phrasing — so an explicit invocation is not required. When you want to invoke it directly:

```
/communicate fix the passive voice in this paragraph and strengthen the hedging
```

```
/communicate proofread this draft before I send it
```

```
/communicate help me write the introduction for this proposal
```

```
/communicate adapt this passage for a US business audience without flattening it
```

```
/communicate in Portuguese we say saudade — how do I render that in English without breaking it?
```

## How it works

Every run walks one loop.

1. **Diagnose.** Five questions (purpose, clarity, integrity, composition, depth) turn the request into a ranked list of ways this piece could fail for this audience.
2. **Align.** Whatever the diagnosis cannot answer from context becomes a question to the user: audience, register, purpose, and which texture rules relax for the register at hand.
3. **Build the rubric.** Each risk pulls in the reference file that probes it, and that file's Questions and Quality Criteria supply the rubric's entries. Questions stop arriving when each can no longer receive an evidenced verdict, so a word polish gets a handful and a chapter gets dozens.
4. **Draft.** Binding rules hold in every register; texture settings follow the alignment.
5. **Score.** Every rubric question gets a verdict with the deciding passage quoted.
6. **Revise.** Each revision request pulls at least one more reference off the ranked risk list and grows the rubric before the next draft.

Two rules never move: prose may not mislead its reader, and facts may not bend. Everything textural belongs to the register, and the register belongs to the user.

## References

| File | Concern |
|------|---------|
| [`write-for-humans.md`](references/write-for-humans.md) | Read every run — binding rules against misleading prose, adjustable texture defaults |
| [`fit.md`](references/fit.md) | Form matched to the verb naming the purpose |
| [`calibrate.md`](references/calibrate.md) | Audience depth — what the reader knows and how the vocabulary lands |
| [`clarify.md`](references/clarify.md) | Order and prerequisites — when concepts appear before their foundations |
| [`activate.md`](references/activate.md) | Hidden actors surfaced without erasing intentional agentless construction |
| [`strengthen.md`](references/strengthen.md) | Cushioning cut, calibration kept |
| [`illustrate.md`](references/illustrate.md) | Witnessed detail in place of category language |
| [`signal-confidence.md`](references/signal-confidence.md) | Certainty language tuned to the warrant the writer holds |
| [`bound-scope.md`](references/bound-scope.md) | Where a claim works and where it breaks |
| [`surface-assumptions.md`](references/surface-assumptions.md) | Silent premises made visible |
| [`arc.md`](references/arc.md) | Tension and pull — a spine for the piece |
| [`arrange.md`](references/arrange.md) | Section order, each standing on what came before |
| [`rhythm.md`](references/rhythm.md) | Cadence varied on purpose |
| [`voice.md`](references/voice.md) | One person, speaking from a named position |
| [`register.md`](references/register.md) | Word weight and habitual vocabulary challenged |
| [`extract-implications.md`](references/extract-implications.md) | What the claims commit the writer to |
| [`dimensionalize.md`](references/dimensionalize.md) | Bundled judgments split into scorable concerns |
| [`pose-questions.md`](references/pose-questions.md) | Inquiry opened where prose would close it |
| [`analogize.md`](references/analogize.md) | Unfamiliar concepts bridged through lived structure |
| [`across-languages.md`](references/across-languages.md) | Meaning kept intact across rhetorical traditions |
| [`frame-guide.md`](references/frame-guide.md) | Blank-page composition: necessity, position, tradition, audience |
| [`clarify-patterns.md`](references/clarify-patterns.md) | Detection heuristics for the clarify pass |
| [`index.md`](references/index.md) | One line per file, for navigation |

## When to use this

When it matters to say what you mean: proposals, documentation, announcements, essays, fiction, anything read more than once or by someone outside the immediate room. It also serves writers working in English from another thinking language, and adaptations across rhetorical traditions.

## Design record

Decisions fixed in this design, recorded so future sessions inherit them instead of remaking them:

- Binding versus adjustable cuts at deception. Rules that keep a reader from being misled never relax; rules that shape texture take their settings from the register, agreed with the user.
- Rubric size follows evidenced verdicts, never a count. Questions join the rubric while each can still receive one.
- Every revision request grows the rubric by at least one reference, chosen from the ranked risk list the diagnosis produced.
- Em dashes: at most one per piece, and only in a piece longer than an A5 page.
- `write-for-humans.md` forked deliberately from a personal reference file. Divergence from its ancestor is intended.

Open to each session: which references load, how many questions the rubric holds, texture settings, and when the rubric gets shown to the user.

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`communicate.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/communicate.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
