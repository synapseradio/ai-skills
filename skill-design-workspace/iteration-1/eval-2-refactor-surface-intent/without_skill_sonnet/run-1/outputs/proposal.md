# Proposal: narrowing surface-intent's trigger

No files in the repository have been modified. This is a proposal only — the
exact replacement text is below, ready to paste into
`skills/surface-intent/SKILL.md` once approved.

## What's wrong with the current trigger

The frontmatter description ends with: "or any moment you are adding to a
system you have not fully read." Read literally, that's true of almost every
write action an agent takes — editing a function in a codebase you haven't
audited end to end, adding a line to a config file, fixing a typo in a doc you
only skimmed. The clause was meant to catch one specific risk (you're about to
introduce something that duplicates or talks past what already exists) but its
wording generalizes to nearly all editing, so the skill is positioned to fire
constantly.

The rest of the description has the same problem in miniature: "a claim,
design, abstraction, instruction, name, config, or rule" is a reasonable list
of *what* the skill protects, but nothing in the description says what's
*excluded* — a one-line bug fix with a known root cause technically produces
an "instruction" (the fixed code) too.

## The joint that actually separates should-fire from shouldn't

Reading the skill body (both beats), the two beats share one implicit target:
**a durable, reusable, or reader-facing artifact** — something other code,
people, or future edits will rely on without re-deriving your reasoning. Beat
1 asks whether that thing already exists before you add it; Beat 2 asks
whether your version of it will be legible to someone who only sees the
output. Neither beat has anything useful to say about a mechanical edit to
something that already exists and isn't being renamed, redesigned, or
recreated — there's no "is this already covered" question to ask about
fixing an off-by-one error.

So the two-part joint that should gate triggering is:

1. **Is a new named/reusable/durable thing being introduced** (a rule,
   abstraction, helper meant to be called from more than one place, config
   surface, schema, naming convention, cross-cutting design decision) — as
   opposed to a mechanical change to something that already exists?
2. **Is the system big or unfamiliar enough that duplication is plausible** —
   as opposed to a file or module you've already read in full within the
   current context?

Both axes need to be true for Beat 1 to earn its keep. Beat 2 (legibility)
can fire on its own even without a "new" thing, but only for the same class of
artifact — a rule, a design doc, an instruction meant for someone else to
act on — not for prose polish (already `communicate`'s job, per this skill's
own README) or private scratch code.

I deliberately did **not** use "the user already told me exactly what to add"
as an exclusion. A duplicate can exist even when the user's request is fully
specified — they may not have checked either. The exclusion that actually
holds up is "mechanical" (rename, reformat, a fix whose root cause is known),
not "specified."

## Proposed frontmatter description (replaces lines 3–12 of SKILL.md)

```yaml
description: >-
  Surface intent before you add, change, or name something durable that
  other code, people, or future edits will rely on — a rule, abstraction,
  reusable helper, config key, schema field, naming convention, or
  cross-cutting design decision. Two triggers, either is enough: (1) you are
  deciding whether such a thing should exist, in a system big enough its
  purpose might already be served elsewhere and you have not checked; (2)
  you are producing one and need its intent legible to a reader who sees
  only the artifact, not your reasoning. Fires on: "is this already
  covered", "why does this exist", "am I duplicating this", or any point
  where you are about to introduce a new named concept into a system you
  have not fully read. Does not fire for mechanical edits (rename,
  formatting, typo fixes), a bug fix with a known root cause, prose polish
  (see communicate), or a fully private, throwaway change nothing else will
  reference.
```

926 characters — within the 1024-char spec limit with room to spare. Keeps
the phrase "a system you have not fully read" (the part of the original that
was doing real work) but now qualifies it with "big enough" and "new named
concept," and adds an explicit skip list, mirroring the TRIGGER/SKIP pattern
already used elsewhere in this repo's skill set (e.g. `claude-api`).

## Proposed body addition: a scope-check gate

Frontmatter controls whether the skill gets *offered* for a task. But nothing
stops a borderline call from loading the skill anyway, so I'd add a fast
self-exit right after the intro paragraph and before "## Beat 1," so the skill
recognizes non-fit immediately rather than running both beats on something
they don't apply to:

```markdown
## Scope check — does this apply?

Before running the beats, check what you're about to touch. This skill is
for durable, reusable, or reader-facing artifacts: a rule, an abstraction, a
helper meant to be called from more than one place, a config surface, a
schema, a naming convention, a cross-cutting design decision. It is not for:

- a mechanical edit (rename, formatting, a typo fix) to something that
  already exists,
- a bug fix once the root cause is known and the fix is the obvious next
  line,
- prose polish where the content and intent are already settled — that's
  `communicate`'s job,
- a fully private, throwaway change that nothing else in the system will
  reference.

If none of the beats' concerns — duplication, scope creep, or an unclear
reader-facing result — are plausible here, skip the beats and do the work.
```

This goes between the intro paragraph (ending "...the first one comes
first.") and the `## Beat 1` heading. Everything else in the body — both
beats, both references — is untouched. Nothing about the dedup method, the
truth-conditions diff, the naming discipline, or the warrant-boundary
handoff changes.

## What I did not change, and why

- **Beat 1 and Beat 2 content** — the mechanism the user called "what makes
  it good." The fix is entirely in when the skill fires, not what it does
  once fired.
- **`references/incoming.md` and `references/outgoing.md`** — no changes;
  they're the deep method, orthogonal to the triggering problem.
- **README.md's opening sentence** ("A skill for the moment before you add,
  change, or produce something") — this still describes the *narrowed*
  scope reasonably (it already says "add, change, or produce," not "edit
  anything"), and README isn't consulted for triggering. Flagged below as a
  question rather than changed, since editing it wasn't asked for and it's
  a judgment call whether the human-facing framing should mirror the new
  gate exactly.

## Questions for the user

1. **README consistency** — should `README.md`'s intro paragraph and its
   "the bug it was built to prevent" line be tightened to match the
   narrowed scope (durable/reusable artifacts, not "anything you add"), or
   is README's looser framing fine since it's read by a human deciding
   whether to install the skill, not used for runtime triggering?
2. **Where's the line for "durable"?** — I've treated a new API endpoint or
   a new React component as durable/reusable enough to warrant Beat 1 (it's
   a named surface others may build on), but a one-off script or a single
   call site isn't. Does that match the intent, or is the bar meant to be
   narrower (only things explicitly meant for reuse, e.g. an exported
   helper) or broader (any new file at all)?
3. **`metadata.context: fork`** — the skill already runs in a forked
   context, which caps the cost of over-triggering (an unnecessary fork
   doesn't pollute the main conversation). Does that change how aggressively
   the description should be narrowed, or is the concern purely about wasted
   fork cycles and wrong signal-to-noise regardless of isolation?
4. **Any concrete false positives/negatives you've already observed?** — I
   reasoned from the skill's own text and the stated over-triggering
   symptom, but if there are specific tasks where it fired and shouldn't
   have (or vice versa), those would sharpen or correct the scope-check
   wording above.
5. **Packaging** — per this repo's `CLAUDE.md`, changing `SKILL.md` requires
   regenerating `packaged/surface-intent.skill` via the skill-creator
   packager in the same change. Should that regeneration happen as part of
   applying this proposal, or is that a separate follow-up step?
