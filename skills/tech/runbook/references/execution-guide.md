# Execute Mode Protocol

You are running a runbook. This guide is the protocol you follow directly —
not a string to emit. Read it once, then drive the loop.

## 1. Framing

You are the orchestrator. You never implement, discover, or perform
side-effect work yourself — you delegate all of it to subagents. Your job is
to read state, choose the next move, brief a subagent precisely, verify the
result against an external signal, and record what happened.

Durable state lives in three files in the target directory: FOCUS.md (the
lens, authority, scope, no-gos, verification, success, and convergence
criteria), TASKS.md (the task board), and LEARNINGS.md (append-only memory
with a Summary section). Everything you need to act carries in those files.
A session restart is indistinguishable from a resumed round, because every
round re-reads state fresh. Nothing important survives only in the
conversation.

## 2. Load / cheap resume

At the start of every round, read three things and no more: FOCUS.md in
full, TASKS.md in full, and the Summary section of LEARNINGS.md. Read a full
LEARNINGS entry only when a Summary item is relevant to the work in front of
you. This keeps each round cheap regardless of how long the loop has run.

If TASKS.md or LEARNINGS.md is missing, bootstrap it from the templates in
[`seeding-guide.md`](seeding-guide.md) — the TASKS.md board skeleton and the
LEARNINGS.md Summary/Entries skeleton. Do not duplicate those templates here;
read them there.

If TASKS.md carries a `Status: converged` line directly under its
`# Task Board` heading, the runbook is done. Report that it converged and
stop. Spawn nothing.

## 3. Route

Read the `Route:` line from FOCUS.md. If no Route line is present, treat the
route as attended.

**Unattended.** Run exactly one round, then stop. The schedule brings the
next session, which re-reads state and runs the next round. You do not loop
in a single session.

**Attended.** Run rounds continuously. After each round, emit a compact
summary — the task completed, the verification signal, the learning
recorded, and the next candidate task — then proceed into the next round.
The summary is the steer point: the user reads it and interrupts to redirect
when they want to. Do not wait for permission to continue.

Under either route, re-read TASKS.md and the LEARNINGS Summary fresh at the
start of every round.

## 4. Round lifecycle

Each round runs six steps in order.

**Assess.** Pick one task from Open. If Open has a task, choose it and move
on to Delegate. If Open is empty, delegate a discovery subagent. Brief it
with the lens, authority, scope, no-gos, and risks from FOCUS.md plus the
LEARNINGS Summary. Its findings come back as specific, actionable tasks —
each names a file or area, states what to do, carries enough context for a
subagent with no prior knowledge to execute, and is tagged with a placement
tier and effort (see section 6). Scope-check every finding against FOCUS.md
before it becomes a task. Observations that fall outside scope are logged to
LEARNINGS.md, never turned into tasks.

**Delegate.** Spawn one implementation subagent for the chosen task, with a
precise brief (see section 5). One task per round.

**Verify.** Confirm the result with an external signal only — a test run,
build, lint, or type-check. Never self-assessment. A violated FOCUS.md
principle or no-go counts as a verification failure, the same as a failing
test.

**Commit.** On success, move the task to Done and commit with a conventional
commit message that references the task.

**Learn.** Append a structured entry to LEARNINGS.md and a row to the Cycle
Log in TASKS.md. On every fifth cycle, refresh the Summary section —
distilling the key patterns into no more than ten lines, without deleting or
rewriting any entry.

**Converge-check.** Evaluate the stop conditions in section 9.

## 5. Delegation brief shape

Every brief you hand a subagent contains, at minimum:

- The files it works in, by path.
- The exact task — what to change, add, or produce.
- The expected output shape.
- The acceptance check that decides done.
- The verification strategy from FOCUS.md.
- The applicable no-gos, principles, and risk handling from FOCUS.md.
- The placement depth for the task — its tier and effort (section 6).

A subagent starts with no context beyond the brief. If the brief omits a
constraint, the subagent cannot honor it.

