#!/usr/bin/env python3
"""Tests for bin/sync-thinkies.py.

Run:  python3 bin/sync-thinkies_test.py
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "sync_thinkies", Path(__file__).with_name("sync-thinkies.py")
)
assert _SPEC and _SPEC.loader
sync = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = sync
_SPEC.loader.exec_module(sync)


class SectionTests(unittest.TestCase):
    def test_heading_at_end_of_file(self):
        self.assertEqual(sync.section("# T\n\n## Steps\n\nbody\n", "Steps"), "body\n")

    def test_stops_at_the_next_level_two_heading(self):
        text = "## Steps\n\none\n\n## Output\n\ntwo\n"
        self.assertEqual(sync.section(text, "Steps"), "one\n")

    def test_keeps_level_three_headings_inside(self):
        text = "## Steps\n\n### 1. A\n\na\n\n### 2. B\n\nb\n## Next\n"
        self.assertEqual(sync.section(text, "Steps"), "### 1. A\n\na\n\n### 2. B\n\nb\n")

    def test_missing_heading(self):
        self.assertIsNone(sync.section("## Other\n", "Steps"))


class CheckTests(unittest.TestCase):
    """Each case runs check() on a temp copy of the parts of the repo it reads."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        for rel in (sync.SKILLS, sync.CANON, sync.BUNDLE, sync.PLUGIN_JSON.parent):
            shutil.copytree(sync.REPO_ROOT / rel, self.tmp / rel)
        with contextlib.redirect_stdout(io.StringIO()):
            sync.write(self.tmp)
        self.baseline = set(sync.check(self.tmp))

    def new_problems(self):
        return set(sync.check(self.tmp)) - self.baseline

    def test_flags_a_one_byte_drift_in_a_reference_copy(self):
        ref = self.tmp / sync.SKILLS / "ponder" / "references" / "wonder.md"
        ref.write_text(ref.read_text() + "x")
        problems = self.new_problems()
        self.assertTrue(any("ponder/references/wonder.md" in p for p in problems), problems)

    def test_flags_a_template_line_that_lacks_at(self):
        skill = self.tmp / sync.SKILLS / "save-note" / "SKILL.md"
        canon = (self.tmp / sync.CANON / "record.md").read_text().strip()
        skill.write_text(
            "---\nname: save-note\ndescription: d\n---\n\n## Record\n\n"
            f"{canon}\n\nFile: `save-note_[t]_[topic].jsonl`\n\n```jsonl\n"
            '{"kind": "result", "text": "[result]"}\n```\n'
        )
        problems = self.new_problems()
        self.assertTrue(any("must start with kind, at" in p for p in problems), problems)

    def test_flags_a_top_level_context_key(self):
        skill = self.tmp / sync.SKILLS / "wonder" / "SKILL.md"
        skill.write_text(
            skill.read_text().replace("name: wonder\n", "name: wonder\ncontext: fork\n")
        )
        problems = self.new_problems()
        self.assertTrue(any("'context' is outside the spec" in p for p in problems), problems)


class RepoTests(unittest.TestCase):
    def test_repo_is_in_sync(self):
        self.assertEqual(sync.check(), [])


if __name__ == "__main__":
    unittest.main()
