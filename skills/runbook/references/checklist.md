# Alignment Checklist

Validate after convergence is detected, before seeding. Present each gate
to the user with pass/fail status.

## Gates

### 1. Lens defined

A clear, singular focus for what the loop discovers and fixes.

- **Pass:** Can state the lens in one sentence. Example: "Security hardening
  against injection and temp file vulnerabilities."
- **Fail:** Lens is vague ("make the code better") or tries to cover
  multiple unrelated concerns.

### 2. Authority cited

A concrete reference the loop consults during discovery.

- **Pass:** Named source — a style guide URL, a PRD file path, a design
  spec, an RFC, or "the codebase's own conventions documented in X."
- **Fail:** No reference, or "best practices" without specifics.

### 3. Scope bounded

Explicit boundaries on what the loop touches.

- **Pass:** Named directories, file patterns, or areas. Both inclusions
  and exclusions are stated.
- **Fail:** "The whole codebase" with no exclusions, or scope is unstated.

### 4. Success criteria set

A concrete definition of "done" that the loop can evaluate.

- **Pass:** Observable condition. Examples: "Two consecutive clean audit
  rounds." "All items in the PRD marked complete." "Test coverage above 80%
  in lib/."
- **Fail:** Open-ended ("keep improving") or subjective ("code feels clean").

### 5. Mode chosen

Tight loop (default) or recursive decomposition.

- **Pass:** Explicitly chosen, with rationale if recursive.
- **Fail (soft):** Not discussed. Default to tight loop and note the assumption.

### 6. No conflicting constraints

Elements do not contradict each other.

- **Pass:** Scope, lens, and authority are compatible. Success criteria
  are achievable within the stated scope.
- **Fail:** Example: lens says "performance optimization" but scope excludes
  the hot paths. Surface the conflict and resolve with the user.

### 7. Optional sections validated (if present)

Convergence, Principles, and Model sections are optional. If the user
provided them during alignment, validate they are well-formed.

- **Convergence:** Must be evaluable by the loop (not subjective).
- **Principles:** Each principle must be a concrete constraint, not a wish.
- **Model:** Default tier should match the loop's typical cognitive demand.
- **Pass (soft):** Omitted sections use defaults. Note the assumptions.

## Presentation

Show the checklist as a compact summary:

```
Alignment checklist:
  [x] Lens: Security hardening — injection and input validation
  [x] Authority: OWASP cheat sheets + project style guide at docs/style.md
  [x] Scope: lib/ and src/ only (excluding vendor/, generated/)
  [x] Success: Two consecutive clean audit rounds
  [x] Mode: Tight loop
  [x] No conflicts detected
  [x] Optional: Convergence set, Principles set, Model defaults to contextual

Ready to seed. Confirm?
```

If any gate fails, state what's missing and return to alignment conversation
to resolve it. Do not proceed to seeding with failed gates.
