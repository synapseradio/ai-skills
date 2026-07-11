Short answer up front, then the reasoning: probably not over-engineered, but it's close, and whether it's *actually* wasted effort depends on two things you can tell me that I can't guess.

**What am I looking at?** An internal admin panel, ~15 users, all on your team, mostly doing read-only lookups ("what's the status of this order"). It's live today on Postgres. The "what if" isn't really about the past — Postgres is already built and presumably working fine — it's about whether the choice was worth what it cost, and what that implies for the next tool like this.

**Two things I don't know and can't verify from here, so I'm asking rather than guessing:**

1. Does this admin tool have its own database, or does it read/write the *same* Postgres instance/tables the main app already uses for orders? If it's the latter, this was never really a "Postgres vs. SQLite" choice — the data already lived in Postgres, and the admin tool just got a connection string. SQLite was never on the table.
2. How's it deployed — one process on one box/container, or multiple replicas / serverless / anything that reschedules the filesystem out from under it? SQLite's whole deal is a single file with a single writer; that's trivial on one stable instance and awkward across ephemeral or horizontally-scaled ones.

I'll assume the less-flattering-for-Postgres case, since that's the one where the "over-engineered" question actually has teeth: a standalone tool with its own datastore, running as one instance. If I've got that wrong, the verdict flips toward "not over-engineered, there was no real choice here" — worth telling me.

Given that assumption, two real unknowns would actually change what you do next, so they're worth splitting into tiles rather than just picking the likely one:

- **Does usage stay this small**, or does the tool eventually get used by more than your team (support, ops, another squad)?
- **Do the requirements stay this simple** (single-row status lookups), or does it accumulate real database work — joins across tables for reporting, several people editing the same order concurrently, something else depending on its data as an API?

Those move independently — you could stay at 15 users forever and still grow gnarly reporting needs, or grow to 100 users doing the exact same simple lookups. Four futures, and none of them are impossible, so all four stay on the board:

**Stayed simple** — small team, simple lookups, forever. Here SQLite would've been strictly better: no server to patch, no connection pool to tune, a backup that's one file copy. Postgres bought you nothing in this world.

**Quiet growth** — more people start using it, but the query pattern never changes. Still mostly fine for SQLite — it handles a pile of concurrent readers and the occasional write from a human without breaking a sweat. This one only bites if you're also running several app instances hitting the same file, which is really axis-two territory.

**Feature creep** — team stays small, but the tool starts doing more: real reporting joins, multiple admins editing concurrently, maybe another service starts depending on its data. Postgres starts earning its keep here even though headcount never moved.

**Escalation** — both happen at once: wider usage and heavier requirements, maybe this "internal tool" quietly becomes something other systems rely on. Postgres was clearly the right call, possibly even underprovisioned for what it's protecting you from.

Here's the part that's true no matter which of those four you're actually heading toward: right now, today, the ops tax of running Postgres — an instance to keep patched, credentials to rotate, backups to verify, a connection pool to reason about — is being paid in full, and at today's actual usage it's buying you nothing that SQLite wouldn't. That's true in all four futures, because all four describe *what happens next*, not what's true this week. So the "did we over-engineer" feeling is a fair read of the present moment, whichever way the future breaks.

The two things that would tell you which future you're actually in, before you'd feel it as a fire: someone from outside your team asking to use the tool (that's the growth axis breaking), and the first time two people's edits actually collide, or someone asks for a query that needs a join (that's the complexity axis breaking). Both are cheap to notice and arrive well before either one would actually hurt you.

Scoring the options against those four worlds: ripping out Postgres now to "fix" the over-engineering wins in Stayed simple and Quiet growth, but actively loses in Feature creep and Escalation — you'd be migrating back under worse conditions, with live users and no clean cutover window. Leaving it exactly as it is survives all four; it costs you a little unnecessary ops overhead in the gentle worlds and pays for itself in the rough ones.

So: don't migrate the tool you already have. The churn of moving it to SQLite and possibly moving it back isn't worth saving on ops for a tool that already works, and "no clean migration window" is a bad trade against "some idle ops overhead." That's not a close call.

But I'd separate that from the actual lesson here, which is forward-looking: for the *next* internal, low-user, mostly-read tool like this, default to SQLite unless you already know at build time it'll need Postgres-only things — cross-service joins, real concurrent multi-writer load, or another system depending on it as an API. Set the two watchpoints above as your graduation trigger (someone outside the original team wants in, or a write actually collides / a join actually gets requested) rather than reaching for Postgres out of habit. That's the actual over-engineering risk worth fixing — not this tool, but the reflex that built it.
