#!/usr/bin/env python3
"""Generate the OpenAI Codex plugin bundle from the Anthropic-format thinkies skills.

Source of truth is ``skills/thinkies/``; this script never writes there. It owns
``extensions/openai/thinkies/skills/`` (wiped and rebuilt each run) and
``extensions/openai/thinkies/.codex-plugin/plugin.json``. The README beside them is
hand-written and left untouched.

Two kinds of transform run over every skill. A structural pass reduces YAML frontmatter to
the two keys Codex documents, and copies only the subdirectories Codex reads. A prose pass
applies the literal string edits listed in ``BODY_EDITS`` below, which remove constructs
that mean something to Claude Code and nothing to Codex. Every edit must match its source
exactly once; a miss aborts the run rather than emitting a half-transformed skill, so that
upstream rewording surfaces here instead of shipping.

Layout and manifest schema: https://developers.openai.com/codex/build-plugins
Skill file shape: https://developers.openai.com/codex/skills

Usage:  python3 bin/generate-openai-plugin.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = REPO_ROOT / "skills" / "thinkies"
DEFAULT_OUT_DIR = REPO_ROOT / "extensions" / "openai" / "thinkies"

#: Frontmatter keys Codex documents for SKILL.md. Everything else is dropped.
KEPT_FRONTMATTER_KEYS = ("name", "description")

#: Subdirectories copied verbatim next to each SKILL.md. A whitelist, so the source
#: ``README.md`` (which points at ``~/.claude/skills/``) and ``evals/`` stay out.
COPIED_SUBDIRS = ("references", "assets", "scripts")

#: Tokens that must not survive into the emitted tree, checked after every file is written.
FORBIDDEN_TOKENS = ("$ARGUMENTS", "CLAUDE_PROJECT_DIR", "TaskCreate", ".claude/")

#: Codex loader constraint on the qualified skill name (``<plugin>:<skill>``).
QUALIFIED_NAME_LIMIT = 64


@dataclass(frozen=True)
class Edit:
    """One literal find-and-replace inside one emitted file.

    ``old`` must occur exactly once in the source file, or the run aborts.
    """

    why: str
    old: str
    new: str
    file: str = "SKILL.md"


# --------------------------------------------------------------------------------------
# Transform rules. Read top to bottom: this is the whole prose-edit surface.
# --------------------------------------------------------------------------------------

#: ``$ARGUMENTS`` is Claude Code slash-command substitution. Codex has no equivalent and
#: would render the token literally. Where the source already names a fallback, that
#: fallback becomes the sole instruction; where it does not, the replacement points the
#: agent at what the user just supplied.
ARGUMENTS_EDITS: dict[str, Edit] = {
    "calibrate-confidence": Edit(
        why="fallback becomes the instruction",
        old="Target: `$ARGUMENTS`, else recent assertions in the current context.",
        new="Target: recent assertions in the current context.",
    ),
    "check-soundness": Edit(
        why="fallback becomes the instruction",
        old="Target: `$ARGUMENTS`, else the synthesis or conclusion in the current context.",
        new="Target: the synthesis or conclusion in the current context.",
    ),
    "cite-sources": Edit(
        why="fallback becomes the instruction; trailing guidance kept intact",
        old="Target: `$ARGUMENTS`, else recent statements that reference external information.",
        new="Target: recent statements that reference external information.",
    ),
    "detect-fallacies": Edit(
        why="fallback becomes the instruction",
        old="Target: `$ARGUMENTS`, else the argument in the current context.",
        new="Target: the argument in the current context.",
    ),
    "flip-assumptions": Edit(
        why="fallback becomes the instruction",
        old="Target: `$ARGUMENTS`, else the claim in the current context.",
        new="Target: the claim in the current context.",
    ),
    "integrate-other-perspectives": Edit(
        why="fallback becomes the instruction",
        old="Target: `$ARGUMENTS`, else the perspectives in the current context.",
        new="Target: the perspectives in the current context.",
    ),
    "integrity": Edit(
        why="fallback becomes the instruction",
        old="Target: `$ARGUMENTS`, else the current response or most recent significant output.",
        new="Target: the current response or most recent significant output.",
    ),
    "trace-logic": Edit(
        why="fallback becomes the instruction",
        old="Target: `$ARGUMENTS`, else the reasoning in the current context.",
        new="Target: the reasoning in the current context.",
    ),
    "synthesize-opposing-views": Edit(
        why="fallback becomes the instruction",
        old="Target: `$ARGUMENTS`, else the thesis and antithesis in the current context.",
        new="Target: the thesis and antithesis in the current context.",
    ),
    "strategize": Edit(
        why=(
            "fallback here is 'ask for clarification', which alone would make the skill "
            "always ask; it is kept as the conditional it was written to be"
        ),
        old="Target: `$ARGUMENTS`, else ask for clarification.",
        new="Target: the problem in the current context; if none is evident, ask for clarification.",
    ),
    "ask-respond": Edit(
        why="the substituted question is simply the user's",
        old="Restate the question from `$ARGUMENTS` in the assistant's first-person point of view.",
        new="Restate the user's question in the assistant's first-person point of view.",
    ),
    "decision-analysis": Edit(
        why="the substituted decision is the one in the user's request",
        old="Locate the concrete decision in `$ARGUMENTS` or the conversation.",
        new="Locate the concrete decision in the user's request or the conversation.",
    ),
    "ponder": Edit(
        why="the substituted text is the user's request",
        old='Detect the problem\'s shape from signals in "$ARGUMENTS" and the conversation.',
        new="Detect the problem's shape from signals in the user's request and the conversation.",
    ),
    "scamper": Edit(
        why="the substituted text is the subject the user brought",
        old='Apply each SCAMPER lens to "$ARGUMENTS":',
        new="Apply each SCAMPER lens to the subject the user brought:",
    ),
    # Bare, unguarded uses under a heading — no fallback in the source to promote, so each
    # gets written guidance in the voice of its own file.
    "cite": Edit(
        why="bare token under '## Input'; the file's closing line already handles 'no link given'",
        old="## Input\n\n$ARGUMENTS\n",
        new=(
            "## Input\n\n"
            "The paper link or links the user supplied — or, when the request carried none, "
            "the papers under discussion in the most recent context.\n"
        ),
    ),
    "tree-of-thought": Edit(
        why="bare token under '## Query' with no fallback",
        old="## Query\n\n`$ARGUMENTS`\n",
        new=(
            "## Query\n\n"
            "The problem the user just posed. If the request named no problem outright, take "
            "the most relevant thread from the recent conversation as the query, and say which "
            "one you took before starting Phase 1.\n"
        ),
    ),
    "what-if": Edit(
        why="bare token under '## Query' with no fallback",
        old="## Query\n\n`$ARGUMENTS`\n",
        new=(
            "## Query\n\n"
            "The future the user just handed you — the decision, hypothetical, or plan named in "
            "their request. If the request named none outright, take the live question from the "
            "recent conversation and say which one you took before Q1.\n"
        ),
    ),
}

#: Edits beyond the ``$ARGUMENTS`` sweep: host-specific paths, a tool call Codex does not
#: have, and delegation language that assumed a harness able to spawn agents.
OTHER_EDITS: dict[str, tuple[Edit, ...]] = {
    "visualize": (
        Edit(
            why="TaskCreate is a Claude Code tool; the intent is progress tracking",
            old=(
                "Before phase 1, call `TaskCreate` once per phase below so progress is tracked "
                "through the workflow."
            ),
            new=(
                "Before phase 1, write down the six phases below as a checklist and mark each one "
                "off as you finish it, so progress stays visible through the workflow."
            ),
        ),
        Edit(
            why="host-specific save path; redirected to the portable target the Persisting section already names",
            old=(
                "| 6. Save | Persist to `${CLAUDE_PROJECT_DIR}/.claude/visualizations/"
                "viz-<timestamp>.html`. Optionally register via CLI. |"
            ),
            new=(
                "| 6. Save | Persist to the location the Persisting section names for this harness. "
                "Optionally register via CLI. |"
            ),
        ),
        Edit(
            why="same host-specific save path, second occurrence outside SKILL.md",
            file="references/phase-present.md",
            old="1. Save to `${CLAUDE_PROJECT_DIR}/.claude/visualizations/viz-<timestamp>.html`",
            new=(
                "1. Save to `~/.visualizations/<slug>-<YYYYMMDD-HHMMSS>.<ext>` — `html` for "
                "browser-runnable charts, `md` for markdown output. Create the directory if missing."
            ),
        ),
        Edit(
            why=(
                "the Persisting bullets route by product name, so a Codex host would fall through "
                "to 'print it in a code block' and contradict phase 6; rekeyed by capability"
            ),
            old="- **Claude.ai (with `artifacts` tool):** emit the visualization as an",
            new="- **A harness with an `artifacts` tool:** emit the visualization as an",
        ),
        Edit(
            why="same routing fix, filesystem branch",
            old="- **Claude Code (with `Bash` and `Write`):** save to",
            new="- **A harness with shell and file-write tools:** save to",
        ),
    ),
    "ask-questions": (
        Edit(
            why=(
                "Fork mode assumed a harness that spawns agents; the sequential path becomes the "
                "instruction and fan-out stays described as a host-dependent enhancement"
            ),
            old=(
                "Forming a question has two parts: gathering the context and shaping the words. "
                "You can keep both, or split them across agents. Pick by where the work is.\n\n"
                "- **Fork to gather and ask.** When the context is large or scattered — many "
                "files, a long history, several places to look — send one or more agents to read "
                "it and come back with a candidate question already formed. Each returns a "
                "question grounded in what it found. Treat the context it rode in on as "
                "unverified until you check it.\n"
            ),
            new=(
                "Forming a question has two parts: gathering the context and shaping the words. "
                "Do both yourself: go read what you need, then shape the question from what you "
                "found. That sequence is the instruction, and it holds in any harness.\n\n"
                "Where a harness lets you delegate to other agents, either part can be split off. "
                "The work is the same, only spread wider, and any context an agent rides in on "
                "stays unverified until you check it.\n\n"
                "- **Send others to gather and ask.** When the context is large or scattered — "
                "many files, a long history, several places to look — one or more agents can read "
                "it and come back with a candidate question already formed, each grounded in what "
                "it found.\n"
            ),
        ),
    ),
    "what-if": (
        Edit(
            why=(
                "Recurse assumed child walks running as separate agents; the sequential walk "
                "becomes the instruction and parallel execution stays available where supported"
            ),
            old=(
                "- **Axes overflow.** When Q3 keeps more unknowns than one walk can carry, fix "
                "the dominant axis and run one child walk per landing, each inheriting the "
                "remaining unknowns as its own Q3 candidates.\n\n"
                "An orchestrator splits the chain at its phases: run Q1 through Q6, stop, and "
                "hand each tile worth entering to a child walk — live per its watchpoints, or "
                "exposed per Q9, never all of them. Aggregate with rules the chain already "
                "carries: a consequence most children reach is close to inevitable (Q7's merge), "
                "and strategies score across the union of what the children return (Q9). Hold "
                "depth at two levels; nesting recovers dimensionality a single walk projects "
                "away, and each level stays tellable.\n\n"
                "**The unless agent.** Alongside the children, an orchestrator runs one more "
                "agent that holds every parked assumption from Q2 and does nothing else. At each "
                "checkpoint — tiles formed, consequences grown, recommendation drafted — it asks "
                "one question per assumption: unless this still holds, which tile flips? When an "
                "assumption breaks, it interrupts the line, and every walk that leaned on the "
                "assumption re-enters at Q2 instead of shipping a recommendation built on a dead "
                "premise."
            ),
            new=(
                "- **Axes overflow.** When Q3 keeps more unknowns than one walk can carry, fix "
                "the dominant axis and take each landing in turn as its own walk, each inheriting "
                "the remaining unknowns as its own Q3 candidates.\n\n"
                "Split the chain at its phases: run Q1 through Q6, stop, then re-enter each tile "
                "worth entering as a child walk — live per its watchpoints, or exposed per Q9, "
                "never all of them. Run those walks one after another and carry each result "
                "forward. Aggregate with rules the chain already carries: a consequence most "
                "children reach is close to inevitable (Q7's merge), and strategies score across "
                "the union of what the children return (Q9). Hold depth at two levels; nesting "
                "recovers dimensionality a single walk projects away, and each level stays "
                "tellable. Where a harness can run the child walks in parallel as separate "
                "agents, do — the aggregation rules are unchanged.\n\n"
                "**The unless check.** Alongside the child walks, keep a running list of every "
                "parked assumption from Q2 and nothing else on it. At each checkpoint — tiles "
                "formed, consequences grown, recommendation drafted — ask one question per "
                "assumption: unless this still holds, which tile flips? When an assumption "
                "breaks, stop the line there, and every walk that leaned on the assumption "
                "re-enters at Q2 instead of shipping a recommendation built on a dead premise. "
                "Where a harness supports it, a dedicated agent can hold this list and interrupt "
                "when one breaks."
            ),
        ),
    ),
}

#: Left deliberately untouched: ``decompose``'s self-referential call to itself (it reads as
#: continued reasoning), ``skill-design``'s advisory skill-creator handoffs and
#: platform.claude.com links (advisory prose, not imperative calls), and every passing prose
#: mention of Claude that carries no instruction.


def body_edits_for(skill_name: str) -> list[Edit]:
    """Every prose edit that applies to one skill, in a stable order."""
    edits: list[Edit] = []
    if skill_name in ARGUMENTS_EDITS:
        edits.append(ARGUMENTS_EDITS[skill_name])
    edits.extend(OTHER_EDITS.get(skill_name, ()))
    return edits


# --------------------------------------------------------------------------------------
# Manifest
# --------------------------------------------------------------------------------------

PLUGIN_MANIFEST: dict[str, object] = {
    "author": {
        "name": "Nick Krause",
        "url": "https://github.com/synapseradio",
    },
    "description": (
        "Reasoning toolkit of 48 skills — decomposition, questioning, assumption excavation, "
        "perspective shifts, decision analysis, ideation, synthesis, and epistemic integrity "
        "checks. Invoke one explicitly by name, or let Codex match one by description."
    ),
    "homepage": "https://github.com/synapseradio/ai-skills/tree/main/extensions/openai/thinkies",
    "interface": {
        "capabilities": ["Read"],
        "category": "Productivity",
        "developerName": "Nick Krause",
        "displayName": "Thinkies",
        "longDescription": (
            "Forty-eight small reasoning skills that each do one thing: break a problem at its "
            "joints, surface what you are assuming, argue the opposite, tile the futures a "
            "decision hinges on, check whether the evidence carries the claim. Each skill is "
            "prose instructions only — no network calls, no credentials, no background state."
        ),
        "shortDescription": "Forty-eight reasoning skills for thinking through hard problems.",
    },
    "keywords": [
        "reasoning",
        "thinking",
        "decision-analysis",
        "creativity",
        "questioning",
        "decomposition",
        "critical-thinking",
        "ideation",
        "socratic",
        "epistemics",
    ],
    "license": "EUPL-1.2",
    "name": "thinkies",
    "repository": "https://github.com/synapseradio/ai-skills",
    "skills": "./skills/",
    "version": "0.1.0",
}


# --------------------------------------------------------------------------------------
# Transform primitives
# --------------------------------------------------------------------------------------


class TransformError(RuntimeError):
    """A transform rule no longer matches its source, or output failed a check."""


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return ``(frontmatter_yaml, body)`` for a SKILL.md, keeping the body byte-exact."""
    if not text.startswith("---\n"):
        raise TransformError("SKILL.md does not open with a YAML frontmatter fence")
    end = text.index("\n---\n", 3)
    return text[4:end], text[end + len("\n---\n") :]


