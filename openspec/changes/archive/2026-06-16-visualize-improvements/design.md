# Design: visualize-improvements

This change spans three capabilities that share one root cause — the skill
resolving consequential choices silently. The verification design comes first,
then decision flow, then templates. Each section carries its own context,
decisions, and risks.

# Verification (visualization-verification)

## Context

The visualize skill verifies every chart in Phase 4 through two paths that must
agree: a structural read-back of the code, and a "visual" path that opens the
artifact in Chrome and reads a screenshot (`skills/visualize/SKILL.md:161-169`,
`skills/visualize/references/phase-refine.md:29-46`). The screenshot path is the
problem this change targets: screen capture is a high-trust permission, and
requiring it for a quick chart pushes the cost onto every user, with
non-technical and one-shot users least able to absorb it.

The skill already contains the seam for a render-free alternative. `mode-refine.md`
splits its audit into a "Structural Audit — Verifiable by Reading Code" and a
"Perceptual Audit — Verifiable by Reasoning About the Spec," the latter stating
plainly that the checks "require reasoning about what the spec will render, not
running it" (`skills/visualize/references/mode-refine.md:65-91`). The markdown
output path is already screenshot-free (`skills/visualize/SKILL.md:171-186`). So
the work is to promote an existing reasoning discipline to the default for HTML
output, retire the screenshot gate, and add an optional mechanical accelerator —
rather than to invent a verification method from scratch.

## Goals / Non-Goals

**Goals:**

- Phase 4 reaches a pass/fail decision from artifact source alone, with no
  browser, browser MCP, or screen capture in the required path.
- Preserve the existing two-pass consensus rigor; both passes become render-free.
- Predict, from source, the defect classes the screenshot was used to catch.
- Provide an optional static-analysis script that mechanically flags
  render-blocking defects, useful to power users, never required.
- Hold one-shot and iterative users to one verification standard.

**Non-Goals:**

- Pixel-level visual fidelity (exact font metrics, sub-pixel spacing, anti-alias
  artifacts). Those need a real renderer and stay out of the required path.
- Removing the Phase 6 presentation `open` that shows the user their finished
  chart. That step captures nothing, is not verification, and stays. What is
  removed is screenshotting and any browser-open used to *verify* a chart —
  including as an opt-in step the agent might suggest.
- Evaluating arbitrary hand-written D3 draw logic by execution. The script
  covers D3 — see Decision 3 — through structural, wiring, and embedded-data
  checks; it does not run the JavaScript or trace custom imperative drawing.
- Shipping the script's tests and fixtures inside the distributed skill.

## Decisions

### Decision 1: Promote reasoning-based audit to the primary render path, rename Path B

Replace Phase 4 "Path B: Visual Verification" with "Path B: Render Inference"
across `SKILL.md` and `phase-refine.md`. The pass reuses and extends the
Perceptual Audit already in `mode-refine.md`, keeping the "two passes, consensus
required" structure intact.

- **Why over alternatives:** Keeping a separate screenshot path "for when tools
  exist" would leave the security ask in place and split the verification
  standard by environment. A single render-free Path B gives one standard
  everywhere. Reusing the existing audit avoids a parallel, drifting checklist.

### Decision 2: A render-inference checklist derived from what screenshots catch

Each screenshot-era check maps to a source-level inference:

| Screenshot caught | Inferred from source |
|---|---|
| Overflow / clipping | Mark/label extents vs. declared `width`/`height`/viewBox and margins |
| Label collision / unreadable text | Tick count × estimated label length vs. available axis span |
| Wrong axis domain / non-zero bar baseline | `scale.domain` / `"zero"` settings on the quantitative axis |
| Empty or partial chart | Encoding fields cross-checked against bound data row keys |
| Missing marks | Declared mark count / data length consistency |
| Broken legend | Legend definition wired to the same field/scale as the series |
| Chart fails to render at all | Engine wiring: required CDN scripts present, render call present, JSON well-formed |
| Page scroll hijacked by the chart | Wheel/touchmove/zoom handlers, `overflow`/`100vh` on the embed container — scroll-eating patterns are in the code |
| Keyboard interaction dead | Interactive marks carry `tabindex`, key handlers, and focus styles (a screenshot never showed this anyway) |

