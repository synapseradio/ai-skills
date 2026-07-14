# Audit: `skills/apache-age`

## Verdict

It is well built, with real defects. The skill is unusually well-sourced for AI-authored
technical content — the load-bearing claims I could check against upstream held up, the
structure follows good progressive-disclosure discipline, and the code examples are mostly
copy-paste correct. But it ships at least one outright factual error that contradicts its own
other pages, one passage of syntax I believe is fabricated, and one buggy example. None of
these is fatal; all are fixable without restructuring. The honest one-line summary: a strong
skill that a careful reviewer would not yet call trustworthy, because the errors it does have
are the kind a user would copy verbatim and get burned by.

## How I checked

I read all six files in full (`SKILL.md`, `README.md`, and the five references). Because the
skill's value rests on specific factual claims — cited GitHub issue numbers, AGE-specific
syntax, casting rules — I verified the highest-stakes ones against upstream sources (the AGE
manual, the apache/age issue tracker, Microsoft/Azure's AGE performance docs, and Stack
Overflow) rather than trusting them. Where I could not verify a claim live, I say so and mark
it. I did not have a running AGE instance, so anything I could not corroborate from
documentation is flagged as attributed-but-unverified, not confirmed.

---

## What is strong (verified)

**The GitHub issue citations are real and on-topic.** This is the thing most likely to be
confabulated in AI-written reference material, so I spot-checked five:

- Issue #2194 — resolves to "Major Performance Difference: SQL vs. Cypher for
  Aggregation/Ordering," matching the skill's aggregation claim (`SKILL.md:50`,
  `nothing-is-automatic.md:423`).
- Issue #1840 — "Please work around limitation of 100 or 50 fields for the function
  parameters such as agtype_build_map," matching the 50-key-pair limit
  (`SKILL.md:111`, `agtype-is-everything.md:254-256`).
- Issue #315 — "Support passing parameters to the cypher function without creating a prepared
  statement," matching the prepared-statement constraint (`the-wrapper-contract.md:51`,
  `hybrid-is-the-point.md:290-293`).
- Issue #195 — "Variable Length Edges feature does not scale well with the length of the
  path," matching the unbounded-path warning (`SKILL.md:106`).
- Issue #1996 — "Is agtype like json? Casting agtype to json," matching the json-cast-failure
  claim (`agtype-is-everything.md:236`).

Five for five. That is a strong signal the author worked from the real issue tracker, not from
memory.

**The EXPLAIN guidance is correct.** I was suspicious of the claim that `EXPLAIN` goes *inside*
the Cypher string (`nothing-is-automatic.md:156-167`), because it is the opposite of how most
databases work. It checks out: Stack Overflow and Azure's AGE docs both show
`SELECT * FROM cypher('g', $$ EXPLAIN ANALYZE MATCH ... $$) AS (result agtype)`. The sample
query plans in `nothing-is-automatic.md:169-185` are the same `agtype_access_operator(VARIADIC
ARRAY[properties, '"Name"'::agtype])` plans that Microsoft's AGE performance page publishes, so
the whole indexing section is grounded in a real source.

**The `->` / `->>` operator usage is valid.** I doubted `node->'properties'->>'email'`
(`hybrid-is-the-point.md:429-431`), but issue #1996 shows an AGE user running `b ->> 1` on an
agtype column and getting a value back. The operators do work on agtype output. (This makes the
bug at `hybrid-is-the-point.md:249`, below, a genuine bug rather than "operators don't exist.")

**Structure and pedagogy are good.** `SKILL.md` stays lean (159 lines) and defers detail to
references via an explicit load table with "when to load" and "do NOT load" guidance
(`SKILL.md:24-36`) — real progressive disclosure, not a wall of text. The five references are
named as memorable principles ("agtype Is Everything," "Nothing Is Automatic") rather than
flat topic labels, which aids recall. The frontmatter is spec-clean: `SKILL.md` carries only
`name` and `description`, and the description is trigger-rich (`SKILL.md:3`). The freedom
calibration (`SKILL.md:38-42`) is a thoughtful touch — telling the reader which rules are rigid
(wrapper syntax) versus discretionary (property naming).

---

## Defects, ranked by what matters most to fix

### 1. `graphid` is described as "globally unique" — this is false and self-contradictory

`schema-is-storage.md:44` states the `id` column is "system-assigned, globally unique." The
AGE manual says the opposite: a graphid "is a unique composition of the entity's label id and a
unique sequence assigned to each label. Note that there will be overlap in ids" across labels
and graphs. The skill even contradicts *itself* elsewhere — `the-wrapper-contract.md:173`,
`the-wrapper-contract.md:247-249`, and `SKILL.md`'s function note all correctly say ids are
"Unique per-graph only, not globally across graphs."

Why this matters most: a reader who trusts `schema-is-storage.md:44` will design a cross-graph
join or a deduplication key on the assumption that graphids never collide, and it will silently
produce wrong results — exactly the failure the other three pages warn against. Fix: change
"globally unique" to "unique within a graph (label_id + per-label sequence); ids can collide
across graphs."

### 2. The `->>` / `<<-` "AGE extended" arrow syntax appears to be fabricated

`the-wrapper-contract.md:108-115` claims:

```
MATCH (a)-[:KNOWS]->>(b)  -- AGE extended form (also valid)
MATCH (a)<<-[:KNOWS]-(b)  -- incoming with AGE extended form
```

and asserts AGE "uses `>>` for outgoing and `<<` for incoming in some contexts." I could find
no corroboration in the AGE manual, the openCypher grammar, or any tutorial — every source uses
only the standard `->` and `<-`. The openCypher relationship grammar has no `->>`/`<<-`
production. I could not run it against a live instance to be certain, but I rate this
high-confidence wrong, and it is presented as copy-paste-valid syntax, so a user will try it
and hit a parse error.

