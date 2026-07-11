---
status: draft
created: 2025-01-11
---

# Skill Boundary Analysis: Thinkies Plugin

Analysis of skill boundaries within the thinkies plugin to identify overlaps, unclear boundaries, and naming confusion.

## Methodology

Examined all 62 skill descriptions across 10 attention layers:

- Observe (4 skills)
- Assess (8 skills)
- Filter (2 skills)
- Lens (5 skills)
- Rotate (4 skills)
- Align (9 skills)
- Integrate (5 skills)
- Traverse (13 skills)
- Anchor (2 skills)
- Engage (8 skills)

Focused on:

1. Skills within same layer with overlapping triggers
2. Skills across layers that might trigger for similar contexts
3. Naming patterns that create confusion
4. Layer placement that doesn't fit taxonomy

---

## CRITICAL OVERLAPS: High Confusion Risk

### 1. traverse-by-branching vs traverse-alternatives

**Issue**: Nearly identical triggers and purposes.

**traverse-by-branching**:

- Trigger: "explore different options," "what are the alternatives," "show me other approaches," "give me multiple paths forward"
- Purpose: Generate multiple viable solutions at decision points

**traverse-alternatives**:

- Trigger: "explore alternative explanations for observations"
- Purpose: Generate plausible alternative explanations before committing to one causal story

**Analysis**: Both generate alternatives. The distinction appears to be:

- `by-branching` = alternative *solutions* (forward-looking)
- `alternatives` = alternative *explanations* (backward-looking causation)

**Problem**: The naming doesn't clarify this. Someone saying "what are the alternatives" could trigger either. The trigger phrases overlap significantly.

**Recommendation**: Either:

- Merge into single skill with both solution-space and explanation-space modes
- Rename `traverse-alternatives` to `traverse-alternative-explanations` to clarify
- Make triggers mutually exclusive (branching = solutions/paths, alternatives = causal explanations only)

---

### 2. trace-logical-justifications vs audit-chain-of-thought

**Issue**: Both verify reasoning chains, unclear distinction.

**trace-logical-justifications**:

- Trigger: "trace the reasoning," "what justifies this claim," "verify the argument," "find unsupported assumptions"
- Purpose: Trace reasoning to identify unsupported assumptions

**audit-chain-of-thought**:

- Trigger: "verify how strong a reasoning chain is"
- Purpose: Tag each step by inference type (deductive, inductive, abductive) to reveal strength

**Analysis**: Both examine reasoning chains for soundness. Distinction:

- `trace-logical-justifications` = finding gaps in justification (missing warrants)
- `audit-chain-of-thought` = classifying inference types to assess strength

**Problem**: "Verify the argument" or "check if this reasoning holds" could trigger either. The functional distinction (gap-finding vs type-classification) isn't clear from triggers.

**Recommendation**:

- Clarify triggers: trace-logical-justifications for "find unsupported claims," audit-chain-of-thought for "classify reasoning types"
- Consider whether these are actually different skills or two approaches to the same operation
- Potentially merge with different execution paths based on what user needs

---

### 3. traverse-through-inference vs trace-logical-justifications vs audit-chain-of-thought

**Issue**: Three-way overlap on examining reasoning chains.

**traverse-through-inference**:

- Trigger: "trace the logic," "show the reasoning," "walk through the steps," "how did you get there"
- Purpose: Make reasoning visible by walking through steps

**Analysis**: Now we have THREE skills for examining reasoning:

- `traverse-through-inference` = make reasoning visible (explanatory)
- `trace-logical-justifications` = find gaps (critical)
- `audit-chain-of-thought` = classify types (analytical)

**Problem**: User says "show me the reasoning" or "trace the logic" - which fires? All three have overlapping triggers.

**Layer confusion**: Two are in Integrate (verification), one is in Traverse (navigation). Is explaining reasoning a traversal through inference-space or an integration verification operation?

