# /research Testing Specification

Testing strategy for the `/research` command, emphasizing chaos engineering for coordination validation.

## Related Documentation

- `specs/RESEARCH-functional.md` — Functional specification

## Testing Philosophy

The core insight from prerelease harvest: **test via deliberate failure (chaos engineering)** validates both persistence and coordination simultaneously. Rather than only testing that coordination works, test recovery when it doesn't.

## Test Phases

### Phase 1: Foundation (Start Here)

Before testing coordination, establish the infrastructure:

| Test | Purpose | Implementation |
|------|---------|----------------|
| Isolated PATCH environments | Prevent test interference | Use `createTestContext()` per test |
| Basic PATCH lifecycle | Create → use → cleanup | Integration test with assertions |
| Single-agent coordination | Spawn → receive → cleanup | Verify Task tool round-trip |
| Property-based invariants | Establish test oracle | Define invariants for all tests |

**Key invariants to establish**:

- PATCH directories cleaned up after research completes
- STRAND integrity maintained across phase transitions
- No orphaned state after any execution path
- Gap summary always reflects actual claim/evidence state

### Phase 2: Failure Scenarios (Chaos Engineering)

Test recovery when things go wrong:

| Scenario | Injection Method | Expected Behavior |
|----------|------------------|-------------------|
| Message corruption | Mutate state.yaml mid-phase | Detect corruption, halt with clear error |
| Partial cleanup | Kill cleanup before completion | Subsequent run completes cleanup |
| Agent timeout | Inject delay beyond timeout | Orchestrator recovers, state preserved |
| Concurrent access | Parallel agents write to STRAND | Serialization prevents corruption |
| Orchestrator death | Kill orchestrator randomly | Reconstruct research from STRAND alone |
| Resource leak | Complete N runs, check for orphans | Zero orphaned directories/processes |

**The critical test**: Kill orchestrator at random points, then verify research can be reconstructed from persisted STRAND state alone. This validates both persistence completeness AND coordination recovery.

### Phase 3: Observability

Enable debugging for multi-agent interactions:

| Capability | Implementation |
|------------|----------------|
| Structured logging | JSON logs with correlation IDs across agents |
| Replay capability | Record/playback coordination sequences |
| STRAND visualization | Graph representation of narrative threading |
| State diff tracking | Before/after comparison at phase boundaries |

## Mode-Specific Testing

### Quick Mode Validation

Quick mode must preserve integrity while reducing scope:

| Requirement | Test |
|-------------|------|
| Beliefs surfaced before evidence | Verify Phase 1 completes before Phase 2 starts |
| Sources cited with quality notes | Check output structure includes citations |
| Confidence calibration present | Verify confidence values in synthesis |
| Gap visibility in output | Check gap_summary populated correctly |

**Calibration testing challenge**: Optimal thresholds require real-world usage data. For now, verify the mechanism works; tune thresholds post-launch.

### Standard Mode Integration

Full 5-phase integration with human checkpoints:

| Checkpoint | Test |
|------------|------|
| After Phase 3 | Verify orchestrator pauses for user input |
| State preservation | Confirm full state available at checkpoint |
| Continuation | Verify research resumes correctly after approval |

### Deep Mode Continuation

Multi-session research across context boundaries:

| Requirement | Test |
|-------------|------|
| Working memory persistence | State survives session end |
| Context reconstruction | New session loads prior state correctly |
| Reconciliation sub-agents | All 4 sub-phases execute in sequence |
| Cross-session gap tracking | Confidence trajectory preserved |

## State Transfer Testing

Each phase receives accumulated state from prior phases:

```yaml
# Test fixtures needed:
phase_1_output:
  beliefs:
    prior_expectations: [...]
    confidence_before_evidence: 0.7

phase_2_output:
  evidence:
    sources_cited: [...]
    gaps_identified: [...]

# Verify each phase can:
# 1. Parse prior phase output
# 2. Add its own output
# 3. Pass accumulated state forward
# 4. Handle malformed input gracefully
```

**Working memory as research quality infrastructure**:

- Beyond save/resume: capture source relationship graphs, not flat lists
- Include quality metadata: diversity scores, coverage gaps, confidence levels
- Enable mid-research reflection: "Here's what you have, here's what's missing"

## Property-Based Testing

Define properties that should hold across all executions:

```typescript
// Invariant: Gap summary reflects reality
property("gap_summary_accurate", (research) => {
  const claims = countClaims(research.synthesis);
  const supported = countSupported(research.reconciliation);
  return research.gap_summary.claims_made === claims &&
         research.gap_summary.claims_supported === supported;
});

// Invariant: Confidence trajectory is monotonic within phase
property("confidence_within_phase", (research) => {
  // Confidence can go up or down between phases
  // But within a phase, trajectory should be stable or improving
});

// Invariant: No information loss across handoffs
property("state_preserved", (phase_n, phase_n_plus_1) => {
  // All prior phase data accessible in subsequent phases
  return contains(phase_n_plus_1.state, phase_n.output);
});
```

## Parallel Workstreams

Tests that can proceed without full coordination:

| Workstream | Focus | Dependencies |
|------------|-------|--------------|
| Quick mode unit tests | Path selection logic | None |
| Working memory schema | Design validation | None |
| Confidence calibration | Framework design | None |
| State serialization | Completeness checks | Schema only |

## Test Infrastructure Needs

| Need | Purpose |
|------|---------|
| Mock switchboard | Isolated coordination testing |
| State snapshot/restore | Reproducible test scenarios |
| Agent stub | Controlled agent responses |
| Timing control | Deterministic timeout testing |

## Success Criteria

Release-ready when:

- [ ] All Phase 1 foundation tests pass
- [ ] At least 3 chaos engineering scenarios pass
- [ ] Quick mode end-to-end works
- [ ] Standard mode completes with human checkpoint
- [ ] No resource leaks detected in 10 consecutive runs
- [ ] State reconstruction from STRAND succeeds after orchestrator kill

## Open Questions

1. **How minimal is minimal?** Quick mode calibration needs usage patterns
2. **What's the replay format?** For debugging multi-agent interactions
3. **How to test human checkpoints?** Mock user input or integration test with prompts?
