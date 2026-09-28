#!/usr/bin/env python3
"""Check or write every copy the thinkies skills share.

The copies: each step skill's ``## Steps`` section as a reference file in the router skills
(ponder, map-out), ask-questions' references and shared sections in generate-questions,
``assets/playback.md`` in each record skill, and the Claude Code plugin bundle under
``extensions/thinkies/skills``. The canon blocks every skill pastes live in
``bin/thinkies-shared/``; skill authors paste them, and this script only checks them.

Usage:  python3 bin/sync-thinkies.py [--check | --write]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS = Path("skills/thinkies")
CANON = Path("bin/thinkies-shared")
BUNDLE = Path("extensions/thinkies/skills")
PLUGIN_JSON = Path("extensions/thinkies/.claude-plugin/plugin.json")
EXCLUDE = ("evals",)

#: Source skill -> (router skill, reference file) pairs that hold its ``## Steps`` section.
STEP_COPIES: dict[str, list[tuple[str, str]]] = {
    "argue-the-opposite": [("ponder", "argue-opposite.md")],
    "assess-current-knowledge": [("ponder", "assess-knowledge.md")],
    "branch-possibilities": [("ponder", "branch-out.md")],
    "consider-alternatives": [("ponder", "consider-alternatives.md")],
    "derive-first-principles": [("ponder", "first-principles.md")],
    "excavate-assumptions": [("ponder", "excavate-assumptions.md")],
    "find-leverage": [("ponder", "find-leverage.md")],
    "invert-the-problem": [("ponder", "invert.md")],
    "run-premortem": [("ponder", "premortem.md")],
    "probe-boundaries": [("ponder", "probe-boundaries.md")],
    "question-the-question": [("ponder", "question-the-question.md")],
    "shift-perspective": [("ponder", "shift-perspective.md")],
    "wonder": [("ponder", "wonder.md")],
    "decompose": [("ponder", "decompose.md"), ("map-out", "decompose.md")],
    "shift-abstraction-level": [("ponder", "select-level.md"), ("map-out", "select-level.md")],
    "compose": [("ponder", "compose.md"), ("map-out", "compose.md")],
    "situate": [("ponder", "situate.md"), ("map-out", "situate.md")],
    "generalize": [("ponder", "generalize.md"), ("map-out", "generalize.md")],
    "instantiate": [("ponder", "instantiate.md"), ("map-out", "instantiate.md")],
    "survey-peers": [("ponder", "survey-peers.md"), ("map-out", "survey-peers.md")],
    "connect-ideas": [("ponder", "connect-ideas.md")],
}
ROUTERS = ("ponder", "map-out")

#: Whole directories copied from one skill into another.
DIR_COPIES: dict[str, list[str]] = {"ask-questions/references": ["generate-questions/references"]}

#: ``##`` sections that must match byte for byte between two skills.
SECTION_COPIES: dict[tuple[str, str], list[str]] = {
    ("ask-questions", "generate-questions"): [
        "The rung test",
        "The four clarity laws",
        "The moves that aren't questions",
        "When the inquiry is done",
        "Route by the move you need",
    ],
}

OUTPUT_SKILLS = frozenset(
    {
        "decompose",
        "shift-abstraction-level",
        "compose",
        "situate",
        "generalize",
        "instantiate",
        "survey-peers",
        "connect-ideas",
        "ask-respond",
    }
)
RECORD_SKILLS = frozenset(
    {
        "ask-respond",
        "ask-questions",
        "generate-questions",
        "ponder",
        "connect-ideas",
        "save-note",
        "check-notes",
        "map-out",
        "domain-analysis",
    }
)
RECORD_WRITERS = RECORD_SKILLS - {"check-notes"}

#: Top-level frontmatter keys the Agent Skills spec allows.
SPEC_KEYS = frozenset(
    {"name", "description", "license", "allowed-tools", "compatibility", "metadata"}
)

MIRROR_TOKEN = "${user_config.records_mirror}"
_RECORD_TAIL = re.compile(r"\nFile: `([^`\n]+)`\n\n```jsonl\n(.*?)\n```\n\Z", re.DOTALL)


def section(text: str, heading: str) -> str | None:
    """Body of the ``## heading`` section up to the next ``## `` line, trimmed, plus a newline."""
    lines = text.splitlines()
    try:
        start = lines.index(f"## {heading}")
    except ValueError:
        return None
    body: list[str] = []
    for line in lines[start + 1 :]:
        if line.startswith("## "):
            break
        body.append(line)
    return "\n".join(body).strip() + "\n"


def frontmatter(text: str) -> dict[str, object] | None:
    """Parsed YAML frontmatter, or None when the file has none."""
    match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return None
    parsed = yaml.safe_load(match.group(1))
    return parsed if isinstance(parsed, dict) else None


def _read(path: Path) -> str | None:
    return path.read_text() if path.is_file() else None