**Recommendation**: This is the clearest sign of accidental complexity. Three skills with overlapping triggers in different layers suggest:

- Either the layer taxonomy is unclear here
- Or these should be unified into one skill with multiple modes
- The distinction between "showing reasoning" and "verifying reasoning" may not be skill-level boundary

---

### 4. focus-attention vs map-landscape vs maintain-focus

**Issue**: Three skills about focus with unclear boundaries.

**map-landscape**:

- Trigger: Starting investigation, unsure how to scope it
- Purpose: Map terrain to understand shape and recommend geometry

**focus-attention**:

- Trigger: Exploring without clear question
- Purpose: Detect implicit focus from exploration patterns

**maintain-focus**:

- Trigger: Request to track objectives while exploring tangents
- Purpose: Maintain focus during investigation

**Analysis**: Lifecycle distinction:

- `map-landscape` = before focus exists (scoping)
- `focus-attention` = discover hidden focus (detection)
- `maintain-focus` = maintain known focus (stability)

**Problem**: These are stages of the same cognitive operation (managing focus), separated into different layers. The layer taxonomy (Observe = intake, Assess = sense properties, Anchor = hold position) creates artificial separation of what might be a unified focus-management skill.

**Recommendation**:

- Consider whether "focus management" is actually three distinct operations or one skill with lifecycle stages
- If kept separate, make temporal/lifecycle progression explicit in triggers
- Current naming doesn't make the progression clear

---

### 5. shift-perspective vs inhabit-perspective

**Issue**: Nearly identical names, subtle distinction.

**shift-perspective**:

- Trigger: "multiple stakeholders or viewpoints to consider"
- Purpose: View from multiple vantage points comprehensively

**inhabit-perspective**:

- Trigger: "understand an opposing viewpoint or different frame"
- Purpose: Temporarily inhabit ONE different frame to understand its coherence

**Analysis**: Distinction is quantity (multiple vs singular perspective-taking).

**Problem**: The naming is too similar. Both are "shift-perspective" variations. Someone saying "consider the other perspective" might trigger either.

**Recommendation**:

- Rename: `shift-perspectives` (plural) vs `lens-inhabit-perspective` or `lens-steelman`
- The through/perspective naming pattern doesn't clearly signal "singular deep inhabitation" vs "multiple viewpoint survey"

---

## MODERATE OVERLAPS: Possible Confusion

### 6. argue-opposite vs inhabit-perspective vs synthesize-opposing-views

**Issue**: Three approaches to understanding opposing views.

**argue-opposite**:

- Trigger: "argue the other side," "what's wrong with this," "steelman the opposition"
- Purpose: Test position by arguing against it

**inhabit-perspective**:

- Trigger: "understand an opposing viewpoint"
- Purpose: Inhabit different frame to understand its coherence

**synthesize-opposing-views**:

- Trigger: "opposing positions" that need synthesis
- Purpose: Examine thesis/antithesis to reach synthesis

**Analysis**: Progressive intensification:

- `argue-opposite` = argue against (adversarial)
- `inhabit-perspective` = understand from inside (empathetic)
- `synthesize-opposing-views` = synthesize opposition (integrative)

**Problem**: "Understand the opposing view" could trigger any of these. The progression from adversarial to empathetic to synthetic isn't clear from naming.

**Layer confusion**: Why is adversarial testing in Align (equilibrium) while empathetic understanding is in Lens (outward shaping) and synthesis is in Engage (orchestration)? This suggests the layer taxonomy may not map cleanly to opposition-handling operations.

---

### 7. traverse-by-questioning vs question-through-dialogue

**Issue**: Both use questions as primary method.

**traverse-by-questioning**:

- Trigger: "explore through questions," "what questions should I be asking," "help me brainstorm possibilities"
- Purpose: Open possibility space through curious inquiry before solutions

**question-through-dialogue**:

- Trigger: "examine claims or test reasoning through questions"
- Purpose: Test reasoning through disciplined questioning that reveals assumptions

**Analysis**: Distinction:

- `by-questioning` = generative questioning (opening space)
- `question-through-dialogue` = critical questioning (testing reasoning)

**Problem**: Someone saying "help me think through this with questions" could trigger either. The generative vs critical distinction isn't clear from naming.

**Layer distinction**: Traverse (navigation) vs Engage (orchestration) suggests one is simpler than the other, but both seem to require multi-step orchestration.

---

### 8. traverse-toward-cause vs find-leverage-points

**Issue**: Both seek high-impact intervention points.

**traverse-toward-cause**:

- Trigger: "find the root cause," "why did this happen," "dig deeper"
- Purpose: Find underlying conditions (root cause analysis)

**find-leverage-points**:

- Trigger: "find the leverage point," "where's the bottleneck," "what's the force multiplier"
- Purpose: Identify exceptional ROI opportunities through bottleneck removal

**Analysis**: Related but distinct:

- `toward-cause` = diagnostic (why did this happen)
- `leverage` = strategic (where to intervene for maximum impact)

**Problem**: Root causes often are leverage points. "What's causing this problem and how do we fix it efficiently?" could trigger both.

**Recommendation**: These may need clearer separation in triggers, or recognition that they compose naturally (find cause THEN identify leverage).

---

### 9. traverse-by-depth vs traverse-by-branching

**Issue**: Both explore systematically but different patterns.

**traverse-by-depth**:

- Trigger: "explore systematically," "map out the branches," "cover all aspects," "be thorough"
- Purpose: Systematic coverage of multiple major aspects

**traverse-by-branching**:

- Trigger: "explore different options," "what are the alternatives," "give me multiple paths"
- Purpose: Generate divergent paths at decision points

**Analysis**: Distinction:

- `by-depth` = exhaustive coverage (depth-first or breadth-first)
- `by-branching` = divergent generation (option-space)

**Problem**: "Explore systematically" and "map out branches" could mean either. One is about thoroughness, other is about divergence, but the triggers don't clearly separate.

---

## NAMING PATTERNS: Structural Issues

### 10. Traverse Preposition Inconsistency

The framework claims traverse skills use prepositions to encode strategy:

- `traverse-by-*` = method (branching, questioning, clustering, depth, association, lateral-leap, inversion)
- `traverse-through-*` = terrain (inference, conflict, disclosure)
- `traverse-toward-*` = destination (cause, principles)

**Issue**: Inconsistent application:

- `traverse-alternatives` breaks pattern (no preposition)
- `traverse-abstraction` breaks pattern (should be `traverse-through-abstraction` or `traverse-abstraction-ladder`)

**Recommendation**: Either enforce preposition pattern strictly or abandon it. Current inconsistency creates confusion about whether the pattern is meaningful.

---

### 11. Engage Skill Naming Opacity

Engage skills are described as "multi-layer orchestration" but names don't reveal what they orchestrate:

- `extract-first-principles` - rebuild from fundamentals
- `synthesize-opposing-views` - thesis/antithesis/synthesis
- `integrate-other-perspectives` - reconcile conflicting perspectives
- `question-through-dialogue` - test through questioning
- `systems-thinking` - understand feedback loops
- `plan-scenarios` - test across futures
- `cite-sources` - verify source claims

**Issue**: These span completely different operations:

- Some are reasoning methodologies (first-principles, dialectic, socratic)
- Some are analytical frameworks (systems-thinking, scenario-planning)
- One is a verification operation (cite-sources)
- One is a conflict resolution pattern (integrate)

**Problem**: "Engage" doesn't convey what makes these similar or why they're grouped. The layer definition says "multi-layer orchestration" but that could describe ANY complex skill.

**Recommendation**: Either:

- Define what makes a skill "engage-worthy" (not all multi-step reasoning belongs here)
- Split into subcategories (engage-reasoning-*, engage-framework-*, engage-verification-*)
- Reconsider whether Engage is a real layer or a catch-all for "complex skills"

---

## LAYER PLACEMENT QUESTIONS

### 12. Is integrity a skill or a layer?

**integrity skill**:

- Trigger: "verify, review, or validate information"
- Purpose: Verify structural integrity by aligning evidence with claims
- Layer: Listed in engage-*category but seems like it should be integrate-*

**Issue**: There's an entire Integrate layer for verification operations, but `integrity` is in Engage. The skill description sounds like integrate-* functionality.

**Question**: Is this misplaced, or does "integrity" refer to something broader than the integrate-* verification operations?

---

### 13. Filter layer has only 2 skills

**Current filter skills**:

- `detect-fallacies` - detect logical fallacies
- `premortem` - premortem (imagine failure)

**Issue**: Framework claims Filter is "inward direction, blocking interference" but only two skills exist. Meanwhile:

- Lens has 5 skills (outward shaping)
- Assess has 8 skills (inward sensing)

**Question**: Is Filter under-developed? Should there be more filtering operations? Or is this layer actually rare in practice?

**Candidates for Filter that might be elsewhere**:

- `reconsider` (blocks commitment to wrong path) - currently in Align
- `detect-cycles` (blocks circular reasoning) - currently in Assess

---

### 14. Anchor layer has only 2 skills

**Current anchor skills**:

- `maintain-focus` - maintain focus during investigation
- `build-shared-understanding` - frame as collaborative discovery

**Issue**: Framework describes Anchor as "static direction, hold position" but limited instantiation.

**Question**: Is "holding position" actually rare? Or are there anchor-like operations distributed across other layers?

**Candidates that might be anchor operations**:

- `detect-current-trajectory` (recognize when conversation drifts) - currently in Assess
- Boundary-geometry focus maintenance - not currently a distinct skill

---

## CROSS-LAYER PATTERNS

### 15. Causation/Explanation cluster

Skills about causation and explanation span multiple layers:

**Traverse**:

- `traverse-toward-cause` - find root cause
- `traverse-alternatives` - alternative explanations

**Integrate**:

- `trace-logical-justifications` - verify causal claims
- `flip-assumptions` - test conditionals

**Align**:

- `evaluate-evidence` - verify causal claims vs correlation

**Issue**: Understanding causation requires operations across 3 layers. Is this composition or confusion?

**Analysis**: Possibly appropriate - different operations on same domain:

- Traverse = finding causes
- Integrate = testing causal claims
- Align = distinguishing correlation from causation

But users asking "why did this happen" might need guidance about which operation they're seeking.

---

### 16. Perspective-taking cluster

Skills about viewpoints span multiple layers:

**Lens**:

- `shift-perspective` - multiple viewpoints
- `inhabit-perspective` - inhabit one viewpoint
- `apply-six-hats` - structured perspective rotation

**Align**:

- `argue-opposite` - argue other side

**Engage**:

- `synthesize-opposing-views` - synthesize opposing views
- `integrate-other-perspectives` - reconcile conflicting perspectives

**Issue**: Six skills across three layers all deal with perspectives/viewpoints. The boundaries between "viewing through lens" vs "arguing the opposition" vs "engaging with dialectic" aren't crisp.

---

## SYNTHESIS: Patterns of Accidental Complexity

### Pattern 1: Lifecycle Separation

Related operations separated into different layers because they represent lifecycle stages:

- Focus management: map-landscape → focus-attention → maintain-focus
- Opposition handling: argue-opposite → examine-viewpoints → synthesize-opposing-views
- Reasoning verification: traverse-through-inference → trace-logical-justifications → audit-chain-of-thought

**Question**: Should lifecycle progressions be:

- Single skills with stages?
- Separate skills with explicit lifecycle relationships?
- Current approach (separate skills, implicit relationships)?

---

