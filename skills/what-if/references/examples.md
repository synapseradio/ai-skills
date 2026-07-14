# What-if: worked examples

Traces in a fixed tag format. `request` holds a verbatim ask; `inferred-task` a reading of it; `gather` what to collect or elicit before tiles can exist; `walk` a question chain a good response follows; `good-ending` the very end of a good response — a full reply surfaces the whole chain out loud first, question before answer, in a voice of its own choosing; `spine` (shown once, in the first example) an excerpt of how that out-loud walk sounds in flight; `why` what earns it; `counter` a tempting wrong turn, with its failure mode named.

<example name="payments-migration">
<request>Should we switch to the new billing engine now, or wait until next year? Our contract with the current provider renews in March.</request>
<inferred-task>A decision under uncertainty with a hard calendar constraint. The ask sounds like a comparison of two products today; the real task evaluates the futures in which either choice plays out.</inferred-task>
<gather>Components of the current integration and the phases of a migration. The March renewal enters as a constraint, near-predetermined. Epistemic sort leaves two unresolvables: whether the new engine matures before mid-year, and whether the pending enterprise deal closes.</gather>
<walk>Q1 maps the integration; the renewal bounds every future. Q2 verifies current pricing and support terms, leaving two unresolvables. Q3 keeps both — each would change the timing of the move — so the full chain runs. Q4 confirms they vary independently. Q5 carries all four tiles; none die. Q6 finds every future one home. Q7 merges "manual invoicing load doubles," reached in three of four tiles — near-inevitable, act on it regardless. Q8 sets the engine's GA announcement before January as the watchpoint. Q9 scores three moves: direct cutover thrives in one tile and dies in two; waiting survives three; "abstract the billing interface now, defer the cutover decision to the January watchpoint" survives all four — recommended as robust, weakest tile named. Q10 never fires.</walk>
<spine>
A full reply walks the chain out loud before its ending, each question surfaced before its answer, in whatever voice fits the asker. An excerpt of how that sounds in flight:

> **Q2 — what do I know, and what must I ask?** Current pricing and support terms check out fine through 2027; verified. Two unknowns survive every check available to me: whether the new engine matures before mid-year, and whether the enterprise deal closes. Nothing else would change the answer.
>
> **Q3 — which of those would change what you'd do?** Both. An early engine pulls migration forward; a landed deal raises the cost of standing half-migrated when volume spikes. Two axes, then: engine maturity and deal timing. Four worlds to walk.

…and onward through Q9, the same open cadence, until the ending below.
</spine>
<good-ending>
Your March renewal splits four ways along two unknowns: whether a new engine matures before mid-year, and whether an enterprise deal closes.

In *Clear runway*, the engine ships early and the deal lands: migrate now, and the volume spike rides new rails. *Ready, quiet* looks like a gift — the engine matures while the deal slips, opening a calm, cheap migration window. *Squeeze* is the world that punishes commitment: the deal lands while the engine drags, a spike hits old rails, and a half-finished migration would be the worst place to stand. *Slow lane* simply extends today: late engine, slipped deal, status quo holding.

Manual invoicing load doubles in three of these four worlds. Automate it now, whichever future arrives.

One hinge decides the map: a GA announcement by January. Silence past January makes Squeeze and Slow lane the working assumption — renew for one year in March and drop cutover plans for the first half.

Recommendation: abstract a billing interface this quarter and let the January hinge decide the cutover. This move survives all four worlds — robust. Its weakest showing comes in Slow lane, where abstraction buys nothing beyond cleaner code, and that ceiling is the price of never standing half-migrated in Squeeze.

| Tile | Landings | Cutover | Wait | Abstract |
| --- | --- | --- | --- | --- |
| Clear runway | early engine, deal lands | thrives | dies | survives |
| Ready, quiet | early engine, deal slips | thrives | survives | survives |
| Squeeze | late engine, deal lands | dies | survives | survives |
| Slow lane | late engine, deal slips | dies | thrives | survives |

</good-ending>
<why>The constraint pruned nothing yet timed every watchpoint, and the merged consequence — invoicing load — became the action item that pays off in every future.</why>
<counter failure="single-tile-forecasting">The model estimates "the engine will probably mature by Q2" and plans a straight migration. That answer forecasts instead of tiling: one bet on the likeliest tile, no coverage of the others, and when the likely future fails to arrive the plan carries no fallback. Probability replaced coverage.</counter>
</example>

