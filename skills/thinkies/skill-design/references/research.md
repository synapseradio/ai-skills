# Research for Design

Run this when the user asks for research during design. Exit with
findings, each with a source a reader could reach, plus a named list of
what stayed unverified. Nothing drops silently.

## What to read, in order

1. The deployment environment's existing skills, where design move 2
   has not already covered them — carry its overlap findings forward
   rather than rereading. Names and descriptions first, because the
   executor decides selection from those alone; then the bodies of any
   skill whose intent overlaps the one under design.
2. The [Agent Skills specification](https://agentskills.io/specification)
   and Anthropic's [skill best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices),
   whenever the design touches loading stages, frontmatter, or
   triggering.
3. The source of truth behind the skill: the docs, codebase, API, or
   corpus. Locate the live home of each fact the skill will point at;
   those homes fill the brief's sources of truth, because a fact with a
   live home gets a pointer, never a copy.
4. Prior art beyond the environment, when the domain has established
   practice worth citing — a style guide, a benchmark, an official
   tool.

## How to verify

Check claims against artifacts rather than against other documents: run
the command, call the API, read the schema. Give a claim inherited from
an existing document the same check, because once it lands in the
skill, readers stop asking where it came from. Where the artifact sits
out of reach, keep the claim marked unverified; it lands in the brief's
open questions.

## How deep

Scale by the stakes: how often the skill gets reused, what a wrong
freeze would cost to reverse, who reads the output. Bound the sweep
before starting — name the questions you must answer to fill the
brief's fields, answer those, and stop.

## Exit

Three lists, all bound for the design brief:

- Findings, each with its source.
- Claims kept but unverified, each marked as such.
- Questions you could not answer, carried into the brief's open
  questions.
