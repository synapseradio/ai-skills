# Audit: skills/apache-age

## Verdict

The skill is well-built structurally and mostly well-built factually, but it contains one fabricated piece of syntax and at least three demonstrably wrong "not supported" claims sitting inside the single reference file marked MANDATORY for first-time users. Everything I could check by reading AGE's actual grammar source and its GitHub issue tracker either confirmed the claim or found it wrong — nothing came back merely "unverifiable." That's a good sign for the skill's overall diligence, but it means the wrong claims are wrong with confidence, not just stale-sounding.

Structure, cross-referencing, packaging, and frontmatter are all clean. The content problems are concentrated in `references/the-wrapper-contract.md`'s "Not Supported in AGE" table and one syntax claim in the same file.

## Method

I read all six files (`SKILL.md` plus five references, ~2,200 lines total). For every load-bearing empirical claim — GitHub issue/PR numbers, "not supported" claims, a named benchmark figure — I checked it against a primary source rather than trusting the prose: I cloned the relevant files from `apache/age` on GitHub (`cypher_gram.y`, `ag_scanner.l`, `agtype.c`), queried `gh api` for every cited issue/PR/discussion number, and ran a web search for the one external benchmark citation. I did not check every single row of every table (e.g., I didn't verify `CALL {} IN TRANSACTIONS` or `LOAD CSV` claims) — I stopped once I had enough confirmed hits and misses to characterize the file's overall reliability, per the "diminishing returns" judgment call. That gap is itself worth naming: an audit is only as good as its coverage, and mine is not exhaustive.

## What's fabricated

`references/the-wrapper-contract.md:108-115` claims AGE has an "extended form" of edge-direction syntax using doubled arrows:

```
MATCH (a)-[:KNOWS]->>(b)  -- AGE extended form (also valid)
MATCH (a)<<-[:KNOWS]-(b)  -- incoming with AGE extended form
```

I pulled AGE's actual parser grammar (`src/backend/parser/cypher_gram.y`, rule `path_relationship`, lines 1451–1480) directly from the `apache/age` repo. It defines exactly three relationship forms: `'-' path_relationship_body '-'` (undirected), `'-' path_relationship_body '-' '>'` (outgoing), and `'<' '-' path_relationship_body '-'` (incoming). There is no fourth production, and no token in the scanner for a doubled arrow. The two example queries in the skill would fail to parse. This isn't a stale claim about a feature that changed — it's a syntax that, as far as the grammar shows, never existed. Anyone who copies those two lines into a query gets a parse error the skill told them to expect success from.

## What's wrong and stale, in the file marked MANDATORY

`the-wrapper-contract.md`'s "Not Supported in AGE" table (lines 187–207) is the reference `SKILL.md` tells every first-time user they must load. I checked several of its rows against `apache/age`'s issue tracker and found three that are flatly incorrect, not just outdated by a point release:

- **List comprehensions** (`[x IN list WHERE ...]`) — the skill says "Not supported," recommend `UNWIND + collect()` instead. AGE has had list comprehension support since at least 2021 (issue #105), with active bug-fixing through 2024 (PR #2094, "Fix issue 1955 - List comprehension in WHERE clause") and a full reimplementation merged June 2025 (PRs #2169, #2189). This has been true for years, not something that changed last month.
- **`EXISTS { MATCH ... }` subqueries** — the skill says "Not supported," recommend "OPTIONAL MATCH + null check" instead. There's an open bug report (#2396) titled "A `WHERE EXISTS { ... }` subquery may crash Apache AGE when it contains both..." — you can't crash on a syntax that doesn't parse. The feature exists; it has edge-case bugs.
- **Map projections** (`n{.name, .age}`) — the skill says "Not supported." PR #1710, "Implement map projection," merged March 2024.

For contrast, the same table's **`FOREACH`** row ("Not supported") is still accurate — there's an open feature request (#2381) with no merged implementation. So the table isn't uniformly wrong; a third-or-so of the rows I spot-checked were wrong, which means the table as a whole can't be trusted without re-verification, even though some individual rows hold up.

Related: `reduce()` is also listed as "Not supported," and that was true until PR #2435 merged it on 2026-06-26 — about three weeks before this audit. I'm treating this one separately from the three above because it's plausibly just overtaken by very recent upstream work rather than an error at authoring time, but it reinforces the same underlying problem: there is no version anchor anywhere in this skill telling a reader which AGE release the "not supported" claims describe, so there's no way to tell "wrong when written" from "correct when written, stale now" from a distance. Given how actively `apache/age` is developing (I found dozens of merged PRs in just the last few months), that absence compounds.

## What checks out

Every citation with a specific, falsifiable identifier that I checked was accurate:

- All nine GitHub issue/PR numbers cited across the reference files (#2194, #195, #1225, #1996, #1840, #1956, #1303, #315, #1431) exist and match their stated subject.
- Discussion #109 ("Will it be possible to assign nodes multiple Labels?") backs the single-label design claim exactly.
- PR #1431 ("Add support for chained expressions in CASE") merged 2023-12-01, matching the skill's "since late 2023" claim — though the skill's framing ("CASE expressions | Supported (since late 2023...)") slightly overstates it: the PR title says it added *chained* expressions in CASE, implying basic CASE support predates it. Minor imprecision, not a fabrication.
- `agtype_access_operator` is a real function in `agtype.c`, backing the indexing guidance in `nothing-is-automatic.md` and `schema-is-storage.md`.
- The AGEFreighter benchmark ("725K vertices + 2.8M edges... ~83 seconds") is a real figure that also appears in Microsoft's Azure Database for PostgreSQL documentation.

This is a genuinely good hit rate for cited claims, which is why the fabricated syntax and the three wrong "unsupported" rows stand out — they're the exception in an otherwise well-sourced document, not representative of a document that guesses freely.

## Structural quality

This part of the skill is solid and I found no problems:

- `packaged/apache-age.skill` is byte-identical in content to the current `skills/apache-age/` source (I unzipped it and diffed). Packaging is not stale.
- `SKILL.md` frontmatter has exactly `name` and `description`, both spec-compliant (description is 467 of 1024 allowed characters, no `<`/`>`). No non-spec keys.
- All five reference links from `SKILL.md`'s loading table resolve to real files.
- Every reference file with a numbered Table of Contents (`hybrid-is-the-point.md`, `nothing-is-automatic.md`, `schema-is-storage.md`) has TOC entries that match its actual `##`/`###` headers in the same order — no drifted anchors.
- The "Reference Loading" table gives explicit load/don't-load guidance and a three-tier "freedom calibration" (low/medium/high), which is a genuinely useful piece of design: it tells the consuming agent not just what exists but when to bother reading it and how much latitude it has once it does.

One duplication worth flagging as a maintenance risk rather than a bug: the agtype-to-SQL casting table appears twice, nearly verbatim, in both `agtype-is-everything.md` (lines 228–252) and `hybrid-is-the-point.md` (lines 397–422). They currently agree with each other, but two independent copies of the same casting rule are two places that can silently drift apart on the next edit.

## What matters most to fix, in order

1. **Delete the `->>`/`<<-` "AGE extended form" syntax claim in `the-wrapper-contract.md`.** It's fabricated and will produce a parse error for anyone who trusts it. This is the single highest-severity item because it's presented as fact with example code, not hedged.
2. **Re-verify every row of the "Not Supported in AGE" table**, not just the ones I happened to check. Given three (list comprehensions, EXISTS subqueries, map projections) were wrong and one more (`reduce()`) went stale three weeks ago, the table's remaining rows (`CALL {} IN TRANSACTIONS`, `LOAD CSV`, `CREATE INDEX`/`CREATE CONSTRAINT` Cypher syntax, APOC procedures, `WITH *`) need the same treatment before they can be trusted. This table sits in the file `SKILL.md` marks MANDATORY for first-time users, so it's the highest-traffic wrong content in the skill.
3. **Add a version/date anchor.** Something like "accurate as of AGE 1.5.0 / July 2026" at the top of `the-wrapper-contract.md` (or all reference files) would let a future maintainer — or a future you — know at a glance whether "not supported" claims need re-checking, given how fast upstream AGE is moving.
4. **Consolidate the duplicated casting table** between `agtype-is-everything.md` and `hybrid-is-the-point.md` into one source of truth, with the other file linking to it, so a future edit can't silently create disagreement between them.

## Questions for the user (unavailable for follow-up, so recorded here)

- Was `the-wrapper-contract.md`'s doubled-arrow syntax tested against a specific AGE fork or version that might genuinely support it, or is it an invention/misremembering? I checked mainline `apache/age`'s grammar and found no support for it, but if there's a fork or patched build this was validated against, that context would change the fix (note the divergence) versus just deleting the claim.
- Is there an intended AGE version this skill targets? Nothing in the files states one, and given how actively upstream is changing (dozens of merged PRs in the last several months alone), pinning a version would materially change how "not supported" claims should be maintained going forward.
- Should the "Not Supported in AGE" table be re-verified now, or is there a reason to defer that (e.g., a planned rewrite, or known low usage of this skill)? I didn't make that call since it's a scope/priority decision, not a technical one.