- **Why:** This makes the render-free path auditable and testable — each row is a
  scenario in the spec. The agent reasons about geometry and wiring it can read,
  not pixels it cannot.

### Decision 3: Prose-first, optional Python script covering all three engines

The prose protocol is complete on its own. The optional script lives under
`skills/visualize/scripts/` (alongside `build_d3.py`, `visualizer.py`), uses
Python stdlib only, detects which engine an input uses, and checks all three:

- **Vega** (`.vg.json` and the JSON embedded in the Vega wrapper HTML): JSON
  well-formedness, scale domains, zero baselines on length encodings, and
  encoding fields cross-checked against the bound data rows.
- **mermaid** (`.md` mermaid blocks and `.html.tmpl` bundles): extract the
  diagram source, check it parses as a recognized diagram type with balanced
  structure, and verify the mermaid.js wiring and render call in HTML bundles.
- **D3** (standalone template HTML): structural and wiring checks (required CDN
  scripts, the render call, `<title>`/`<desc>`, data-table `<details>`) plus
  embedded-data sanity where the data and field references are declared inline.

The script prints defects with file and cause, exits non-zero when
render-blocking defects are found, and degrades to a clear "not applicable"
rather than failing the workflow.

- **Why over alternatives:** A required script would reintroduce an environmental
  dependency (Python availability, parse coverage) as a new gate — the exact
  failure mode we are removing for browsers. Stdlib-only keeps it runnable
  wherever Python is. Engine depth varies with how declarative each engine is —
  Vega JSON yields the deepest mechanical checks, mermaid source parses cleanly,
  and D3's imperative draw logic caps what static analysis can prove, so the D3
  checks target structure and wiring while prose reasoning carries D3 draw intent.

### Decision 3a: Tests live in the skill but never ship

The script's tests and broken-spec fixtures live under `skills/visualize/evals/`.
The packager's `ROOT_EXCLUDE_DIRS = {"evals"}` drops a skill-root `evals/`
directory from the `.skill` archive, so the tests stay co-located with the source
for maintainers yet never reach an installed user.

- **Why over alternatives:** Putting fixtures under `scripts/` would ship them
  inside `packaged/visualize.skill`, bloating the distributed artifact with test
  data. The repo-level `examples/` tree is also non-installable, but `evals/`
  keeps the tests next to the code they exercise while the packager guarantees
  exclusion.

### Decision 4: Keep one standard for both user types

The non-technical one-shot path and the power-user iterative path share the same
pass/fail criteria. Depth differs (a power user may run the script and open a
browser); the bar to present does not.

- **Why:** A standard that loosens for one-shot users would make the cheap path
  the untrustworthy path — the opposite of the goal.

## Risks / Trade-offs

- **Render inference misses a genuinely visual defect** (e.g., a font that
  overflows in ways the estimate did not predict) → Mitigation: conservative
  extent estimates that flag when crowding is plausible; the static-analysis
  script catches mechanical defects the prose pass might gloss; the protocol
  states its limits honestly rather than implying pixel certainty. No browser
  fallback is offered — the screenshot capability is removed by design, so the
  mitigation is rigor in the source-level checks, not an escape hatch.
- **Static analysis of D3 imperative draw logic is brittle** → Mitigation: the
  script still covers D3, but its D3 checks target structure, wiring, and
  embedded data rather than executing the JavaScript; prose reasoning carries D3
  draw intent; the script never gates the workflow.
