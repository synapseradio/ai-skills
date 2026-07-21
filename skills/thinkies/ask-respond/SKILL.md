---
name: ask-respond
description: Structured Q&A that decomposes questions before answering
---

Follow these steps:

### 1. Mirror the question

Restate the question from `$ARGUMENTS` in the assistant's first-person point of view.

- "how do you feel?" → "how do I feel?"
- "what day is it?" → "what day is it?"

### 2. Decompose the question

Break it into component parts at natural joints. Identify what is actually being asked, what assumptions are embedded, and what sub-questions must be answered first. Consider it in context of the current conversation.

### 3. Assess current knowledge

For each component, map known vs assumed vs unknown by source:

- Direct observation from context
- Documentation or authoritative sources
- Inference from related facts
- Assumption without evidence

Separate verified facts from inferences and acknowledge gaps explicitly.

### 4. Respond

Answer calibrated to the evidence available.

### 5. Propose next action

If the question implies a request for action, propose a course of action or further inquiry, then ask permission to proceed.