<example name="berlin-offer">
<request>I got a job offer in Berlin. I like my current team, but the company is restructuring. Should I take it?</request>
<inferred-task>A personal decision whose outcome hinges on unknowns the requester cannot resolve alone. Some unknowns belong to the must-ask bucket — elicit them before tiling rather than assuming.</inferred-task>
<gather>Phases of the move: offer deadline, notice period, visa, relocation. Ask for the offer expiry date and family constraints. The visa timeline can be verified, so it stays off the axes. The restructuring outcome and how the requester settles abroad stay unresolvable.</gather>
<walk>Q2 verifies the visa timeline and asks for the offer expiry — verified unknowns never become axes. Q3 keeps the restructuring outcome and settling abroad; both would flip the decision. Q4 confirms independence. Q5 keeps all four tiles; none inconsistent. Q6 passes. Q7 finds the tiles agree on little — few merged consequences, a warning that the decision is genuinely contested. Q8 finds the watchpoint: whether the restructuring announcement lands before the offer expires — the ordering of two dates, both checkable. Q9 scores accepting now (dies in one tile) and declining now (dies in another) — nothing survives most tiles. Q10 fires: negotiate a two-week extension past the announcement. An information purchase with a named end date, recommended as the committed move.</walk>
<good-ending>
Your decision splits on two things nobody can look up today: whether your role survives the restructuring, and whether Berlin turns out to fit you.

Where both break your way abroad, taking the offer trades a team you love for a city that repays the trade. Where your role gets cut, declining strands you in a shrinking room. Where your role survives and Berlin disappoints, accepting swaps a good seat for a hard landing. Four worlds — and a clean yes or no today dies in at least one of them, which makes any confident answer a bet dressed as advice.

One date decides most of this: whether a restructuring announcement lands before your offer expires.

Recommendation: ask for a two-week extension past that announcement. One slightly awkward email buys the single fact that separates your futures, and the move holds up in every world. If they refuse the extension, weigh the refusal too — it tells you something about how much they want you.
</good-ending>
<why>Verifiable unknowns got verified instead of branched on, and when no move survived the tiles, the chain routed to buying information rather than hedging — the exit at Q10 produced a commitment, never a shrug.</why>
<counter failure="correlated-axes">The model picks "job satisfaction in Berlin" and "career growth in Berlin" as axes. Both express the same underlying unknown, so concrete futures fit two tiles at once, the tiling overlaps, and one uncertainty gets counted twice while the restructuring — the actual fault line — never earns an axis. Q4, asked honestly, catches this.</counter>
</example>

<example name="riverfront-plan">
<request>Our town is redesigning the riverfront. The flood projections are contested and the federal grant is uncertain. What should the plan assume?</request>
<inferred-task>The ask sounds like choosing what to assume; the real task maps which futures any design must survive, so the council stops needing a single assumption at all.</inferred-task>
<gather>Components: levee, park, housing parcels. Phases: permitting, then construction seasons. The municipal bond ceiling enters as a hard constraint. Axes: flood regime shifts severe versus moderate; grant arrives versus fails.</gather>
<walk>Q1 through Q4 proceed cleanly. Q5 keeps "severe floods, no grant" on the board — internally consistent and grim; consistency, never desirability, decides survival. Q6 passes. Q7 merges "insurance premiums rise," reached in three of four tiles. Q8 sets the grant application deadline as the watchpoint. Q9 premortems the fear tile — what made the disaster inevitable was amenities built before defenses — and backcasts from the desired tile. The sequencing rule "flood defenses complete before amenities begin" survives every tile: recommended as robust. Q10 never fires.</walk>
<good-ending>
Two unknowns shape every version of your riverfront: how hard the flood regime shifts, and whether federal money arrives.

In the friendliest telling, moderate floods and a funded grant deliver the full build on schedule. Lose the grant and the same build arrives slower, on bond money alone. Harder floods with federal help stress the defenses early yet leave a district that holds. A fourth telling stays on the board because it is internally consistent, however unwelcome: severe floods, no grant, and every dollar forced to choose between a levee and a lawn.

Insurance premiums rise in three of these four worlds. Negotiate district-level coverage now, whichever future arrives.

The grant application deadline is the hinge. Miss it, and the plan drops a second construction season and rescopes amenities to bond capacity.

