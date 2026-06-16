# Tasks: visualize-improvements

## 1. Plan and fan out

- [x] 1.1 Read every change artifact before touching code: `proposal.md`, `design.md`, and all three specs (`visualization-verification`, `visualization-decision-flow`, `visualization-templates`). The design's three capability sections each carry their own decisions and risks.
- [x] 1.2 Produce an execution plan that partitions the remaining groups into independent workstreams by specialist, and decide what fans out in parallel versus what must sequence. The natural specialists: (a) skill-prose author for the verification and decision-flow narrative (groups 2 and 4); (b) Python author for the static-analysis script and its `evals` tests (group 3); (c) Vega-spec specialist; (d) D3/JavaScript specialist for `assets/d3/templates`, `_shared`, fragments, and `build_d3.py`; (e) mermaid specialist (group 5 mermaid config + templates). Independent streams run concurrently.
- [x] 1.3 Encode the hard dependencies in the plan: resolve the D3 build source-of-truth (5.1) before any template edit, so fixes land once rather than 26×; the static-analysis script (group 3) must exist before the template audit-gate (5.8); the cross-engine theme (5.2) and isolation wrapper (5.3) precede the per-template composition and CSS-scoping fixes (5.4, 5.6); `_shared`/fragment edits precede every `build_d3.py` rebuild; packaging (group 6) runs last, after all streams land and tests pass.
- [x] 1.4 Lead with tests where a stream has them — the script's `evals` fixtures and failing tests (3.1–3.2) come before the implementation. Keep prose changes and behavior changes as separate, reviewable units of work.
- [x] 1.5 The goal is a one-shot-correct skill: assign each stream a clear mission and success check from its capability spec, so a specialist can verify its own slice without the others.

## 2. Render-free verification protocol in skill prose

- [x] 2.1 In `skills/visualize/SKILL.md`, rewrite the Phase 4 row (line 151) so it describes structural read-back plus render inference, with no "open in Chrome, read screenshot".
- [x] 2.2 In `skills/visualize/SKILL.md`, rewrite the HTML-output protocol block (lines 161-169): rename Path B to "Render Inference", remove the `open -a "Google Chrome"` step and screenshot reading, and replace the visual checklist with the render-inference checks.
- [x] 2.3 In `skills/visualize/references/phase-refine.md`, replace "Path B: Visual Verification" (lines 29-46) with "Path B: Render Inference": the source-derived checklist (overflow/clipping, label collision, axis domain/zero baseline, encoding-vs-data, mark count, legend wiring, engine wiring, scroll containment, keyboard-interaction wiring). Note that scroll hijacking and unwired keyboard interaction are the defects the original "second draft" targeted. Keep Consensus, Editorial Integrity, Fix Priority, Second Draft sections.
- [x] 2.4 In `skills/visualize/references/phase-refine.md`, remove any browser-open or screenshot step from the Second Draft section entirely — no opt-in escape, no "you could open it in a browser" suggestion.
- [x] 2.5 In `skills/visualize/references/mode-refine.md`, promote the "Perceptual Audit — Verifiable by Reasoning About the Spec" to the primary render path and align headings with phase-refine.md's render-inference checklist.
- [x] 2.6 Reconcile the markdown-output verification wording (`SKILL.md:171-186`) so it reads as one render-free family with the HTML path, and confirm `references/markdown-patterns.md` Phase 4 checklist agrees.
- [x] 2.7 Read back all edited prose: confirm no remaining required screenshot/browser/MCP step, and that one-shot and power-user paths share one pass/fail standard.

## 3. Optional static-analysis script — all engines, tests that do not ship (tests first)

- [x] 3.1 Add broken-artifact fixtures under `skills/visualize/evals/` (skill-root `evals/` is excluded from the `.skill` package). Cover all three engines: Vega (non-zero bar baseline, encoding referencing an absent data field, malformed JSON), D3 (HTML missing CDN script or render call; a scrolljacking artifact that binds a wheel/zoom handler or sets `overflow`/`100vh`; an interactive artifact whose marks lack `tabindex`/key handlers/focus), mermaid (unrecognized/unbalanced diagram source, and an HTML bundle missing mermaid.js wiring). Add one known-good artifact per engine.
- [x] 3.2 Under `skills/visualize/evals/`, write failing tests asserting the (not-yet-built) script flags each fixture's defect and passes every known-good artifact; run them and confirm they fail for the right reason.
- [x] 3.3 Implement the script under `skills/visualize/scripts/` (Python stdlib only). Detect the engine per input and check all three: Vega `.vg.json` and wrapper-embedded JSON (well-formedness, scale domains, zero baselines, encoding-vs-data); mermaid source (recognized diagram type, balanced structure, mermaid.js wiring in HTML bundles); D3 HTML (CDN scripts, render call, `<title>`/`<desc>`, data-table `<details>`, embedded-data sanity). Apply scroll-containment and keyboard-wiring checks across whichever engines emit HTML (scroll-eating wheel/zoom/`overflow`/`100vh` patterns; interactive marks missing `tabindex`/key handlers/focus).
- [x] 3.4 Make the script print defects with file and cause, exit non-zero on render-blocking defects, and degrade to a clear "not applicable" without erroring when an input is unsupported.
- [x] 3.5 Run the tests from 3.2 and confirm they pass; confirm every known-good artifact is clean.
- [x] 3.6 Reference the script in the Phase 4 prose as an optional accelerator, stating explicitly that its absence or failure does not block verification.

