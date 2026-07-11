# PRD: Unified Package Architecture

**Status**: Draft
**Duration**: 3 days
**Created**: 2025-12-25

## Problem Statement

The repository contains two coexisting plugin architectures with no clear signals to distinguish them:

**Binary plugins** (journal, perspectives, switchboard):

- Source code lives in `packages/{name}/`
- Compiles to ~60MB binary in `plugins/{name}/dist/`
- Uses workspace imports (`@seed/lib`, `@seed/page`)
- Plugin `lib/` directories are empty

**Markdown-only plugins** (thinkies, software, expression):

- Source code lives IN the plugin directory (`plugins/{name}/lib/`, `plugins/{name}/scripts/`)
- Uses relative imports to vendored copies of shared utilities
- No compilation step

### Consequences

1. **Vendored code drift**: `page.ts` exists in 4+ locations with different implementations. The canonical version in `packages/lib/` has evolved (CAID protocol) while vendored copies remain outdated (CAI protocol).

2. **Unclear code location**: Without reading import statements, you cannot determine whether a plugin's code lives in `packages/` or `plugins/`.

3. **Inconsistent patterns**: `lib/` means "empty" for binary plugins, "vendored utilities" for markdown plugins, and "domain code" for packages.

4. **Import fragility**: Relative paths like `../../../lib/page.ts` break when files move.

### Evidence

| File | Location | Lines | Status |
|------|----------|-------|--------|
| page.ts | packages/lib/ | 762 | Canonical (CAID) |
| page.ts | plugins/thinkies/lib/ | 575 | Outdated (CAI) |
| page.ts | plugins/software/lib/ | 575 | Outdated (CAI) |
| page.ts | plugins/expression/lib/ | 77 | Minimal subset |
| page.ts | plugins/software/commands/vestigial-detect/scripts/lib/ | 167 | Command-specific copy |

## Proposed Solution

Migrate all plugin code to `packages/`, making `plugins/` purely an interface layer.

### Target Architecture

```
packages/                          # ALL code lives here
  lib/                             # Shared library (exists)
  shared/                          # CLI utilities (exists)
  journal/                         # Journal CLI (exists)
  perspectives/                    # Perspectives CLI (exists)
  switchboard/                     # Switchboard CLI (exists)
  thinkies/                        # NEW: Thinkies CLI
  software/                        # NEW: Software CLI
  expression/                      # NEW: Expression CLI

plugins/                           # Interface only - NO code
  {each}/
    .claude-plugin/plugin.json     # Metadata
    skills/                        # SKILL.md files + thin wrappers
    commands/                      # Command markdown files
    dist/{name}                    # Compiled binary
```

### What This Communicates

| Signal | Meaning |
|--------|---------|
| `packages/{name}/` exists | This plugin has executable code |
| `plugins/{name}/dist/` exists | Binary distribution (all plugins) |
| `plugins/{name}/lib/` | **Should not exist** |
| Skill `scripts/` directory | Contains thin wrapper + compiled binary |

### Architectural Constraint

Workspace imports (`@seed/lib`) only work from `packages/*` directories. This is defined in root `package.json`:

```json
"workspaces": ["packages/*"]
```

Files in `plugins/` cannot use workspace imports. This constraint drives the architecture: to eliminate vendored copies, code must move to `packages/`.

## Success Criteria

### Must Have

- [ ] All TypeScript code lives in `packages/`
- [ ] No vendored `lib/` directories in `plugins/`
- [ ] All plugins compile to binary
- [ ] Skill scripts are thin wrappers invoking CLI
- [ ] All imports use `@seed/lib` or `@seed/page`
- [ ] Tests pass

### Should Have

- [ ] Build time under 60 seconds for all plugins
- [ ] Documentation updated (CLAUDE.md, relevant references)

### Nice to Have

- [ ] Binary size optimization (currently ~60MB each)

## Implementation Plan

### Day 1: Thinkies Migration (Proof of Concept)

**Objective**: Establish the pattern with the simplest plugin.

**Scope**:

- 1 script to migrate (`validate_url.ts`)
- ~200 lines unique code
- ~1400 lines vendored code to delete

**Tasks**:

1. **Create package structure**

   ```
   packages/thinkies/
     package.json
     cli.ts
     commands/
       validate-url.ts
     lib/
       common.ts        # migrated from plugins/thinkies/scripts/common.ts
   ```

2. **Implement CLI** using `defineCommand` pattern from `@seed/page`