def reduce_frontmatter(frontmatter_yaml: str) -> str:
    """Reduce frontmatter to name and description, preserving both values verbatim.

    Codex documents only these two keys. ``metadata``, ``compatibility``, ``license``, and
    ``allowed-tools`` are dropped. The emitted description round-trips to the same string
    the source parsed to; only its line wrapping may differ.
    """
    parsed = yaml.safe_load(frontmatter_yaml)
    if not isinstance(parsed, dict):
        raise TransformError("frontmatter did not parse to a mapping")

    kept = {}
    for key in KEPT_FRONTMATTER_KEYS:
        value = parsed.get(key)
        if not isinstance(value, str) or not value.strip():
            raise TransformError(f"frontmatter key {key!r} is missing or empty")
        kept[key] = value

    emitted = yaml.safe_dump(
        kept,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=96,
    )
    if yaml.safe_load(emitted) != kept:
        raise TransformError("frontmatter did not survive the round trip verbatim")
    return f"---\n{emitted}---\n"


def apply_edits(text: str, edits: list[Edit], where: str) -> str:
    """Apply each edit whose ``file`` matches ``where``. Each must match exactly once."""
    for edit in edits:
        if edit.file != where:
            continue
        found = text.count(edit.old)
        if found != 1:
            raise TransformError(
                f"{where}: transform rule matched {found} times, expected 1 "
                f"({edit.why}) — source text moved; update the rule.\n  old: {edit.old[:120]!r}"
            )
        text = text.replace(edit.old, edit.new)
    return text