Recommendation: sequence the build so flood defenses complete before any amenity breaks ground. A premortem of the fourth telling shows every version of its disaster beginning with amenities first. The rule survives all four worlds — robust — and its cost lands in the gentlest one, where a park waits a season it never strictly needed to.
</good-ending>
<why>Desirability stayed out of plausibility. The unpleasant tile received a premortem instead of quiet deletion, and the sequencing rule it produced holds even in the futures nobody wants.</why>
<counter failure="choice-as-axis">The model makes "we build the levee / we skip the levee" an axis. That places the council's own decision inside the uncertainty table — a strategy to score in Q9, never a fault line for Q3. Axes hold what the actor cannot control; treating a choice as an uncertainty collapses the stress test into a decision matrix that flatters whichever option got a friendlier tile.</counter>
</example>

<example name="trpc-migration">
<request>We're a TypeScript shop and the REST boilerplate is killing us. What if we migrated our API layer to tRPC?</request>
<inferred-task>Read this as an architecture call whose payoff depends on who consumes the API in each future. Treat today's boilerplate pain as real, and ask which tomorrow it gets traded against.</inferred-task>
<gather>Map the components: route handlers, a generated OpenAPI spec, a web client, a mobile client. Record a near-predetermined constraint: two partner integrations consume the REST surface today, so it cannot vanish this year. Check the mobile team's stack by reading their repo or asking — a checkable fact never becomes an axis. Keep two unresolvables: whether partner-facing API business grows beyond the current integrations, and whether internal iteration speed becomes a real bottleneck.</gather>
<walk>At Q1, map the API surface and let the partner contract bound every future. At Q2, verify the mobile stack (TypeScript, shared types already imported — one grep) and move it to the known pile. At Q3, keep both unresolvables; each would change the architecture. At Q4, confirm independence. At Q5, carry all four tiles. At Q7, merge "the OpenAPI spec stays load-bearing," reached in three of four tiles — invest in spec generation whichever future arrives. At Q8, set a watchpoint: a third partner integration entering the sales pipeline before autumn. At Q9, score three moves: a full tRPC migration thrives where the API stays internal and dies where partners multiply; staying on REST survives everywhere and thrives nowhere; "tRPC for internal clients, generated OpenAPI kept at the partner edge" survives all four — recommend it as robust and name its weakest tile. Q10 never fires.</walk>
<good-ending>
Your migration question splits on two unknowns: whether partner-facing API business grows, and whether iteration speed truly becomes your bottleneck.

In *Platform play*, partners multiply while speed binds, a REST surface quietly becomes a product, and a pure tRPC bet dies at a partner's first integration meeting. *Steady partners* rewards contract stability; boilerplate stays annoying and survivable. *Internal engine* inverts the story — partners stall, the boilerplate tax compounds, and a full migration thrives. *Quiet quarter* forgives nearly any choice.

An OpenAPI spec stays load-bearing in three of these four worlds. Invest in generating it from code, whichever arrives.

The hinge: a third partner integration entering the sales pipeline before autumn. Past that point, freeze any REST deprecation and treat the edge as a product surface.

Recommendation: adopt tRPC for internal clients and keep a generated OpenAPI layer at the partner edge. This survives all four worlds — robust. It works hardest in Platform play, where maintaining two surfaces is the price of never having bet wrong.

| Tile | Landings | Full tRPC | Stay REST | tRPC + edge |
| --- | --- | --- | --- | --- |
| Platform play | partners grow, speed binds | dies | survives | survives |
| Steady partners | partners grow, speed fine | dies | thrives | survives |
| Internal engine | partners stall, speed binds | thrives | dies | survives |
| Quiet quarter | partners stall, speed fine | survives | survives | survives |

</good-ending>
<why>A checkable fact stayed a fact instead of becoming an axis, which keeps tile space spent on genuine unknowns — and a merged consequence turned spec generation from a chore into a hedge that pays in every tile.</why>
<counter failure="resolvable-as-axis">A model makes "the mobile team can consume a TS client: yes or no" an axis. One grep of a package.json answers that today, yet half the tile space now simulates a fact — four narratives shrink to two useful ones, and a recommendation hedges against a future that was never uncertain. Ask Q2 honestly to catch this: verify the verifiable, and spend tiles only on what no one can look up.</counter>
</example>

