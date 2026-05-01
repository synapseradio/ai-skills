# Arrange

Order sections, arguments, and paragraphs so the sequence serves the purpose.

## Diagnostic Question

Ask: Is the ordering of arguments, sections, or paragraphs purposeful? Could a reader explain why this comes before that? Where does the sequence feel arbitrary -- where would rearranging change nothing?

## Instructions

1. **Distinguish arrangement from arc** -- Arc is about tension and resolution: what does the reader want to know, and when do they get it? Arrangement is about logical ordering: what must come first to make what follows possible? A piece can have strong arc (compelling pull) and weak arrangement (sections in arbitrary order), or strong arrangement (clear logical progression) and weak arc (no tension driving the reader forward). Both matter; they do different work.

2. **Identify the ordering principle** -- Every arrangement implies a logic. Name it:
   - **Dependency** -- A requires understanding B, so B comes first
   - **Chronological** -- Events in the order they occurred
   - **Priority** -- Most important first (inverted pyramid)
   - **Accumulative** -- Each section builds on the previous, compounding understanding
   - **Comparative** -- Alternatives presented side by side for evaluation
   - **Problem-solution** -- Problem established, then solution proposed
   - **General-to-specific** or **specific-to-general** -- Zoom in or zoom out

   If no ordering principle is discernible, the arrangement is likely arbitrary.

3. **Test the ordering** -- For each major section or argument, ask: does this depend on something that comes after it? Could a reader arriving at this point follow without backtracking? The prerequisite-trace from `clarify.md` applies at section level, not just sentence level.

4. **Check for buried leads** -- The most important point sometimes hides in the middle or end because the writer discovered it last. Writing order is not reading order. The reader's needs, not the writer's discovery process, should determine arrangement.

5. **Evaluate paragraph-level progression** -- Within sections, paragraphs should advance the argument. Each paragraph earns its place by doing work the previous paragraph could not. If two paragraphs could swap without consequence, one of them may be redundant, or both may need a stronger connection to the section's purpose.

6. **Respect tradition-specific ordering** -- Arrangement conventions vary across rhetorical traditions. Anglo-American expects thesis-first deductive ordering. French academic builds through dialectical movement. Arabic rhetoric accumulates through parallel restatement. Japanese ki-shō-ten-ketsu delays the turn. Load `tradition.md` when the arrangement follows a non-Anglo convention that may appear disordered to an untrained reader.

## Examples

### Dependency ordering violated

**Before:**

- Section 1: How to configure the caching layer
- Section 2: Why caching improves performance
- Section 3: What caching is

**Ordering test:** Section 1 assumes the reader understands caching (Section 3) and why they want it (Section 2). The dependency chain runs backward.

**After:**

- Section 1: What caching is
- Section 2: Why caching improves performance
- Section 3: How to configure the caching layer

**What changed:** Sections now follow dependency order. Each section can be understood without reading ahead.

### Buried lead

**Before:** A blog post opens with three paragraphs of background context, then discusses related work, then in paragraph seven states: "What none of these approaches address is that the problem is not algorithmic -- it is organizational."

**Ordering test:** The strongest claim -- the reframing -- is buried. The reader wades through context they cannot evaluate because they do not yet know what the piece argues.

**After:** Open with the reframing: "The performance problem is not algorithmic -- it is organizational. Here is why that matters and what to do about it." Background and related work follow, now purposeful -- the reader knows what they are being prepared to evaluate.

**What changed:** The arrangement shifted from writer's discovery order (background → insight) to reader's need order (insight → supporting context).

### Arbitrary section order revealed

**Before:** A proposal with four sections -- Budget, Timeline, Technical Approach, Risk Assessment -- presented in that order.

**Ordering test:** Could these sections appear in any order? Budget before Technical Approach means the reader evaluates cost before understanding what they are paying for. Risk Assessment at the end means risks are an afterthought.

**After:** Technical Approach → Risk Assessment → Timeline → Budget. The reader first understands what is proposed, then what could go wrong, then how long it takes, then what it costs. Each section builds on the previous.

**What changed:** The arrangement now follows a decision logic -- understand, evaluate risk, assess feasibility, approve cost.