- **Removing the screenshot capability is BREAKING for any flow that assumed it** →
  Mitigation: no opt-in is offered — the capability is removed by design; the
  change is documented as BREAKING in the proposal; no other skill depends on it,
  and the Phase 6 presentation `open` (which captures nothing) still shows the
  user their chart.
- **Two render-free passes could collapse into one** if both just re-read code →
  Mitigation: keep the passes distinct in purpose — structural validates the code
  is correct; render-inference predicts what that correct code will draw — and
  require an explicit consensus step.

## Migration Plan

1. Edit `SKILL.md` Phase 4 row (line 151) and the Phase 4 protocol block
   (lines 157-186): rename Path B to Render Inference, remove the `open -a` /
   screenshot instructions, point to the render-inference checklist.
2. Edit `references/phase-refine.md`: replace Path B with the render-inference
   checklist; keep consensus and fix-priority sections.
3. Edit `references/mode-refine.md`: present the reasoning-based audit as the
   primary render path; align headings.
4. Add the optional script under `scripts/` and reference it as optional in the
   protocol.
5. Regenerate `packaged/visualize.skill` with the official packager; refresh the
   `extensions/` bundle if one exists for this skill.
6. Rollback: revert the prose edits and the script; the prior screenshot
   protocol returns with no data migration.

## Open Questions

- For mermaid, how far should "parses as a recognized diagram type" go before it
  duplicates mermaid's own parser? (Leaning: structural sanity only — diagram
  keyword recognized, blocks balanced — not a full grammar.)

# Decision flow (visualization-decision-flow)

## Context

`SKILL.md` inlines the full principle catalog (encoding, composition, color,
narrative, spacing, simplicity), and the mode docs hold the application
methodology — `mode-encode.md:3` states the split outright. The agent reads
`SKILL.md`, comes away holding the principles, produces something plausible, and
never feels the absence of the HOW, so the references go unread. Separately, the
engine decision tree ends in a default leaf ("everything else → Vega",
`engine-selection.md:29`), and it asks render surface first
(`engine-selection.md:11`), which silently eliminates mermaid for any browser
target even though mermaid emits standalone HTML (`engine-selection.md:22-25`)
and owns the only flow/sequence/gantt templates.

## Goals / Non-Goals

**Goals:** references read at the point of need; engine chosen by an explicit,
stated, criteria-based decision among equals; a non-expert served by reasoning
plus, when needed, one informed question; the phase/mode model coherent.

**Non-Goals:** thinning `SKILL.md` (the fat spine stays); a weighted-score
decision matrix; making D3 more frequent for its own sake.

## Decisions

### Decision F1: Fat spine, gates do the pulling

Keep the inlined principles in `SKILL.md` for triggering and quick lookup.
Force the references in through proof-of-work gates — each step emits an output
only its reference lets the agent produce (e.g., an encoding table citing the
channel-effectiveness ranks from the encode reference).

- **Why over thinning:** stripping principles from `SKILL.md` would force the
  fetch but risk the skill triggering and quick-reference value. Gates get the
  references read without losing the spine.

### Decision F2: No-default, criteria-among-equals, ask after reasoning

Replace the decision tree's default leaf with a criteria evaluation over
Markdown/mermaid, Vega, and D3 held equal. Criteria: content type (process/flow
→ mermaid), render surface (markdown-only → Markdown engine), custom
interactivity (→ D3), structural capability (sankey → D3), auditability (informs,
never auto-resolves). When criteria do not discriminate, ask the user a question
in their terms after reasoning.

- **Why:** a default is the engine equivalent of a skipped reference — a choice by
  omission. Reasoning then asking makes the easy cases collapse and reserves the
  question for genuine forks, phrased so the answer teaches a non-expert.
- **Why not a weighted matrix:** invented weights launder a gut call; yes/no
  discriminators plus one informed question are more honest and auditable.

### Decision F3: Accessibility is a floor, not a criterion

Every engine meets the same accessibility floor; accessibility never selects an
engine. Per-mark keyboard reachability matters only where interaction exists,
which the interactivity criterion already governs.

