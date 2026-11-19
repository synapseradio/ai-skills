---
name: run-premortem
description: Use before carrying out a plan, launch, or change that would be costly to get wrong. Imagines it has already failed badly and works backward to the causes, so the dangerous ones get addressed while the plan can still change.
---

The subject is the plan or decision named in the request, or the one the conversation is about to act on.

## Steps

### 1. Assume failure

Assume the plan has already been implemented and failed catastrophically. Write the headline.

### 2. Work backwards

From the headline, trace back what went wrong, one event leading to the next.

### 3. Generate failure modes

List failure modes across technical, human, process, external, and timing dimensions. Include the unlikely and the embarrassing; step 6 does the filtering.

### 4. Surface hidden assumptions

Name what the plan took for granted and the dependencies it never listed.

### 5. Group by theme

Group the failure modes by the cause they share.

### 6. Find the unaddressed

Check each theme against what the current plan already covers, and name the ones it does not address.

### 7. Design interventions

Design interventions for the most dangerous of those: the ones that would do the most harm and that nothing in the plan would catch. An intervention changes the plan, or names a signal to watch and the action it triggers.

## Return

Return the headline, the failure modes by theme, the hidden assumptions, the themes the plan leaves unaddressed, and the interventions. The run ends when each of the most dangerous unaddressed themes has an intervention.
