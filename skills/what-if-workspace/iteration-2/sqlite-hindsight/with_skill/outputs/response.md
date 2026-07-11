Fun one to gut-check, so let's actually walk it instead of just vibes-answering "yeah probably lol."

**What's actually in play.** Four pieces: the admin tool itself, the order data it shows, your 15-person team, and however the thing is deployed and kept running. One thing bounds every version of this story before we even start: it's already built and working on Postgres. Nothing's on fire. So this isn't "which do we pick" — it's "was this the right size," which changes the payoff of getting an answer. There's no urgent decision waiting on it.

**What do I know, and what's just true either way?** Known: 15 users max, mostly reading order statuses. Generally true regardless of your specific setup, so no need to treat these as open questions: SQLite handles a handful of concurrent readers without breaking a sweat, and in WAL mode it tolerates light concurrent writes too — 15 people are nowhere near the ceiling of either engine on the read side. Postgres, meanwhile, brings costs that don't shrink just because the tool is small: a server process to run, connections to manage, patching and backups for someone to own, usually a monthly hosting line. SQLite skips all of that — it's a file that ships with the app.

That's most of the answer already, for the pure "15 people reading statuses" story. But two things about your actual setup would flip the verdict, and I don't know either:

1. Is this tool read-only (mirroring order data from wherever orders really get created), or can your team edit something through it — mark an order resolved, leave a note? Either answer is a completely normal way to have built this; I just need to know which one you've got.
2. How does it run — one process on one box somewhere, or something that can spin up more than one instance at a time (serverless functions, an autoscaling group, replicas behind a load balancer)? Again, no wrong answer here, just need the shape.

Since nobody's around to ask, I'll assume: mostly reads with occasional light edits (matches "checking order statuses"), and a single always-on instance, since that's the default for a scrappy internal tool. Flag these — if either assumption is backwards, the read below shifts, and I'll say exactly how.

**Which of those would actually change what you conclude?** Both. Whether people write concurrently decides whether SQLite is even safe to use here; whether the app can run as more than one process at once decides whether a single SQLite file can reliably exist at all. Two axes, so four tiles. Checked that they move independently — a single instance can have either low or high write activity, and low write activity can happen on a single instance or many — so both stay, no merging.

Four worlds:

- **Right-sized** (light writes, single instance): SQLite would've done the job fine, arguably better — Postgres is carrying machinery this workload never asked for.
- **Wrong reason** (light writes, many instances): even with almost no writes, a single SQLite file becomes the actual liability the moment more than one process might touch it — file locking over shared storage gets unreliable fast. Postgres wins here, but because of topology, not load.
- **Elbows out** (heavier writes, single instance): a couple of admins editing the same order around the same time. SQLite in WAL mode shrugs this off up to a real point — it only gets ugly under sustained, simultaneous writers, which is a stretch at 15 users. Mild edge still goes to SQLite; Postgres isn't clearly earning its keep even here.
- **No contest** (heavier writes, many instances): real concurrent writers across real concurrent processes. This is exactly what Postgres is for. No argument.

All four hold up under a stress check — "Wrong reason" in particular isn't self-contradictory just because the load is light: plenty of small, low-traffic apps still run on platforms that autoscale by default, so light-load-plus-multi-instance is a normal combination, not a fluke.

| Tile | Writes | Topology | Migrate to SQLite now | Leave as-is | SQLite-first going forward |
|---|---|---|---|---|---|
| Right-sized | light | single instance | thrives | survives | thrives |
| Wrong reason | light | multi-instance | dies | thrives | survives |
| Elbows out | heavier | single instance | survives | thrives | survives |
| No contest | heavier | multi-instance | dies | thrives | survives |

One thing holds in three of these four worlds, everywhere except the genuinely busy one: the number 15 was never actually the variable that decided this. It's whether more than one process can touch the file at once. If you find yourself explaining the Postgres choice by pointing at user count, that's the tell you're reaching for the wrong justification — right or wrong, it isn't why it matters here.

Both hinges are checkable today, not future events to wait on:

- Does anyone actually edit through this tool, and has that ever thrown a locked-database-style error or a lost update? A five-minute ask-the-team or grep-for-write-queries settles axis one.
- What does the deployment config say — replica count, autoscaling, serverless? A five-minute look at the infra settles axis two.

So: don't migrate the tool that's currently running. It works, nothing's forcing the question, and "leave as-is" never dies across any of the four worlds — at worst (Right-sized) it just means you're quietly paying more in hosting and ops attention than the workload needs, which is a real but survivable cost, not a wrong call. Migrating it now would thrive in exactly one world and die in two, which is a bad trade for a system that isn't hurting anyone.

The actual lesson is forward-looking: default to SQLite for the next small internal tool at this scale, and only reach for Postgres once you can point to a concrete reason — an actual multi-writer conflict or an actual multi-instance deployment — rather than reaching for it as the reflexive "serious" choice. That default survives all four worlds here, and it's the one place where yes, this specific tool probably was oversized for the job — not a costly mistake, just an unnecessary one.
