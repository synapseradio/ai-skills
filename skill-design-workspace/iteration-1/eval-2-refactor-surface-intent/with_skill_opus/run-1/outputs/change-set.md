# Refactor change set — `surface-intent` over-triggers

**Recommendation in one line:** rewrite the skill's `description` so it fires on the one condition that makes the skill valuable — the risk that what you are about to add already exists or conflicts with what is there — and stop advertising the two clauses that make it fire on nearly every write action. Keep the body and both references untouched; nothing that makes the skill good lives in the description.

This document follows skill-design's Refactor mode. The exit artifact of that mode is a typed change set plus the updated files once the user approves. The task forbids touching existing files and the requester is unavailable, so this is the change set alone: the proposed replacement text, the reasoning tied to the principles, the check that would confirm it, and the questions I would otherwise ask before applying.

---

## 1. Restated intent (needs confirmation)

**One sentence:** surface-intent is the discipline for the moment before you introduce something into an existing system — it makes you read what already serves that purpose before you write, so you sharpen or extend what exists instead of adding a duplicate, and then makes your own addition legible enough to act on.

Refactor move 2 requires confirming this restatement with the user before proposing changes, because a refactor against a misread intent optimizes the wrong thing. The user is unavailable, so I proceed on this reading and flag it as **assumed, not confirmed** — see Open Question A. Everything below depends on it.

The restatement is drawn from the skill's own README (`skills/surface-intent/README.md:8`, "The bug it was built to prevent is the everyday one — adding a thing that already existed because nobody looked first") and from Beat 1 of the body. I read that as the load-bearing intent, with Beat 2 (legibility) as a discipline the skill also runs once active, not as a second independent reason to summon it. Open Question A is exactly this split.

---

## 2. Diagnosis — why it over-fires

The description is the sole text present when the runtime decides whether to use the skill (skill-design principle 1, "Schedule the workspace"; principle 3, "Make every delegated decision decidable"). So invocation over-firing is a property of the description alone. Three spans in it each independently widen the trigger to cover almost every write action.

**Span 1 — the unbounded catch-all.** `SKILL.md:11-12`: "or any moment you are adding to a system you have not fully read." Nearly every write is an addition to a system the agent has not fully read. This is the exact clause the task names, and skill-design's own `references/principles.md:73-77` already holds it up as its worked example of a non-decidable description: "A description that fires on 'any moment you are adding to a system you have not fully read,' for instance, triggers on nearly every write action — an over-firing the trigger-rate check would expose." The skill that judges skills already flagged this one.

**Span 2 — the clarity clause.** `SKILL.md:7-8`: "or when what you produce needs to be clear enough for its reader to act on," reinforced by the listed trigger `"make this clearer"` on line 9. Essentially all writing and all code needs to be clear enough to act on. This clause makes the skill a candidate on every prose or code task. It also collides with a neighbor: the skill's own README (`README.md:15-17`) cedes prose polishing to `communicate` — "`communicate` polishes the prose once you are writing it." So this clause both over-fires (principle 3) and duplicates a home that already exists (principle 2, "Route, don't hold"). Two principles point the same way here.

**Span 3 — the artifact enumeration.** `SKILL.md:4`: "a claim, design, abstraction, instruction, name, config, or rule." Taken as a trigger surface, this covers nearly every artifact an agent produces — every function definition is a name, every edit touches an instruction or rule. The list is useful *inside* the skill to show breadth of applicability, but at the front of the description it reads as "fires on all artifact types."

The mechanism is the same in all three: decidability was bought by flattening rather than by clarity (principle 3 — "Buy decidability with clarity, never with flattened decisions"). "Use it whenever you add anything unread" decides every case and fits almost none. The fix is to name the actual decision factor the agent can evaluate at selection time.

**What is *not* wrong.** The body (`SKILL.md:17-93`) and both references contain no over-trigger — the catch-all phrase appears only in the frontmatter description. Beat 2's legibility discipline is sound and is not the problem; the problem is that Beat 2 is *advertised as an independent trigger*. So the smallest change that moves the check is a description rewrite with the body left exactly as is. This matters for "without gutting what makes it good": the two-beat method, the reconnaissance depth in `incoming.md`, and the dedup discipline all stay verbatim.

