# Incoming intent — reconnaissance before you act

The method behind Beat 1. Survey, then decide, then write. The survey is cheap
relative to the duplicate it prevents.

## Survey: cast a wide net

The thing you are about to add rarely lives where you would file it. Search several
ways, since each angle is blind to what the others find, and read what each surfaces
— a hit you do not open is not reconnaissance.

- **By name** — the words you would call it, then the synonyms you would not.
- **By purpose** — the words the existing thing would use for its job, which may
  share no vocabulary with your name for it.
- **By place** — where something like this would live, and what else lives there.

## Sort what you find: known, assumed, unknown

- **Known** — you read it and can point to file and line. The only pile you may
  build on.
- **Assumed** — you believe it but have not confirmed it. Confirm it, or mark it
  open. An assumption treated as known is how duplicates get in.
- **Unknown** — a question you have not answered. Name it so it does not silently
  shape the decision.

The failure mode is the middle pile masquerading as the first. "I assume nothing
covers this" is not "I read the system and nothing covers this." (Prior art:
`thinkies/assess-current-knowledge` maps the same split in more detail.)

## Diff by truth-conditions, not wording

Compare what each thing *makes true* or *makes happen*, not the words it uses. Two
things can share no vocabulary and mean the same; share most words and mean
different things. Ask of both: under what conditions is each satisfied? What does
each cause or forbid? Matching answers mean the same intent in two outfits — adding
the second is duplication, however different it reads. Differing answers name the
only part worth adding.

## Decide: sharpen, extend, or add

- **Already covered** — sharpen the existing thing if it is weak. A second statement
  of the same intent splits it; the two drift apart under later edits.
- **Partly covered** — extend the smallest unit that closes the gap. Do not rebuild
  the surroundings because you are already there.
- **Not covered** — add it, and because you surveyed, say so with evidence.

State the finding, not just the conclusion: what you searched, what you found, why
it led where it did. "Searched X, Y, Z; found A, covers half, extending A" is
checkable. "I checked, it's not there" asks for your word.

## Worked example

You want to add: *every claim should rest on something the reader can verify.* It
feels missing, so the urge is to write it.

Beat 1 instead. Name it: "claims must rest on checkable evidence." Survey by name
(claim, evidence, verify, source, cite), by purpose (not asserting without backing),
by place (the core rules). The name search is thin — the urge to add grows. But the
purpose search finds an existing rule: *every load-bearing assertion needs a
resolvable source, or an explicit unsourced mark.* None of your words. Diff by
truth-conditions: both are satisfied exactly when a claim has checkable backing.
Same condition, different outfit — **already covered**.

So you do not add. If your framing broadens "checkable" past strictly empirical
claims, that is a one-line sharpening of the existing rule, not a new rule beside
it. The duplicate never enters, and the reader can check why.