def transform_skill_md(text: str, edits: list[Edit]) -> str:
    """Run the structural pass on the frontmatter and the prose pass on the body."""
    frontmatter_yaml, body = split_frontmatter(text)
    return reduce_frontmatter(frontmatter_yaml) + apply_edits(body, edits, "SKILL.md")


# --------------------------------------------------------------------------------------
# Emit
# --------------------------------------------------------------------------------------


@dataclass
class Result:
    skills: list[str] = field(default_factory=list)
    files: int = 0
    bytes: int = 0


def _write(path: Path, text: str) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = text.encode("utf-8")
    path.write_bytes(data)
    return len(data)


def emit_skill(source: Path, target: Path, result: Result) -> None:
    """Emit one skill: transformed SKILL.md plus the whitelisted subdirectories."""
    edits = body_edits_for(source.name)
    result.bytes += _write(
        target / "SKILL.md", transform_skill_md((source / "SKILL.md").read_text(), edits)
    )
    result.files += 1

    for subdir in COPIED_SUBDIRS:
        source_sub = source / subdir
        if not source_sub.is_dir():
            continue
        for source_file in sorted(p for p in source_sub.rglob("*") if p.is_file()):
            relative = source_file.relative_to(source)
            target_file = target / relative
            target_file.parent.mkdir(parents=True, exist_ok=True)
            file_edits = [e for e in edits if e.file == relative.as_posix()]
            if file_edits:
                result.bytes += _write(
                    target_file,
                    apply_edits(source_file.read_text(), file_edits, relative.as_posix()),
                )
            else:
                shutil.copy2(source_file, target_file)
                result.bytes += target_file.stat().st_size
            result.files += 1


