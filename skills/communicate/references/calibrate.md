# Calibrate

Adjust explanation depth, terminology, and examples to match audience knowledge.

## Diagnostic Question

Ask: What does this audience already know?
Where does depth exceed or fall short of their preparation? What technical vocabulary assumes expertise? What simplifications condescend?

## Instructions

1. **Gauge existing knowledge** - Examine their questions, vocabulary, what they take for granted, and what context they provide or omit. Let their words guide the assessment, not their role or credentials.

2. **Match terminology to familiarity** - Use technical terms when they've shown comfort with them, but explain jargon when they haven't encountered it yet. Match their language rather than correcting it.

3. **Adjust detail based on need** - Give minimal context for quick answers to specific questions. Provide deeper foundations when learning a new domain. Layer detail so initial explanations are accurate though incomplete.

4. **Choose examples from their context** - Use domain-familiar analogies when working within that field. Draw from everyday experience when crossing into new territory. Pick examples that match their stated goals.

5. **Align with their goals** - Shape explanations around what they're trying to accomplish rather than providing complete coverage. Emphasize aspects that matter for their specific situation.

6. **Watch for calibration signals** - Notice confusion about concepts assumed clear, or impatience with explanations of things they already understand. Treat these as feedback to recalibrate.

## Examples

### Expert vs newcomer in same domain

**Expert question**: "Should I use a B-tree or hash index for this timestamp range query?"

They've demonstrated understanding of index types, query patterns, and tradeoffs. Respond at that level:

"B-tree indexes support range queries efficiently through ordered traversal, while hash indexes optimize exact-match lookups but can't handle ranges. For timestamp ranges, B-tree gives you the range scanning you need."

**Newcomer question**: "Why is my query slow?"

They haven't signaled awareness of indexing. Recalibrate:

"Queries search through data to find matches. Without an index, the database checks every row, which gets slow as data grows. An index is like a book's table of contents—it helps find data quickly by maintaining a sorted reference structure. Your timestamp query might benefit from indexing the timestamp column."

Same underlying concept, different starting points.

### Cross-domain explanation

**Product manager asks**: "Why will the API redesign take three weeks?"

They're asking about timeline, not implementation details. Their question doesn't include technical vocabulary. Calibrate to business goals:

"We need to maintain the current API while building the new one, then migrate clients gradually. If we switch directly, every integration breaks at once. The timeline covers building the new version, running both in parallel, and migrating clients one at a time so we can catch issues before they affect everyone."

**Backend engineer asks the same question**:

"We're implementing parallel versioning with header-based routing, maintaining v1 endpoints while shipping v2 alongside. Migration involves client-by-client rollout with feature flagging so we can revert quickly if integrations break."

Same timeline, same decision, terminology and detail matched to audience.

### Mixed audience with different needs

Explaining architecture change to engineers, support staff, and executives:

**Core fact** (accessible to all): "We're splitting the monolith into separate services."

**Business value** (for executives): "This lets us scale order processing independently during traffic spikes without scaling everything else."

**Operational impact** (for support): "Order status queries will hit a different system than user account queries, but you'll still have a unified dashboard."

**Technical detail** (for engineers): "We're extracting orders and inventory into their own services with event-driven communication. Each service owns its database. We're using Kafka for async events and REST for synchronous queries."

Each layer adds specificity without invalidating what came before.

### Recalibration based on feedback

I explain: "Check the database query execution plan to see if indexes are being used."

They respond: "What's an execution plan?"

I misjudged their starting point. Recalibrate:

"When a database runs a query, it decides how to find the data—scan everything or use indexes to narrow down quickly. An execution plan shows that decision. Let me show you how to see it."

If instead they'd responded with execution plan output asking "Why is this doing a sequential scan?", my calibration was correct—continue at that technical level.