## 4. Decision flow — mandatory reads and no-default engine choice

- [x] 4.1 Replace permissive reference-loading language across `SKILL.md` and `references/` ("load as needed", "When to load", "load ONE based on signal") with proof-of-work gates: each design step names its mandatory reference and the reference-derived output that proves it was read.
- [x] 4.2 In `references/phase-implement.md`, define each Build sub-step's gate output (e.g., an encoding table citing channel-effectiveness ranks from the encode reference) so skipping the reference leaves a visible hole.
- [x] 4.3 Rewrite engine selection (`SKILL.md` + `references/engine-selection.md`): remove the "everything else → Vega" default; present a criteria evaluation over Markdown/mermaid, Vega, and D3 as equals; make content type a criterion (process/flow/sequence/gantt → mermaid, even for browser surfaces); add the "ask the user after reasoning" step phrased in the user's terms. (Also reconciled `phase-research.md` step 3, `template-selection.md`, and `README.md`, which carried the same default.)
- [x] 4.4 State accessibility as a held-constant floor, not an engine-selection criterion; fold per-mark keyboard nav into the interactivity criterion.
- [x] 4.5 Collapse the phase/mode duality: retire "Refine" from the Build mode list (it is the Verify phase); reconcile the mode tables and the Signal Detection routing in `SKILL.md`.
- [x] 4.6 Read back: confirm no permissive "as needed" loading language remains and that engine selection has no default leaf.

## 5. Templates — fragment + single wrapper, theme, isolation, fixes

Architecture: Design **T6** (fragment + one engine-agnostic wrapper, assembled into
runnable single-file examples). Audit findings below are verified against source;
line citations are pre-conversion (identify the defect by chart, not line, once
fragments exist). All shared fixes land in the wrapper/`_shared` and propagate by
re-assembly. The whole generated tree is excluded from prettier (root cause of the
original drift; see Design Templates "Reality correction").

- [x] 5.1 **Build the foundation FIRST.** Create `assets/_shared/wrapper.html` (engine-agnostic base: `{{TITLE}}`/`{{HEAD}}`/`{{STYLE}}`/`{{BODY}}`, page chrome once), `assets/_shared/theme.css` (single-source OpenColors `:root` tokens), and root-scoped helpers (tooltip, keyboard-nav, data-table — each takes the fragment root, no document-global `#tooltip`/`#data-table`). Generalize `build_d3.py` → `scripts/build_viz.py`: assemble wrapper + fragment(s) into a runnable example, assign per-instance uids, dedupe engine imports, inline theme + helpers once on a `VizHelpers` namespace, expose tokens as a JS object for Vega/mermaid. Prove the round-trip on ONE chart per engine before scaling.
- [x] 5.2 **Convert D3 charts to fragments (from the intact templates — Design T4 reversed).** The committed `assets/d3/templates/**/*.html` are the recovery source (the old `fragments/*.frag.html` were destroyed by prettier). Extract each into `assets/d3/fragments/<cat>/<name>.frag.html` (per-instance-scoped `<section class="viz">`, scoped `<script>`, no doctype/head/body), re-assemble examples, and **prove no JS/data/ARIA lost** by `git diff` review (only intended diffs: link→inline, scoping). `build_viz.py --check` clean.
- [x] 5.3 **Convert Vega to fragments.** The current `assets/vega/wrapper.html` embed logic becomes a per-fragment `vegaEmbed` into the scoped root with the spec inline; Vega `config` (palette/axis) sourced from the shared theme tokens, not per-spec hex. Each Vega chart becomes a fragment + assembled example.
- [x] 5.4 **Convert mermaid to fragments.** The three `.html.tmpl` become mermaid fragments carrying the hardened `mermaid.initialize` (task 5.8); the `.md.tmpl` stays a fenced-block form (no init). Scoped `<pre class="mermaid">` + `<noscript>` preserved.
- [x] 5.5 **Single-source theme across engines (T2).** No raw palette hex anywhere: D3 fragments use `var(--oc-*)` (or the JS token object), Vega `config` and mermaid `themeVariables` read the same tokens the assembler injects. Editing `theme.css` propagates to all three. (The `--oc-orange-8` relabel — formerly mislabeled `--oc-orange-7`, value `#e8590c` = true open-color orange-8 — is already applied.)
- [x] 5.6 **Composability / isolation (T1, B1, B4).** Per-instance scoping makes two fragments coexist in one wrapper: no duplicate `id`s, no leaked CSS, no clashing globals, no shared `#tooltip` singleton, scroll/zoom contained to each fragment. Verify with a two-fragments-in-one-document assembly that renders both without collision.
- [x] 5.7 **Per-template correctness & accessibility fixes (audit Section A), applied in fragments.**
    - [x] 5.7.1 A0 (HIGH, all 25 D3 SVGs): invalid ARIA nesting — `role="img"` parent makes per-mark `role="listitem"`/`aria-label` dropped (`assets/d3/templates/relationships/heatmap.html:140,323`; `relationships/radar-chart.html:180,360`; `distributions/violin-plot.html:288`; `geographic/choropleth.html:278`; +21). Switch container to `role="list"`/`group` or `graphics-document`+`graphics-symbol`.
    - [x] 5.7.2 A1 (HIGH): `relationships/heatmap.html` keyboard offsets inverted — data day-major (`:175-179`), keydown hour-major (`:356`, `:362`). Re-index by (day,hour).
    - [x] 5.7.3 A3 (HIGH): `geographic/choropleth.html:230` linear color scale on right-skewed population (`:169,215`) flattens most states. Use quantile/threshold/log.
    - [x] 5.7.4 A5 (HIGH, Vega): `assets/vega/templates/compositions/waffle-chart.vg.json:147` hardcodes tooltip percentages by category name. Derive from `datum.value`.
    - [x] 5.7.5 A2 (MED): `compositions/pie-chart.html:157` shows first word only; `fill:white` (`:156,169`) may fail contrast. Show full label; compute contrast-safe text color.
    - [x] 5.7.6 A4 (MED): candlestick red/green-only encoding (`assets/vega/templates/temporal/candlestick.vg.json:6,82` + D3 twin). Add redundant shape (hollow vs filled body).
    - [x] 5.7.7 A6 (MED): `temporal/sparkline.html:244-249` has `<title>` but no `<desc>` and no chart-level title/desc pair. Add them.
    - [x] 5.7.8 A7 (MED): `networks/sankey.html` ships placeholder frontmatter (`:2-3`), dead `totalSourceFlow` (`:526-538`), and a misleading percentage base. Fill metadata, remove dead code, fix the base.
    - [x] 5.7.9 A8 (LOW): `relationships/radar-chart.html:396-406` keyboard can't cross series. Add cross-series traversal.
