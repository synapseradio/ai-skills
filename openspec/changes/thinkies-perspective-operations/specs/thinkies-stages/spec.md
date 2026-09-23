# Spec Delta: thinkies-stages

## Purpose

Divides the work of every thinkies skill into three stages: analysis,
interaction, and presentation. Analysis ends at a structured result. Only a
presentation step, working from that result, produces output shaped for a
reader.

## ADDED Requirements

### Requirement: Every step belongs to exactly one stage

Every step of every thinkies skill SHALL do the work of exactly one of three
stages. Analysis operates on perspectives and produces the structured result.
Interaction exchanges with a person to gather input for the analysis.
Presentation shapes the structured result for a reader. A step that does the
work of two stages MUST be split where one stage's work ends and the other's
begins, and each part MUST be assigned to its own stage.

#### Scenario: A step that labels and also words the label for a reader is split

- **WHEN** a step assigns a label and also tells the reader how to read it, as
  `calibrate-confidence` step 7 does by sorting uncertainty into personal
  ignorance or collective uncertainty and then saying "Show where certainty
  ends and speculation begins"
- **THEN** the label is an analysis step, and the instruction to show the
  boundary to a reader is a presentation step

#### Scenario: A step that tags provenance and also supplies reader phrases is split

- **WHEN** a step tags each claim as drawn from a source or as the agent's own
  analysis, and also supplies phrases such as "According to…", as
  `cite-sources` step 5 does
- **THEN** the provenance tag is an analysis step, and the phrases belong to a
  presentation step

#### Scenario: No step is left without a stage

- **WHEN** the steps of any thinkies skill are audited
- **THEN** each step, or each part of a split step, is assigned to exactly one
  stage, and no step remains unassigned

### Requirement: Analytic skills end at the structured result

An analytic skill SHALL end its run at the structured result. An analytic skill
MUST NOT contain a step whose work is shaping output for a reader. Such steps
include choosing a citation style, a prose form, a sentence length, a tone, a
delivery order, a visual, or a closing offer.

#### Scenario: Choosing a citation style leaves cite-sources

- **WHEN** `cite-sources` runs
- **THEN** its run ends at validated source records with a provenance tag on
  each claim, and the choice between formal citations, simple references, and
  inline links is made in presentation

#### Scenario: decision-analysis ends at its analysis record

- **WHEN** `decision-analysis` completes its phases
- **THEN** its run ends at the analysis record, and filling the visual template,
  explaining the theory, and offering the visual and the theory in a closing
  line all happen outside the analytic run

### Requirement: Interaction feeds the analysis

The interaction stage SHALL hold the dialogue skills `strategize`,
`question-through-dialogue`, and `ask-questions`, and every dialogue step inside
any other skill. Whatever an interaction step obtains from the person MUST enter
the analysis as an input recorded in the structured result.

#### Scenario: scamper's clarify phase runs as interaction

- **WHEN** `scamper` Phase 0 confirms with the user how the request should be
  read
- **THEN** that exchange runs as interaction, and the structured result records
  the confirmed reading as the input Phase 1 started from

#### Scenario: A dialogue step is assigned to interaction wherever it sits

- **WHEN** a step in any skill exchanges with a person to gather input
- **THEN** that step is assigned to the interaction stage, whichever file holds
  it

### Requirement: Presentation runs last and takes the structured result

Presentation SHALL run after the last analysis step of a run. A presentational
skill SHALL accept a structured result as its input, and MUST shape that result
without re-running the analysis that produced it.

#### Scenario: A presentational skill names its input

- **WHEN** the instructions of a presentational skill are read
- **THEN** they name the structured result as an input the skill accepts

#### Scenario: No analysis follows presentation within a run

- **WHEN** a run includes both analysis and presentation
- **THEN** no analysis step follows the first presentation step in that run

### Requirement: Presentation chooses a view and never reshapes the result

A presentation step SHALL choose a view of the structured result: which parts
appear, in what order, and at what level of detail. A presentation step MUST NOT
alter the structured result. Where a view merges, excludes, or omits parts of
the result, the view MUST record what it merged, excluded, or omitted, and the
structured result MUST keep every part.

#### Scenario: The decision-analysis visual fits three states

- **WHEN** the analysis record holds four states and the visual template has
  room for three
- **THEN** the visual shows three states and records which states it merged or
  excluded, and the analysis record still holds all four

### Requirement: Presentation adds no analytic judgment

A presentation step MUST NOT make an analytic judgment that the structured
result does not already contain. Where a view calls for a judgment that the
result lacks, an analysis step SHALL make that judgment and record it in the
result before the view uses it, or the view SHALL leave that slot out.

#### Scenario: The unlisted-arrival slot has no judgment behind it

- **WHEN** the decision-analysis visual asks for the most plausible state that
  could arrive unlisted, and the analysis record names none
- **THEN** the presentation step does not supply one, and the slot is either
  filled from a judgment the analysis recorded or left out of the view
