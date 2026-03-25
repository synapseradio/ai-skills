# Sequencer

Chain skills, agents, and natural-language instructions into ordered pipelines with accumulating context.

## Install

```bash
claude install-skill github:nke/ai-skills/skills/sequencer
```

Or copy the `skills/sequencer/` directory into `~/.claude/skills/sequencer/`.

## Usage

### Arrow syntax

```
/seq /skill-review skills/my-skill -> fix any issues -> /commit
```

### Bullet list

```
/seq
- /skill-review skills/my-skill
- fix any issues
- /commit
```

### Prose

```
/seq review the skill, fix issues, then commit
```

### Parallel steps

```
/seq /analyze -> ( /lint | /test ) -> /commit
```

### Generate from description

```
/seq generate review the new skill and ship it
```

### Help

```
/seq help
```

## How It Works

Each step runs sequentially via subagents. Every step's output is written to `/tmp/seq-{id}/step-{N}.md` and fed as context to the next step. Parallel groups (`( a | b )`) run concurrently and merge before continuing.

## File Structure

```
skills/sequencer/
├── SKILL.md                        # Main skill definition
├── README.md                       # This file
└── references/
    ├── parsing-guide.md            # Input format recognition and step extraction
    ├── execution-model.md          # Subagent spawning, context accumulation, parallelism
    └── syntax-reference.md         # Quick-reference card (/seq help)
```
