# RFC: Discourse Resume Capability

## Status

Draft

## Context

Discourse sessions orchestrate multi-perspective dialogues through isolated agents. Each agent embodies a distinct epistemic framework (empiricism, constructivism, pragmatism, etc.) and engages with others through blocking turn-taking scripts. This architecture produces genuine perspective collision rather than blended synthesis.

However, discourse is currently ephemeral:

- Sessions end via round limit, user interrupt, or natural conclusion
- No mechanism to continue where participants left off
- No way to add new perspectives to an existing dialogue
- Ad-hoc personas aren't persisted, making faithful resume impossible

When a productive dialogue is interrupted—by time constraints, context limits, or the need to reflect—the conversation is lost. The same participants could be re-instantiated, but without memory of what was said.

This RFC proposes resume and extend capabilities for discourse sessions.

## Goals

1. **Resume**: Continue a dialogue with the same participants, preserving full context
2. **Extend**: Add new perspectives to an existing dialogue
3. **Preserve fidelity**: Resumed dialogues faithfully continue the original personas
4. **Maintain simplicity**: Scripts stay simple; orchestrator handles workflow complexity

## Non-Goals

- Modifying historical turns (dialogue history is append-only)
- Removing participants (only adding is supported)
- Real-time collaborative editing of personas

---

## Operations

### `--resume`

Continue an existing dialogue with the same participants.

```bash
discourse-session.ts --resume \
  --dialogue-id "api-design-2025-12-21" \
  [--rounds N]
```

**Behavior**:

1. Load dialogue from `.thinkies/.dialogues/{id}.yaml`
2. Extract persona IDs from `data.participants[].persona_id`
3. Lookup each persona from `.thinkies/.personas/{id}.yaml`
4. Calculate remaining rounds (see Round Calculation)
5. Create new PATCH for coordination
6. Return structured output:

```yaml
patch_id: "835eeb54-97ca-4180-ab29-ce27745f8933"
dialogue_id: "api-design-2025-12-21"
topic: "API versioning strategy"
remaining_rounds: null  # unlimited
first_speaker: "pragmatist"

personas:
  - persona_id: "pragmatist"
    expertise_domain: "..."
    epistemic_framework: "pragmatism"
    # ... full definition

turns:
  - turn_number: 1
    persona_id: "purist"
    content: "..."
  # ... prior history
```

### `--extend`

Add a new perspective to an existing dialogue.

```bash
discourse-session.ts --extend \
  --dialogue-id "api-design-2025-12-21" \
  --add-persona "security-architect"
```

**Behavior**:

1. Load dialogue
2. Verify persona exists in `.thinkies/.personas/`
3. Add persona ID to `data.participants`
4. Update dialogue file
5. Create new PATCH
6. Return structured output with all participants' persona definitions

---

## Schema Changes

### Dialogue Data

Add fields to support resume:

```yaml
data:
  topic: "API versioning strategy"
  participants:
    - persona_id: "pragmatist"
      role: "participant"
    - persona_id: "purist"
      role: "participant"
  turns: [...]
  status: "active"

  # NEW: Resume support
  max_rounds: 3
  completed_rounds: 3
  session_history:
    - patch_id: "835eeb54-..."
      started: "2025-12-21T20:36:02Z"
      ended: "2025-12-21T20:38:00Z"
      rounds_completed: 3
```

### TypeScript Types

```typescript
interface DialogueData {
  topic: string;
  participants: DialogueParticipant[];
  turns: DialogueTurn[];
  status: 'active' | 'completed';
  insights: string[];

  // Resume support
  max_rounds: number | null;
  completed_rounds: number;
  session_history: SessionRecord[];
}

interface SessionRecord {
  patch_id: string;
  started: string;
  ended: string | null;
  rounds_completed: number;
}
```

---

## Round Calculation

```typescript
function calculateRemainingRounds(
  maxRounds: number | null,
  completedRounds: number,
  explicitRounds?: number
): number | null {
  // Explicit override takes precedence
  if (explicitRounds !== undefined) {
    return explicitRounds;
  }

  // No original limit → unlimited
  if (maxRounds === null) {
    return null;
  }

  // Calculate remaining
  const remaining = maxRounds - completedRounds;

  // If exhausted, go unlimited (they asked for more)
  if (remaining <= 0) {
    return null;
  }

  return remaining;
}
```

**Rationale**: When someone resumes an exhausted dialogue, they explicitly want more. Going unlimited honors that intent rather than blocking with "no rounds remaining."

---

## First Speaker Selection

```typescript
function determineFirstSpeaker(
  participants: DialogueParticipant[],
  turns: DialogueTurn[]
): string {
  if (turns.length === 0) {
    return participants[0].persona_id;
  }

  const lastTurn = turns[turns.length - 1];
  const other = participants.find(p =>
    p.persona_id !== lastTurn.persona_id
  );
  return other?.persona_id ?? participants[0].persona_id;
}
```

---

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Dialogue not found | Exit 1: "Dialogue {id} not found" |
| Persona not found | Exit 1: "Persona {id} not found in .thinkies/.personas/" |
| Dialogue already active | Warning, allow resume anyway |

---

## Output Format

Human-readable header with YAML body:

```
═══════════════════════════════════════════════════════════════
  DISCOURSE SESSION RESUMED
───────────────────────────────────────────────────────────────
  Patch ID:     835eeb54-97ca-4180-ab29-ce27745f8933
  Dialogue ID:  api-design-2025-12-21
  Prior Turns:  6
  Remaining:    unlimited
  First:        pragmatist
═══════════════════════════════════════════════════════════════

patch_id: "835eeb54-97ca-4180-ab29-ce27745f8933"
dialogue_id: "api-design-2025-12-21"
topic: "API versioning strategy"
...
```

---

## Files Modified

| File | Change |
|------|--------|
| `plugins/switchboard/scripts/discourse-session.ts` | Add `--resume`, `--extend` |
| `plugins/switchboard/lib/discourse-types.ts` | Add `SessionRecord`, update `DialogueData` |
| `plugins/switchboard/commands/discourse.md` | Document new operations |

---

## Testing

```bash
# Initialize with saved personas
bun discourse-session.ts --init \
  --topic "test" \
  --participants "empirical-researcher,systems-thinker" \
  --max-rounds 2

# [Run 2 rounds]

# Resume (should be unlimited since 2/2 completed)
bun discourse-session.ts --resume \
  --dialogue-id "test-2025-12-21"

# Extend with new perspective
bun discourse-session.ts --extend \
  --dialogue-id "test-2025-12-21" \
  --add-persona "critical-evaluator"
```

---

## Open Questions

1. **Persona drift**: If a persona definition is modified between sessions, continued dialogue may be inconsistent. Should we snapshot persona definitions in the dialogue file?

2. **Session boundaries**: Should turns from different sessions be visually distinguished in the dialogue file?

3. **Extend dynamics**: When adding a new perspective, how is it introduced to the existing participants? Cold start or warm introduction?
