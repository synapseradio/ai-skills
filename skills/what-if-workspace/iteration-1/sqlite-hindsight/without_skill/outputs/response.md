Honestly, probably yes — for that scale, SQLite would very likely have worked fine, and in some ways would have been the better fit.

The usual worry with SQLite is concurrent writes: it locks the whole database file for writers, so two people updating at the exact same instant means one waits a beat. With WAL mode turned on, readers stop blocking writers entirely, and for 15 people occasionally changing an order status, that contention is a non-issue in practice. Read-heavy traffic — which "checking order statuses" mostly is — scales into the thousands of users on SQLite without strain.

What you'd have given up by going with SQLite:

- Network access from multiple servers. SQLite is embedded, not client-server — it works great if the tool runs as a single process on one box, but if you ever have multiple app servers or containers hitting the same data, you need it on shared storage or you're better off with Postgres.
- Built-in replication and backup tooling. You'd be doing periodic file copies or something like litestream instead of `pg_dump`.
- The richer type system and constraint checking, if you were actually leaning on those.

What you'd have gained: no separate database process to run, patch, or monitor. No connection pool to tune, no instance size to pick, no "why did the DB run out of connections" page at 2am. Just a file sitting next to the app. For a tool a handful of people use, that's real operational simplicity you're currently paying for.

So — not "wrong," but if the honest requirement was "15 people, mostly reads, runs on one box," SQLite was probably the right-sized tool, and Postgres bought you multi-writer/multi-server support and headroom you don't currently need. Whether that counts as over-engineering or reasonable margin really comes down to: do you expect this thing to grow past an internal tool, does your team already have Postgres operational muscle memory (that's worth something), and is it sharing infra or credentials with other services that are already on Postgres anyway.

One practical note either way: if it's running fine right now, this isn't a case where I'd suggest migrating just to be "right-sized." The churn and risk of switching a working system over usually costs more than the thing you're optimizing away.
