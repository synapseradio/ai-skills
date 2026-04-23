# Workflow: Seed → Structured Prompt (Mode A)

Input: prose describing a task, project, or rough intent. Output: a
6-section structured prompt the user can paste into an agent conversation,
an API call, or use directly.

Load this file only when the mode detection in SKILL.md Stage 1 resolves
to **seed**.

---

## Stage 1 — Inventory (seed mode)

From the seed text and surrounding conversation, identify:

| Item | Signal |
|---|---|
| **Core task** | The verb + object the user wants done (refactor X, review Y, build Z) |
| **Domain** | What specialist lens applies (frontend? security? data? ops?) |
| **Known constraints** | Stack, dependencies, deadlines, style preferences |
| **Available context files** | Files, docs, URLs the user already references |
| **Pre-work checks** | Domain-specific things to verify, load, or confirm *before* producing output — these land in "Context To Gather" |
| **Stakes** | Why the user cares — what's at risk, what's the payoff. This becomes the closing paragraph of the Task section, not a separate heading. |
| **Ambiguities worth asking** | Decisions that would fork the execution path |

Resolve ambiguities in one of three ways:

- If the disambiguation meaningfully changes the output, use `AskUserQuestion`
- If a reasonable default exists, note the assumption in the output
- If the ambiguity doesn't matter for the current task, ignore it

Don't ask about minor style preferences. Ask only when a wrong default
would cost the user a retry.

## Stage 2 — Shape

Assign inventoried content to buckets:

| Bucket | What goes here |
|---|---|
| **Frame** | Specialist identity + stance (not "You are an expert in X" but "We're working on X together — bring the perspective of someone who's debugged this class of problem before") |
| **Task** | The bounded, completable mission, closing with a one- to two-sentence stakes paragraph — what matters about this, what the cost of getting it wrong is. Stakes ride here; there is no separate Why heading. |
| **Context** | Files and background the agent already has. Include file paths only if they exist — never fabricate. If no files apply, say so. |
| **Tooling** | Relevant tools, MCPs, skills. Omit irrelevant ones to save context. |
| **Context To Gather** | Pre-work: domain-specific things the agent should verify, load, or check *before* producing output. 2-4 items. Imperative form or self-directed question form: *"Check X before Y"*, *"Ask yourself: what would break if Z?"* |
| **Constraints & Invitations** | Mechanically-checkable musts (schema, tests pass) stay as musts. Judgment criteria become invitations (*"Take the time you need — flagged partial progress beats polished summary that skips steps"*). |

## Stage 3 — Temper

Run the anti-pattern lint from `eip-anti-patterns.md` over every phrase
in every bucket. Common hits in seed mode:

- **#6 Authoritarian tone** in the Frame bucket — "You are X" → reshape
- **#2 Demanding certainty** in Constraints — "definitive answer" → separate
  recommendation from caveats
- **#5 All-at-once** in the Task bucket — multi-component tasks → propose
  stages
- **#9 Perfect-prompt** — too many conditionals → trim to essentials

## Stage 4 — Emit

Output format (copy-pasteable structured prompt). The fenced block below
shows the *template* — emit the contents, not the backticks:

```
## Frame

[Specialist identity framed as shared-context, 1-2 sentences]

## Task

[Bounded, completable mission]

[Closing paragraph: the stakes. Why this matters. What's the cost of
getting it wrong. 1-2 sentences, honest. This sits at the bottom of Task —
no separate Why section.]

## Context

[Files, background, prior knowledge the agent already has]
- path/to/file.ext — why it's relevant
- [or: "No files attached — work from conversation signal"]

## Tooling

[Relevant tools/skills, 2-5 items]
- Tool/skill name — when to use it

## Context To Gather

[Pre-work checks — 2-4 items, imperative or self-directed-question form]
- Check X before Y
- Ask yourself: what would break if Z?

## Constraints & Invitations

**Must:**
- [mechanically verifiable]

**Invited:**
- [honesty defaults, transparency asks, permission-to-fail statements]
```

If the user has indicated they'll evaluate via a subagent, this exact
structure is eval-friendly — each section is a clear boundary.

## Example

**Seed:** *"Review the auth middleware for security issues."*

**Output** (emitted as plain markdown, not inside a code block — the
fenced block below is for the template only):

```
## Frame

We're doing a security-oriented read of the auth middleware — bring the
lens of someone who's seen common auth failure modes in production.

## Task

Review `src/middleware/auth.ts` for security issues and produce a
prioritized findings report.

Authentication is the gate to every downstream permission check. A
weakness here compromises the whole system, and the cost of a missed
finding is much higher than the cost of surfacing something that turns
out to be fine.

## Context

- `src/middleware/auth.ts` — the code under review
- `tests/middleware/auth.test.ts` — existing coverage
- `docs/security.md` — project security guidelines (if it exists)

If `docs/security.md` doesn't exist, infer the project's security
posture from the existing middleware and tests.

## Tooling

- Read, Grep — code inspection
- `software:debug` — when a finding needs hypothesis-driven investigation

## Context To Gather

- Check constant-time comparison before accepting any equality check on
  tokens or secrets
- Ask yourself: what does an attacker see in the error response?
- Verify token lifetime and rotation semantics
- Look for implicit trust across module boundaries

## Constraints & Invitations

**Must:**
- Each finding names file, line, and suggested remediation
- Findings prioritized HIGH / MEDIUM / LOW

**Invited:**
- Flag where you're inferring intent from code vs. seeing it documented
- Note blind spots — anything you didn't examine and why
- If a finding is borderline, explain the uncertainty rather than picking
  a side
```

This emits directly as text (not inside a code block in the final output)
so the user can copy it.

## Edge Cases

| Situation | Response |
|---|---|
| Task already well-structured | Emit minimal changes, note no assembly needed |
| Task too vague to structure | Use `AskUserQuestion` for 1-2 targeted questions |
| Context files referenced but not accessible | Note in output: *"[file] referenced but not readable here — include its contents or path in conversation"* |
| Multiple plausible specialists | Pick one, note the assumption, offer the alternative as a one-line addendum |
