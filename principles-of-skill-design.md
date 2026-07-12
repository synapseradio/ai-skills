# Principles of Skill Design

A skill instructs an agent: it loads into a working session and directs what the agent reads, in what order, and how the work closes. These principles govern how to write one. They come from building `contribute-to-docs` (in `.claude/skills/contribute-to-docs/`) against the documentation contract in `docs/contributing/`, and they generalize to any skill that operates on a body of knowledge someone maintains.

## Contain by purpose

Every sentence belongs to the container whose purpose it serves, and each container changes at its own rate under its own maintainer. Code holds the volatile exact: the members of a config, the files of a directory, the rows of a table. Documentation holds the durable: why a thing exists, the problem it solves, its boundaries, the constraints and requirements on changing it. A skill holds session orchestration: routing, reading order, phase sequencing, gate ordering.

Test each sentence a skill holds: when it states a principle, a goal, a constraint, or a requirement, it belongs to the docs, and the skill points there. The finished state reads from either side — the docs stand self-evident, naming the skill only by its purpose and location, while the skill dissolves into sequencing and pointers wherever it once held content.

## A skill schedules attention

A skill spends its reader's scarcest resource, context, and earns its place by scheduling that spend: which page to read for which task, at which step a judgment arises, which check closes the work. Progressive disclosure prices the reading. The description loads into every session, so it carries triggering alone. The body loads per invocation, so it stays lean. References load per task type, and the canonical pages load at the step that needs them. Read cost then scales with the task rather than with the corpus.

Authority follows the same shape. When the skill and the source it serves disagree, the source wins, and the skill instructs its executor to surface the disagreement. A skill that could silently override its source would fork the contract it exists to route.

## Type every rule before placing it

A rule has a kind, and its kind decides where it lives and how it gets verified.

An invariant states a property of the artifact that holds at all times — checkable right now, by inspection, with no knowledge of the actions that produced the artifact. "Every link between pages takes the root-relative form."

A requirement obligates an action during a task — checkable only while the task runs. "When you add a page, register it in the sidebar."

Establish invariants once, in the contract of the system they protect, each beside the check that verifies it. Attach requirements to the process step where the action happens. A misplaced rule usually wears the other kind's clothing: "when you add a page, register it" hides the invariant "every page has a sidebar entry," and restating the property form reveals both where it belongs and how an audit verifies it.

## One home per fact; relocate the affordance

Two copies of a fact drift apart the moment one updates. Give every fact one home and make every other occurrence a pointer. When a pointer alone cannot do the work — an audit needs something to run, an author needs the exact set — resist copying the fact to where the work happens, and move the affordance to the fact's home instead. A check that lives beside the invariant it verifies lets "run the check beside each invariant" suffice from anywhere. Adding a fact then costs one edit, and no consumer can act on a stale copy.

A corollary for files: a file whose content reduces to pointers has already dissolved, and deleting it completes the design.

## State the generating fact

Where several rules share a cause, state the cause as the invariant and let the rules follow from it. "The site renders through this engine" grounds the callout markers, the routing scheme, and the sidebar mechanism in one stroke; an executor that knows the generator can derive the conventions it generates, and extend them correctly to a case the author never listed. Rules stated without their generator must be memorized one by one, and they die one by one when the generator changes.

## Write process as a decidable loop

A list of verbs underdetermines behavior. Each phase of a process names its object — what it works on — and its exit condition — how the executor knows the phase is done. The loop names its re-entry edges: a red check returns to execution and becomes the task; a discovered misunderstanding returns to alignment rather than getting improvised past. "Ask until mutual understanding" without an exit condition gets skipped by one executor and looped forever by another; "the user confirms a short statement of subject, intent, and scope" decides.

## Price every word for the executor

The reader of a skill works with bounded context and may run on a smaller model than the author. Every abstract term costs grounding: an instruction to preserve "harmony" spends the executor's tokens rediscovering what the author meant, where "broken links, contradictory claims, stale content, missing registrations" execute directly. The same pricing bans self-justifying prose. A section that argues why its rules live there signals misplacement and gives the executor nothing to act on. State the rule flat, and put the why only where it changes behavior — in the clause that prevents the specific wrong action.

## Encode only verified claims

A skill multiplies whatever it states across every future session, so a wrong claim in a skill is wrong at scale. Check each claim against the artifact — the wiring, the script, the hook, the config — before encoding it, and give claims inherited from existing documentation the same check, because encoding launders them. Expect the check to pay off: a source of truth carries stale claims too, and authoring a skill against it doubles as an audit of it.

## Verification classifies, and names its remainder

A gate that can fail falsely, handed over without a classification discipline, trains its executor to silence it — rewriting a working link ranks among the cheapest ways to turn red into green. Teach the reading of failures: which class always means a real defect, which usually means the checker's own limits, and what confirming each one requires. Then state what no gate covers — voice, altitude, placement, ownership — as an explicit remainder handed to review, so the unverifiable work gets scheduled instead of silently dropped.

## Encode agreements, not guesses

The decisions a skill freezes — scope, naming, placement, process shape — belong to the owner of the system it serves. Form each agreement in dialogue before encoding it, and keep the questions few, concrete, and decision-shaped. Iterate on the draft with the owner while iterations stay cheap; measurement against baselines earns its cost once the shape has settled.

## The process applies to itself

The first evaluation of a skill runs its own process on the work of building it. A change that introduces a verification page passes that page's gates; the loop that will govern future sessions governs the session that writes it. Self-application finds the gaps at the cheapest possible moment — before any downstream session inherits them.
