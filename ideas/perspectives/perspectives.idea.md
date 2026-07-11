# Perspectives CLI

Unified CLI for persona management and dialogue lifecycle, consolidating multiple scripts into a coherent command structure.

## Problem

Persona operations are scattered across 7+ individual scripts with no unified interface. Skills invoke scripts directly, making composition difficult.

## Key Capabilities

- **Persona CRUD**: Save, read, list, search personas
- **Dialogue lifecycle**: Start, turn, end, show, list, resume, extend
- **Trace management**: Capture and query automaton execution traces for collision analysis

## Status

Specification complete. See `specs/perspectives.cli.md` for the full design.

## Related

- `packages/perspectives/` — Implementation location
- `docs/ideas/discourse/` — Resume/extend capability that builds on this CLI
