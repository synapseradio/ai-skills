# Refactor proposal: `skills/surface-intent` triggering

Mode: skill-design Refactor. No files under `skills/surface-intent/` were
touched — this is the proposal to review first.

## Files read

- `skills/surface-intent/SKILL.md` (frontmatter + both beats)
- `skills/surface-intent/README.md`
- `skills/surface-intent/references/incoming.md`
- `skills/surface-intent/references/outgoing.md`
- `skills/skill-design/references/principles.md` (principle 3, and its own
  worked example)
- `skills/skill-design/references/audit-rubric.md` (principle 3's check)

## Restated intent (needs your confirmation)

Surface Intent exists for the moment you are choosing what new thing to add
and where — a rule, a name, a config key, a helper, a design — inside a
system that already has structure you have not fully surveyed. Its job is to
make you look before you add (Beat 1) and make what you add legible to a
reader who wasn't in your head (Beat 2). It is not meant to fire on every
edit to unfamiliar code, only on the subset where you are the one deciding
scope or shape rather than executing a spot someone already identified.

If that restatement is wrong, the changes below are wrong too — flag it
before you read further.

## Diagnosis

The description carries five trigger clauses. Two of them are unbounded
enough to fire on nearly any write action, which is the reported symptom:

1. `"...or any moment you are adding to a system you have not fully read."`
   (SKILL.md:10-11) — this is the exact phrase `skill-design`'s own
   `references/principles.md:72-75` names as the paradigm case of
   over-firing under principle 3 ("Make every delegated decision
   decidable"): *"A description that fires on 'any moment you are adding to
   a system you have not fully read,' for instance, triggers on nearly every
   write action."* The skill you're refactoring is cited, unmodified, as the
   textbook failure in the skill that governs how to refactor it.

2. `"...or when what you produce needs to be clear enough for its reader to
   act on"` (SKILL.md:7-8) — narrower than #1 but still nearly universal.
   Almost every output "needs to be clear enough for its reader to act on";
   the clause names no property that distinguishes Beat 2's actual target
   (a durable artifact someone reads without your context) from a quick
   inline answer.

The other three clauses — "might already exist or might talk past what is
there," "duplication or scope creep is a risk," and the quoted trigger
phrases ("is this already covered", "am I duplicating this", etc.) — are
fine. They name a real condition or quote a real utterance; they just get
drowned out by the two catch-alls sitting next to them.

**I only found #1 named in your task. #2 is a second instance of the same
failure shape that I found while reading, not something you flagged.**
Whether to fix it too is your call, not mine — see Question 2 below.

## Proposed changes

All three edits touch only the `description` field in
`skills/surface-intent/SKILL.md:3-12`. Nothing in the body (both beats,
lines 17-93) or either reference file changes — the method being taught
isn't the problem, only the surface that decides when to teach it.

### Change A — delete the catch-all disjunct

**Principle served:** 3, Make every delegated decision decidable.

**Edit:**

```
- "before I add this", "am I
- duplicating this", or any moment you are adding to a system you have not fully
- read. It directs you to read what already serves the purpose before you act, and
+ "before I add this", "am I
+ duplicating this". It directs you to read what already serves the purpose before you act, and
```

**Reason:** everything this clause would catch is already caught by
"might already exist or might talk past what is there" or "duplication or
scope creep is a risk," a few words earlier in the same sentence. It adds
no discriminating condition — it names an epistemic state (haven't fully
read the system) that is true on nearly every turn — so removing it loses
no real coverage, only the unbounded reach.

**Predicted observable effect:** trigger rate falls on prompts like "add a
null check to this function you just opened" or "fix this off-by-one in a
file you haven't seen before" — routine edits to unfamiliar code with no
new named thing being introduced — while staying at 1.0 on the existing
positive set (duplication checks, "is this already covered," introducing a
new rule/helper/config).

### Change B — bound the risk clause, name the near miss

**Principle served:** 3 (clarity, not flattening) and skill-design's Design
mode move 1 ("name two nearby requests that should not trigger").

**Edit:**

```
- Use this when you are about to
- introduce something that might already exist or might talk past what is there,
- when duplication or scope creep is a risk, or when what you produce needs to be
- clear enough for its reader to act on. Triggers: "is this already covered",
+ Use this when you are choosing what to add and where — a new rule, name,
+ abstraction, config key, or design — in a part of the system you have not
+ yet surveyed, so duplication or a design that talks past what exists is a
+ live risk. Skip it when the user already named the exact file or rule to
+ change, or the task is a fully specified fix with nothing left to invent.
+ Triggers: "is this already covered",
```

**Reason:** "duplication or scope creep is a risk" states a consequence,
not a condition — it never says what makes the risk live, so an executor
can rationalize almost any write into satisfying it. Naming the actual
condition (introducing something new, unsurveyed territory) and its
negation (user already pointed at the spot, or the fix is fully specified)
gives the decision a basis on both sides, the exact gap principle 3 checks
for.

**Predicted observable effect:** the routine-edit class from Change A stays
uncaught (reinforcement, not redundant with A). The real gain shows on
middle-ground prompts with no named target — "clean up this module,"
"refactor this helper" — which should now trigger only when the request
actually involves choosing a new name, abstraction, or rule, not merely
because the code is unfamiliar.

### Change C — narrow the reader-clarity clause

**Principle served:** 3, same failure shape as Change A one level down.

Already folded into Change B's edit above (the "Triggers:" sentence keeps
going) — the "clear enough for its reader to act on" language is replaced,
not appended to. If you'd rather keep Beat 2's trigger separate from the
Beat 1 language in B, the standalone version is:

```
- or when what you produce needs to be
- clear enough for its reader to act on.
+ or when what you are producing will outlive this conversation and be read
+ by someone without your context — a rule, a name, a public interface, a
+ doc — and needs to be clear enough to act on without them reconstructing
+ your reasoning.
```

**Reason:** as written, this clause alone can summon the skill for any
output whatsoever, since nearly everything "needs to be clear enough to act
on." Scoping it to artifacts that outlive the turn and get read without the
writer's context matches what Beat 2 (`references/outgoing.md`) actually
teaches — naming, one named root, progressive disclosure for a *reader*,
not for the person who just wrote it.

**Predicted observable effect:** trigger rate drops on prompts asking for a
quick inline answer or scratch output with no lasting artifact ("what does
this regex do," "give me a one-off script to rename these files"), while
staying high on prompts asking to write a rule, name a new abstraction, or
design a public interface.

**This change is conditional on Question 2 — hold it if the answer comes
back "only fix what I named."**

## How to measure this (not yet run)

No `evals/` directory exists under `skills/surface-intent/` today — this is
itself a gap under principle 10 (Make the skill observable), separate from
the triggering bug, worth naming even though it's not what was asked. `git
log --oneline -- skills/surface-intent` shows one commit; the skill has
never had a labeled trigger set.

Principle 3's own check is the standard trigger-rate harness: about 20
labeled prompts, three runs each, trigger rate against a 0.5 threshold,
run on the description alone (`references/principles.md:68-71`). I'm
proposing the labeled set below rather than building and running the
harness myself in this pass, since running it means executing a live
description-triggering harness across repeated runs — a separate,
approval-worthy step, not a file edit.

Proposed labeled set (draft — refine before running):

**Should trigger (10):**

1. "Is this already covered by an existing rule before I add a new one?"
2. "I want to add a helper that formats dates — does something like that exist?"
3. "Before I add this config key, check if we already have an equivalent."
4. "Am I duplicating logic that's already in the codebase somewhere?"
5. "I need to name a new abstraction for this — is there a name for it already?"
6. "Design a new rule for the style guide covering trailing commas."
7. "Why does this pattern exist — should I follow it or does it need fixing?"
8. "Write a public API for the export feature — check nothing like it exists first."
9. "Draft a new section for the README that other contributors will read."
10. "I'm about to introduce a new pattern for error handling — has someone already solved this?"

**Should NOT trigger (10):**

1. "Fix the off-by-one bug on line 42 of parser.py."
2. "Add a null check right here where I pointed." (user named the exact spot)
3. "Run the test suite and tell me what fails."
4. "What does this regex do?"
5. "Rename this variable from `x` to `count` throughout the file." (user dictated the name)
6. "Implement this fully-specified ticket: change the timeout from 30s to 60s."
7. "Give me a one-off script to bulk-rename these five files."
8. "Summarize this PR diff for me."
9. "Add the log line the user just asked for in this exact function."
10. "Debug why this test is flaking." (no new artifact, no new name)

Run this set against the current description (baseline), then against
each of Change A alone, A+B, and A+B+C, to isolate which edit moves the
rate and by how much — stacking all three at once would hide which change
did the work.

## Open questions

1. **Was the removed catch-all deliberate?** "Any moment you are adding to
   a system you have not fully read" might have been meant as a genuine
   wide net for cases the enumerated clauses miss, not just loose phrasing.
   If there's a real case only that phrase caught, name it so it can be
   folded into Change B explicitly instead of dropped.
2. **Is the reader-clarity clause (Change C) in scope?** You named the
   "any moment..." phrase specifically; I found a second over-broad clause
   while reading. Fix both, or hold C and ship only A+B?
3. **Should I build and run the trigger-rate harness now?** I drafted 20
   labeled prompts above but haven't executed them — that requires deciding
   how many runs per prompt and where the harness lives. Say go and I'll
   set it up as a follow-up, or treat the draft set as good enough for a
   human read for now.
4. **Any threshold preference beyond the 0.5 default** `principles.md`
   cites, given that this skill's failure mode (an unread duplicate ending
   up in the system) is more expensive to miss than to over-trigger on?
