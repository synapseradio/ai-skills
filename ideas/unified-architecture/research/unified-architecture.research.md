# Current State Analysis

Investigation findings from 2025-12-25 plugin architecture survey.

## Plugin Inventory

| Plugin | Skills | Distribution | CLI | Code Location |
|--------|--------|--------------|-----|---------------|
| journal | 2 | Binary | Yes | packages/journal/ |
| perspectives | 13 | Binary | Yes | packages/perspectives/ |
| switchboard | 7 | Binary | Yes | packages/switchboard/ |
| thinkies | 63 | Markdown + scripts | No | plugins/thinkies/ |
| software | 27 | Markdown + scripts | No | plugins/software/ |
| expression | 16 | Markdown + scripts | No | plugins/expression/ |

## Directory Pattern Inventory

### Consistent Across All Plugins

| Directory | Purpose |
|-----------|---------|
| `.claude-plugin/plugin.json` | Plugin metadata |
| `skills/` | Skill directories with SKILL.md |
| `commands/` | Command markdown files |
| `CHANGELOG.md` | Version history |
| `README.md` | Plugin description |

### Variable Directories

| Directory | Appears In | Meaning |
|-----------|------------|---------|
| `lib/` | thinkies, software, expression | Vendored shared utilities |
| `lib/` | perspectives, switchboard | Empty (code in packages/) |
| `scripts/` | thinkies, software, expression | Plugin-level scripts |
| `dist/` | journal, perspectives, switchboard | Compiled binary |
| `agents/` | perspectives, switchboard, thinkies | Agent identity frames |
| `docs/` | perspectives, switchboard, thinkies | Plugin documentation |
| `references/` | software, switchboard | Reference documentation |
| `personas/` | perspectives | Persona definitions |
| `schemas/` | switchboard | Schema definitions |

## Code Location Analysis

### Binary Plugins

Source code lives in `packages/{name}/`:

```
packages/journal/
  cli.ts              # Entry point
  commands/           # Command implementations
    read/
    write/
  lib/                # Domain-specific utilities
    thread_decay.ts
    thread_detection.ts
    ...
  package.json        # Workspace package
```

Skills invoke compiled binary:

```typescript
// plugins/journal/skills/journal-write/scripts/write.ts
const cli = `${import.meta.dir}/journal`;  // 60MB binary copied here
process.exit(await Bun.spawn([cli, 'write', ...args]).exited);
```

### Markdown-Only Plugins

Source code lives in `plugins/{name}/`:

```
plugins/thinkies/
  lib/                # Vendored copies of @seed/lib
    page.ts           # 575 lines, outdated
    core.ts
    store.ts
    yaml.ts
  scripts/            # Plugin utilities
    common.ts
  skills/
    cite-sources/
      scripts/
        validate_url.ts  # Imports from ../../lib/page.ts
```

Skills run scripts directly:

```typescript
// plugins/thinkies/skills/cite-sources/scripts/validate_url.ts
import { pageError } from '../../../lib/page.ts';  // Relative to vendored copy
```

## Import Pattern Analysis

### packages/ (Workspace Imports)

```typescript
import { createPageSuccess } from '@seed/lib/page';
import { defineCommand } from '@seed/page';
```

### plugins/ (Relative Imports)

```typescript
import { pageError } from '../../../lib/page.ts';
import { VALIDATE_URL_HELP } from '../../../scripts/common.ts';
```

No plugin code uses `@seed/lib` imports. This is architecturally impossible because plugins/ is outside the workspace scope defined in root package.json.

## Vendored File Inventory

### page.ts

| Location | Lines | Protocol | Status |
|----------|-------|----------|--------|
| packages/lib/page.ts | 762 | CAID (4-part) | Canonical |
| plugins/thinkies/lib/page.ts | 575 | CAI (3-part) | Outdated |
| plugins/software/lib/page.ts | 575 | CAI (3-part) | Outdated |
| plugins/expression/lib/page.ts | 77 | Minimal | Subset only |
| plugins/software/commands/vestigial-detect/scripts/lib/page.ts | 167 | Unknown | Command-specific |

### Other Vendored Files (in plugins/thinkies/lib/)

| File | Lines | Canonical Location |
|------|-------|-------------------|
| core.ts | 175 | packages/lib/core.ts |
| store.ts | 260 | packages/lib/store.ts |
| yaml.ts | 50 | packages/lib/yaml.ts |
| types.ts | 120 | packages/lib/types.ts |
| env.ts | 40 | (utility) |

## Skill Script Inventory

Scripts that need migration:

### thinkies

| Script | Location | Lines |
|--------|----------|-------|
| validate_url.ts | skills/cite-sources/scripts/ | ~100 |
| common.ts | scripts/ | ~120 |

### software

| Script | Location | Lines |
|--------|----------|-------|
| list-hunks.ts | skills/improve-selective-stage/scripts/ | ~150 |
| stage-hunks.ts | skills/improve-selective-stage/scripts/ | ~200 |
| count-references.ts | commands/vestigial-detect/scripts/ | ~100 |
| detect-dead-code.ts | commands/vestigial-detect/scripts/ | ~150 |
| detect-project-type.ts | commands/vestigial-detect/scripts/ | ~200 |
| detect-stale-files.ts | commands/vestigial-detect/scripts/ | ~100 |
| git-archaeology.ts | commands/vestigial-detect/scripts/ | ~150 |
| simulate-removal.ts | commands/vestigial-detect/scripts/ | ~100 |
| common.ts | scripts/ | ~50 |

### expression

| Script | Location | Lines |
|--------|----------|-------|
| check-coherence.ts | scripts/ | ~80 |
| check-confidence.ts | scripts/ | ~80 |
| mermaid-preview.ts | skills/visualize/scripts/ | ~100 |
| mermaid-theme.ts | skills/visualize/scripts/ | ~100 |
| common.ts | scripts/ | ~50 |

## Migration Complexity Assessment

| Plugin | Unique Code | Vendored Code | Scripts | Complexity |
|--------|-------------|---------------|---------|------------|
| thinkies | ~200 lines | ~1400 lines | 1 | Low |
| expression | ~300 lines | ~170 lines | 4 | Low |
| software | ~2000 lines | ~600 lines | 9 | Medium |

Total: ~2500 lines unique code to migrate, ~2200 lines vendored code to delete.
