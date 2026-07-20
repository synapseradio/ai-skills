Two of your four are already answered in the doc, one's solid, and the backfill one is worth splitting.

**Cut #1 (cursor vs. offset)** — the doc says cursor-based explicitly. Asking it signals you didn't read what they published.

**Cut #2 (rate limit)** — also stated: 600/min, 429 + Retry-After. Same problem.

**Keep #3 (customer_id filter)** — this one's real. The doc only lists `status`, `created_after`, `created_before` as filters, so whether `customer_id` exists changes whether you filter server-side or pull everything and filter client-side. Good question as-is.

**Rewrite #4** — it's actually two things stitched together, and the second half ("or should I just design to 600/min") answers itself — that's your call, not theirs, so drop it. What's left ("will you throttle me differently for a 4M backfill") is worth asking, but it's not the sharpest version of the real gap. Do the math first: 4M orders ÷ 100/page = 40,000 requests ÷ 600/min ≈ 67 hours (~2.8 days) — so the documented limit alone is *survivable*, which changes what you actually need to ask them. The two things the doc genuinely doesn't cover for a multi-day traversal are:

1. **Is there a bulk/export endpoint for one-time large backfills**, instead of cursor-paging 40k requests? (If yes, this whole plan changes — highest-value question of the set.)
2. **Cursor stability over a multi-day pagination window** — if new orders are created while you're backfilling, do you get duplicates/skips, or is the cursor's ordering guarantee stable regardless of concurrent writes?

So I'd send: customer_id filter, the bulk-export question, and the cursor-stability question — three, not four, and none of them ask what's already published.
