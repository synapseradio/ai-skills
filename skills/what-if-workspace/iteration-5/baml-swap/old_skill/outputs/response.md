I read the extraction proposal, its design doc, its task list, the stub adapter package, the live inference port, the initiative ledger, and the BAML source files themselves before answering. Two facts reshape the question you asked. `extract-inference-adapter` carries a full proposal, design doc, and task list, and every line in `tasks.md` sits unchecked. The destination package, `@indra/runtime-inference-baml`, holds only scaffolding (`package.json`, tsconfig trio, `rslib.config.ts`, `vitest.config.ts`) around a `src/index.ts` that exports nothing yet. `own-inference` carries no proposal at all; the initiative ledger names it in two lines and stops there. And the entire BAML footprint today spans one client, one persona, one function, fifty-nine lines across `baml_src/`. A comment in `explore.baml` notes that the live call "only fires at task 5.2 (deferred)" — nobody has exercised it yet.

That last fact carries most of the weight below, so I want to walk you through how I got there rather than just assert it.

## What bounds this

Three things sit in front of you: the port (`Inference`, an Effect `Context.Tag` plus interface, already shaped to host more than one adapter), the BAML adapter (still living inside `@indra/runtime-core`, its result type `WelcomeResult` imported straight from the generated `baml_client`), and a hypothetical Effect-Schema adapter that doesn't exist yet. The extraction's own design doc names a hard constraint here: the port can't cleanly host a second adapter until `WelcomeResult` moves out of the generated client and into `@indra/runtime-contracts`. The doc calls the alternative — leaving the type where it sits and having the core import it — a recreation of the exact coupling the change exists to cut, and rejects it outright. Whatever you decide about BAML's future, that one move (`WelcomeResult` into contracts, the port formalized as a module the core owns) sits on the critical path either way.

## What I know, what only you can answer

Verified straight from the repo: the extraction sits specified in full, with every task on its list still unbuilt; `own-inference` has no design surface to build against; the current inference footprint amounts to one function; Effect already runs as the shared dependency across every runtime package — core, host, contracts, choreography, and the BAML adapter stub alike. So `own-inference` would add Effect Schema to a codebase where Effect itself already runs everywhere; the new dependency lands narrower than it first sounds.

One thing nothing in the repo settles, and only you can: whether you actually mean to retire BAML for good, or whether "possibly swap" leaves the door open either way. I can't ask you directly here, so that assumption survives forward as a genuine unknown rather than something I quietly picked for you.

## Which unresolvables would actually change your move

Two survive scrutiny. First, retirement intent: commit now, or keep the option open without deciding. Second, how much more inference surface gets built against BAML before either the extraction or a swap lands — it could stay near its current single function, or grow as you add personas and actors before returning to this question.

A third candidate dissolves on inspection: how much of BAML's prompt templating and client routing an Effect-Schema adapter would need to replicate. `clients.baml` declares one provider in eleven lines with no retry logic and no routing to reproduce. Whatever adapter replaces it costs little to build regardless of which future arrives, so this drops out as a live axis rather than carrying forward as one.

Held apart, the two remaining axes move independently — you can commit to retiring BAML while the surface keeps growing before you act on that commitment, and you can leave the door open while nothing more gets built for months. Two axes earn the full walk.

## The tiles

Four combinations survive triage, none ruled out as flatly impossible, though one strains under its own weight.

**Clean break.** You commit to retiring BAML, and the surface stays near its current single function. The path runs straight: move `WelcomeResult` into contracts, formalize the port, write `own-inference`'s proposal from a blank page, and add an Effect-Schema `Layer` as a second implementation of `Inference`. The BAML adapter package built by the extraction's later steps goes largely unused.

**Overrun commitment.** You commit to retiring BAML, but momentum on other runtime work — choreography, program validation, more personas — lands new `.baml` functions before `own-inference` gets designed. The commitment holds in name while the surface it was meant to shrink keeps growing underneath it. This tile strains: a real commitment tends to slow new investment in the thing it plans to remove, but nothing in the repo stops parallel work from outrunning a decision that hasn't shipped code yet, so I carry it forward rather than kill it.

