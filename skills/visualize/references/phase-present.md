# Phase 5 + 6: Present and Complete

Output the final visualization, collect user feedback, persist the artifact, and exit.

## Entry Conditions

Phase 4 (Refinement) complete. The visualization has passed:

- Structural audit
- Perceptual audit
- Clarity audit and glance test
- Regression check

## Presentation

### Produce Final Output

Generate the standalone HTML file following `base-template.md` structure:

1. Add HTML comment frontmatter (name, description, chart-type, project, created)
2. Embed data for standalone operation
3. Include all styles inline for portability
4. Verify ESM imports use CDN URLs (`https://cdn.jsdelivr.net/npm/d3@7/+esm`)

### Present to User

State what was built and why:

1. **Restate the argument**: "This visualization shows that ___."
2. **Summarize encoding choices**: which data mapped to which channels, and why
3. **Note accessibility features**: colorblind safety, keyboard navigation, screen reader support
4. **Acknowledge limitations**: what the visualization does not show, what simplifications were made

## User Review Checkpoint

Ask the user explicitly:

1. **"Does this communicate [the argument]?"** — validates the visualization serves its purpose
2. **"Ready to save, or iterate further?"** — gives the user control over completion

**Feedback routing:**

| User Feedback | Route To |
|---------------|----------|
| "Change the chart type" or "try a different encoding" | Phase 2: Research |
| "Fix the layout" or "move this element" | Phase 3: compose |
| "Add annotations" or "improve the title" | Phase 3: narrate |
| "Add filtering" or "make it interactive" | Phase 3: interact |
| "Something feels off" or "make it clearer" | Phase 4: Refinement |
| "Looks good, save it" | Phase 6: Complete |

## Completion

### Persist the Visualization

1. Save to `${CLAUDE_PROJECT_DIR}/.claude/visualizations/viz-<timestamp>.html`
2. **If Python 3 is available**: run `python3 scripts/visualizer.py create --file <path>` to register in organized storage at `~/.visualizer-skill/visualizations/`
3. **If Python 3 is unavailable**: the saved file is the final artifact — no registration needed

| Command | Purpose |
|---------|---------|
| `python3 scripts/visualizer.py create --file <path>` | Save and register visualization |
| `python3 scripts/visualizer.py list [--type] [--project]` | List stored visualizations |
| `python3 scripts/visualizer.py search <query>` | Substring search all fields |
| `python3 scripts/visualizer.py show <id>` | View visualization details |
| `python3 scripts/visualizer.py delete <id> --force` | Remove from storage |

### Mark Complete

1. Mark all visualization tasks as completed
2. Summarize what was built: argument, encoding, key design decisions
3. Note any recommended follow-up (additional views, dashboard integration, data refresh schedule)

## Exit

Visualization registered and user confirmed. Workflow complete.
