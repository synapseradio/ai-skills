# visualization-templates Specification

## Purpose

TBD - created by archiving change visualize-improvements. Update Purpose after archive.

## Requirements

### Requirement: Templates compose without collision

Every template SHALL be safe to place alongside other templates in one HTML
document. Multiple visualizations in one document MUST coexist without colliding
element IDs, leaking global CSS, clashing JavaScript globals, shared body-level
singletons, or page-level scroll and zoom capture. Identifiers and styles MUST be
scoped per instance.

#### Scenario: Two charts in one document

- **WHEN** two templates are placed in the same `index.html`
- **THEN** both render correctly, their IDs and styles do not collide, and neither captures the host page's scroll

#### Scenario: Repeated template instances

- **WHEN** the same template is instantiated more than once in one document
- **THEN** each instance is independently scoped and renders without interfering with the others

### Requirement: A single cross-engine color theme is the source of color

Color SHALL come from one shared OpenColors accessible theme used across engines.
Templates MUST reference the shared theme rather than duplicating palette values,
so a change to the theme propagates everywhere.

#### Scenario: Theme change propagates

- **WHEN** the shared OpenColors theme is changed
- **THEN** Vega, D3, and mermaid outputs reflect the change without per-template palette edits

### Requirement: A diagram-isolation component sandboxes a single chart

The skill SHALL provide an isolation wrapper that sandboxes any one chart when
several are requested in one document. Each chart placed in the wrapper MUST be
isolated from the styles, scripts, and scroll behavior of its neighbors.

#### Scenario: Several visualizations requested at once

- **WHEN** the user asks for more than one visualization in a single page
- **THEN** each chart is placed in the isolation wrapper and cannot affect its neighbors

### Requirement: No known-broken template ships

Templates SHALL ship free of known correctness and accessibility defects:
zero baselines on length encodings, units on axes and tooltips, SVG
title/description, a working data-table fallback, and keyboard wiring on
interactive marks. A template MUST pass the verification checks before it ships.

#### Scenario: Audit gate on shipped templates

- **WHEN** the static-analysis checks are run across all shipped templates
- **THEN** every template passes, with no render-blocking or accessibility defect remaining

### Requirement: Mermaid templates carry a one-shot-resilient configuration

Mermaid templates SHALL embed a configuration that survives common one-shot
failure modes — diagram overflow, label wrapping, oversized text, and parse
fragility from special characters. The configuration MUST be applied by default
in the mermaid HTML bundle.

#### Scenario: Dense flowchart renders cleanly

- **WHEN** a flowchart with long labels and special characters is produced
- **THEN** it renders within its container without overflow or parse failure
