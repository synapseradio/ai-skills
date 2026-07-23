#!/usr/bin/env python3
"""Tests for bin/generate-openai-plugin.py.

The repo has no test framework, so this uses stdlib ``unittest`` and adds no dependency
beyond the PyYAML the packager already requires.

Run:  python3 bin/generate-openai-plugin_test.py
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

# The generator is a hyphenated executable, so load it by path. It must be registered in
# sys.modules before exec_module, or its dataclasses cannot resolve their own annotations.
_SPEC = importlib.util.spec_from_file_location(
    "generate_openai_plugin", Path(__file__).with_name("generate-openai-plugin.py")
)
assert _SPEC and _SPEC.loader
gen = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = gen
_SPEC.loader.exec_module(gen)


class FrontmatterTests(unittest.TestCase):
    """The structural pass: reduce to name and description, both verbatim."""

    def test_drops_every_key_outside_the_codex_pair(self):
        emitted = gen.reduce_frontmatter(
            "name: demo\n"
            "description: Does a thing.\n"
            "license: EUPL-1.2\n"
            "allowed-tools:\n  - Read\n"
            "compatibility: anything\n"
            "metadata:\n  context: fork\n"
        )
        parsed = yaml.safe_load(emitted.removeprefix("---\n").removesuffix("---\n"))
        self.assertEqual(set(parsed), {"name", "description"})
        self.assertEqual(parsed["description"], "Does a thing.")

    def test_preserves_a_folded_description_verbatim(self):
        source = (
            'name: demo\ndescription: >-\n  Line one, with "quotes": and a colon.\n  Line two.\n'
        )
        expected = yaml.safe_load(source)["description"]
        emitted = gen.reduce_frontmatter(source)
        self.assertEqual(yaml.safe_load(emitted.strip("-\n"))["description"], expected)

    def test_rejects_an_empty_description(self):
        with self.assertRaises(gen.TransformError):
            gen.reduce_frontmatter("name: demo\ndescription: ''\n")


class EditTests(unittest.TestCase):
    """The prose pass fails loudly rather than emitting a half-transformed skill."""

    def test_applies_a_matching_edit(self):
        edit = gen.Edit(why="t", old="alpha", new="beta")
        self.assertEqual(gen.apply_edits("say alpha now", [edit], "SKILL.md"), "say beta now")

    def test_raises_when_the_source_text_moved(self):
        edit = gen.Edit(why="t", old="gone", new="x")
        with self.assertRaises(gen.TransformError):
            gen.apply_edits("nothing here", [edit], "SKILL.md")

    def test_raises_when_the_match_is_ambiguous(self):
        edit = gen.Edit(why="t", old="dup", new="x")
        with self.assertRaises(gen.TransformError):
            gen.apply_edits("dup and dup", [edit], "SKILL.md")

    def test_edits_are_scoped_to_their_own_file(self):
        edit = gen.Edit(why="t", old="alpha", new="beta", file="references/other.md")
        self.assertEqual(gen.apply_edits("alpha", [edit], "SKILL.md"), "alpha")


class EmittedTreeTests(unittest.TestCase):
    """Acceptance checks against a freshly generated tree."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="openai-thinkies-"))
        cls.result = gen.generate(gen.SOURCE_DIR, cls.tmp)
        cls.skills_root = cls.tmp / "skills"

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_every_source_skill_is_present(self):
        source_names = sorted(
            p.name for p in gen.SOURCE_DIR.iterdir() if (p / "SKILL.md").is_file()
        )
        emitted_names = sorted(p.name for p in self.skills_root.iterdir() if p.is_dir())
        self.assertEqual(emitted_names, source_names)
        self.assertEqual(len(emitted_names), 48)

    def test_skill_folders_are_flat_with_no_group_level(self):
        self.assertFalse((self.skills_root / "thinkies").exists())
        for skill in self.skills_root.iterdir():
            self.assertTrue((skill / "SKILL.md").is_file(), skill)

    def test_no_forbidden_token_survives(self):
        gen.check_no_forbidden_tokens(self.tmp)

    def test_excluded_source_files_stay_out(self):
        self.assertEqual(list(self.skills_root.rglob("README.md")), [])
        self.assertEqual(list(self.skills_root.rglob("evals")), [])

    def test_frontmatter_holds_exactly_name_and_description(self):
        for skill_md in sorted(self.skills_root.glob("*/SKILL.md")):
            frontmatter, _ = gen.split_frontmatter(skill_md.read_text())
            parsed = yaml.safe_load(frontmatter)
            self.assertEqual(set(parsed), {"name", "description"}, skill_md)
            self.assertTrue(parsed["name"].strip(), skill_md)
            self.assertTrue(parsed["description"].strip(), skill_md)

    def test_description_matches_the_source_verbatim(self):
        for skill_md in sorted(self.skills_root.glob("*/SKILL.md")):
            source_md = gen.SOURCE_DIR / skill_md.parent.name / "SKILL.md"
            emitted, _ = gen.split_frontmatter(skill_md.read_text())
            original, _ = gen.split_frontmatter(source_md.read_text())
            self.assertEqual(
                yaml.safe_load(emitted)["description"],
                yaml.safe_load(original)["description"],
                skill_md,
            )

    def test_name_matches_its_directory(self):
        for skill_md in sorted(self.skills_root.glob("*/SKILL.md")):
            frontmatter, _ = gen.split_frontmatter(skill_md.read_text())
            self.assertEqual(yaml.safe_load(frontmatter)["name"], skill_md.parent.name)

    def test_qualified_names_fit_the_loader_limit(self):
        for skill in sorted(p.name for p in self.skills_root.iterdir() if p.is_dir()):
            self.assertLessEqual(len(f"thinkies:{skill}"), gen.QUALIFIED_NAME_LIMIT, skill)

    def test_manifest_parses_and_points_at_the_skills_directory(self):
        manifest = json.loads((self.tmp / ".codex-plugin" / "plugin.json").read_text())
        self.assertEqual(manifest["name"], "thinkies")
        self.assertEqual(manifest["skills"], "./skills/")
        for required in ("version", "description", "license", "repository"):
            self.assertTrue(manifest[required], required)

    def test_only_the_manifest_lives_in_codex_plugin(self):
        entries = sorted(p.name for p in (self.tmp / ".codex-plugin").iterdir())
        self.assertEqual(entries, ["plugin.json"])

    def test_visualize_keeps_its_scripts_and_no_python_fallback(self):
        visualize = self.skills_root / "visualize"
        self.assertTrue((visualize / "scripts" / "visualizer.py").is_file())
        self.assertIn(
            "If not: the saved file is the final artifact",
            (visualize / "references" / "phase-present.md").read_text(),
        )

    def test_regenerating_produces_an_identical_tree(self):
        second = Path(tempfile.mkdtemp(prefix="openai-thinkies-again-"))
        try:
            gen.generate(gen.SOURCE_DIR, second)
            first_files = {
                p.relative_to(self.tmp): p.read_bytes() for p in self.tmp.rglob("*") if p.is_file()
            }
            second_files = {
                p.relative_to(second): p.read_bytes() for p in second.rglob("*") if p.is_file()
            }
            self.assertEqual(sorted(first_files), sorted(second_files))
            self.assertEqual(first_files, second_files)
        finally:
            shutil.rmtree(second, ignore_errors=True)

    def test_source_tree_is_never_written_to(self):
        before = {p: p.stat().st_mtime_ns for p in gen.SOURCE_DIR.rglob("*") if p.is_file()}
        third = Path(tempfile.mkdtemp(prefix="openai-thinkies-ro-"))
        try:
            gen.generate(gen.SOURCE_DIR, third)
        finally:
            shutil.rmtree(third, ignore_errors=True)
        after = {p: p.stat().st_mtime_ns for p in gen.SOURCE_DIR.rglob("*") if p.is_file()}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main(verbosity=2)
