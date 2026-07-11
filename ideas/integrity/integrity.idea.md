---
status: draft
created: 2025-01-11
---

# integrity Examples

## Examples

These examples demonstrate claim analysis—examining structure, evidence, and reasoning. The skill surfaces what verification *requires*; external research to fulfill those requirements is a separate operation.

---

### Historical Narrative Review

A document claims: "The Renaissance began in Florence primarily because the Medici family funded artists, which sparked a cultural revolution across Europe."

**Arise**: Historical summary. Verification triggered by causal claim presented as settled fact.

**Recognition**:

| Signal | Claim Type | Lens |
|--------|------------|------|
| "primarily because" | causal with priority | trace-logical-justifications |
| "began in Florence" | origin | ask-what-breaks |
| "sparked... across Europe" | diffusion scope | audit-chain-of-thought |

**Audit**:

- **assess-current-knowledge** ← *inventory first*: Claims: Florence as origin, Medici as primary cause, direct chain to European transformation. Assumptions: patronage was necessary not merely accelerating; other cities subordinate.

- **trace-logical-justifications** ← "primarily because": Causal claim needs warrant chain. "Primarily" is ambiguous—temporal priority? Greater weight? Necessary condition? Traces to documented commissions but chain to "primary cause" is incomplete. → *Finding: warrant incomplete.*

- **ask-what-breaks** ← "began in Florence" + "sparked across Europe": Counter-evidence: Venice and Rome had parallel movements with different causes. Byzantine scholars (1453) brought Greek texts before Medici patronage peaked. Islamic transmission through Spain predates Florence. → *Finding: multiple defeaters exist.*

**Testify**:

- Warrant incomplete → "primarily because" overstates; Medici were one factor among several
- Defeaters exist for origin → "began in Florence" oversimplifies regional development
- Scope warrant thin → "sparked across Europe" conflates Italian development with later northern spread

### Verification Summary

**Claims Verified**

- Medici provided significant patronage: Supported by documented commissions (Brunelleschi, Donatello, Botticelli)

**Claims Requiring Attention**

- "Primarily because": Incomplete warrant. One necessary condition among several (banking wealth, Byzantine migration, humanist networks, civic ideology)
- "Sparked across Europe": Oversimplified diffusion. Italian Renaissance developed regionally; Northern Renaissance had distinct characteristics

**Acknowledged Uncertainty**

- Relative causal weight remains debated among historians
- Periodization contested (Petrarch and Giotto predate "Florentine" Renaissance)

**After Verification** *(illustrative grounded form)*: "Florence became a major center of Renaissance culture, where Medici patronage—enabled by banking wealth and civic competition—funded artists and scholars who drew on classical texts preserved through Byzantine and Islamic transmission. The movement developed across Italian city-states before spreading to Northern Europe over two centuries."

**Transfer**: Signal→lens mapping travels. "Primarily because" in any domain signals causal priority requiring trace-logical-justifications. Domain-specific: Medici, Byzantine scholars. Portable: causal language needs causal evidence.

---

### Medical Treatment Decision

A patient reviews information stating: "This new treatment has a 70% success rate and minimal side effects according to recent studies."

**Arise**: Treatment information. Verification triggered by health decision with significant consequences—numbers and qualifiers without context.

**Recognition**:

| Signal | Claim Type | Lens |
|--------|------------|------|
| "70% success rate" | quantitative without context | cite-sources + trace-logical-justifications |
| "minimal side effects" | relative without baseline | premortem |
| "recent studies" | authority appeal without citation | cite-sources |
| "new treatment" | novelty framing | ask-what-breaks |

**Audit**:

- **assess-current-knowledge** ← *inventory first*: Claims: specific success rate, side effect characterization, research backing. Unknown: study population, "success" definition, comparison baseline, funding sources, follow-up duration.

- **cite-sources** ← "recent studies": No journal names, sample sizes, or methodology. "Recent studies" unverifiable without citations. → *Finding: source claim unverifiable.*

- **trace-logical-justifications** ← "70%": What warrants the number? Need: study design (RCT vs observational), population, outcome definition, duration. → *Finding: warrant chain broken.*