def check_no_forbidden_tokens(root: Path) -> None:
    """Fail if any Claude-host construct survived into the emitted tree."""
    offenders = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        for token in FORBIDDEN_TOKENS:
            if token in text:
                offenders.append(f"{path.relative_to(root)}: {token}")
    if offenders:
        raise TransformError("forbidden tokens survived:\n  " + "\n  ".join(offenders))


def generate(source_dir: Path, out_dir: Path) -> Result:
    """Rebuild the plugin bundle. Wipes ``skills/`` only; any README stays put."""
    skills_root = out_dir / "skills"
    if skills_root.exists():
        shutil.rmtree(skills_root)

    result = Result()
    for source in sorted(p for p in source_dir.iterdir() if (p / "SKILL.md").is_file()):
        emit_skill(source, skills_root / source.name, result)
        result.skills.append(source.name)

    manifest = json.dumps(PLUGIN_MANIFEST, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    result.bytes += _write(out_dir / ".codex-plugin" / "plugin.json", manifest)
    result.files += 1

    check_no_forbidden_tokens(out_dir / "skills")
    for name in result.skills:
        qualified = f"{PLUGIN_MANIFEST['name']}:{name}"
        if len(qualified) > QUALIFIED_NAME_LIMIT:
            raise TransformError(f"qualified skill name too long ({len(qualified)}): {qualified}")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT_DIR, help="output plugin root")
    parser.add_argument("--source", type=Path, default=SOURCE_DIR, help="source skills directory")
    args = parser.parse_args(argv)

    try:
        result = generate(args.source, args.out)
    except TransformError as error:
        print(f"generate-openai-plugin: {error}", file=sys.stderr)
        return 1

    longest = max(result.skills, key=lambda n: len(n))
    print(f"skills:  {len(result.skills)}")
    print(f"files:   {result.files}")
    print(f"bytes:   {result.bytes} ({result.bytes / 1_048_576:.1f} MiB)")
    print(f"longest qualified name: thinkies:{longest} ({len('thinkies:' + longest)} chars)")
    print(f"output:  {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
