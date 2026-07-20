Two of your four are already answered in the doc they published — sending those signals you didn't read it closely.

**Cut Q1** — "cursor-based or offset-based" is answered verbatim: "Pagination: cursor-based."

**Cut Q2** — "what's the rate limit" is answered verbatim: "600 requests/minute per token, 429 with Retry-After."

**Keep Q3** — genuine gap. The doc lists `status`, `created_after`, `created_before` as the only filters; `customer_id` isn't among them. Real question, plainly answerable, worth sending as-is.

**Keep Q4, but split it** — this is the one that actually matters, and it's doing two jobs at once. As written it bundles "is there a different limit for bulk jobs" with an implicit fallback ("or should I just design to 600/min"), which also assumes rate limiting is the only risk in a 4M-record backfill. For a job that size (67+ min even at max throughput), the more likely failure mode isn't the rate limit — it's the cursor. I'd send two questions instead:

1. "For a one-time backfill of ~4M orders, is there a different rate limit or recommended approach, or should I design to the documented 600/min?"
2. "Does the `next_cursor` stay valid across a multi-hour run if new orders are created in the meantime, and can I resume from a stored cursor if my job restarts partway through?"

That second one is the one most backfill scripts get bitten by later — worth asking now rather than discovering it mid-run.