def _files(root: Path, exclude: tuple[str, ...] = ()) -> dict[Path, Path]:
    """Relative path -> absolute path for every file under root, skipping top-level excludes."""
    if not root.is_dir():
        return {}
    return {
        p.relative_to(root): p
        for p in sorted(root.rglob("*"))
        if p.is_file() and p.relative_to(root).parts[0] not in exclude
    }


def _skill_md(root: Path, skill: str) -> str | None:
    return _read(root / SKILLS / skill / "SKILL.md")


def _check_template(skill: str, block: str, kinds: dict[str, list[str]]) -> list[str]:
    problems: list[str] = []
    where = f"{SKILLS / skill / 'SKILL.md'}: ## Record template"
    for n, line in enumerate(block.splitlines(), 1):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as err:
            problems.append(f"{where}: line {n} is not JSON ({err.msg})")
            continue
        if not isinstance(obj, dict):
            problems.append(f"{where}: line {n} is not a JSON object")
            continue
        keys = list(obj)
        kind = obj.get("kind")
        if keys[:2] != ["kind", "at"] or kind not in kinds:
            problems.append(f"{where}: line {n} must start with kind, at and name a known kind")
            continue
        fields = kinds[kind]
        rest = keys[2:]
        ok = len(rest) == len(fields) and all(
            key in field.split("|") for key, field in zip(rest, fields)
        )
        if not ok:
            want = ", ".join(["kind", "at", *fields])
            problems.append(f"{where}: line {n} ({kind}) keys {keys} differ from {want}")
    return problems


def check(root: Path = REPO_ROOT) -> list[str]:
    """One line per mismatch, each naming the path."""
    problems: list[str] = []
    canon = root / CANON
    c1 = (canon / "output.md").read_text().strip() + "\n"
    c2 = (canon / "record.md").read_text().strip()
    c3 = (canon / "record-compat.txt").read_text().strip()
    kinds = json.loads((canon / "record-kinds.json").read_text())
    c5 = (canon / "playback.md").read_text()

    # 1, 2: reference copies of each source's ## Steps.
    for source, targets in STEP_COPIES.items():
        text = _skill_md(root, source)
        steps = section(text, "Steps") if text else None
        if steps is None:
            problems.append(f"{SKILLS / source / 'SKILL.md'}: no ## Steps section")
            continue
        if "$ARGUMENTS" in steps:
            problems.append(f"{SKILLS / source / 'SKILL.md'}: ## Steps contains $ARGUMENTS")
        for router, name in targets:
            rel = SKILLS / router / "references" / name
            if _read(root / rel) != steps:
                problems.append(f"{rel}: differs from {source}'s ## Steps")

    # 3: Output sections.
    for skill in sorted(OUTPUT_SKILLS):
        text = _skill_md(root, skill) or ""
        if section(text, "Output") != c1:
            problems.append(
                f"{SKILLS / skill / 'SKILL.md'}: ## Output differs from {CANON}/output.md"
            )

    # 4-8: Record sections, templates, file names, playback, compatibility.
    for skill in sorted(RECORD_SKILLS):
        rel = SKILLS / skill / "SKILL.md"
        text = _skill_md(root, skill) or ""
        record = section(text, "Record")
        if record is None or not record.startswith(c2):
            problems.append(f"{rel}: ## Record does not start with {CANON}/record.md")
        tail = _RECORD_TAIL.search(record or "")
        if tail is None or (record or "").count("```jsonl\n") != 1:
            problems.append(f"{rel}: ## Record does not end with a File: line and one jsonl block")
        else:
            problems.extend(_check_template(skill, tail.group(2), kinds))
            if skill in RECORD_WRITERS and not tail.group(1).startswith(f"{skill}_"):
                problems.append(f"{rel}: File: line does not start with {skill}_")
        playback = SKILLS / skill / "assets" / "playback.md"
        if _read(root / playback) != c5:
            problems.append(f"{playback}: differs from {CANON}/playback.md")
        if skill in RECORD_WRITERS:
            meta = frontmatter(text) or {}
            if c3 not in str(meta.get("compatibility", "")):
                problems.append(f"{rel}: compatibility lacks {CANON}/record-compat.txt")

    # 9: the mirror option each record skill substitutes.
    plugin = json.loads((root / PLUGIN_JSON).read_text())
    option = plugin.get("userConfig", {}).get("records_mirror", {})
    if option.get("type") != "directory":
        for path in sorted((root / SKILLS).rglob("*.md")):
            if MIRROR_TOKEN in path.read_text():
                problems.append(
                    f"{path.relative_to(root)}: uses {MIRROR_TOKEN} but {PLUGIN_JSON} "
                    "lacks userConfig.records_mirror of type directory"
                )

    # 10, 11: the plugin bundle mirrors the source.
    for skill_dir in sorted(p for p in (root / SKILLS).iterdir() if p.is_dir()):
        bundle_dir = root / BUNDLE / skill_dir.name
        for rel, src in _files(skill_dir, EXCLUDE).items():
            dst = bundle_dir / rel
            if not dst.is_file() or dst.read_bytes() != src.read_bytes():
                problems.append(f"{BUNDLE / skill_dir.name / rel}: differs from its source")
    for rel in _files(root / BUNDLE):
        src = root / SKILLS / rel
        if not src.is_file() or (len(rel.parts) > 1 and rel.parts[1] in EXCLUDE):
            problems.append(f"{BUNDLE / rel}: has no source")

    # 12: spec-only frontmatter.
    for path in sorted((root / SKILLS).rglob("SKILL.md")):
        meta = frontmatter(path.read_text())
        if meta is None:
            problems.append(f"{path.relative_to(root)}: no frontmatter")
            continue
        for key in sorted(set(meta) - SPEC_KEYS):
            problems.append(
                f"{path.relative_to(root)}: frontmatter key {key!r} is outside the spec"
            )

    # 13: whole-directory copies.
    for source, targets in DIR_COPIES.items():
        src_files = _files(root / SKILLS / source)
        for target in targets:
            dst_files = _files(root / SKILLS / target)
            for rel, src in src_files.items():
                dst = dst_files.get(rel)
                if dst is None or dst.read_bytes() != src.read_bytes():
                    problems.append(
                        f"{SKILLS / target / rel}: differs from {SKILLS / source / rel}"
                    )
            for rel in sorted(set(dst_files) - set(src_files)):
                problems.append(f"{SKILLS / target / rel}: not in {SKILLS / source}")

    # 14: shared sections.
    for (left, right), headings in SECTION_COPIES.items():
        left_text = _skill_md(root, left) or ""
        right_text = _skill_md(root, right) or ""
        for heading in headings:
            a, b = section(left_text, heading), section(right_text, heading)
            if a is None or b is None or a != b:
                problems.append(
                    f"{SKILLS / right / 'SKILL.md'}: ## {heading} missing or differs from {left}"
                )

    # 15: orphaned router references.
    targets = {(r, n) for pairs in STEP_COPIES.values() for r, n in pairs}
    for router in ROUTERS:
        for path in sorted((root / SKILLS / router / "references").glob("*.md")):
            if (router, path.name) not in targets:
                problems.append(f"{path.relative_to(root)}: not a STEP_COPIES target")

    return problems


