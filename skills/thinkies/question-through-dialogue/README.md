# question-through-dialogue

Use Socratic questioning to reveal assumptions. Clarifies the claim, probes assumptions by category, examines evidence, explores implications, and synthesizes understanding.

## It helps when

- You hold a conviction strongly and want to find out what it rests on, by answering rather than reading.
- Someone's claim deserves questions more than counterarguments.
- A belief has hardened into a rule, and you suspect the rule outgrew its reason.

## How a session goes

The questions come in five kinds, in order: what exactly the claim says, what it assumes (sorted as factual, causal, value, definitional, contextual, or capability), what supports it, what follows from it, and whether it is the right question at all. When you answer as you go, the claim can change under the questioning. At the end comes a synthesis: what stands on solid ground, what stays uncertain, which assumptions proved critical, and which questions still need answers.

Trimmed from a staged conversation, the user's side played by a second agent as an enthusiastic early riser, on "Everyone should wake up at 5 a.m." ([full run](https://github.com/synapseradio/ai-skills/blob/main/examples/thinkies/question-through-dialogue/five-am-for-everyone.md)):

> **Skill:** (Step 4, explore implications) Follow "everyone should" forward. If every person woke at 5 a.m., what else must be true? Shops, buses, and hospitals would need staff at hours that are now the quiet ones, and the 5 a.m. quiet you prize would come from other people still sleeping. Does "everyone" undo the very advantage that makes the claim attractive?
>
> **User (played):** That one lands: if literally everyone were up at 5, the quiet would shrink, and I can see that "everyone" works against the very advantage I'm praising.
>
> […]
>
> The claim moved through three forms. It began as "everyone should wake up at 5 a.m." (a rule about a clock time). […] It ended as "protect a quiet block each day for your most important work; early morning is often the easiest place to find one."

## Install

```bash
npx skills add https://github.com/synapseradio/ai-skills
```

Or copy `skills/thinkies/question-through-dialogue/` into `~/.claude/skills/question-through-dialogue/`.

## Usage

```
/question-through-dialogue <claim or topic>
```

## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`question-through-dialogue.skill`](https://github.com/synapseradio/ai-skills/raw/main/packaged/thinkies/question-through-dialogue.skill)

## License

[EUPL-1.2](https://github.com/synapseradio/ai-skills/blob/main/LICENSE)
