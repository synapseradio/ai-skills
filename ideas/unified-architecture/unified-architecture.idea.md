# Unified Package Architecture

> **Status: Completed (restructured differently).** The migration went the opposite direction: `packages/` was removed. CLI source now lives in `plugins/{name}/src/`, shared libraries in `shared/`, with vendored copies in `plugins/{name}/vendor/`. This idea doc is retained as historical context.

Migrate all plugin code to `packages/`, making `plugins/` purely an interface layer.

## Problem

Two plugin architectures coexist without clear signals:

- **Binary plugins** (journal, perspectives, switchboard): Code in `packages/`, compiles to binary
- **Markdown-only plugins** (thinkies, software, expression): Code in `plugins/`, uses vendored copies

This causes vendored code drift (e.g., `page.ts` exists in 4+ locations with different implementations) and unclear code location.

## Key Change

All TypeScript code lives in `packages/`. Plugins contain only:

- `plugin.json` metadata
- SKILL.md files
- Command markdown
- Compiled binary in `dist/`

## Status

Proposal with implementation plan. See `unified-architecture.proposal.md` for the PRD and `research/unified-architecture.research.md` for the current state analysis.

## Related

- `packages/` — Target location for all code
- `plugins/` — Interface-only after migration
