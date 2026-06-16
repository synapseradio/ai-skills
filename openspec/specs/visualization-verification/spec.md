# visualization-verification Specification

## Purpose

TBD - created by archiving change visualize-improvements. Update Purpose after archive.

## Requirements

### Requirement: The skill never screenshots and never suggests screenshotting

The skill MUST NOT capture a screenshot, take a screen recording, or drive a
browser to inspect a chart at any point, and it MUST NOT suggest, instruct, or
invite the user to capture a screenshot of a chart. The screenshot-based
verification capability is removed from the skill entirely. Opening a finished
artifact for the user to view during presentation (Phase 6) is a separate act
that captures nothing and is not affected by this requirement.

#### Scenario: Agent never captures a screenshot

- **WHEN** the skill runs end to end
- **THEN** it takes no screenshot or screen recording and drives no browser to inspect the chart

#### Scenario: Agent never suggests a screenshot

- **WHEN** the skill presents results or guidance to the user
- **THEN** it does not instruct or invite the user to screenshot, photograph, or screen-record the chart

#### Scenario: No permission prompt for screen access

- **WHEN** a one-shot visualization request is fulfilled end to end
- **THEN** the workflow requests no screen-recording, screenshot, or browser-control permission

### Requirement: Verification decides from artifact source alone

Phase 4 verification SHALL reach a pass or fail decision using only the
generated artifact source (Vega JSON, D3/mermaid HTML, or markdown). It MUST NOT
require opening a browser, invoking a browser MCP, or any rendered preview.

#### Scenario: Agent has no browser or screen-capture tools

- **WHEN** an agent without browser automation or screen-capture access finishes a draft chart
- **THEN** it completes Phase 4 verification from the artifact source alone and proceeds to Present

### Requirement: Two independent render-free passes must reach consensus

Phase 4 SHALL run two passes over the artifact source — a structural pass over
the code and a render-inference pass that predicts the rendered outcome — and
both MUST agree the artifact is correct before it is presented. When the passes
disagree, the agent SHALL treat the artifact as failing, fix the cited defect,
and re-run both passes.

#### Scenario: Passes disagree

- **WHEN** the structural pass reports a missing unit but the render-inference pass reports no visible problem
- **THEN** the agent treats the artifact as failing, fixes the defect, and re-verifies

#### Scenario: Both passes agree

- **WHEN** both passes find no defects
- **THEN** the artifact advances to Phase 5 (Present)

### Requirement: Render inference predicts rendered defects from source

The render-inference pass SHALL predict, from the spec or HTML alone, the
defects a screenshot was previously used to catch. It MUST at minimum check:
element overflow or clipping against the declared viewport or SVG dimensions;
overlapping or unreadable axis and data labels given tick counts and label
lengths; axis domains, including a zero baseline on bar length encodings; mark
count consistency with the bound data rows; legend-to-series wiring; encodings
that would yield empty, NaN, or undefined output; engine wiring such as required
CDN scripts and the render call for the chosen engine; **scroll containment**
(wheel, touchmove, zoom/pan, or `overflow`/`100vh` patterns that would hijack the
host page's scroll); and **keyboard-interaction wiring** (interactive marks carry
`tabindex`, key handlers, and visible focus, so interactivity is reachable
without a mouse). Scroll hijacking and unwired keyboard interaction are the
defects the prior screenshot-based "second draft" was meant to catch, and both
are detectable from source.

#### Scenario: Predicted label collision

- **WHEN** a category axis binds more labels than the declared width can show without overlap
- **THEN** the render-inference pass flags a label-collision defect with the field and the crowding cause

#### Scenario: Predicted empty render

- **WHEN** an encoding references a data field absent from the bound rows
- **THEN** the render-inference pass flags a render-blocking defect before Present

#### Scenario: Predicted scroll hijack

- **WHEN** an artifact binds a wheel/zoom handler or sets `overflow`/`100vh` in a way that would capture the host page's scroll
- **THEN** the render-inference pass flags a scroll-containment defect before Present

#### Scenario: Interactive marks lack keyboard wiring

- **WHEN** an artifact defines interactive marks without `tabindex`, key handlers, or visible focus
- **THEN** the render-inference pass flags a keyboard-wiring defect before Present

### Requirement: Static-analysis script is an optional accelerator across all engines

The skill SHALL provide an optional script that parses a generated artifact and
mechanically reports render-blocking defects. The script MUST accept artifacts
from all three engines — Vega, D3, and mermaid — and report defects for whichever
engine an input uses. The prose protocol MUST be sufficient on its own; the
script MUST NOT be a prerequisite for completing verification, and its absence or
failure to run MUST NOT block the workflow.

#### Scenario: Script is unavailable

- **WHEN** the static-analysis script cannot run in the current environment
- **THEN** the agent completes verification using the prose protocol and presents the result

#### Scenario: Each engine is checked

- **WHEN** the script is given a Vega spec, a D3 HTML artifact, and a mermaid artifact in turn
- **THEN** it identifies each artifact's engine and reports render-blocking defects for that engine rather than skipping it

#### Scenario: Power user runs the script

- **WHEN** a user asks for a mechanical check across iterations
- **THEN** the agent runs the script, folds its findings into the render-inference pass, and reports flagged defects

### Requirement: Verification serves one-shot and iterative users at one standard

The protocol SHALL let a non-technical user reach a trustworthy result in a
single turn with no extra steps, while letting a power user apply the same checks
at greater depth across turns. Both paths MUST use the same pass/fail criteria so
the verification standard does not vary by user.

#### Scenario: Non-technical one-shot request

- **WHEN** a non-technical user asks for a quick chart and gives no further input
- **THEN** the agent verifies and presents in one turn without asking the user to inspect or screenshot anything

#### Scenario: Power-user iteration

- **WHEN** a power user refines a chart across several turns
- **THEN** each iteration is held to the same render-free pass/fail criteria as the one-shot path

### Requirement: Markdown output keeps a render-free verification path

Markdown-engine output (`.md`) SHALL be verified without a screenshot, using a
structural read-back plus a render-confirmation step appropriate to the
destination surface. This path MUST remain consistent in standard with the
HTML render-free protocol.

#### Scenario: Markdown with a mermaid block

- **WHEN** the output is markdown containing a mermaid block
- **THEN** verification confirms the block's structural validity from source and notes the target surface's rendering support, without capturing a screenshot
