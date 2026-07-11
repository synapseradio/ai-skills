# Traversable Content Interface

Unified content traversal abstraction across all journal content types for THREAD detection and graph analysis.

## Problem

Journal content types have different structures (sessions have entries, reflections don't, catches have threads, insights have tags). Code handling these types must understand each schema variant.

## Key Insight

The common abstraction is not entries—it is **traversable content**. Each content type provides:

1. Identifier (how to reference)
2. Extractable text (for keyword analysis)
3. Discoverable links (for graph analysis)

## Key Capabilities

- **Type-safe content loading**: Generic loaders with variant narrowing
- **Unified text extraction**: Consistent interface regardless of schema
- **Link discovery**: Works across sessions, catches, insights, etc.

## Status

Design complete. See `specs/traversable-content.spec.md` for the interface specification.

## Related

- `plugins/journal/lib/` — Implementation location
- THREAD detection system — Primary consumer
