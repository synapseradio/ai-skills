You're asking whether to pivot to selling API access to your categorization engine and sunset the consumer app, three weeks before a board meeting, and it feels irreversible. Let me walk through why it splits the way it does, because the "one-way door" framing turns out to be only half right.

**What am I looking at, and what bounds it?** Two products share one engine: a consumer app at flat ~2k MAU, and a categorization engine underneath it that three companies have now asked to pay for directly. Six people is a hard ceiling on how much you can run in parallel — that bounds every option below, not just the ambitious ones. Fourteen months of runway is the other hard bound, and it matters less as a deadline than as a pace-setter: you need real signal in weeks, not months, because burning the whole runway to find out which bet was right isn't a plan. And there's a dependency worth naming: if the app is where the engine gets tuned against live edge cases, killing it outright doesn't just lose users, it may slow the engine's own improvement — something to check before treating "sunset" as free.

**What do I know, and what would help to know?** The known facts — team size, runway, flat MAU, three inbound emails, board date — are given. A few things are checkable rather than uncertain, so I'm not turning them into guesswork: whether the engine can be pulled out of the app's codebase cleanly is an engineering question you can answer this week, not a future event, so it stays off the table below as an assumption to verify rather than a scenario branch.

Past that, a handful of things only you hold, and I'm proceeding on stated assumptions for each since there's no one to ask right now:

- What did the three companies actually float — a budget, a use case, a timeline — or was it just "we'd pay for this," untested? *Assumption: no numbers yet, just interest.* If one of them already named a contract size, that changes the read below substantially in the API's favor.
- What's the monthly burn behind the 14-month number, and does it assume any cuts? *Assumption: 14 months at current burn, no belt-tightening baked in.*
- Does the app carry any revenue today, or is it a pure cost center? *Assumption: negligible revenue.*
- Has anyone on the team actually sold into companies before, or would this be founders learning enterprise sales from zero? *Assumption: no dedicated seller — founders would run this themselves.*

None of these are "yes/no on whether you're doing okay" questions — they're just numbers and dates I don't have. If any assumption above is wrong, say so and the read shifts, but I'll proceed on these for now.

**Which unknowns would actually change what you do?** Two things survive that test. First: is the API interest a real market — multiple companies who'll pay a sustaining price — or is it three polite emails that don't convert? Second: is the consumer app's flatness a market verdict (this product has a ceiling) or an execution gap (nobody's tried the right channel or hook yet)? Both would change the call. A third candidate — "can the team actually run both motions at once" — isn't really an uncertainty about the future; it's a resourcing constraint you already know (six people, finite hours), so it shapes the recommendation rather than becoming its own axis.

**Do those two vary independently?** Yes. A real API market doesn't tell you anything about whether the app could still grow with a different lever, and a dead-end app doesn't tell you anything about whether enterprise demand is real. Two independent axes, four worlds.

**Which worlds survive?** All four are internally consistent — none breaks a constraint or contradicts something already true — so all four stay on the board:

- *Platform emerges* (API real, app dead): the inbound turns into real paying pilots, and the app's flatness confirms it was never the vehicle — the engine was the asset the whole time.
- *Stretched thin* (API real, app latent): API pilots convert into a genuine pipeline, but a cheap growth test also shows the app responding to a lever nobody had tried. With six people, chasing both starves each — you build the API well enough to bill, and discover the app's real potential too late to fund it.
- *False signal* (API soft, app dead): the three emails were tire-kicking, none convert into anything that covers a salary, and the app confirms there's no rescue on either side. The runway clock becomes the entire story.
- *Wrong bet* (API soft, app latent): the API interest fizzles into unpaid pilots and slow procurement, while a starved app — the one thing nobody invested in during the scramble — turns out to have had a cheap, real growth unlock sitting unused, discovered only after the goodwill and dev time needed to act on it are already gone.

Every plausible future lands in exactly one of those four — clean fit, no overlaps, nothing left homeless.

