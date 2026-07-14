---
name: skill-design
description: >-
  Design, strengthen, or audit an Agent Skill. Use before building any new
  skill — this skill produces a researched design brief that skill-creator
  can build from — and whenever an existing skill needs judgment or change:
  it over-triggers, under-triggers, bloats its context, drifts from its
  sources, or needs a quality check. Triggers: "design a skill", "plan a
  skill before building it", "audit this skill", "review my SKILL.md",
  "strengthen this skill", "refactor this skill", "is this skill well
  built", or any request to evaluate or improve how a skill routes,
  decides, or spends context. Packaging and eval mechanics stay with
  skill-creator; this skill decides what to build and verifies fit.
compatibility: >-
  Runs in the main conversation; design and refactor modes converse with
  the user. Floor executor: an agent that can read a skill's files, quote
  evidence from them by file and line, and walk numbered moves in order.
  Audit mode assumes file search over the target skill's directory.
---

# Skill Design

Use this skill to design a new Agent Skill, to improve an existing one, or
to judge one against ten principles. Work the same way in every mode: pose a
principle as a question about the skill at hand — the one in front of you,
or the one taking shape — gather evidence from its files or from research,
then run the check the principle names.

One question cuts across all ten principles: can every decision the skill
hands the agent running it be made from what the skill provides? Where you
find a decision that cannot, you have found work. The principles themselves
rest on six facts, each carrying its evidence; `references/evidence.md`
holds that derivation.

## Route first

Decide the mode from the state of the world, never from your own capability:

- No SKILL.md exists yet — an idea, a captured workflow, a conversation to
  distill → **Design**.
- A SKILL.md exists and the user wants change — a stated misfit, a
  strengthening request → **Refactor**.
- A SKILL.md exists and the user wants judgment without change → **Audit**.

When a request straddles two modes ("audit this and fix what you find"), run
Audit first and carry its report into Refactor as evidence. When you cannot
tell which mode fits, ask the user one question rather than guessing. When a
request fits no mode at all, say so — name what the request needs that no
mode covers, and ask the user whether to stretch a mode or work outside this
skill. Never force a fit.

Every mode ends at a named artifact. The mode closes when the artifact exists
and satisfies its specification, never when the work feels done. Each mode
names that specification where the artifact is defined: the brief's field
list, the change set's requirements in refactor move 5, the audit rubric's
report format.

## The ten principles

Each line below compresses one principle. `references/principles.md` holds
the full statements with their checks and evidence; read it before design or
refactor work. For audit, `references/audit-rubric.md` operationalizes the
same ten.

1. **Schedule the workspace** — description at startup, body on activation,
   references on demand; read cost scales with the task, never with the corpus.
2. **Route, don't hold** — one home per fact; every other occurrence points
   there; on disagreement the source wins.
3. **Make every delegated decision decidable** — from what the skill provides;
   buy decidability with clarity, never by flattening rules.
4. **Declare the floor, and write to it** — correctness gets judged at the
   weakest declared executor; ground abstract terms in referents that
   executor can act on.
5. **State the generator, and bound the enumeration** — state the fact the
   rules follow from, then still enumerate the cases that carry the weight.
6. **Type every rule by its check** — invariants by inspection, obligations
   at task boundaries, preferences as distributions over runs.
7. **Expect probability, and buy certainty with artifacts** — prose shifts a
   distribution; where an operation must not vary, ship a script.
8. **Verify each claim in the mode its kind admits** — encoded error
   compounds at the rate of reuse; name what no check covers.
9. **Freeze deliberately** — write down, somewhere a maintainer reads, what
   the skill hard-codes, what it leaves open, and what sign says to revisit.
10. **Make the skill observable** — evals before the skill; pair every
    expected effect with the check that would confirm or refute it.

## Design mode

Design decides what a skill will do and for whom, before any SKILL.md
exists. Its output feeds a build process — skill-creator or hand-authoring —
and never includes the SKILL.md itself.

1. **Surface the intent.** Name the task region where invoking the skill
   helps, the phrases that should summon it, and two nearby requests that
   should not. Confirm with the user before moving on.
2. **Read what exists.** Search the deployment environment for skills that
   overlap the intent and read any you find. Overlap resolves by narrowing
   the new skill, extending the existing one, or replacing it — surface that
   choice to the user rather than deciding it silently.
