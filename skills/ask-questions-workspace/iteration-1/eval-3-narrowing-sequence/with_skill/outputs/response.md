Here's a funnel: start broad enough to be surprised, then narrow one variable at a time until you have something you can reproduce yourself.

1. **"Where do you feel it — is it the whole app, or specific pages/actions?"** — Establishes scope before you drill into anything. Coverage before depth.
2. **"Which one(s), specifically?"** (skip if #1 already named one) — Pins the trigger to an action, not a vibe.
3. **"What actually happens — a spinner that hangs, the screen freezing, or a delay before something responds?"** — "Slow" hides at least three different failure modes; you need to know which.
4. **"Roughly how long does it take, versus what you'd expect?"** — Turns "slow" into a number you can compare against a benchmark or a log timestamp.
5. **"Does it happen every time you do that, or only sometimes?"** — Consistent bugs and intermittent ones get debugged completely differently.
6. **"Is this new, or has it always been this way? Anything change recently — an update, more data, a different device?"** — Separates a regression from a longstanding limitation, and surfaces a possible cause for free.
7. **"What device, browser, and connection are you on when it happens?"** — Rules in/out environment as the variable, especially if #5 was "sometimes."
8. **"Can you walk me through the exact steps right before it slows down, one more time — I want to try it myself"** — The payoff rung: a reproduction case you can actually run.

Close with a catch-all — **"Anything about it I haven't asked that stood out to you?"** — in case the real signal is something outside this list entirely.

Don't fire all eight at once; let each answer decide whether the next one is still needed (e.g., if they say "everywhere, all the time," you can skip straight to #6 and #7). Drop in a quick recap after 3-4 answers — "so it's the search page, every time, taking ~5s longer than it used to" — before pushing further, so you're not narrowing on a misread.
