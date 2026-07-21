# Design Mode

In Design you decide what a skill will do and for whom, before any
SKILL.md exists. The output feeds a build — skill-creator or hand
authoring — and never includes the SKILL.md itself. Read
[principles.md](./principles.md) before working the moves.

## The moves

1. **Surface the intent.** Name the tasks where invoking the skill
   helps, the phrases that should trigger it, and nearby requests that
   should not. Confirm with the user before moving on.
2. **Read what exists.** Search the deployment environment for skills
   that overlap the intent and read any you find. Resolve overlap by
   narrowing the new skill, extending the existing one, or replacing
   it — put that choice to the user rather than deciding it silently.
3. **Research when asked.** When the user wants the ground researched,
   follow [research.md](./research.md). Exit with sourced findings and
   a named list of what stayed unverified, all bound for the brief.
4. **Choose the floor.** Name the weakest executor the skill must work
   on and what that executor can act on. This choice shapes every
   sentence the builder writes.
5. **Decide what stays fixed.** List the decisions you will hard-code
   into the skill for every future session — scope, process shape,
   naming — and the decisions left open. Mark the fixed decision most
   likely to need revisiting, and the sign that would show it.
6. **Write the design brief.** The exit artifact, specified below.

## The design brief

The brief contains, by name:

- **Intent** — the tasks served, trigger phrasings, and the near misses
  that must not trigger.
- **Floor** — the weakest declared executor, with the reasoning behind
  the choice.
- **Sources of truth** — each body of knowledge behind the skill, and
  the single home chosen for each fact.
- **Structure sketch** — what goes in the description, the body,
  references, and scripts, with principle 1 as the reason.
- **Fixed decisions** — what you fixed, what stays open, and the
  revisit sign from move 5.
- **Checks** — what deserves measuring and why, and any operation that
  needs a script instead of prose. Mechanics — trigger queries, eval
  schemas, harnesses — belong with skill-creator.
- **Open questions** — everything left unverified, so the builder
  schedules the gaps instead of inheriting them.

Hand the brief onward: whoever runs skill-creator next can answer its
intake questions from the brief alone.
