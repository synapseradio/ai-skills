#!/usr/bin/env python3
"""Grade every eval run against its assertions, blind to which skill version produced it.

The grader sees only the user's message, the assistant's reply, and the assertion
list. It never learns whether the reply came from the current skill or the
snapshot, so it cannot favour either. Verdicts are forced into the viewer's
expected shape (text / passed / evidence) by a JSON schema.
"""

import json
import pathlib
import subprocess
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor

REPO = pathlib.Path("/Users/nke/projects/ai/ai-skills")
ITER = REPO / "skills/ask-questions-workspace/iteration-1"
CWD = pathlib.Path("/tmp/aq-eval-cwd")
CONFIGS = ("with_skill", "old_skill")

MODEL = "sonnet"
EFFORT = "high"
CONCURRENCY = 5
TIMEOUT_S = 600

SCHEMA = json.dumps(
    {
        "type": "object",
        "properties": {
            "expectations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "passed": {"type": "boolean"},
                        "evidence": {"type": "string"},
                    },
                    "required": ["text", "passed", "evidence"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["expectations"],
        "additionalProperties": False,
    }
)

TEMPLATE = """You are grading one assistant reply against a fixed checklist. Be strict and literal: an assertion passes only when the reply actually demonstrates it, not when the reply is merely good or gestures in the right direction. A generous grader makes the whole benchmark useless, because it stops distinguishing between versions.

THE USER'S MESSAGE:
---
{prompt}
---

THE ASSISTANT'S REPLY:
---
{response}
---

THE ASSERTIONS, in order:
{assertions}

For each assertion, in the same order, return an object with:
- "text": the assertion, copied verbatim
- "passed": true only if the reply clearly satisfies it
- "evidence": a short quotation from the reply that justifies your verdict, or a specific statement of what is missing when it fails

Return every assertion, in the original order.
"""


def grade_one(eval_dir: pathlib.Path, config: str) -> str:
    try:
        return _grade_one(eval_dir, config)
    except Exception as exc:  # noqa: BLE001
        (eval_dir / config / "grading_error.txt").write_text(traceback.format_exc())
        return f"CRASH {eval_dir.name}/{config}: {exc!r}"


def _grade_one(eval_dir: pathlib.Path, config: str) -> str:
    out_dir = eval_dir / config
    resp = out_dir / "outputs" / "response.md"
    tag = f"{eval_dir.name}/{config}"
    if not resp.exists():
        return f"SKIP {tag} (no response.md)"

    meta = json.loads((eval_dir / "eval_metadata.json").read_text())
    assertions = meta["assertions"]
    numbered = "\n".join(f"{i + 1}. {a}" for i, a in enumerate(assertions))

    prompt = TEMPLATE.format(
        prompt=meta["prompt"],
        response=resp.read_text().strip(),
        assertions=numbered,
    )

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
        "",
        "--json-schema",
        SCHEMA,
        "--output-format",
        "json",
        "--no-session-persistence",
    ]
    proc = subprocess.run(cmd, cwd=CWD, capture_output=True, text=True, timeout=TIMEOUT_S)
    if proc.returncode != 0:
        raise RuntimeError(f"exit {proc.returncode}: {proc.stderr[:800]}")

    events = json.loads(proc.stdout)
    result = next(e for e in reversed(events) if e.get("type") == "result")
    if result.get("is_error"):
        raise RuntimeError(f"grader error: {json.dumps(result)[:800]}")

    payload = result.get("result")
    if isinstance(payload, str):
        payload = json.loads(payload)
    exps = payload["expectations"]

    # Guard against a grader that drops or invents assertions -- realign to the
    # canonical list so the aggregate counts stay comparable across runs.
    by_text = {e["text"].strip(): e for e in exps}
    aligned = []
    for i, a in enumerate(assertions):
        e = by_text.get(a.strip()) or (exps[i] if i < len(exps) else None)
        aligned.append(
            {
                "text": a,
                "passed": bool(e["passed"]) if e else False,
                "evidence": (e or {}).get("evidence", "grader returned no verdict"),
            }
        )

    passed = sum(1 for e in aligned if e["passed"])
    (out_dir / "grading.json").write_text(
        json.dumps(
            {
                "eval_id": meta["eval_id"],
                "eval_name": meta["eval_name"],
                "config": config,
                "expectations": aligned,
                "passed_count": passed,
                "total_count": len(aligned),
                "pass_rate": round(passed / len(aligned), 3) if aligned else 0.0,
            },
            indent=2,
        )
        + "\n"
    )

    return f"ok {tag}: {passed}/{len(aligned)}"


def main() -> int:
    eval_dirs = sorted(
        (d for d in ITER.iterdir() if d.is_dir() and d.name.startswith("eval-")),
        key=lambda p: int(p.name.split("-")[1]),
    )
    jobs = [(d, c) for d in eval_dirs for c in CONFIGS]
    print(f"grading {len(jobs)} runs, concurrency {CONCURRENCY}", flush=True)

    failures = 0
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as pool:
        for line in pool.map(lambda a: grade_one(*a), jobs):
            print(line, flush=True)
            if not line.startswith("ok "):
                failures += 1

    print(f"\ndone. {len(jobs) - failures}/{len(jobs)} graded.", flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