- [x] 5.8 **Mermaid hardening (audit B5 + mermaid-config report).**
    - [x] 5.8.1 Harden `mermaid.initialize` in the three `.html.tmpl` (`assets/markdown/templates/mermaid-flowchart.html.tmpl:87`, `mermaid-sequence.html.tmpl:96`, `mermaid-gantt.html.tmpl:101`): `theme:'base'` + `themeVariables` (fontSize, `fontFamily:'system-ui,...'`, contrast colors drawn from the shared OpenColors theme, not brand hexes), the `flowchart` sub-options (`htmlLabels:true`, `defaultRenderer:'dagre-wrapper'`, `curve:'monotoneY'`, `nodeSpacing:70`, `rankSpacing:100`, `padding:34`, `useMaxWidth:true`, `diagramPadding:16`), and a `themeCSS` with node-label `white-space:normal`+padding and edge-label padding. Highest-value pairing: `htmlLabels:true` + themeCSS wrapping.
    - [x] 5.8.2 Fix orientation `LR`→`TD` in `mermaid-flowchart.html.tmpl:71` and `mermaid-flowchart.md.tmpl:13` (LR shrinks labels unreadably on column-width surfaces).
    - [x] 5.8.3 Keep `securityLevel` strict by default (Design T5) — do not silently loosen; the templates have no clickable nodes.
    - [x] 5.8.4 `.md.tmpl` caveat: fenced blocks cannot carry init and per-block `%%{init}%%` is banned — only `TD` orientation + short labels are portable there.
    - [x] 5.8.5 Update `references/markdown-patterns.md:128-136` to teach the hardened initialize, the setting→failure table, and the `TD`-not-`LR` rule.
- [x] 5.9 Gate: `scripts/build_viz.py --check` clean (assembled examples match), then `scripts/check_render.py` passes on every generated example across all three engines, plus the two-fragments-in-one-document composition assembly. Confirm no known-broken template ships.

## 6. Package and verify

- [x] 6.1 Regenerate `packaged/visualize.skill` with the official skill-creator packager.
- [x] 6.2 Confirm `packaged/visualize.skill` excludes `evals/` (tests and fixtures do not ship), while including the script under `scripts/`.
- [x] 6.3 Refresh the `extensions/` bundle for this skill if one exists; otherwise note none exists.
- [x] 6.4 Run `openspec validate "visualize-improvements"` and confirm it passes.
- [x] 6.5 Final review: grep the skill for `screenshot`, `screen record`, `open -a`, and `chrome`. Confirm no step takes or suggests a screenshot, and that the only surviving `open` is the Phase 6 presentation step that shows the user their finished chart. Any other hit (e.g. the narrate "screenshot test" metaphor) must be unrelated to capturing the screen.
