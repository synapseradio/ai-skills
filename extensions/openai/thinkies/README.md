# Thinkies for OpenAI Codex

Forty-eight reasoning skills packaged as an OpenAI Codex plugin. Each skill is prose
instructions in a `SKILL.md` — no network calls, no credentials, no background state.

This bundle is generated. The source of truth lives at `skills/thinkies/` in this repo, and
`bin/generate-openai-plugin.py` rebuilds everything here except this file. Edit the source,
re-run the generator, never hand-edit `skills/` below.

## Install into the ChatGPT desktop app

Plugins appear in the desktop app under Work mode or under Codex. Personal plugins load from
a marketplace file at `~/.agents/plugins/marketplace.json`.

1. Copy this plugin somewhere stable:

    ```bash
    mkdir -p ~/.codex/plugins
    cp -R /absolute/path/to/ai-skills/extensions/openai/thinkies ~/.codex/plugins/thinkies
    ```

2. Create or edit `~/.agents/plugins/marketplace.json`. Codex resolves `source.path` relative
   to the marketplace root, so an absolute path is the reliable choice:

    ```json
    {
      "name": "personal",
      "interface": { "displayName": "Personal" },
      "plugins": [
        {
          "name": "thinkies",
          "source": { "source": "local", "path": "/Users/you/.codex/plugins/thinkies" },
          "policy": { "installation": "AVAILABLE", "authentication": "ON_USE" },
          "category": "Productivity"
        }
      ]
    }
    ```

3. Restart the ChatGPT desktop app. Select Codex (or select ChatGPT and switch to Work mode),
   then open Plugins, choose your marketplace, and install Thinkies.

4. Start a new chat. Invoke a skill explicitly with `/skills` or by typing `$decompose`, or
   just describe your problem and let Codex match a skill by its description.

The equivalent CLI route registers a marketplace root instead of hand-editing the file. The
command also accepts `owner/repo`, `owner/repo@ref`, Git URLs with `--ref` and `--sparse PATH`,
and npm sources:

```bash
codex plugin marketplace add ./path/to/a/marketplace/root
codex plugin marketplace list
```

Installed plugins land in `~/.codex/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/$VERSION/`,
where `$VERSION` is `local` for a local source.

### Two things to confirm by trying

Steps 1 through 4 are assembled from OpenAI's published documentation, not from a successful
run on a personal ChatGPT Plus or Pro account. Two points are unverified:

- **Whether your account can install a personal local marketplace at all.** OpenAI documents
  the Plugins Directory as visible across ChatGPT plans and Codex as included on all plans,
  and it documents the personal marketplace path. It does not state that a Plus or Pro user
  on a personal account can install from one — eligibility is described as depending on plan,
  workspace settings, role, and surface, and plugins are documented as a Work mode or Codex
  feature rather than a Chat mode one. If the Personal tab is missing or the install button
  does nothing, that is the constraint you have hit, not a defect in this bundle.
- **Path resolution for `source.path`.** The docs say it resolves relative to the marketplace
  root rather than to the `.agents/plugins/` folder. The absolute path above sidesteps the
  ambiguity; a relative path may or may not work.

If either blocks you, the Codex CLI route below needs neither a marketplace nor an install
flow.

## Install into Codex CLI, without the plugin mechanism

Codex reads unbundled skills from `.agents/skills` directories: `$HOME/.agents/skills`,
`$CWD/.agents/skills`, and every directory from the working directory up to `$REPO_ROOT`. Any
skill folder dropped in one of those is picked up directly.

Symlink for a copy that tracks the repo:

```bash
mkdir -p ~/.agents/skills
for skill in /absolute/path/to/ai-skills/extensions/openai/thinkies/skills/*/; do
  ln -sfn "${skill%/}" ~/.agents/skills/
done
```

Or copy for a snapshot that does not move under you:

```bash
mkdir -p ~/.agents/skills
cp -R /absolute/path/to/ai-skills/extensions/openai/thinkies/skills/* ~/.agents/skills/
```

Codex picks up changes automatically; restart it if an edit does not appear. Skills installed
this way carry no plugin prefix — invoke `$decompose` rather than `$thinkies:decompose`.

## What to expect from forty-eight skills at once

Codex puts a list of every available skill's name and description into context so it can
choose one, and caps that list at 2% of the model's context window (or 8,000 characters when
the window is unknown). Past that it shortens descriptions first, then omits skills and warns.
Forty-eight skills with descriptions this detailed will hit that ceiling. Explicit invocation
with `$name` always works; implicit description matching may not reach every skill. Installing
the `.agents/skills` subset you actually use is the way to keep matching sharp.

## What differs from the Claude Code bundle

The generator rewrites the constructs that mean something to Claude Code and nothing to Codex:
slash-command argument substitution, a task-tracking tool call, host-specific save paths, and
delegation language that assumed a harness able to spawn agents. Reasoning content is
untouched. Read the transform rules at the top of `bin/generate-openai-plugin.py`.

## Sources

- [Build plugins](https://developers.openai.com/codex/build-plugins) — plugin layout, manifest
  fields, marketplace setup, install cache path.
- [Plugins](https://developers.openai.com/codex/plugins) — where plugins are available and how
  to install them.
- [Build skills](https://developers.openai.com/codex/skills) — `SKILL.md` shape, `.agents/skills`
  discovery, explicit and implicit invocation, the skills-list context budget.

## License

EUPL-1.2, matching the source skills.
