# visualization-decision-flow Specification

## Purpose

TBD - created by archiving change visualize-improvements. Update Purpose after archive.

## Requirements

### Requirement: Reference reading is mandatory through proof-of-work gates

The skill SHALL require its design references to be read at the point of need by
gating each design step behind an output that can only be produced from the
reference. The progression MUST treat a step as incomplete when its
reference-derived output is absent. Permissive phrasing that lets the agent judge
whether a reference is needed MUST be removed.

#### Scenario: Encoding step gated on reference-derived output

- **WHEN** the agent reaches the encoding step
- **THEN** it must produce the encoding table with each channel's effectiveness rank, which it cannot fill from memory, forcing the encode reference to be read

#### Scenario: Skipping a reference leaves a visible hole

- **WHEN** the agent advances without the reference-derived output for a step
- **THEN** the step is treated as incomplete and the agent cannot proceed to the next step

### Requirement: Engine selection has no default

The skill SHALL choose the engine by reasoning over criteria with all engines —
Markdown/mermaid, Vega, and D3 — held equal. No engine MAY be selected as a
fallthrough default. The chosen engine MUST be justified by a criterion the agent
states.

#### Scenario: Common browser chart is not auto-assigned to Vega

- **WHEN** a simple quantitative chart targets a browser surface
- **THEN** the agent reasons over the criteria rather than defaulting to Vega, and states the criterion that decides the engine

### Requirement: All three engines are weighed, content type can select mermaid

Engine reasoning SHALL consider Markdown/mermaid, Vega, and D3 every time.
Content type MUST be a criterion: process, flow, sequence, and timeline diagrams
select mermaid even when the destination is a browser, because mermaid is the
only engine with those templates.

#### Scenario: Flowchart for a dashboard selects mermaid

- **WHEN** the user asks for a flowchart or process diagram destined for a browser surface
- **THEN** the agent selects mermaid (emitted as standalone HTML), not Vega or D3

### Requirement: Unresolved criteria trigger an informed question

When the discriminating criteria do not select an engine, the skill SHALL ask the
user a question phrased in the user's terms, after reasoning, so the question
carries the context a non-expert needs. It MUST NOT resolve the tie silently.

#### Scenario: Static-versus-interactive tie asks the user

- **WHEN** criteria leave a chart equally servable as static or interactive
- **THEN** the agent asks whether the user needs to hover or filter the data versus a static picture, rather than picking an engine silently

### Requirement: Accessibility is a held-constant floor, not an engine criterion

The skill SHALL require every engine to meet the same accessibility floor and
MUST NOT use accessibility to select an engine. Per-mark keyboard reachability is
required only where interaction exists, which the interactivity criterion already
governs.

#### Scenario: Static chart meets the floor on any engine

- **WHEN** a static chart is produced on any engine
- **THEN** accessibility is satisfied through the data-table fallback and SVG title/description, without that need steering the engine choice

### Requirement: One ordered process, with Refine as the Verify phase

The skill SHALL present its phases and modes as a single ordered design process.
"Refine" MUST be the Verify phase, not an item in the Build-phase mode menu.

#### Scenario: Refine is not offered as a Build mode

- **WHEN** the agent is in the Build phase choosing what to apply
- **THEN** the available modes are encode, compose, narrate, interact, and access, and Refine appears only as the Verify phase
