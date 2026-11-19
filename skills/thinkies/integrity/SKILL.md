---
name: integrity
description: Use as the full final check on a response, report, or other output before it is relied on. Verifies that every claim in it is backed by what supports it, and reports which claims hold, which need attention, and what stays assumed.
---

## Steps

### 1. Identify the target

Target: `$ARGUMENTS`, else the current response or most recent significant output.

The target is always text on the page: an artifact the request names, the reply as written, or a document in hand. A run that starts with no earlier output, such as a subagent handed only this skill, takes the artifact its request names. With no artifact to check, ask for one and stop.

### 2. Apply the verification lenses

1. **Inventory**: separate established claims from assumptions
2. **Dissection**: trace support chains to bedrock or mark as floating
3. **Pattern**: check for epistemic weaknesses and biases
4. **Calibration**: match confidence to evidence
5. **Resolution**: align claims with what supports them

For each claim: trace its justification chain, identify hidden premises, check for fallacies, hunt for defeaters, and verify cited sources.

### 3. Report

```markdown
## Verification Summary

### Claims Verified
- [Claim]: [Support basis]

### Claims Requiring Attention
- [Claim]: [Issue identified]

### Acknowledged Uncertainty
- [What remains unknown or assumed]
```

The summary is for a person to assess. It shows what each claim rests on so they can check it, and it does not certify the artifact as correct. If significant issues are found, offer to revise the artifact with corrections applied. In a run with no one to offer to, give each correction beside its claim under Claims Requiring Attention and leave the artifact unchanged.

The run is done when every claim in the artifact sits under one of the three headings.
