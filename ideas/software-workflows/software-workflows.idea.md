# Software Plugin Workflow Redesign

## Problem

The software plugin is organized around **cognitive mode menus** — abstract categories (assess, design, implement, refactor) that each contain a table of modes. Using them requires two-level routing: pick the right skill, then pick the right mode within it. This creates friction:

1. **Manual routing burden** — The user must know the taxonomy to find the right tool. "I want to understand what this code does" → is that assess? refactor? design? The categories overlap and the user must guess.
2. **Commands add routing without value** — The 4 commands (assess, design, implement, refactor) are thin wrappers that load the skill and do signal detection. They're a dispatch layer over a dispatch layer.
3. **Modes are disconnected from tasks** — A mode like "blast-radius" or "archaeology" is a *technique*, not a *workflow*. Users don't think "I need blast-radius mode" — they think "I'm about to make a change and I need to know what could break."
4. **No progressive structure** — Modes are peers in a menu, but real engineering tasks have phases. You scope before you detect, you detect before you verify, you verify before you act.

## Exemplar: vestigial-detect

The vestigial-detect command demonstrates what workflow-oriented organization looks like:

- **Five clear phases**: scope → detect → investigate → verify → remove
- **Sequential progression**: each phase builds on prior outputs
- **Automated tooling**: scripts that execute mechanical parts (detect-dead-code.ts, detect-stale-files.ts, git-archaeology.ts, simulate-removal.ts, count-references.ts)
- **Checkpoints**: journal entries between phases to record state
- **Multi-domain applicability**: same workflow works for code, docs, and processes
- **Progressive refinement**: candidates get filtered through increasing rigor (confidence levels → risk classification → verification status → removal tiers)

This is what engineering actually looks like — not choosing a mode from a menu, but entering a workflow that guides you through what needs to happen.

## Core Concept

Restructure the software plugin around **workflow-oriented skills** — each skill represents a complete engineering workflow with clear phases, automated tooling where applicable, checkpoints between stages, and progressive refinement of outputs.

The existing cognitive modes don't disappear — they become **techniques within phases**. "Blast-radius" becomes a step in the "change safety" workflow. "Archaeology" becomes a step in the "codebase understanding" workflow. The modes were always techniques; they just weren't placed within the workflows that give them context.

### Design principles

1. **Workflows, not menus** — Skills represent complete tasks with beginning, middle, and end
2. **Phases, not modes** — Sequential stages that build on each other
3. **Techniques within phases** — Existing mode content becomes steps within workflow phases
4. **Automated where mechanical** — Scripts handle detection/scanning; judgment stays human
5. **Checkpoints between phases** — Record state so workflows can be paused and resumed
6. **Entry by intent, not taxonomy** — Users describe what they want to do, not which category it falls under

## Initial Thoughts

- The existing mode reference files (28 `.md` files across assess, design, implement, refactor) contain real knowledge. The restructure should relocate, not discard.
- vestigial-detect already has scripts and tests — this infrastructure pattern should extend to other workflows.
- The command/skill duplication (4 commands that just proxy to 4 skills) should collapse. Each workflow should be one skill, potentially with a command entry point if slash-command invocation adds value.
- Some existing modes naturally cluster into workflows (e.g., cartography + dependency + flow = "codebase understanding" workflow). Others might need rethinking.

## Open Questions

- [ ] What are the natural workflows that engineering work actually follows?
- [ ] How do the 28 existing mode references map onto those workflows?
- [ ] Which workflows benefit from automated tooling (scripts)?
- [ ] Should vestigial-detect remain a separate workflow or become a phase within "refactor"?
- [ ] How does skill routing change — can Claude auto-detect workflow from user intent?
- [ ] What happens to the command layer — keep, merge, or eliminate?
- [ ] How do workflows compose — can one workflow invoke phases of another?
- [ ] What checkpointing mechanism works across workflows (journal? structured state?)?
