# Proposal: visualize-improvements

## Why

The visualize skill degrades its own output through decisions it makes by
omission. It skips its reference docs because `SKILL.md` says to load them "as
needed" (`skills/visualize/references/phase-implement.md:3`), so the application
methodology in the mode docs goes unread while the agent feels equipped from the
principles inlined in `SKILL.md` (`skills/visualize/references/mode-encode.md:3`).
It falls through to Vega because the engine decision tree has a default leaf
("everything else → Vega", `skills/visualize/references/engine-selection.md:29`),
so the engine is never truly chosen. And its templates were each written as a
standalone page, so they collide when a user drops several into one document.
Each failure is the same disease: a consequential choice left implicit. This
change makes those choices explicit and verifiable across three fronts — how the
skill verifies output, how it decides, and how its templates behave alone and
composed.

## What Changes

**Verification (visualization-verification)**

- **BREAKING**: Remove the screenshot capability entirely. The skill never
  captures a screenshot, never drives a browser to inspect a chart, and never
  suggests the user screenshot one. The only surviving `open` is the Phase 6
  presentation step that shows the user their finished chart.
- Replace the screenshot-based "visual" verification with **render inference** —
  predicting rendered defects from the spec/HTML source, including the scroll
  hijacking and unwired keyboard interaction the original "second draft" was
  meant to catch.
- Add an **optional static-analysis script** (all engines: Vega, D3, mermaid)
  that mechanically flags render-blocking defects; prose stands on its own.

**Decision flow (visualization-decision-flow)**

- Make reference reading **mandatory through proof-of-work gates**: each design
  step produces an output only its reference lets the agent produce, so skipping
  leaves a visible hole. The principle catalog stays inlined in `SKILL.md` (fat
  spine); the gates, not polite wording, pull the references in.
- **BREAKING**: Remove the engine default. The engine is chosen by reasoning
  over criteria with all engines — Markdown/mermaid, Vega, D3 — held equal.
  Content type selects mermaid (flowchart/sequence/gantt) even for browser
  surfaces; custom interactivity selects D3; sankey selects D3. When criteria do
  not discriminate, the agent **asks the user** an informed question in their own
  terms, after reasoning.
- Treat accessibility as a held-constant floor every engine must meet, not an
  engine-selection criterion.
- Collapse the phase/mode duality into one ordered process and retire
  "Refine" as a Build mode — it is the Verify phase.

**Templates (visualization-templates)**

- Make **every template composable**: multiple visualizations coexist in one
  HTML document without colliding IDs, leaking CSS, clashing globals, shared
  body-level singletons, or page-level scroll/zoom capture.
- Introduce **cross-engine shared components**: a single OpenColors accessible
  color theme used across engines, and a diagram-isolation wrapper that sandboxes
  any one chart when several share a page.
- Fix **per-template** correctness and accessibility defects so no known-broken
  template ships.
- Port a one-shot-resilient **mermaid configuration** into the mermaid templates.

## Capabilities

### New Capabilities

- `visualization-verification`: how the skill confirms a chart is correct before
  presenting it — render-free, all-engine, no screenshots ever.
- `visualization-decision-flow`: how the skill decides — mandatory
  reference-grounded reads and a no-default, criteria-based engine choice that
  serves a non-expert user.
- `visualization-templates`: how templates behave alone and composed —
  collision-free composition, cross-engine shared theme and isolation, and
  defect-free shipping.

### Modified Capabilities

<!-- None. No existing specs under openspec/specs/; this introduces the first. -->

## Impact

- **Skill prose**: `skills/visualize/SKILL.md` (Phase 4 protocol, workflow,
  engine selection, mode tables), and `references/` — `phase-refine.md`,
  `mode-refine.md`, `phase-implement.md`, `phase-context.md`, `phase-research.md`,
  `engine-selection.md`, `markdown-patterns.md`, and each `mode-*.md`.
- **Assets**: `assets/vega/templates/**`, `assets/vega/wrapper.html`,
  `assets/d3/templates/**`, `assets/d3/_shared/**`, `assets/d3/fragments/**`,
  `assets/markdown/templates/**` (mermaid config) — composition, shared theme,
  isolation, and per-template fixes.
- **Scripts**: new static-analysis script under `scripts/`; `build_d3.py` may
  need to regenerate D3 templates after shared-scaffold changes.
- **Tests**: fixtures and tests under `skills/visualize/evals/` (skill-root
  `evals/` is excluded from the `.skill` package).
- **Packaging**: regenerate `packaged/visualize.skill`; refresh any
  `extensions/` bundle.
