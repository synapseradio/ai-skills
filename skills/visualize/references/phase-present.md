# Phase 5 + 6: Present and Save

Output the final visualization, collect user feedback, persist the artifact.

## Entry Conditions

Phase 4 (Verify) complete. The visualization has passed both render-free passes —
structural read-back and render inference — on the second draft.

## Produce Final Output

Every browser chart — Vega, D3, or mermaid — is a fragment assembled into one
self-contained HTML file by the shared wrapper. Pick the chart's fragment at
`assets/<engine>/fragments/<cat>/<name>.frag.html`, edit its data, labels, and title,
then assemble it (the assembler injects the wrapper, the OpenColors theme, and the
shared helpers, and scopes the chart to its own instance):

```bash
python3 scripts/build_viz.py --fragment <fragment> --out final.html
```

A ready-to-open example for every chart already exists at
`assets/<engine>/templates/<cat>/<name>.html`.

**Dashboard / multiple charts:** assemble several fragments into the one wrapper —
they are per-instance scoped, so ids, styles, globals, and scroll never collide:

```bash
python3 scripts/build_viz.py --compose <frag-a> <frag-b> --out dashboard.html
```

**Markdown-surface output:** copy the matching `assets/markdown/templates/<name>.md.tmpl`.

## Present to User

1. **Restate the argument:** "This visualization shows that ___."
2. **Summarize encoding:** which data mapped to which channels, and why
3. **Note accessibility:** OpenColors palette, redundant encoding, data table fallback
4. **Acknowledge limitations:** what the visualization does not show, what was simplified

## User Review Checkpoint

| User Feedback | Route To |
|---------------|----------|
| "Change the chart type" | Phase 2: Research |
| "Fix the layout" / "move this" | Phase 3: compose |
| "Add annotations" / "improve title" | Phase 3: narrate |
| "Make it interactive" / "add filtering" | Phase 3: interact |
| "Something feels off" / "make clearer" | Phase 4: Verify |
| "Looks good, save it" | Save (below) |

## Save

1. Save to `${CLAUDE_PROJECT_DIR}/.claude/visualizations/viz-<timestamp>.html`
2. If Python 3 available: `python3 scripts/visualizer.py create --file <path>`
3. If not: the saved file is the final artifact

| CLI Command | Purpose |
|-------------|---------|
| `create --file <path>` | Save and register |
| `list [--type] [--project]` | List stored |
| `search <query>` | Search all fields |
| `show <id>` | View details |
| `delete <id> --force` | Remove |

## Exit

Visualization saved and user confirmed. Workflow complete.