3. **Research the ground.** Follow `references/research.md`. Exit with
   findings that each carry a source, plus a list of what stayed unverified.
4. **Choose the floor.** Name the weakest executor the skill must serve and
   what that executor can act on. This choice shapes every sentence the
   build will write.
5. **Decide what stays fixed.** List the decisions the skill will hard-code
   for every future session — scope, process shape, naming — and the
   decisions it leaves open to each session. Mark the fixed decision most
   likely to need revisiting, and what sign would show it.
6. **Write the design brief.** The exit artifact, specified below.

### The design brief

The brief contains, by name:

- **Intent** — the task region, trigger phrasings, and the near misses that
  must not trigger.
- **Floor** — the weakest declared executor, with the reasoning or evidence
  behind the choice.
- **Sources of truth** — each body of knowledge the skill routes over, and
  the single home chosen for each fact.
- **Structure sketch** — what goes in the description, the body, references,
  and scripts, justified by principle 1.
- **Fixed decisions** — what the skill hard-codes, what it leaves open, and
  the revisit sign from move 5.
- **Checks** — the evals to build first, candidate trigger queries in both
  polarities, and any operation that needs a script instead of prose.
- **Open questions** — everything research left unverified, so the build
  schedules the gaps instead of inheriting them.

Hand the brief to the build. When skill-creator runs next, the brief answers
its intake questions.

## Refactor mode

Refactor aligns an existing skill with its purpose by verifying properties
against evidence. Ask whether each decision the skill delegates can be made
from what it provides — never whether the skill matches a structure you
prefer.

1. **Read the whole skill** — SKILL.md, every reference, every script.
   Propose nothing before this completes.
2. **Restate the intent** in one sentence and confirm it with the user. A
   refactor against a misread intent optimizes the wrong thing.
3. **Question, then collect.** For each principle that bears on the stated
   misfit, pose it as a question — "which decisions does this skill delegate,
   and what does it provide to decide them?" — and collect evidence: quotes,
   file-and-line references, token counts. Verdicts come after evidence.
4. **Ask where evidence runs out.** When the artifact cannot answer a
   question (does this description over-trigger? no trigger data exists),
   ask the user or propose the measurement. Never invent the answer.
5. **Propose a typed change set.** Each change names the principle it serves,
   predicts an observable effect, and names the check that would confirm the
   prediction. Prefer the smallest change that moves the check.
6. **Run what runs today.** Where evals or a trigger harness exist, run them
   before and after the change. Where none exist, say so in the change set —
   that gap itself counts as a finding under principle 10.

Exit artifact: the change set — and the updated skill files once the user
approves the changes.

## Audit mode

Audit renders per-principle verdicts from evidence and changes nothing.

1. Read the whole skill, references and scripts included.
2. Walk `references/audit-rubric.md`: one entry per principle, each naming
   the question to ask, the evidence to collect, and how to decide.
3. Give each principle one verdict — **pass**, **fail**, or **not checkable
   today** — with evidence cited by file and line. A not-checkable verdict
   names the missing check and routes it to review; it never silently drops.
4. Close with the two failures that cost the most, so a follow-up refactor
   knows where to start.

Exit artifact: the audit report. If the user then asks for fixes, enter
Refactor mode carrying the report as its evidence base.

## The moves set a floor

Walk each mode's numbered moves in order when unsure how to proceed. An
executor that never departs from them still reaches the mode's exit
artifact. When you can see a better move than the listed one — one that
serves the mode's opening sentence more directly for this task — take it,
and tell the user what you changed and why.

## Scaling evidence

Match how much evidence you gather to what the task shows, never to your own
sense of capability: how many sessions will reuse the skill, what a wrong
decision would cost to undo, and who reads the output. A skill for one
person's weekend project needs less evidence per claim than a skill shipping
to a team's marketplace. The moves stay the same in both cases; gather more
evidence per move as stakes rise.

## References

- `references/principles.md` — the ten principles in full: statement, check,
  evidence. Read before design or refactor work.
- `references/evidence.md` — definitions, the measured findings, and the
  checks table. Read when a verdict needs its source.
- `references/audit-rubric.md` — the audit walk, one entry per principle.
  Read at the start of every audit.
- `references/research.md` — design mode's context gathering. Read at design
  move 3.