def _write_if_changed(path: Path, data: bytes) -> None:
    if path.is_file() and path.read_bytes() == data:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    print(f"wrote {path}")


def _prune(root: Path, keep: set[Path]) -> None:
    """Delete files under root not in keep, then empty directories."""
    for rel, path in _files(root).items():
        if rel not in keep:
            path.unlink()
            print(f"deleted {path}")
    for d in sorted((p for p in root.rglob("*") if p.is_dir()), reverse=True):
        if not any(d.iterdir()):
            d.rmdir()


def write(root: Path = REPO_ROOT) -> None:
    """Write every generated copy. Never writes plugin.json or any section agents author."""
    skills = root / SKILLS
    for source, targets in STEP_COPIES.items():
        text = _skill_md(root, source)
        steps = section(text, "Steps") if text else None
        if steps is None:
            print(f"skipped {SKILLS / source}: no ## Steps section", file=sys.stderr)
            continue
        for router, name in targets:
            _write_if_changed(skills / router / "references" / name, steps.encode())

    targets = {(r, n) for pairs in STEP_COPIES.values() for r, n in pairs}
    for router in ROUTERS:
        for path in sorted((skills / router / "references").glob("*.md")):
            if (router, path.name) not in targets:
                path.unlink()
                print(f"deleted {path}")

    for source, dests in DIR_COPIES.items():
        src_files = _files(skills / source)
        for dest in dests:
            for rel, src in src_files.items():
                _write_if_changed(skills / dest / rel, src.read_bytes())
            if (skills / dest).is_dir():
                _prune(skills / dest, set(src_files))

    playback = (root / CANON / "playback.md").read_bytes()
    for skill in sorted(RECORD_SKILLS):
        _write_if_changed(skills / skill / "assets" / "playback.md", playback)

    bundle = root / BUNDLE
    keep: set[Path] = set()
    for skill_dir in sorted(p for p in skills.iterdir() if p.is_dir()):
        for rel, src in _files(skill_dir, EXCLUDE).items():
            keep.add(Path(skill_dir.name) / rel)
            _write_if_changed(bundle / skill_dir.name / rel, src.read_bytes())
    _prune(bundle, keep)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="report mismatches (default)")
    mode.add_argument("--write", action="store_true", help="write every generated copy")
    args = parser.parse_args()
    if args.write:
        write()
        return 0
    problems = check()
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