---

## 3. The typed change set

### Change 1 (primary) — rewrite the `description`

- **Serves:** principle 3 (make the invocation decision decidable) and principle 2 (route pure-prose-clarity to its existing home, `communicate`, instead of duplicating it).
- **What changes:** replace the description frontmatter only. Body and references unchanged. The `metadata: context: fork` block is preserved.
- **Predicted observable effect:** on a labeled prompt set (Section 5), trigger rate on the negative pile — routine edits to already-read code, pure prose-tightening with no new material — falls toward zero, while trigger rate on the positive pile — "am I duplicating this rule", "does a helper for this already exist", "is this already covered" — stays high. In principle-3 terms, the description stops firing on "nearly every write action" while still firing on the dedup/overlap moment that is the skill's job.
- **Check that would confirm it:** the description harness skill-design cites — about 20 labeled prompts, three runs each, trigger rate against a 0.5 threshold (`principles.md:70-72`). No such harness exists for surface-intent today; Section 5 supplies the labeled set to build it. Until it runs, this prediction is checked by inspection only, which is itself a principle-10 finding (Section 6).

The proposed replacement description:

```yaml
---
name: surface-intent
description: >-
  Look before you add. Surface intent applies when you are about to introduce
  something — a rule, claim, abstraction, helper, name, config, or design — into
  an existing body of work, and there is real risk it already exists, overlaps
  with, or talks past what is already there. It has you name what you are adding
  in one line, search and read what already serves that purpose, and decide
  whether to sharpen the existing thing, extend it, or add anew — then make your
  addition legible enough that the next reader can act on it without
  reconstructing your intent. Triggers: "is this already covered", "am I
  duplicating this", "does something already handle this", "before I add this
  rule or helper", "why does this exist". Not for polishing prose that introduces
  nothing new — that is communicate's job — or for edits confined to code you
  have already read.
metadata:
  context: fork
---
```

How each diagnosed span is resolved:

- **Span 1** (the catch-all) is removed and replaced by a condition the agent can actually evaluate at selection time: "real risk it already exists, overlaps with, or talks past what is already there." Most write actions — fixing a bug in a file you just read, renaming a variable — carry no such risk and so no longer match.
- **Span 2** (the clarity clause) is demoted. Legibility survives as the tail of the sentence ("then make your addition legible..."), so Beat 2 is still described, but it is no longer a standalone trigger and "make this clearer" is dropped from the trigger list. The explicit "Not for polishing prose... that is communicate's job" line routes bare-clarity requests to their real home.
- **Span 3** (the enumeration) is kept — breadth of applicability is genuine and worth signaling — but it now sits *inside* the guarded condition ("...and there is real risk it already exists"), so it reads as "any of these artifact types, when the overlap risk is present," not "fires on all artifact types."

Character count of the description string is roughly 830, well under the 1024 spec limit, and it contains no `<` or `>`.

### Change 2 (recommended, not applied) — record the frozen decision in the README

Principle 9 ("Freeze deliberately") asks the skill to state, where a maintainer reads, what it fixes and which fixed decision to revisit when it misfires. The README has a "See also" section but no such record. I recommend adding one line to `README.md` noting that the skill deliberately narrows its trigger to the Beat-1 overlap risk and cedes pure-legibility requests to `communicate`, with the revisit sign being "users report the skill failing to fire on legibility-only work they wanted it for."

This edits a second file and is adjacent to, not part of, the triggering fix, so I am surfacing it rather than folding it in silently (scope belongs to the user). Apply it only if you accept the Open Question A resolution below; it documents that call.

---

## 4. What I deliberately did not change

- **The body of `SKILL.md` (lines 17-93)** — Beat 1, Beat 2, and the four steps under each. No over-trigger lives here, and this is the skill's substance.
- **`references/incoming.md` and `references/outgoing.md`** — the reconnaissance/dedup method and the expression discipline. Untouched.
- **Beat 2 as a discipline.** It is still described and still runs once the skill is active. What changes is only that it no longer, by itself, *summons* the skill. This is the one debatable call in the set; it is Open Question A.