Fix: delete lines 108-115. Nothing else depends on them.

### 3. Buggy example: `upsert.p->>'name'` reads the wrong nesting level

`hybrid-is-the-point.md:249`:

```sql
SELECT upsert.p->>'name' AS name FROM upsert;
```

Here `p` is a vertex agtype whose shape is `{"id":..., "label":..., "properties":{"name":...}}`.
`p->>'name'` extracts a top-level key `name`, which does not exist, so it returns `null`. The
name lives under `properties`. The very same reference gets this right 180 lines later for
email: `node->'properties'->>'email'` (`hybrid-is-the-point.md:431`). Fix line 249 to
`upsert.p->'properties'->>'name'`.

### 4. The `cypher()` return type is stated two incompatible ways

`SKILL.md:56` and `SKILL.md:103` say `cypher()` "returns `SETOF record`" — which is the correct
explanation for *why* PostgreSQL demands an explicit `AS (col agtype)` list.
`the-wrapper-contract.md:15-16` states the signature as `RETURNS SETOF agtype`. If it truly
returned `SETOF agtype`, the column list would not be mandatory — so the reference's stated
signature undercuts the mandatory-column-list rule it exists to teach. Pick one (the `SETOF
record` framing is the useful one) and make both pages agree.

### 5. `SKILL.md`'s "NEVER" overstates the text-cast rule its own reference nuances

`SKILL.md:108` says agtype "can only cast to `varchar` among string types (not json/text)."
But `agtype-is-everything.md:235` and `hybrid-is-the-point.md:404` both say `::text` *works on
scalar* agtype and only fails on non-scalars. Several of the skill's own examples rely on
`::text` for scalars (e.g. `hybrid-is-the-point.md:78`, `schema-is-storage.md:485`,
`nothing-is-automatic.md:220`). The blanket "not text" in the top-level NEVER list is stricter
than reality and stricter than the rest of the skill. Fix: soften to "text works only on
scalar agtype; use varchar for entities and to be safe."

### 6. Substantial duplication across references creates drift risk

The `cypher()` signature and column-list rules appear in four places (`SKILL.md`,
`the-wrapper-contract.md:8-51`, `hybrid-is-the-point.md:30-47`, `agtype-is-everything.md:9-17`).
The agtype→SQL casting table is near-duplicated between `agtype-is-everything.md:228-241` and
`hybrid-is-the-point.md:401-408`. The "how AGE stores graphs" model is repeated in
`schema-is-storage.md:27-54` and `nothing-is-automatic.md:27-42`. Defect #1 (the graphid
contradiction) is the direct symptom of this: the same fact stated in multiple places drifted
out of sync. This is not a correctness bug today beyond #1, but it is the mechanism by which the
next one appears. Worth a consolidation pass, or at minimum reconciling the duplicated facts.

### 7. Claims I could not verify — attributed but unconfirmed

These are not errors; they are unresolved. An honest audit flags them rather than passing them
off as checked:

- **"Discussion #109"** for single-label support (`SKILL.md:110`,
  `the-wrapper-contract.md:173,197`, `agtype-is-everything.md`). Issue #109 in the results is a
  doc typo in the *age-website* repo, not about labels. GitHub discussions are numbered
  separately from issues, so Discussion #109 may well be correct — but I could not open it to
  confirm. The single-label-per-vertex fact itself is true and widely documented; only the
  specific citation is unverified.
- **"~15x faster"** for SQL vs Cypher aggregation (`SKILL.md:50`,
  `nothing-is-automatic.md:423`). Issue #2194 confirms a "major" gap exists; I did not confirm
  the specific 15x multiplier.
- **"7s → 7min on 1.5M vertices"** for unbounded paths (`SKILL.md:106`). Issue #195 confirms the
  scaling problem; the specific numbers are unverified.
- **AGEFreighter "725K vertices + 2.8M edges in ~83 seconds"** (`nothing-is-automatic.md:353`).
  Plausible, unverified.

Recommendation: keep these but consider softening precise figures to ranges unless the author
has the exact source line, since a wrong-looking specific number damages trust more than an
honest approximation.

---

## Smaller notes (low priority)

- `agtype-is-everything.md:35` and `285-286` claim `'NaN'::float = 'NaN'::float → true` as an
  AGE deviation from IEEE-754. Plausible and consistent with sort-ordering needs, but
  unverified — worth a citation if kept as a load-bearing claim.
- The time-sensitive "Not Supported" table (`the-wrapper-contract.md:191-207`: list
  comprehensions, `reduce()`, map projections, etc.) is accurate to AGE's historical state but
  is exactly the kind of list that goes stale as AGE adds features (the table itself notes CASE
  was added in PR #1431). Consider dating it or noting the AGE version it reflects.
- `README.md` install command uses `npx skills add ...` (`README.md:10`), which is not the
  install path the repo's own `CLAUDE.md` documents (`.skill` upload + the packaged footer).
  Worth confirming that command is real and current.

## Questions I would ask the author (recorded here since no one is available)

1. Was `-[:KNOWS]->>(b)` / `<<-` (defect #2) tested against a live AGE instance, or drawn from
   memory? If there is a source, I will retract; I found none.
2. What AGE version does the "Not Supported" table target? Naming it would let readers trust or
   discount it against their own version.
3. Do you have the source lines for the 15x, the 7s→7min figures, and the AGEFreighter
   benchmark? If so, cite them inline; if not, I would soften to ranges.
</content>

</invoke>