### Decision F4: One ordered process; Refine is Verify

Collapse the phase/mode duality into a single ordered process and retire "Refine"
as a Build mode — it is the Verify phase, sitting at a different level than
encode/compose/narrate/interact/access.

## Risks / Trade-offs

- **Gates add steps to the one-shot path** → Mitigation: gate outputs are the
  artifacts the agent should produce anyway (encoding table, etc.); the cost buys
  the quality the references carry.
- **"Ask the user" could fire too often and nag** → Mitigation: it fires only
  after reasoning fails to discriminate; most requests resolve on criteria.

# Templates (visualization-templates)

## Context

Templates were authored as standalone pages. Composing several into one document
surfaces collision bugs (duplicate IDs, leaking CSS, clashing globals, body-level
tooltip singletons, page-level scroll capture), and color is duplicated per
template rather than shared. A bug-hunt across all templates is in flight; its
findings populate the task list.

## Goals / Non-Goals

**Goals:** every template composable and isolatable; one cross-engine OpenColors
theme; no known-broken template ships; mermaid one-shot resilience.

**Non-Goals:** redesigning chart types or adding new ones; changing the template
catalogue's coverage.

## Decisions

### Decision T1: Composition by per-instance scoping

Make templates safe to co-locate by scoping identifiers and styles per instance
and containing scroll/zoom to the chart's own container, rather than relying on
the page being single-chart.

### Decision T2: Shared theme and isolation in the D3 `_shared` layer

`assets/d3/_shared/` already centralizes scaffold; extend that seam toward the
cross-engine shared OpenColors theme and a diagram-isolation wrapper, so the
shared layer is the single source for color and sandboxing.

### Decision T3: The verification script is the template audit gate

Author the verification checks once (Change-internal, the
visualization-verification capability); run them across all templates to find
defects and to gate shipping. The bug list becomes tasks, not new requirements.

### Decision T4: The skeleton is canonical — repair it and regenerate

The D3 build tooling is broken and the committed templates have drifted from it.
`assets/d3/_shared/skeleton.html` carries placeholders as `EXTRA_IMPORTS;` /
`HELPERS_JS;` / `CHART_JS;` rather than `{{...}}`, so `build_d3.py`'s substitution
never matches and `--check` reports all 25 drifted; meanwhile 7 committed
templates use external `<link>`/`<script src>` while 19 inline the shared assets.

**Decision:** the skeleton plus `_shared`/fragments is the single source of truth.
Repair the skeleton placeholders, settle on the inline model, and regenerate every
D3 template from it. The 7 divergent external-`<link>` templates are regenerated
into the canonical inline form, which dissolves the inline-versus-link split (B2)
as a side effect. Every composability and theme fix (B1–B4, the shared theme)
lands once in the skeleton/`_shared`/fragments and propagates by regeneration, so
no fix is reapplied 26 times.

- **Why over retiring the script:** a generator keeps the 25+ templates
  consistent and makes the shared-layer fixes land in one place; hand-maintaining
  them is what let them drift in the first place.

**Reality correction (found during apply).** The drift root cause is the repo's
own format hook: `.prettierignore` does not exclude `*.html`, and lefthook's
`prettier-html` job runs `prettier --write` on every staged `.html` with
`stage_fixed: true`. Prettier mangled the skeleton's JS-context `{{...}}`
placeholders into `{ { EXTRA_IMPORTS; } }`, and — because the fragments hold raw
JS *outside* any `<script>` — it collapsed and comment-killed the `chart-js` in 24
of 25 `*.frag.html` files and wrapped their frontmatter. The fragments are
therefore not recoverable source. The committed `templates/*.html` survived intact
(their JS lives inside `<script>`, which prettier formats correctly). So T4 is
executed in reverse: the **intact templates are the recovery source**, fragments
are reconstructed *from* them, the skeleton is repaired, and the entire D3 build
tree (`_shared/skeleton.html`, `fragments/`, `templates/`) is added to
`.prettierignore` so the generator — now the single formatter of record for these
files — can no longer be overwritten by prettier. Without that ignore, any fix
recurs on the next commit.