Naming the tradeoff (skill-design's own move, and Core Rule 6): narrowing the trigger to Beat-1 risk means a request that is *purely* "make this clearer," with nothing new being introduced, will now route to `communicate` instead of surface-intent. I judge that correct — it is what the README already says should happen and it is the largest single source of over-firing — but it is a real behavior change at the trigger boundary, so it is the first thing I would confirm with the user.

---

## 5. Trigger test set to make the change observable (principle 10)

No eval or trigger harness exists for surface-intent (`skills/surface-intent/` contains only `SKILL.md`, `README.md`, and the two references; `find` shows evals only under `skills/skill-design/`). That absence is itself a principle-10 finding: the change's predicted effect cannot be measured until a harness exists. Below is a labeled set to build one, in both polarities, so the description can be optimized against data rather than intuition.

**Should trigger (positive):**

1. "I'm about to add a rule that every claim needs a source — is that already covered somewhere?"
2. "Before I write this date-formatting helper, does one already exist in the codebase?"
3. "Am I duplicating an existing validation path by adding this?"
4. "I want to add a config option for retries; is there already one that does this?"
5. "Why does this abstraction exist, and does my new one talk past it?"
6. "Adding a new section to the style guide — is this ground already covered?"

**Should not trigger (negative / near-miss):**

1. "Rename this variable to `retryCount`." (edit confined to code already in hand; no existence risk)
2. "Make this paragraph more concise." (pure prose polish, nothing new introduced — `communicate`'s lane)
3. "Fix the off-by-one in this loop I just read." (change to already-read code; no overlap question)
4. "Tighten the wording of this error message." (legibility only, no addition)
5. "Format this file with the linter." (mechanical, no intent to surface)
6. "Translate this comment to English." (transformation of existing content, no dedup risk)

Run each about three times and score trigger rate against a 0.5 threshold (`principles.md:70-72`). The primary change succeeds if the positive pile stays high and the negative pile — especially near-misses 1 and 2, which the *current* description fires on via Spans 1 and 2 — drops toward zero.

---

## 6. Open questions (recorded in place of asking)

**A. Should Beat-2-only requests still summon the skill?** The proposed description routes a pure "make this clearer," with no new material being introduced, to `communicate` and stops surface-intent from firing on it. This is the one place the refactor narrows behavior rather than just sharpening it. It matches the README's own boundary (`README.md:15-17`), but it is a judgment call about what "without gutting what makes it good" protects — the two-beat *method* (preserved) versus the two-beat *trigger surface* (narrowed). If the user wants legibility-only requests to keep summoning surface-intent, the "Not for polishing prose..." line and the removal of "make this clearer" should be reconsidered. This is the single most important thing to confirm before applying Change 1.

**B. Is Beat 1 the primary intent, or are the two beats co-equal at the trigger?** Section 1's restatement treats Beat 1 (look-before-you-add) as the reason to invoke and Beat 2 as what you also do once active. If the user considers the two beats genuinely co-equal reasons to summon the skill, the description should give legibility more prominence than the tail clause it now gets. My reading leans Beat-1-primary because that is the bug the README says the skill exists to prevent, but I did not confirm it.

**C. Does any consumer rely on the current trigger phrasings?** If another skill, agent, or router config references surface-intent by the phrases being dropped ("make this clearer," "any moment you are adding to a system you have not fully read"), narrowing them could break that dependency. I did not find such a reference in this repo, but I did not search deployment environments outside it. Worth a check before shipping.

**D. Should Change 2 (the README freeze note) be applied?** It serves principle 9 but edits a second file and slightly expands scope. Include it or leave it — the user's call.

---

## Summary of files that would change if approved

- `skills/surface-intent/SKILL.md` — description frontmatter only (Change 1). Body and references unchanged.
- `skills/surface-intent/README.md` — one added line recording the frozen trigger decision (Change 2, optional).
- `packaged/surface-intent.skill` — would need regeneration after the SKILL.md change, per the repo's packaging convention in `CLAUDE.md`.

No files were modified in producing this deliverable.