3. **Migrate validate_url.ts** to `packages/thinkies/commands/validate-url.ts`
   - Update imports to `@seed/lib/page`
   - Wire into CLI router

4. **Update skill wrapper** at `plugins/thinkies/skills/cite-sources/scripts/`
   - Thin wrapper invoking compiled binary

5. **Delete vendored lib/** from `plugins/thinkies/`

6. **Add build script** to root package.json

7. **Verify**: Tests pass, skill invocation works

**Deliverable**: Working thinkies CLI with validate-url command.

### Day 2: Expression Migration

**Objective**: Migrate a plugin with multiple related scripts.

**Scope**:

- 4 scripts to migrate
- ~300 lines unique code
- ~170 lines vendored code to delete

**Scripts to migrate**:

- `check-coherence.ts`
- `check-confidence.ts`
- `mermaid-preview.ts`
- `mermaid-theme.ts`

**Tasks**:

1. **Create package structure**

   ```
   packages/expression/
     package.json
     cli.ts
     commands/
       check-coherence.ts
       check-confidence.ts
       mermaid/
         preview.ts
         theme.ts
     lib/
       common.ts
   ```

2. **Migrate scripts** with import updates

3. **Update skill wrappers** in `plugins/expression/skills/visualize/scripts/`

4. **Delete vendored lib/**

5. **Add build script**

6. **Verify**

**Deliverable**: Working expression CLI with all commands.

### Day 3: Software Migration

**Objective**: Migrate the most complex plugin.

**Scope**:

- Multiple scripts including nested command structure
- ~2000 lines unique code
- ~600 lines vendored code to delete

**Complexity factors**:

- `commands/vestigial-detect/` has nested `scripts/lib/` directory
- Multiple scripts in skill directories

**Scripts to migrate**:

- `list-hunks.ts`, `stage-hunks.ts` (from improve-selective-stage skill)
- `count-references.ts`, `detect-dead-code.ts`, `detect-project-type.ts`, `detect-stale-files.ts`, `git-archaeology.ts`, `simulate-removal.ts` (from vestigial-detect command)

**Tasks**:

1. **Create package structure**

   ```
   packages/software/
     package.json
     cli.ts
     commands/
       hunks/
         list.ts
         stage.ts
       vestigial/
         count-references.ts
         detect-dead-code.ts
         detect-project-type.ts
         detect-stale-files.ts
         git-archaeology.ts
         simulate-removal.ts
     lib/
       common.ts
   ```

2. **Migrate all scripts** with import updates

3. **Update skill and command wrappers**

4. **Delete ALL vendored copies** including nested `scripts/lib/`

5. **Add build script**

6. **Verify**

7. **Final cleanup**: Update documentation, remove any remaining dead code

**Deliverable**: Working software CLI, all vendored code eliminated.

## CLI Command Structure

### thinkies

```
thinkies validate-url <url>
```

### expression

```
expression check-coherence [options]
expression check-confidence [options]
expression mermaid preview [options]
expression mermaid theme [options]
```

### software

```
software hunks list <path>
software hunks stage --hunks <json>
software vestigial count-references [options]
software vestigial detect-dead-code [options]
software vestigial detect-project-type [options]
software vestigial detect-stale-files [options]
software vestigial git-archaeology [options]
software vestigial simulate-removal [options]
```

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Binary size (~60MB each) | Disk usage increases | Certain | Accept for now; optimize later if needed |
| Build time increases | Slower CI | Medium | Parallel builds, incremental compilation |
| Breaking skill invocations | Skills fail | Medium | Test each skill after migration |
| Missing edge cases in scripts | Runtime errors | Low | Preserve existing tests, add integration tests |

## Decision Criteria

### Accept If

- All tests pass after migration
- Skill invocations work identically
- No vendored `lib/` directories remain in `plugins/`
- Code location is unambiguous (all in `packages/`)

### Reject If

- Build time exceeds 5 minutes
- Any skill functionality regresses
- Migration introduces new dependencies

## Out of Scope

- Binary size optimization
- Restructuring skill directory layout
- Changing skill invocation patterns (beyond thin wrappers)
- Modifying the shared `@seed/lib` API

## Dependencies

- `@seed/page` for `defineCommand` pattern
- `@seed/lib` for shared utilities (page, store, yaml, etc.)
- Bun compiler for binary generation

## Rollback Plan

Each day's work is independently committable. If Day 2 or Day 3 encounters blocking issues:

1. Commit completed work
2. Revert incomplete migration
3. Document blockers for future resolution

The repository remains functional at each day boundary.
