# CLAUDE.md

Repo-wide guidance for Claude sessions working in `ai-skills`. Skill-specific guidance lives in each skill's `SKILL.md`; this file documents conventions that span the whole repo.

## Layout

- `skills/<name>/` — source skills. Each has a `SKILL.md` with YAML frontmatter and optional `references/`, `scripts/`, `assets/` subdirectories.
- `skills/packaged/<name>.skill` — distributable ZIP of the matching source skill. Committed to git so the README remote URLs on `main` resolve without a release pipeline.
- `extensions/<plugin-name>/` — Claude Code plugin bundles wrapping one or more skills. Each has `.claude-plugin/plugin.json` at the plugin root and a `skills/<skill-name>/` copy of the source skill.
- `agents/<name>.md` — subagent definitions.
- `examples/` — runnable usage fixtures; not installable.

## Packaging a skill to `.skill`

Every source skill must have a matching `skills/packaged/<name>.skill`. Regenerate whenever the source skill changes.

**Use the official packager from the installed `skill-creator` plugin. Do not vendor or reimplement it** — the plugin updates independently and a local copy would drift.

If `skill-creator` is not installed, install it once via Claude Code:

```
/plugin install skill-creator@claude-plugins-official
```

To package one skill:

```bash
SKILL_CREATOR_DIR="$(find "${HOME}/.claude/plugins/marketplaces" \
  -type d -path '*skill-creator/skills/skill-creator' 2>/dev/null | head -n1)"
(cd "${SKILL_CREATOR_DIR}" && python3 -m scripts.package_skill \
  "${PWD_OF_REPO}/skills/<skill-name>" \
  "${PWD_OF_REPO}/skills/packaged")
```

To (re)package every skill:

```bash
SKILL_CREATOR_DIR="$(find "${HOME}/.claude/plugins/marketplaces" \
  -type d -path '*skill-creator/skills/skill-creator' 2>/dev/null | head -n1)"
REPO="$(pwd -P)"
for skill in skills/*/; do
  name="$(basename "${skill}")"
  [[ "${name}" == packaged ]] && continue
  (cd "${SKILL_CREATOR_DIR}" && python3 -m scripts.package_skill \
    "${REPO}/${skill%/}" "${REPO}/skills/packaged")
done
```

The packager validates frontmatter (requires `PyYAML` — `pip install pyyaml` if missing), excludes `__pycache__`, `node_modules`, `*.pyc`, `.DS_Store`, and root-level `evals/`, then writes `<name>.skill` (ZIP) with `<name>/SKILL.md` at the archive root.

## README footer convention

Every source skill's `README.md` ends with an install footer. The link target is the absolute GitHub raw URL so the link resolves anywhere the README is rendered — not just on github.com:

```markdown
## Install as a `.skill`

Upload this file in Claude.ai → Settings → Skills:

[`<name>.skill`](https://github.com/synapseradio/ai-skills/raw/main/skills/packaged/<name>.skill)
```

When adding a new skill, append this footer and regenerate `skills/packaged/`.

## Extensions

`extensions/<plugin-name>/` is a self-contained Claude Code plugin bundle:

```
extensions/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json       # required: name; strongly recommended: version, description, author, repository, license
├── README.md             # install instructions
└── skills/
    └── <skill-name>/
        └── SKILL.md      # copy of the source skill; regenerate when source changes
```

The skill in `extensions/` is a build artifact; the source in `skills/<skill-name>/` is the single source of truth. When the source changes, re-copy the skill tree into the extension bundle.

Install locally for development:

```
claude --plugin-dir extensions/<plugin-name>
```

Install from a marketplace once published:

```
/plugin install <plugin-name>@<marketplace-name>
```

## House rules

- Don't vendor the skill-creator packager (Apache-2.0 upstream; it will update and our copy will drift). Invoke it in-place from the installed plugin.
- When adding a skill: create source, run the packager, append the README footer, regenerate the `extensions/` bundle if one exists for that skill, commit all four in one change.
- `.skill` files are binary ZIPs — skip them in the lint pipeline.

## SKILL.md frontmatter — spec-only

Every `SKILL.md` frontmatter conforms to the official Agent Skills spec. **No top-level frontmatter key may exist that is outside the spec's allow-list**, and every field value must satisfy the spec's constraints.

**Allow-list** (from the `skill-creator` plugin's `quick_validate.py`, which the packager invokes):

- `name` — kebab-case (lowercase letters, digits, hyphens only; no leading/trailing/double hyphens), ≤ 64 chars.
- `description` — string, ≤ 1024 chars, must not contain `<` or `>`.
- `license` — string.
- `allowed-tools` — array of tool name strings.
- `compatibility` — string, ≤ 500 chars.
- `metadata` — dictionary for any skill-specific extension fields. **Nested keys under `metadata` are unconstrained** — this is the escape hatch for repo-specific conventions.

**Anything else at top level is a violation**, including conventions this repo previously used (`context`, `user-invocable`, `version`). Move them under `metadata:` when they still carry meaning; drop them when they don't.

Example — moving a non-spec field under `metadata`:

```yaml
---
name: my-skill
description: One-line trigger description.
metadata:
  context: fork
  user-invocable: true
---
```

The packager validates this on every run. A failing skill never produces a `.skill` file.