### Decision T6: Fragment + single engine-agnostic wrapper (supersedes the standalone-file model)

The composability requirement cannot be met by standalone full-document templates:
you cannot validly nest several `<!doctype html>` documents in one page. The
resolution (user decision during apply) is to make **every chart a fragment** and
provide **one engine-agnostic base wrapper** that hosts one or more fragments. The
single-file deliverable is preserved by *assembling* wrapper + fragment(s) into one
runnable HTML file; composition is several fragments in the one wrapper.

**The contract:**

- `assets/_shared/wrapper.html` — engine-agnostic base. Placeholders: `{{TITLE}}`,
  `{{HEAD}}` (deduped engine imports/CDN + the inlined `{{STYLE}}`), `{{BODY}}`
  (the assembled fragment bodies). It carries the page chrome (`body`, the centered
  card) once.
- `assets/_shared/theme.css` — the single source of color: the OpenColors `:root`
  tokens (T2). D3/CSS consume the vars; the assembler also exposes the same tokens
  as a JS object for Vega `config` and mermaid `themeVariables`, so one edit
  propagates to all three engines.
- `assets/_shared/*.js` — shared helpers (tooltip, keyboard nav, data table)
  rewritten to be **root-scoped**: each takes the fragment's root element rather
  than reaching for document-global `#tooltip`/`#data-table` (fixes B1/B4). The
  assembler inlines them once on a `VizHelpers` namespace shared by every fragment.
- `assets/<engine>/fragments/<cat>/<name>.frag.html` — a chart fragment: a
  per-instance-scoped `<section class="viz" data-viz="<uid>">` (figcaption title +
  subtitle, the chart mount, a per-instance tooltip, the `<details>` data table)
  plus one scoped `<script>`. No `<!doctype>`/`<head>`/`<body>`. All ids and CSS
  are scoped under the section root; scroll/zoom is contained to it.
- `assets/<engine>/templates/<cat>/<name>.html` — the **generated** runnable
  single-chart example (wrapper + one fragment), kept for the "open a file" UX.
- `scripts/build_viz.py` — the generalized assembler (evolves `build_d3.py`):
  assigns per-instance uids, dedupes engine imports, injects theme + scoped helpers,
  and emits the example. `--check` verifies committed examples match assembly.

This makes T1 (composition by per-instance scoping), T2 (shared theme), and T3/T4
(generator authoritative) land in **one** place — the wrapper + `_shared` — and
propagate to every engine by regeneration. The prettier exclusion (above) covers
the whole generated tree so the assembler stays the single formatter of record.

### Decision T5: Keep mermaid `securityLevel` strict by default

The docsify config that informs the mermaid hardening sets
`securityLevel: 'loose'` to enable `click href` cross-links. The visualize
templates have no clickable nodes, and loosening the security posture is a user
decision, not a default. The hardened mermaid config adopts the structural
settings (spacing, `htmlLabels`, themeCSS wrapping, renderer, orientation) but
leaves `securityLevel` at its strict default.

## Risks / Trade-offs

- **Touching shared scaffold regenerates many templates** → Mitigation:
  `build_d3.py` regenerates D3 templates from `_shared/` + fragments; change the
  shared layer once and rebuild rather than editing each template.
- **The audit may surface more than expected** → Mitigation: the templates spec
  fixes the invariants; specific fixes append to tasks as the audit reports, so
  scope stays visible.

## Open Questions

- Does the cross-engine theme live as a small shared file both the Vega wrapper
  and D3 `_shared` import, or is it duplicated per engine with a single source of
  truth that the build copies? (Pending the audit's read of how `_shared` is
  consumed.)
