# Proposal: tighten `surface-intent` so it fires when it should

## What I read

- `skills/surface-intent/SKILL.md` (frontmatter description + the two beats)
- `skills/surface-intent/README.md`
- `skills/surface-intent/references/incoming.md` and `references/outgoing.md`
- Sibling descriptions for house style: `communicate`, `prompt`, `waypoint`, `visualize`

I changed no files. Everything below is a proposal for you to accept, adjust, or reject.

## The diagnosis

The skill is good. Its two beats are sound and its references are strong. The problem is not the content — it is that the **description matches almost every write action**, so the trigger carries no signal. Three clauses do the damage:

1. `any moment you are adding to a system you have not fully read` — this is the phrase you flagged. It describes nearly every edit anyone ever makes. Taken literally it fires on a one-line bugfix, a typo, a loop body.
2. `what you produce needs to be clear enough for its reader to act on` — every artifact wants to be clear. As a trigger it selects for "all writing."
3. `"make this clearer"` in the trigger list — same over-reach; every editing request wants things clearer.

A description that matches everything is functionally the same as a description that matches nothing: the model cannot use it to *discriminate*, so it either fires constantly (noise, fatigue, the skill gets ignored) or the harness down-weights it. Either way the genuine cases — the ones where surfacing intent actually prevents a duplicate rule or a design that talks past the existing one — get no special pull.

So the fix is a precision fix, not a rewrite. Keep the two beats and both references exactly as they are. Narrow the **description** (the trigger surface) to the situations where the skill earns its interruption, and optionally add one short scoping line to the body so it self-limits even after it loads.

## What the skill is actually for (the discriminator)

Reading the beats and references, the skill delivers value in exactly two situations:

- **Beat 1 value — dedup / anti-drift.** You are about to add a *cross-cutting or shared* artifact (a rule, an abstraction, a design, a named concept, a config key, an instruction/prompt, an interface, a doc section) into a system that may already have one, and you have not surveyed the prior art. The cost it prevents is a duplicate that later drifts, or a design that talks past the one already in place.
- **Beat 2 value — legibility for a second party.** You are producing an artifact whose reader must act on it **without you present** — a rule, a spec, an instruction, an API — where reconstructing your meaning is costly.

The common thread in both: **the thing outlives the moment, it lives in shared space, and prior art plausibly already exists.** That is the condition to gate on.

The mirror image — where the skill should stay silent — is equally clear and is exactly the population the current description wrongly captures:

- local, self-contained edits with no shared surface (a bugfix inside one function, a loop, a rename);
- throwaway or scratch work;
- work in a system you have already read and know well (no prior art to talk past, no second reader to lose).

## Proposed description

Drop-in replacement for the `description:` field (also in `proposed-description.md` as a clean frontmatter block). 841 characters, no `<`/`>`, conforms to the spec allow-list.

> Surface the intent already in a system before you add to it, and make your own
> intent legible in what you produce. Use before you introduce something
> cross-cutting or shared — a rule, abstraction, design, named concept, config,
> instruction, or interface — into a system whose prior art you have not surveyed,
> where a duplicate, a scope overrun, or a design that talks past the one already
> there is a real risk; or when what you produce must be clear enough for a second
> reader to act on it without you present. Triggers: "is this already covered", "am
> I duplicating this", "why does this exist", "before I add this rule", "make this
> clear enough to act on". Skip it for trivial, local, or throwaway edits, and for
> systems you already know well — reach for it when the thing you add outlives the
> moment and prior art plausibly already exists.

### How each change maps to the over-firing cause

| Original clause | Change | Why |
| --- | --- | --- |
| `any moment you are adding to a system you have not fully read` | Replaced with the gated condition: cross-cutting/shared artifact + unsurveyed prior art + real dedup/scope/talk-past risk | This is the catch-all. Gating on artifact *kind* and *risk* is what turns "every edit" into "the edits that duplicate or drift." |
| `clear enough for its reader to act on` | Narrowed to `a second reader to act on it without you present` | Removes "all writing." A second party acting without you is the case where legibility is load-bearing. |
| Trigger `"make this clearer"` | Replaced with `"make this clear enough to act on"` | Keeps the user-phrase hook but drops the every-edit connotation. |
| (none) | Added `Skip it for trivial, local, or throwaway edits…` | Explicit negative scope. `tavily-cli` sets the repo precedent for a "Do NOT trigger" clause; it gives the model a bright line to suppress the false positives. |
| Kept: `"is this already covered"`, `"am I duplicating this"`, `"why does this exist"` | Unchanged | High-precision user phrases. These are the cases where firing is almost always right; keep them. |

What is preserved: the two-intent framing (the thing that makes the skill good), the concrete artifact list, and the strongest explicit triggers. Nothing in the beats or references needs to move.

## Optional second change: a one-line scope gate in the body

The description governs **whether the skill loads**. It does not govern whether the model keeps applying the skill once loaded on a marginal case. If you want belt-and-suspenders precision, add a short gate at the top of `SKILL.md`, right after the title and before Beat 1:

> ## When this fires
>
> Reach for this before a cross-cutting or shared artifact — a rule, abstraction,
> design, named concept, config, instruction, interface, or doc section — where a
> duplicate or a design that talks past the existing one would be costly, or where
> the output's reader must act on it without you. Skip it for local, self-contained,
> or throwaway edits and for systems you have already read: there is no prior art to
> talk past and no second reader to lose.

Honest caveat, by the skill's own Beat 1: this gate says the same thing as the description, so it looks like a duplicate. It is not quite — by truth-conditions the two gate different events (the description is read by the harness to decide *loading*; the body gate is read by the model to decide *continued application after loading*). Still, two copies drift under later edits. If you take this, treat the description as canonical and keep the body gate to this single short paragraph; do not let it grow a second copy of the artifact list that has to be maintained in lockstep. I lean toward shipping the description change alone first and adding the body gate only if firing is still too loose in practice — but that is a scope call that belongs to you.

## What I could not decide without you (open questions)

1. **Is the observed problem noise, or degraded output?** I assumed over-firing = too many low-value invocations (precision). If instead the pain is that when it *does* fire on a trivial edit it drags the work down, the body gate matters more than the description. Which is it?
2. **Is there a triggering eval I should calibrate against?** `skill-creator` supports description evals with labeled fire / no-fire cases. If a benchmark of examples exists for this skill, I would tune the wording to it rather than by hand, and report precision/recall before and after. Does one exist, and should I run it?
3. **Should this fire on ordinary code changes at all, or is it aimed at authoring rules / skills / docs / prompts?** The examples and the sibling positioning (next to `communicate`, `prompt`, `scout`) read as authoring-of-durable-artifacts. If code is out of scope, I can narrow the artifact list further and drop `interface`. How wide do you want the net?
4. **Do you want negative scoping in descriptions as a house pattern?** Only `tavily-cli` currently uses a "skip it for…" clause. I used one because it is the most direct lever against false positives, but if the repo prefers descriptions without negatives, I will fold the exclusion into the positive condition instead.
5. **Keep README prose in sync?** The README restates the skill but is not a trigger surface, so triggering does not require touching it. Say the word if you want its wording aligned with the tightened description.

## Recommendation

Ship the **description change** (Section "Proposed description"). It is the single highest-value edit: it directly removes the three over-firing clauses you flagged while keeping the two beats, the references, and the high-precision user phrases untouched. Hold the body gate as a fast follow only if real usage shows the skill still loading on trivial edits. Then repackage `packaged/surface-intent.skill` and regenerate any `extensions/` bundle, since the frontmatter changed.
