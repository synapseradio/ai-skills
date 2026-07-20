#!/usr/bin/env python3
"""Run every ask-questions eval through `claude -p`, once per skill version.

Each run is isolated with --safe-mode so the user's global CLAUDE.md and every
other installed skill stay out of the way. The only variable between the
with_skill and old_skill configurations is which SKILL.md the prompt points at.
"""

import json
import pathlib
import shutil
import subprocess
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor

REPO = pathlib.Path("/Users/nke/projects/ai/ai-skills")
ITER = REPO / "skills/ask-questions-workspace/iteration-1"
CWD = pathlib.Path("/tmp/aq-eval-cwd")

CONFIGS = {
    "with_skill": REPO / "skills/ask-questions",
    "old_skill": REPO / "skills/ask-questions-workspace/skill-snapshot",
}

MODEL = "sonnet"
EFFORT = "high"
CONCURRENCY = 5
TIMEOUT_S = 900

TEMPLATE = """You are an assistant replying to a user in a live session.

First, read {skill_md} in full, along with every reference file under {refs_dir}/ that it routes you to for this situation. Follow that skill's process to decide what to send.

Then reply to the user's message below. Your entire output is the reply you would send that user. No preamble about having consulted a skill, no meta-commentary on your process, and no reading out a reference file's Questions worksheet verbatim -- those are internal worksheets.

The user's message:

---
{user_prompt}
---
"""


def run_one(eval_dir: pathlib.Path, config: str) -> str:
    """Never raises. A failed job returns a failure string so the fleet survives it."""
    try:
        return _run_one(eval_dir, config)
    except Exception as exc:  # noqa: BLE001
        detail = traceback.format_exc()
        try:
            (eval_dir / config).mkdir(parents=True, exist_ok=True)
            (eval_dir / config / "error.txt").write_text(detail)
        except Exception:  # noqa: BLE001
            pass
        return f"CRASH {eval_dir.name}/{config}: {exc!r}"


def _run_one(eval_dir: pathlib.Path, config: str) -> str:
    skill_root = CONFIGS[config]
    prompt = TEMPLATE.format(
        skill_md=skill_root / "SKILL.md",
        refs_dir=skill_root / "references",
        user_prompt=(eval_dir / "prompt.txt").read_text().strip(),
    )
    out_dir = eval_dir / config
    (out_dir / "outputs").mkdir(parents=True, exist_ok=True)
    if not (out_dir / "outputs").is_dir():
        raise RuntimeError(f"output dir vanished after mkdir: {out_dir / 'outputs'}")

    cmd = [
        "claude",
        "-p",
        prompt,
        "--model",
        MODEL,
        "--effort",
        EFFORT,
        "--safe-mode",
        "--tools",
        "Read",
        "--add-dir",
        str(skill_root),
        "--permission-mode",
        "dontAsk",
        "--output-format",
        "json",
        "--no-session-persistence",
    ]

    tag = f"{eval_dir.name}/{config}"
    try:
        proc = subprocess.run(cmd, cwd=CWD, capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        (out_dir / "error.txt").write_text(f"timeout after {TIMEOUT_S}s\n")
        return f"TIMEOUT {tag}"

    if proc.returncode != 0:
        (out_dir / "error.txt").write_text(f"exit {proc.returncode}\n\nSTDERR:\n{proc.stderr}\n")
        return f"EXIT{proc.returncode} {tag}"

    try:
        events = json.loads(proc.stdout)
        result = next(e for e in reversed(events) if e.get("type") == "result")
    except Exception as exc:  # noqa: BLE001
        (out_dir / "error.txt").write_text(f"unparseable output: {exc}\n\n{proc.stdout[:4000]}\n")
        return f"BADJSON {tag}"

    if result.get("is_error"):
        (out_dir / "error.txt").write_text(json.dumps(result, indent=2))
        return f"ERROR {tag}"

    (out_dir / "outputs").mkdir(parents=True, exist_ok=True)
    (out_dir / "outputs" / "response.md").write_text(result.get("result", "") + "\n")

    usage = result.get("usage", {}) or {}
    total_tokens = sum(
        usage.get(k, 0) or 0
        for k in (
            "input_tokens",
            "cache_creation_input_tokens",
            "cache_read_input_tokens",
            "output_tokens",
        )
    )
    duration_ms = result.get("duration_ms", 0)
    (out_dir / "timing.json").write_text(
        json.dumps(
            {
                "total_tokens": total_tokens,
                "duration_ms": duration_ms,
                "total_duration_seconds": round(duration_ms / 1000, 1),
                "output_tokens": usage.get("output_tokens", 0),
                "num_turns": result.get("num_turns"),
                "total_cost_usd": result.get("total_cost_usd"),
                "model": MODEL,
                "effort": EFFORT,
            },
            indent=2,
        )
        + "\n"
    )

    return f"ok {tag} ({round(duration_ms / 1000)}s, {total_tokens} tok)"


def main() -> int:
    CWD.mkdir(parents=True, exist_ok=True)

    eval_dirs = sorted(
        (d for d in ITER.iterdir() if d.is_dir() and d.name.startswith("eval-")),
        key=lambda p: int(p.name.split("-")[1]),
    )
    # Clear every prior config dir up front so the whole set runs under identical
    # conditions -- a benchmark that mixes stale and fresh runs compares nothing.
    for d in eval_dirs:
        for cfg in CONFIGS:
            shutil.rmtree(d / cfg, ignore_errors=True)
            (d / cfg / "outputs").mkdir(parents=True, exist_ok=True)

    jobs = [(d, cfg) for d in eval_dirs for cfg in CONFIGS]
    print(f"running {len(jobs)} evals, concurrency {CONCURRENCY}", flush=True)

    failures = 0
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        for line in pool.map(lambda a: run_one(*a), jobs):
            print(line, flush=True)
            if not line.startswith("ok "):
                failures += 1

    print(f"\ndone. {len(jobs) - failures}/{len(jobs)} succeeded.", flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
