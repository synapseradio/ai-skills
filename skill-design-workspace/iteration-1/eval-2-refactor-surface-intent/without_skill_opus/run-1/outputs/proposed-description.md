# Drop-in frontmatter for `skills/surface-intent/SKILL.md`

Replace the current `description:` block with the one below. Everything else in
the frontmatter and body stays as-is.

```yaml
---
name: surface-intent
description: >-
  Surface the intent already in a system before you add to it, and make your own
  intent legible in what you produce. Use before you introduce something
  cross-cutting or shared — a rule, abstraction, design, named concept, config,
  instruction, or interface — into a system whose prior art you have not surveyed,
  where a duplicate, a scope overrun, or a design that talks past the one already
  there is a real risk; or when what you produce must be clear enough for a second
  reader to act on it without you present. Triggers: "is this already covered", "am
  I duplicating this", "why does this exist", "before I add this rule", "make this
  clear enough to act on". Skip it for trivial, local, or throwaway edits, and for
  systems you already know well — reach for it when the thing you add outlives the
  moment and prior art plausibly already exists.
metadata:
  context: fork
---
```

## Spec conformance check

- `name` — unchanged, valid kebab-case.
- `description` — 841 characters (≤ 1024), contains no `<` or `>`.
- `metadata.context` — unchanged; `context` correctly sits under `metadata`, not at top level.
- No non-spec top-level keys introduced.

## After applying

The frontmatter change means the packaged artifact is stale. Regenerate it with the
official packager, then update any extension bundle:

```bash
SKILL_CREATOR_DIR="$(find "${HOME}/.claude/plugins/marketplaces" \
  -type d -path '*skill-creator/skills/skill-creator' 2>/dev/null | head -n1)"
(cd "${SKILL_CREATOR_DIR}" && python3 -m scripts.package_skill \
  /Users/nke/projects/ai/ai-skills/skills/surface-intent \
  /Users/nke/projects/ai/ai-skills/packaged)
```
