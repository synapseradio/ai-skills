# Bridge

Connect unfamiliar concepts to familiar ones through structural analogy.

## Diagnostic Question

Ask: What unfamiliar concepts appear without anchoring to the familiar?
What structural analogies could make the strange accessible? Where could comparison to familiar experience illuminate the new?

## Instructions

1. **Identify what needs bridging** - Examine what the audience doesn't understand. Is it an invisible process, abstract relationship, technical mechanism, or non-intuitive behavior?

2. **Find familiar territory** - Search for experiences the audience already has that share structural similarities. Draw from physical systems, social situations, routine activities, or natural phenomena they navigate intuitively.

3. **Map relationships, not features** - Match how elements relate in both domains rather than whether components look similar. Focus on cause-effect chains, functional roles, interaction patterns, constraints, and dependencies.

4. **Make the mapping explicit** - Explain which parts of the familiar domain correspond to which parts of the unfamiliar concept. Walk through the analogy step by step rather than assuming inference.

5. **Acknowledge where bridges end** - Identify and state where the analogy breaks down, what aspects don't map cleanly, and what conclusions it might suggest that aren't valid.

6. **Build multiple bridges when needed** - Use different analogies for different aspects of complex concepts when a single analogy can't capture all important relationships.

7. **Refine progressively** - Start with the simplest version that captures the core relationship, then add nuance and detail as understanding develops.

## Examples

### Explaining API endpoints to non-technical stakeholders

**Bridge to restaurant service**:

"An API endpoint works like a restaurant waiter. When you want something from the kitchen, you don't go into the kitchen yourself. You tell the waiter what you want from the menu, they take your order to the kitchen, the kitchen prepares it, and the waiter brings back what you requested."

**Explicit mapping**:

- Customer → our application
- Waiter → API endpoint
- Kitchen → external service
- Menu → API documentation
- Placing order → making API call
- Receiving food → getting response

**Where bridge ends**: Unlike a waiter who might interpret vague requests, APIs require precise formatting.

**What bridge teaches**: Why we can't "get the data directly" and why API documentation matters—you need to order from the menu.

### Explaining Git branching to collaborators new to version control

**Bridge to document editing**:

"A Git branch is like making a copy of a shared document to propose changes. You make a copy, edit your copy however you want, then show the changes to the team for review. While you're editing, others can edit their own copies independently. Eventually, you compare versions, discuss changes, and merge the good parts back."

**Explicit mapping**:

- Main branch → canonical document
- Creating branch → making copy for proposed changes
- Commits → saving versions of edits
- Merging → incorporating accepted changes

**Where bridge ends**: Unlike document copies, Git merge requires reconciling line-by-line changes, and branches maintain connection to original.

**What bridge teaches**: Why branches enable parallel work, why you need to "merge" rather than just replace, why merge conflicts happen when two people edit same section.

### Explaining database indexing

**Bridge to book index**:

"A database index works like the index in the back of a textbook. Without an index, finding information about a specific topic means reading through every page. With an index, you look up the topic alphabetically, find the page numbers, and jump directly there."

**Extend for write cost**: "Every time you add or change content in the book, you need to update the index. That's why writes are slower with indexes. If you indexed every word, finding anything would be instant, but updating the index would take forever."

**Where bridge ends**: Book indexes are manually created; database indexes maintain themselves automatically.

**What bridge teaches**: Why we can't index everything, why certain columns benefit more, why the planner might not use an index for small tables.

### Explaining async programming to synchronous thinkers

**Bridge to kitchen operations**:

"Synchronous cooking: completely finish one dish before starting the next. Asynchronous cooking: start tasks that take time, then work on other things while waiting. Put rice on to cook, and while it's cooking, prep vegetables. You don't stand watching the rice."

**Explicit mapping**:

- Synchronous code → single-task cooking
- Async operations → tasks you start and check on later
- Await → checking whether task is done
- Callbacks/promises → reminders when to return to task

**Where bridge ends**: Code doesn't have physical constraints like stove burners—you can have thousands of async operations.

**What bridge teaches**: Why async isn't "running in parallel" but rather "not blocking while waiting," why you can't treat async functions like synchronous ones—you can't serve rice before it's cooked.