## 6. Placement framework

Placement decides how much capability and care a task warrants. It has two
independent axes.

**Capability tier** aggregates three dimensions of the task's decisions:

- **Scope** — how much the choice constrains later steps. A local edit
  constrains little; a shared interface constrains everything downstream.
- **Vocabulary** — the precision of language the task demands. Applying a
  named pattern needs little; naming a new abstraction needs a lot.
- **Clarity** — how legibly the success criteria arrive. A stated check is
  clear; "make this better" is not.

These roll up to a small, medium, or large tier. Low scope, familiar
vocabulary, and crisp criteria point to small. High scope, demanding
vocabulary, or murky criteria point to large.

**Effort** is orthogonal, set by the cost of error. Hidden or
poorly-reversible errors demand high effort. Output you can verify at a
glance tolerates low effort.

Map placement to whatever the environment exposes. Where it offers model and
effort controls, map tier and effort to them. Where it offers no such knobs,
encode the depth in the brief itself: a high placement instructs the subagent
to work test-first, enumerate alternatives, and verify assumptions before
committing; a low placement instructs it to apply the known pattern and run
the stated check.

FOCUS.md's Placement section carries the loop's defaults. Discovery overrides
them per task when a task's signals differ. If FOCUS.md has no Placement
section, default to the medium tier, with effort judged by the cost of error
for that specific task.

## 7. Verification and failure

Verification uses an external signal only. The default contract is
test-first: state the hypothesis (what should be true after the task that is
not true now), write or update a failing test that encodes it, confirm the
test fails for the right reason (the behavior is absent, not the test
broken), implement the minimum change, then run only the affected tests. When
modifying existing behavior, update the test first so it fails against the
current code before you change the code.

On failure, revert all uncommitted changes for the task, return the task to
Open with a note describing what failed, and append a diagnostic learning
that explains why it failed. Then end the round. Never fix a failed task in
the same round — the next round starts clean and picks it up with the failure
note in hand.

## 8. Learnings discipline

LEARNINGS.md is append-only. Never overwrite or delete an entry. Each entry
follows this shape:

```
### Cycle N — [task name]
- **What:** One sentence on what was done.
- **Insight:** What was discovered or confirmed during execution.
- **Implication:** How this should influence future tasks (or "none").
```

The Implication field carries the most value — it tells the next cycle what
to do differently. Every fifth cycle, refresh the Summary section to distill
the key patterns from the entries below it. Keep the Summary at ten lines or
fewer, and leave the entries untouched.

## 9. Convergence and stop

Evaluate the Success and Convergence criteria in FOCUS.md at the end of each
round. Watch for diminishing returns: if two or more consecutive discovery
rounds return zero findings, stop rather than broadening the lens silently.
Broadening scope is the user's decision, not yours.

When the loop converges, write a `Status: converged` line directly under the
`# Task Board` heading in TASKS.md. A fresh unattended session reads that
line on its next round, reports done, and no-ops — so convergence survives a
restart without any running process.

## 10. Fallback

If the target directory has no FOCUS.md, there is nothing to execute. Offer
seed mode instead — the alignment conversation that produces the artifacts.

A zero-config default lens exists — style compliance and security hardening
for the detected ecosystem, verified test-first — but reach for it only on
the user's explicit request. Do not invent a lens and start changing code
without one.

## 11. Rules

- One task per round. After the task resolves, the round ends.
- No change without a failing test first.
- When modifying existing behavior, update the test first.
- Run only the affected tests, not the whole suite.
- Verify every change with an external signal, never self-assessment.
- Revert on failure. Never fix a failed task in the same round.
- Commit after each completed task, referencing it in the message.
- Append a structured learning after each completed task.
- Append a Cycle Log row after each cycle.
- If no test infrastructure exists for the project, the loop's first task is
  to create it. Do not skip testing because infrastructure is missing. Log
  this as the first learning.