- **premortem** ← "minimal": Medical marketing often reports relative risk, not absolute benefit. "Minimal" lacks comparison—minimal compared to what? → *Finding: qualifier may mask significant effects.*

**Testify**:

- Source unverifiable → "recent studies" cannot support claim without citations
- Warrant chain broken → "70%" requires methodology, population, outcome definition
- Comparison missing → "minimal" uninterpretable without reference point

### Verification Summary

**Claims Verified**

- Treatment has been studied: Assumed from regulatory context, but citation needed

**Claims Requiring Attention**

- "70% success rate": Unverifiable. Need: absolute numbers, confidence intervals, population match, outcome definition
- "Minimal side effects": Uninterpretable. Need: frequency data, severity scale, comparison baseline
- "Recent studies": Unverifiable. Quality, independence, methodology unknown

**Acknowledged Uncertainty**

- Patient-study population match unknown
- Long-term effects beyond study duration unknown
- Publication bias possible

**After Verification** *(illustrative grounded form)*: "Treatment X showed 70% response rate (95% CI: 64-76%) in a phase 3 randomized trial of 412 patients with stage 2-3 disease, compared to 55% with standard care (Smith et al., NEJM 2024). Response defined as 50% symptom reduction at 12 weeks. Side effects in >10% of patients: fatigue (23%), nausea (15%), headache (12%). Serious adverse events requiring discontinuation: 4%. No data beyond 2 years."

**Decision bridge**: Questions for your physician: Does my profile match the study population? What are my alternatives? What happens if I don't pursue this?

**Transfer**: Numbers without context always require baseline and methodology questions. "70%" appears in medical, financial, scientific claims alike. Domain-specific: RCT design, CI interpretation. Portable: naked numbers need grounding.

---

### Startup Investment Pitch

An investor reviews a pitch deck claiming: "Our AI solution reduces customer churn by 35% based on pilot results, addressing a $50B market opportunity."

**Arise**: Investment documentation. Verification triggered by financial decision based on projected outcomes—percentage claims and market sizing without methodology.

**Recognition**:

| Signal | Claim Type | Lens |
|--------|------------|------|
| "reduces... by 35%" | causal with specific metric | audit-chain-of-thought + trace-logical-justifications |
| "based on pilot results" | evidence appeal | cite-sources + ask-what-breaks |
| "$50B market opportunity" | scale claim | trace-logical-justifications |

**Audit**:

- **assess-current-knowledge** ← *inventory first*: Claims: specific reduction metric, pilot validation, market size. Assumptions: pilot generalizes, market addressable, causation flows from AI not from pilot attention.

- **audit-chain-of-thought** ← "reduces": Implies causation. But during pilots: extra attention, manual interventions, self-selected engaged customers. Inference from "churn was lower" to "AI reduces churn" skips confounders. → *Finding: causal inference unsupported.*

- **trace-logical-justifications** ← "35%" + "$50B": The 35% needs: baseline rate, control group, duration, segment. Relative or absolute? The $50B needs: TAM/SAM/SOM breakdown, capturable share, competitive dynamics. → *Finding: both metrics float without grounding.*

- **detect-fallacies** ← pitch format: Survivorship bias—failed pilots don't appear in decks. Appeal to large market doesn't establish defensibility. → *Finding: structural biases present.*

**Testify**:

- Causal inference unsupported → "reduces churn" may be correlation with pilot attention
- Metrics ungrounded → "35%" and "$50B" require methodology and breakdown
- Structural biases → pitch format systematically omits failure cases

### Verification Summary

**Claims Verified**

- Pilot showed churn reduction: Accepted as measured observation, pending design review

**Claims Requiring Attention**

- "35% reduction": From what baseline? Absolute or relative? With control group? Need: baseline rate, duration, segment, methodology
- "$50B market": TAM ≠ SAM ≠ SOM. What's realistically capturable?
- Causation: Did AI reduce churn, or did pilot process?

**Acknowledged Uncertainty**

- Competitive response to entry
- Whether pilot segment represents target market
- Reproducibility at scale

