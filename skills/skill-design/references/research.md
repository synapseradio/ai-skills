# Research for Design

Design move 3 runs through this file. Exit with findings that each carry a
source a reader could reach, plus a named list of what stayed unverified.
Nothing silently drops.

## What to read, in order

1. The deployment environment's existing skills, where design move 2 has
   not already covered them — carry move 2's overlap findings forward
   rather than re-reading. Names and descriptions first, since that surface
   decides selection; then the bodies of any skill whose intent overlaps
   the one under design.
2. The Agent Skills specification and its companion guides — the
   [specification](https://agentskills.io/specification),
   [evaluating skills](https://agentskills.io/skill-creation/evaluating-skills),
   [optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions),
   and [best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
   — whenever the design touches loading stages, frontmatter, triggering, or
   evals.
3. The domain's source of truth: the docs, codebase, API, or corpus the
   skill will route over. Locate where each fact the skill needs already
   lives; those homes drive the brief's sources-of-truth section, because a
   fact with a live home gets a pointer, never a copy.
4. Prior art beyond the environment, when the domain has established
   practice worth citing — a style guide, a benchmark, an official tool.

## How to verify

Check claims against artifacts rather than against other documents: run the
command, call the API, read the schema, count the tokens. A claim inherited
from an existing document gets the same check, because encoding launders it —
once the skill states it, readers stop asking where it came from. Where the
artifact sits out of reach, keep the claim and mark it unverified; it lands
in the brief's open questions.

## How deep

Scale by the stakes the task shows: how many sessions will reuse the skill,
what a wrong freeze would cost to reverse, who consumes the output. Bound the
sweep before starting — name the questions research must answer to fill the
brief's fields, answer those, and stop. Research that outruns the brief's
fields spends the workspace without scheduling it.

## Exit

Three lists, all destined for the design brief:

- Findings, each with its source.
- Claims kept but unverified, each marked as such.
- Questions research could not answer, carried into the brief's open
  questions.
