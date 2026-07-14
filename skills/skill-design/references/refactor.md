# Refactor Mode

In Refactor you align an existing skill with its purpose by verifying
properties against evidence. Ask whether the executor can close each
delegated decision from what the skill provides — never whether the
skill matches a structure you prefer. Read
[principles.md](./principles.md) before working the moves.

## The moves

1. **Read the whole skill** — SKILL.md, every reference, every script.
   Propose nothing before this completes.
2. **Restate the intent** in one sentence and confirm it with the user.
   Get this wrong and every change that follows aims at the wrong
   target.
3. **Question, then collect.** For each principle that bears on the
   misfit — the one the user stated, or the ones you agreed on after a
   full walk — pose it as a question and collect evidence: quotes, file
   and line references, sizes. Verdicts come after evidence. For a
   decision that will not close, ask which of its parts — the skill's
   opening names them — the skill leaves unsupplied, and gather
   evidence on that part.
4. **Ask where evidence runs out.** When the answer sits in no file
   (does this description trigger too often? no trigger data exists),
   ask the user or propose the measurement. Never invent the answer.
5. **Propose a typed change set.** For each change, name the principle
   behind it, predict an observable effect, and name the check that
   would confirm the prediction. Prefer the smallest change the check
   can detect.
6. **Run what runs today.** Where checks exist, run them before and
   after the change; the harness lives with skill-creator. Where none
   exist, say so in the change set — that gap itself counts as a
   finding under principle 10.

Exit artifact: the change set — and the updated skill files once the
user approves the changes.