**After Verification** *(illustrative grounded form)*: "Pilot with 50 mid-market SaaS customers over 6 months showed churn rate of 8% vs. 12% historical baseline (35% relative reduction, 4 percentage points absolute). No control group. Customers self-selected from engaged accounts. Market sizing: $50B TAM per Gartner; enterprise segment ($30B) requires sales infrastructure not built. Mid-market SAM ~$8B; realistic year-3 capture at 0.5% = $40M potential."

**Due diligence requirements**: Controlled A/B with randomized customers. Unit economics at scale. Reference calls on renewal intent. Competitive analysis.

**Transfer**: Percentage reductions without baselines appear everywhere. "35% of what?" is always valid. Domain-specific: TAM/SAM/SOM, unit economics. Portable: skepticism toward selection effects and survivorship bias.

---

### Philosophical Argument Assessment

A student essay argues: "Consciousness cannot be explained by physical processes because subjective experience is fundamentally different from objective measurement."

**Arise**: Philosophical argument. Verification triggered by logical structure—a universal negative ("cannot") supported by categorical distinction ("fundamentally different").

**Recognition**:

| Signal | Claim Type | Lens |
|--------|------------|------|
| "cannot be explained" | universal negative | trace-logical-justifications |
| "fundamentally different" | categorical distinction | audit-chain-of-thought |
| "because" | logical connective | detect-fallacies |

Note: Philosophical arguments require examining *logical structure* rather than empirical evidence. Lenses apply to reasoning form.

**Audit**:

- **assess-current-knowledge** ← *inventory first*: Claims: (1) explanatory gap exists, (2) subjective/objective are fundamentally different, (3) this difference makes explanation impossible. Key assumption: "explanation" requires categorical similarity.

- **trace-logical-justifications** ← "cannot": What warrants impossibility? "Fundamentally different" is definitional. But "cannot be explained" traces to unstated premise—explanation requires same-category terms. This premise carries argumentative weight but floats without defense. → *Finding: key warrant assumed, not argued.*

- **detect-fallacies** ← "because": Moves from "current gap" to "principled impossibility." Resembles argument from ignorance, but may be conceivability argument. Exact form determines validity. → *Finding: argument form ambiguous.*

**Testify**:

- Key warrant assumed → premise about explanation requiring categorical similarity needs defense
- Argument form ambiguous → validity depends on whether ignorance argument or conceivability argument
- Gap ≠ impossibility → epistemic gap doesn't entail metaphysical claim

### Verification Summary

**Claims Verified**

- Subjective/objective distinction is coherent: Widely accepted philosophical distinction
- Current explanatory gap exists: Accurate—no consensus physical account of phenomenal experience

**Claims Requiring Attention**

- "Cannot be explained": Conflates epistemic gap with metaphysical impossibility; requires justification
- Hidden premise: Assumes explanation requires categorical homogeneity—some theories reject this

**Acknowledged Uncertainty**

- Whether "hard problem" reflects ontological barrier or conceptual confusion is contested
- Validity depends on theory of explanation
- Competing positions (functionalism, type-B physicalism, illusionism, panpsychism) offer responses

**After Verification** *(illustrative grounded form)*: The argument as stated is incomplete. A stronger version:

1. Subjective experience has properties (what-it's-likeness) that objective descriptions cannot capture
2. Physical explanations are objective descriptions
3. Therefore, physical explanations cannot capture subjective experience
4. What cannot be captured cannot be explained

The critical move is premise 4. Functionalists deny capturing subjective character is required for explanation. Type-B physicalists accept explanatory gap while denying metaphysical gap. The argument needs to defend its theory of explanation.

**Theory-dependence note**: Unlike empirical claims, philosophical arguments often have validity that varies by theoretical framework. Verification in philosophy means identifying theoretical commitments that determine validity, not establishing absolute truth.

**Transfer**: Universal negatives ("cannot," "impossible," "never") always require examining what would make them true. Domain-specific: philosophy of mind positions. Portable: hidden premises carrying argumentative weight appear in legal, ethical, policy arguments. The move from "we don't currently" to "we can't ever" is a common conflation.