### Pattern 2: Method vs Domain Confusion

Some skills are named by method (socratic, dialectic, first-principles), others by domain (causation, explanation, perspective). This creates taxonomic inconsistency.

---

### Pattern 3: Granularity Inconsistency

Some skills are atomic operations:

- `detect-fallacies` - pattern match against known fallacies

Others are complex orchestrations:

- `systems-thinking` - understand feedback loops and emergence
- `synthesize-opposing-views` - thesis/antithesis/synthesis progression

The granularity difference is 2+ orders of magnitude but both are "skills."

---

### Pattern 4: Underspecified Layers

Filter (2 skills) and Anchor (2 skills) suggest either:

- These layers are genuinely rare in practice
- The layer definitions are unclear so skills aren't being placed there
- Operations that belong here are scattered across other layers

---

## RECOMMENDATIONS

### High Priority (Clear Overlaps)

1. **Merge or clarify traverse-by-branching vs traverse-alternatives**
   - Current state: Overlapping triggers, unclear boundary
   - Options: Merge, or rename alternatives to traverse-alternative-explanations

2. **Consolidate reasoning-chain verification (3 skills)**
   - traverse-through-inference, trace-logical-justifications, audit-chain-of-thought
   - Current state: Three overlapping approaches across two layers
   - Options: Single skill with modes, or make triggers completely distinct

3. **Rename shift-perspective vs inhabit-perspective**
   - Current state: Too similar, quantity difference not clear
   - Options: shift-perspectives vs lens-inhabit-perspective

### Medium Priority (Moderate Confusion)

1. **Clarify opposition-handling progression**
   - argue-opposite → examine-viewpoints → synthesize-opposing-views
   - Document as composition pattern, make triggers distinct

2. **Enforce or abandon traverse preposition pattern**
   - Fix: traverse-alternatives, traverse-abstraction
   - Or abandon if pattern isn't meaningful

3. **Review Engage layer definition**
   - Skills span completely different operations
   - Either tighten definition or split into subcategories

### Low Priority (Structural Questions)

1. **Audit layer placement**
   - Is integrity in wrong layer?
   - Should some assess-*or align-* skills be filter-*or anchor-*?

2. **Investigate underspecified layers**
   - Why do Filter and Anchor have only 2 skills each?
   - Are operations missing or is the layer taxonomy unclear?

---

## IMPLICATIONS FOR SKILL DISCOVERY

The overlaps and unclear boundaries create three problems for skill discovery:

### 1. Trigger Ambiguity

When user says "explore alternatives" or "verify this reasoning," multiple skills might match. Without clear differentiation, skill selection becomes arbitrary.

### 2. Layer Taxonomy Questions

The attention layer framework claims to provide clear operational positions, but:

- Lifecycle progressions span multiple layers
- Similar operations appear in different layers
- Some layers are heavily populated, others sparse

This suggests either:

- The taxonomy doesn't match actual operation patterns
- Layer boundaries need refinement
- Skills need reclassification

### 3. Granularity Inconsistency

Some skills are atomic operations, others are complex orchestrations. This makes it unclear:

- When to invoke vs compose
- What counts as a "skill" vs a "command" vs a "technique"
- How skills should relate to each other

---

## QUESTIONS FOR HUMAN JUDGMENT

1. **Merge philosophy**: Should overlapping skills be merged into single skills with modes, or kept separate with clearer boundaries?

2. **Layer taxonomy**: Is the 10-layer framework helping or hindering skill organization? Should it be revised based on actual skill distribution?

3. **Granularity standard**: Should there be minimum/maximum complexity for skills? Should complex orchestrations become commands instead?

4. **Naming consistency**: Should all traverse skills follow preposition patterns? Should all engage skills follow naming conventions?

5. **Lifecycle handling**: How should lifecycle progressions (observe → assess → anchor focus) be represented? Single skills, explicit relationships, or current implicit approach?
