---
name: surface-intent
description: 'Surface intent before you add, change, or produce something — a claim, design, abstraction,
  instruction, name, config, or rule. Use this when you are about to introduce something that might
  already exist or might talk past what is there, when duplication or scope creep is a risk, or when
  what you produce needs to be clear enough for its reader to act on. Triggers: "is this already covered",
  "make this clearer", "why does this exist", "before I add this", "am I duplicating this", or any
  moment you are adding to a system you have not fully read. It directs you to read what already serves
  the purpose before you act, and to make your own intent legible in what you produce.'
---

# Surface Intent

There are two kinds of intent in any change. The intent already sitting in what
exists, and the intent you are about to express. Most avoidable mistakes — the
duplicate rule, the helper that already existed, the design that talks past the
one in place — come from skipping the first. You act before you have surfaced
what is already there. So this skill has two beats, and the first one comes first.

## Beat 1 — Before you act, surface what is already there

You are about to add or change something. Before you write it, find out what the
system already does about it. Do not assume; look.

1. **Name it in one line.** Say plainly what you are about to add or change, and
   the purpose it serves. "A rule that claims must be checkable." "A helper that
   formats a date." One sentence. If you cannot say it in one line, you do not yet
   understand it well enough to add it.

2. **Read what already serves that purpose.** Search the system for it — by name,
   by the words it would use, by where it would live. Open what you find and read
   it. This is reconnaissance, not a guess. The thing you are about to write is
   often already written, under a name you did not predict.

3. **Diff against what exists.** Compare what you would add to what is already
   there, on purpose, not on wording:
   - **Already covered** — the existing thing does this job. Sharpen it if it is
     weak. Do not add a second one that says the same thing in other words.
   - **Partly covered** — most of it exists. Extend the smallest piece that is
     missing. Do not rebuild the whole.
   - **Not covered** — nothing serves this purpose. Now you may add it.

4. **State what you found.** Tell the reader what you searched, what you found, and
   why you concluded covered, partly, or not. This lets them check your dedup
   instead of taking your word for it. A silent "I checked" is not checkable.

The deeper method — how to survey, the known / assumed / unknown split, how to
compare two things by their truth-conditions, and a worked example of a duplicate
caught this way — is in `references/incoming.md`.

## Beat 2 — As you produce, surface your own intent

Now you are writing the thing. Make your intent legible in the artifact itself, so
the next reader does not have to reconstruct it.

1. **Name things for what they are.** A name should say what the thing is, so the
   reader needs no comment to learn what it does. If you reach for a comment to
   explain *what* a function or section does, the name is wrong — fix the name.
   Comments are for *why*.

2. **Prefer one named root over indirection.** When several things share a purpose,
   name the purpose once and let each thing be a recognizable instance of it. Do
   not wire them together with pointers and cross-references that hide the shared
   intent behind a trail the reader has to follow. One named root beats many links.

3. **Make it clear enough to act on.** Write so that whoever has to act on this can
   do so on the first read, without reconstructing what you meant. Clarity is the
   goal. Say it plainly at the top, and put the deeper framing — the rationale, the
   edge cases, the vocabulary — in a reference they can open when they need it. The
   top stays terse; the depth waits below. This is how this skill is built: two
   beats here, the method in the references.

4. **Self-check before you ship.** Ask: could a second reader, holding only the
   inputs and my output, follow this and reach the same place? Where the answer is
   no, the intent did not make it onto the page — fix it. Rank what is solid above
   what is shaky; do not flatten the two into one confident voice. If a claim rests
   on your conviction rather than something the reader can check, ground it or cut
   it. (Grounding a claim in evidence is its own discipline — warrant — and lives
   elsewhere; this skill only points at the seam. See `references/outgoing.md`.)

The full expression discipline — naming, intent over indirection, calibrating for
clarity, progressive disclosure, the reflexive self-check, and where the warrant
boundary sits — is in `references/outgoing.md`.

## References

- `references/incoming.md` — the reconnaissance and dedup method for Beat 1.
- `references/outgoing.md` — the expression discipline for Beat 2.