**Drifting status quo.** No decision gets made either way, and feature work lands wherever the wiring already runs — BAML. Functions accumulate across more personas and actors. The switching cost for a future swap climbs with every function added, and the extraction, already specified and waiting, sits as the cheapest available lever to contain that drift, whenever it gets picked up.

**Stable status quo.** No decision gets made, and the surface simply doesn't grow much because attention goes elsewhere for a while. Low stakes either way — the extraction still costs little and buys real structure; nothing forces urgency on `own-inference`.

| Tile | Retirement intent | Surface growth | What it costs to wait |
|---|---|---|---|
| Clean break | Commit now | Stays small | Wasted scaffolding for the adapter package, already cheap to abandon |
| Overrun commitment | Commit now | Grows anyway | Coupling deepens while the swap gets designed |
| Drifting status quo | Stays open | Grows | Switching cost climbs per function added |
| Stable status quo | Stays open | Stays small | Nothing forces a decision |

## What follows inside each tile

Trace the consequences forward and one thing repeats across all four: moving `WelcomeResult` into contracts and formalizing the port pay off immediately, on their own, whether or not any swap ever happens. The benefit the proposal names for that move, that the core typechecks without running BAML's codegen, doesn't wait on `own-inference` existing. Only the second half of the extraction (physically relocating `inference.layer.ts`, `baml_src/`, and the generated client into `@indra/runtime-inference-baml`, then wiring the host to it) carries a cost that depends on BAML sticking around a while — cheap to skip only in the tile where you're certain enough to walk away from BAML today.

In "drifting status quo" and "overrun commitment," every month that passes before the extraction lands adds another stretch where new `.baml` functions get authored against a core that still transitively touches the generated client, each one adding to what a future swap has to reproduce. In "clean break," none of that pressure applies, because the swap happens before the surface has room to grow.

## Where to watch

Two signals tell you which world you're actually in, and both stay checkable against the repo without asking anyone.

For retirement intent: watch whether `openspec/changes/own-inference/` gets created and a real proposal gets written before `extract-inference-adapter`'s tasks get checked off. A real proposal appearing early signals "clean break" or "overrun commitment"; its absence, alongside the extraction actually landing, signals either status quo tile.

For surface growth: watch `packages/runtime/core/baml_src/` for a second `function` block or a new `.baml` file. One appearing before the port gets formalized signals "overrun commitment" or "drifting status quo"; the file count holding at one function until the extraction lands signals the calmer tiles.

## The call

Finish `extract-inference-adapter` as it already sits specified, starting now. Move `WelcomeResult` into `@indra/runtime-contracts`, formalize the port as a module the core owns, and only then decide whether the physical relocation of the live BAML layer into its own package still earns its keep.

That move survives every tile above. It thrives in three of the four, anywhere BAML sticks around even briefly, since isolating it costs little and buys real structure regardless of what comes next. It runs weakest only in "clean break," where the later relocation step goes unused — and even there the loss stays bounded, since the package sits as scaffolding today, nothing has migrated into it yet, and abandoning an unused stub costs nothing worth protecting against.

Skipping straight to `own-inference` risks more than it looks: that proposal doesn't exist yet, so you'd be designing a replacement for prompt templating, client handling, and parsing checked against a schema, all from nothing, while the core still imports BAML's generated types the whole time you're doing it. In two of the four tiles, that leaves BAML tangled through the core partway through a migration, with an unfinished second adapter competing for the same one function.

Staying on BAML forever answers a question this decision doesn't actually require you to settle today. The extraction pays for itself independent of whether you ever swap — nothing about "core stops depending on a Rust-backed codegen DSL" needs an Effect-Schema adapter to exist. Treat the retirement question as genuinely open, finish the extraction because it's fully designed and cheap regardless, and write `own-inference`'s proposal once you're actually ready to decide. A plan that doesn't exist yet shouldn't set the pace for a decision that's ready to ship today.