**What follows from what, inside each?** In *Platform emerges*, converted pilots enable hiring a support function and force you to formalize pricing and SLAs; sunsetting the app frees engineering time that goes straight into hardening the API. In *Stretched thin*, split attention blocks focused execution on either front and amplifies burn without proportional revenue — you end up making the same hard choice later, just with less runway left to make it. In *False signal*, the absence of revenue on both sides forces a bridge conversation — a raise, deep cuts, or a shutdown talk — well before month 14, because discovery alone can't eat the whole runway. In *Wrong bet*, an early full sunset blocks any chance of testing the app's latent growth before the option disappears.

One consequence shows up in three of the four worlds regardless of which arrives: talking to the three companies now, this week, to turn "interested" into a signed pilot or a clear no, is close to free and valuable everywhere — do that no matter what. And a related pattern spans *Stretched thin* and *Wrong bet*: a hard, immediate shutdown of the app forecloses value in exactly the worlds where the app was hiding something real, while a soft freeze — no new investment, but not deleted — costs almost nothing in the other two. That argues against treating this as a single irreversible cut on day one.

**What would tell me which world is arriving, and early?** Two watchpoints, both resolvable inside the next three to four weeks — conveniently right around your board date:

- Whether at least one of the three companies signs a paid pilot or a real letter of intent with an actual dollar figure, versus stays at "let's stay in touch." A signed pilot predicts *real* API demand; continued vagueness after a concrete proposal predicts *soft*.
- Whether one sharp, cheap growth experiment on the app — a new acquisition channel, an onboarding change, a pricing test — moves activation meaningfully, versus moves nothing despite a genuine lever. Movement predicts *latent*; nothing predicts *dead*.

**Which move survives every world?** Three options, scored against all four:

| World | Full pivot now | Status quo | Staged validation |
| --- | --- | --- | --- |
| Platform emerges | thrives | dies | survives |
| Stretched thin | dies | survives | thrives |
| False signal | dies | dies | survives |
| Wrong bet | dies | survives | survives |

A full pivot today — sunset the app, commit fully to the API, announce it at the board meeting — wins big in *Platform emerges* but dies in the other three: it forecloses the app's value in the worlds where that value was real, and it burns weeks of runway on a market that might not exist, before you'd have any evidence either way. Status quo — treat the emails as a distraction, keep grinding on the app as-is — never dies outright, but it never wins either; it's the "don't decide" option wearing a decision's clothes, and it does nothing about the fact that a flat app and a 14-month clock are already a problem. Staged validation — freeze new investment in the app without killing it, spend the next three to four weeks running both cheap probes above in parallel, and bring the board a decision framed by what those probes show rather than a final call made blind — survives or thrives in all four worlds. It's the only option that never dies.

Its weakest showing is in *Platform emerges*, where it costs a few weeks of speed against a full immediate pivot. That gap closes almost entirely if you negotiate pricing and contract terms with the three companies during the same window, so that a confirmed signal converts straight into signed paper instead of restarting a sales process from scratch after the board meeting.

Putting it together: your fourteen months and six people don't split cleanly on "pivot or don't" — they split on whether the API interest is a real market and whether the app's flatness is a verdict or an unexplored lever. Where both resolve toward the API, the platform emerges cleanly and the app was never the asset. Where the API is real but the app also had a latent unlock, six people chasing both starves each, and the honest move is choosing on purpose rather than by accident. Where the API interest turns out soft and the app is genuinely dead, the runway clock becomes the whole story, and you'll want to know that with thirteen months left, not with two. And where the API fizzles but the app had something real, the worst outcome is having already deleted the evidence before anyone looked.

One thing is worth doing regardless of which world shows up: get real answers from the three companies this week, not sentiment, but a signed pilot or a clear no.

Recommendation: don't treat this as the one-way door it feels like. Freeze new investment in the consumer app — no new features, no new spend — but don't shut it down yet. Use the three weeks before the board meeting to run two cheap, parallel probes: push the three companies to a signed pilot or a real no, and run one sharp growth experiment on the app. Bring the board the framework above, not a final verdict, with a commitment to a real decision within four to six weeks once both watchpoints have fired. This is the one move that doesn't die in any of the four worlds; the price you pay for it is a few weeks of slower commitment if the platform future turns out to be the real one, and you can close most of that gap by lining up contract terms with the three companies during the same window, so a "yes" converts immediately into signed revenue instead of a second sales cycle.