<example name="hardware-holiday-run">
<request>We crowdfunded 4,000 units of our air quality monitor and two retail chains want to talk. Do we commit to a production run of 20,000 units for the holidays? The tariff ruling on our category is still pending and we haven't passed EMC certification yet.</request>
<inferred-task>A sizing decision carrying three unresolved unknowns, not two — the tile geometry follows the questions, never a familiar grid. One combination of landings breaks the calendar, so this tiling also shows genuine kills.</inferred-task>
<gather>Components: the crowdfund batch, the retail channel, the production run, the certification process, the cash on hand. Constraints: cash covers one run; retail shelves need units by October; the 4,000 backers ship first, already promised. Verify the contract manufacturer's quote and the certification lab's queue — both checkable this week. Seven open questions survive the sort, so the walk affords seven tiles. Three unknowns would each change the run: the tariff ruling (rises or holds), retail conversion (purchase orders land big or stay small), and EMC certification (a first pass, or a board respin).</gather>
<walk>Q1 maps the parts; October and the cash that covers one run bound every future. Q2 verifies the quote and the lab queue, leaves three unresolvables, and counts seven open questions — the tile budget. Q3 keeps all three axes; each would resize or retime the run. Q4 checks independence: certification moves on engineering, not markets, and the chains sign on landed cost, so a tariff rise thins margin without deciding the purchase orders. Q5 lays out eight combinations against a budget of seven — and cross-impact kills two: a board respin adds twelve weeks, which blows the October shelf date, so no tile holds "respin" and "big purchase orders" together. Six tiles carry forward, named and storied. Q6 passes. Q7 merges "a second cash source gets drawn" — reached in five of six tiles, so arrange the credit line now, whichever future arrives. Q8 sets three watchpoints: the EMC pre-scan result in three weeks, the ruling's published docket date, and the first purchase order term sheet. Q9 scores three moves: committing the full run now dies in four tiles; staying at 4,000 thrives where orders stay small and dies where they land big; tooling for 20,000 now while releasing material buys at two gates — the pre-scan, then the ruling — survives all six. Robust, weakest tile named, and that weakest tile earns a child walk of its own. Q10 never fires.</walk>
<good-ending>
Your run size splits across three unknowns, and they make six worlds rather than four — a respin cannot share a tile with big purchase orders, because twelve added weeks erase the October shelf date whichever way the tariff lands.

The two respin worlds, *Redraw* and *Hard winter*, are calendar stories: the holidays happen without you, and the question becomes how much cash is still standing in January. The two worlds with big orders, *Green light* and *Thin margin*, differ only in who pays the tariff — in one the run pays for itself, in the other the same run works twice as hard for half the margin. The two remaining worlds, *Slow shelf* and *Headwind*, pass certification cleanly and then wait: inventory moving at crowdfund speed while retail decides whether to care.

Five of these six worlds draw on a second cash source. Open the credit line now, whichever arrives.

Three hinges tell you where you are early: the EMC pre-scan in three weeks predicts pass or respin before tooling money moves; the ruling carries a published docket date; and the first term sheet reveals whether the chains are ordering big or hedging small.

Recommendation: tool for 20,000 now — tooling is the long pole and the smallest check — and release the material buys at two gates, the pre-scan and the ruling. This survives all six worlds. It runs weakest in *Hard winter*, where even gated spending leaves you leaner than never having tooled; that world deserves a walk of its own — enter it with both landings taken as known, and plan January from inside it.

| Tile | Landings | Full run now | Stay at 4,000 | Tool, then gate |
| --- | --- | --- | --- | --- |
| Green light | pass, big orders, tariffs hold | thrives | dies | thrives |
| Thin margin | pass, big orders, tariffs rise | survives | dies | survives |
| Slow shelf | pass, small orders, tariffs hold | dies | thrives | survives |
| Headwind | pass, small orders, tariffs rise | dies | survives | survives |
| Redraw | respin, small orders, tariffs hold | dies | thrives | survives |
| Hard winter | respin, small orders, tariffs rise | dies | survives | survives |

</good-ending>
<why>The geometry followed the questions: seven surfaced, so six tiles fit, and the two kills came from cross-impact — a respin pushing "big orders" toward its alternative — rather than from tidiness. Six worlds stayed tellable by pairing them along the axis that separates their stories.</why>
<counter failure="forcing-the-square">The model drops the certification axis to keep a familiar 2×2 — certification becomes an adjective ("execution risk") instead of a fault line — and the one unknown with a hard calendar consequence never shapes a tile. The recommendation then commits tooling cash three weeks before a pre-scan that was always going to arrive. The tile budget comes from the questions the walk surfaced, never from the shape of a grid seen before.</counter>
</example>
