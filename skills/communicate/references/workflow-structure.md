# Structure Workflow

Rhetorical tradition adaptation. Not editing. Not translation. Not grammar correction. Prose can be grammatically flawless in English and still fail to communicate — not because the words are wrong but because the argument's structure operates in a different rhetorical tradition than the target audience expects. Arabic parallel-restatement reads as repetitive to Anglo-American audiences. French dialectical structure reads as evasive. Japanese indirection reads as unclear. The problem is rhetorical convention. This workflow adapts argument structure to function within the target tradition without altering content.

## What This Workflow Is Not

Not grammar correction — the prose is already correct.
Not stylistic improvement — the Clarify and Redraft workflows handle that.
Not translation — the prose is already in the target language.

It is: making the argument's structure work in a different rhetorical tradition. The scope is structural adaptation across traditions — organization, positional conventions, explicitness calibration — while content, voice, and vocabulary remain untouched.

## When to Use This Workflow

- Prose is correct but feels "foreign" to its intended audience
- The audience has different organizational expectations than the tradition the prose was written in
- Moving between rhetorical traditions (Arabic to Anglo-American, French to US business, Japanese academic to international conference, German scholarly to general readership)
- A reader says "I can't follow this" about prose that follows a coherent non-Anglo organizational logic

## NEVER

1. **Never treat the source tradition as deficient.** The source prose operates within a coherent rhetorical system. Adaptation is not correction. Name the source tradition's logic before proposing changes.
2. **Never silently normalize to Anglo-American English.** Annotate every significant structural adaptation. "I changed X to Y" must be accompanied by "X was doing Z in your tradition; Y does the equivalent in the target tradition."
3. **Never adapt content along with structure.** Scope is enforced: structure only. If the user's ideas change in the adaptation, that is a failure. What is claimed must survive intact; how it is organized may change.
4. **Never assume the user wants full adaptation.** Always offer the "explain the original structure" option. Sometimes preserving the rhetorical tradition with a framing note is stronger than adapting away from it.
5. **Never adapt voice, vocabulary, or specific word choices** unless explicitly requested. This workflow operates on argument architecture, not surface expression.

## Phase 1: Identify Source Tradition

Analyze the existing prose to identify what rhetorical tradition produced it.

Load: `@./references/tradition.md`

Signals to examine:

- **Organizational logic** — Linear progression (Anglo-American), parallel/associative (Arabic/Semitic), dialectical thesis-antithesis-synthesis (French), indirect approach building to implication (Japanese), extended scaffolding with delayed thesis (German academic), circular/spiral (oral traditions)
- **Epistemic conventions** — Direct assertion vs. nuanced hedging vs. thorough qualification before commitment
- **High-context vs. low-context** — What is made explicit vs. what the reader is trusted to supply
- **Positional conventions** — How the writer positions relative to subject: removed observer, embedded participant, dialectical examiner, accumulated authority

If the tradition is unclear, state what signals are present and ask the user for confirmation before proceeding.

## Phase 2: Identify Target Tradition

The user specifies or implies the target audience. If not explicit, ask:

- Who is the primary audience for this in its new form?
- What country or professional context?
- What communication norms does that context carry?

Load: `@./references/calibrate.md`

Map the target audience to its expected rhetorical conventions. Professional context matters: US academic writing differs from US business writing, which differs from US journalism. Identify the specific register, not just the national tradition. Load fit to check whether the prose's form matches its function in the target tradition — adaptation that preserves content but misaligns form and purpose has not finished the job.

Load: `@./references/fit.md`

## Phase 3: Map Divergence

Identify the specific structural differences between source and target tradition that require adaptation. Use these five dimensions:

| Dimension | What to Compare |
|-----------|----------------|
| **Organization** | Parallel/circular vs. linear-deductive; associative vs. hierarchical; delayed thesis vs. thesis-first |
| **Position-taking** | Dialectical (hold contradiction first) vs. thesis-first; accumulated authority vs. stated upfront |
| **Explicitness** | High-context (implied, reader supplies) vs. low-context (stated, writer supplies) |
| **Certainty** | Hedged/graduated commitment vs. assertive/direct claims |
| **Elaboration** | Extended scaffolding, parallel restatement, accumulative persuasion vs. economical, hierarchical evidence |

For each dimension where source and target diverge: name what the source tradition is doing, name what the target tradition expects, and assess the cost of adaptation.

## Phase 4: Adapt

Transform the structure to function within the target tradition. Enforce scope constraints throughout.

**What moves:**

- Organization — argument sequencing, section order, thesis placement
- Positional conventions — where the writer's stance appears and how it is introduced
- Explicitness calibration — making implied content explicit (high-context to low-context) or removing over-explanation (low-context to high-context)

Load: `@./references/arc.md` — for arc redesign toward target convention
Load: `@./references/clarify.md` — for resequencing and information flow
Load: `@./references/calibrate.md` — for explicitness calibration

**What does NOT move:**

- Content — what is claimed, argued, or asserted
- Voice — how the writer sounds, their authorial presence
- Vocabulary — specific word choices, register, diction
- Ideas — the intellectual substance of the piece

If adaptation pressure pushes toward changing content, stop and name the tension. The user decides whether to expand scope.

## Phase 5: Annotate

Produce the adapted version with full structural annotation. This phase is mandatory — adaptation without annotation is silent normalization.

**1. Name the structural moves:**
Be specific. Not "restructured for clarity" but "moved thesis from final paragraph to opening paragraph; converted parallel-restatement pattern into hierarchical evidence chain; made the implied causal link in paragraph 3 explicit."

**2. Name what was lost:**
Every structural move costs something. Name the cost. Example annotation standard:

> "Your parallel elaboration was compressed into a linear argument. The accumulative persuasion was replaced by hierarchical evidence. The reader will process this faster but will not feel the weight of the repeated pattern."

> "The dialectical structure — holding the counter-argument before committing — was converted to thesis-first assertion. The adapted version loses the intellectual move of demonstrating you can inhabit the opposing position."

**3. Offer the alternative:**
Always include: "I can also provide a version that keeps your original rhetorical structure and adds a brief framing note for your audience explaining how to read it. Sometimes the move that feels foreign is the strongest part."

Load: `@./references/voice.md` — for what positional moves and authorial stance the adaptation preserves or loses

## Annotation Standard

Every annotation must address three questions:

1. What structural move was made? (specific, not general)
2. What did the original version do that the adapted version cannot? (name the rhetorical function and its cost)
3. Could the original structure be preserved with scaffolding for the target audience?

## Tradition Reference

Key signatures for rapid identification:

| Tradition | Structural Signature | Organization |
|-----------|---------------------|--------------|
| Anglo-American | Thesis-first, linear evidence chain | Deductive, hierarchical |
| Arabic/Semitic | Parallel restatement, accumulative | Associative, coordinate |
| French academic | Thesis-antithesis-synthesis | Dialectical |
| Japanese | Indirect approach, ki-sho-ten-ketsu | Inductive, implicative |
| German academic | Extended scaffolding, delayed thesis | Thorough qualification |
| Latin American (oral) | Circular/spiral, ecosystem metaphor | Recursive, relational |
| High-context East Asian | Reader-responsible, implied connections | Contextual |

Full reference for identification and comparison: `@./references/tradition-signatures.md`
