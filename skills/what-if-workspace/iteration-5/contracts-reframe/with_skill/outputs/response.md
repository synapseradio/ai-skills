Two axes surfaced, so the full chain, four tiles.

Start with what's already settled. I read `framework-native-contracts`'s proposal and design doc, plus both proposals that claim to rebase onto it — `scope-context-by-actor-subtree` and `validate-program-at-load`. The rebase is already real, not aspirational: both docs' Sequencing sections state the dependency in prose, and `scope-context-by-actor-subtree`'s static no-meld argument (SC3, SC6) leans directly on contracts being typed data that a compiler can check. I also checked `packages/runtime/contracts/src/types.ts` directly — nothing has changed there yet. It still carries the old "parser's eventual output" header, string-named inference, dotted paths, the whole model. So the decision in front of you isn't reverting an already-migrated codebase. It's whether to let two already-written specs keep depending on a foundation that hasn't been built, or hold them back until it has.

I also checked what "costs me JSON-serializable actor definitions" actually costs today. No persistence capability exists anywhere in `openspec/specs`, and nothing in the runtime currently serializes an `ActorDef` — the design doc says so, and a grep of every consumer of the contracts types confirms it: everything lives inside `choreography` and `core`, in-process. The `.in` files elsewhere in the repo belong to a legacy predecessor system, not evidence of a parser this contract needs to serve today. The serializability you'd give up has no live claimant right now. It's a bet against the future, not a dependency you're severing out from under someone.

That leaves two live unknowns. I looked for a third — whether a `.in` parser for INDRA ever gets built — but the design already treats that as fine either way, so it doesn't move the recommendation and drops out.

**Axis 1 — does DL5 hold?** The design doc calls this out itself as "the load-bearing decision to confirm before the rest is written": keeping turn logic as inspectable data via a typed builder, versus letting it become ordinary TypeScript control flow. It's unresolved because nobody has built the typed builder against a real actor yet.

**Axis 2 — does persistence become urgent sooner than "designed deliberately"?** The design doc names this itself as a one-way-door risk, distinct from DL5.

Four tiles:

- **Clean landing** (DL5 holds, persistence stays deferred). The typed builder ships, the skeleton re-authoring goes smoothly, and both dependent proposals' static-checking stories — typed scope closing over no-meld, branch totality as a structural check — land as designed.
- **Pressured but sound** (DL5 holds, persistence gets needed soon). The typed model itself is fine, but the team has to invent the function-reference-in-definition seam under deadline pressure instead of designing it deliberately. The design doc's own split — state persists, definitions get re-supplied from code — covers this if the need is "resume a statically-authored program." It doesn't cover a need to serialize a dynamically-constructed definition; that would be a real fire.
- **Foundation reopens** (DL5 breaks, persistence stays deferred). The typed-builder-as-data approach turns out more awkward in practice than plain control flow. Because both dependent proposals' static-checking claims assume turn logic is walkable data, this doesn't just cost `framework-native-contracts` — it reopens both proposals already written against it. At least there's no deadline pressure, so there's room to redesign.
- **Compound failure** (DL5 breaks, persistence gets needed soon). Both fires at once: the foundation both dependents already rebased onto turns out unsound, exactly when persistence urgency hits and the org needs the serializability this change explicitly surrendered. Worth naming: the plain-JSON-serializability this proposal frames purely as parser-era baggage would have been insurance against exactly this combination.

Recap:

| | Persistence stays deferred | Persistence needed soon |
|---|---|---|
| **DL5 holds** | Clean landing | Pressured but sound |
| **DL5 breaks** | Foundation reopens | Compound failure |

What holds regardless of which tile arrives: DL1 through DL4, the value model itself — typed inference references instead of string names, a returned value instead of a `storeIn` slot, typed scoped state instead of a dotted-path world — none of it depends on DL5 or on persistence timing. Every tile keeps it. The part of this proposal actually carrying risk is narrower than "the reframe": it's specifically DL5 (turn logic as data) and the serializability trade, not the typed-value model around them.

Two watchpoints, matched to what the axes are waiting on:

- **DL5**: the proposal already schedules re-authoring `skeleton.ts` against the typed builder as part of landing this change. That rewrite is the watchpoint. If it reads naturally, DL5 holds; if it needs escape hatches to express what a plain `if`/`return` would express for free, DL5 is breaking. It fires early — before either dependent proposal's spec needs to be finalized, if you sequence it there.
- **Persistence urgency**: watch for the first real product ask that implies resuming a program across a process restart, or persisting a dynamically-authored actor definition rather than a statically-coded one. That request is the trigger, and it arrives before the cost does — which is exactly the lead time needed to design the seam instead of inventing it under pressure.

Neither "commit as currently sequenced" nor "keep the parser-output model" survives every tile. Committing as sequenced dies in "foundation reopens" and worse in "compound failure," because both dependent proposals are already textually built on DL5 holding — if it breaks after their specs are locked, the rework compounds across three documents instead of one. Reverting to the string-addressed model dies in the tile that's most likely to happen: DL5's pattern — a typed builder producing an inspectable data structure — has real precedent (typed query builders, ORMs), so treating it as likely to fail is the pessimistic read, not the base rate.

The move that holds everywhere: land DL1 through DL4, DL6, and DL7 now — the typed value model every tile keeps — but treat DL5 as a named, time-boxed spike, the `skeleton.ts` rewrite you're already planning, that resolves before you finalize the specs of `scope-context-by-actor-subtree` and `validate-program-at-load`, rather than letting their static-checking sections keep citing DL5 as settled. It costs nothing in the clean tile — the spike is work you'd do anyway. It saves the worst tile's compounding cost by catching a DL5 failure before two more documents, and possibly two more implementations, are built on top of it. It's exposed exactly once: if persistence urgency hits regardless of how DL5 resolves, resequencing doesn't touch that risk at all. Whether the state/definitions split actually covers whatever the real persistence ask turns out to be is worth a one-line confirmation in the design doc rather than an assumption riding along silently.
