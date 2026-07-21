"""Tests for the optional static-analysis script `scripts/check_render.py`.

These tests live under the skill-root `evals/` directory, which the packager's
`ROOT_EXCLUDE_DIRS = {"evals"}` drops from the distributed `.skill` archive, so
they never ship to an installed user (design Decision 3a).

Run from this directory:

    python3 -m unittest
    # or
    python3 test_check_render.py

Each test names the defect it pins so a failure reads as a sentence about which
render-blocking defect the checker stopped catching.
"""

import sys
import unittest
from pathlib import Path

# The script under test lives in the sibling `scripts/` directory. Put it on the
# path so `import check_render` resolves to the real implementation.
EVALS_DIR = Path(__file__).resolve().parent
SKILL_DIR = EVALS_DIR.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
FIXTURES_DIR = EVALS_DIR / "fixtures"
sys.path.insert(0, str(SCRIPTS_DIR))

import check_render  # noqa: E402  (path set up above)


def codes(path: Path) -> set[str]:
    """Return the set of defect codes the checker reports for one file."""
    result = check_render.check_file(path)
    return {d.code for d in result.defects}


def fixture(name: str) -> Path:
    return FIXTURES_DIR / name


class EngineDetection(unittest.TestCase):
    def test_detects_vega_from_vg_json_extension(self):
        result = check_render.check_file(fixture("vega_good.vg.json"))
        self.assertEqual(result.engine, "vega")

    def test_detects_d3_from_html_with_d3_import(self):
        result = check_render.check_file(fixture("d3_good.html"))
        self.assertEqual(result.engine, "d3")

    def test_detects_mermaid_from_html_with_mermaid_block(self):
        result = check_render.check_file(fixture("mermaid_good.html"))
        self.assertEqual(result.engine, "mermaid")

    def test_detects_mermaid_from_markdown_fenced_block(self):
        result = check_render.check_file(fixture("mermaid_good.md"))
        self.assertEqual(result.engine, "mermaid")

    def test_unsupported_input_is_not_applicable(self):
        result = check_render.check_file(fixture("unsupported.txt"))
        self.assertFalse(result.applicable)
        self.assertEqual(result.defects, [])


class VegaChecks(unittest.TestCase):
    def test_good_vega_spec_is_clean(self):
        result = check_render.check_file(fixture("vega_good.vg.json"))
        self.assertTrue(result.applicable)
        self.assertEqual(result.defects, [], msg=[d.message for d in result.defects])

    def test_flags_nonzero_bar_baseline(self):
        self.assertIn(
            "vega-nonzero-baseline", codes(fixture("vega_broken_nonzero_baseline.vg.json"))
        )

    def test_flags_encoding_field_absent_from_data(self):
        self.assertIn("vega-missing-field", codes(fixture("vega_broken_missing_field.vg.json")))

    def test_flags_malformed_json(self):
        self.assertIn("vega-malformed-json", codes(fixture("vega_broken_malformed.vg.json")))


class D3Checks(unittest.TestCase):
    def test_good_d3_artifact_is_clean(self):
        result = check_render.check_file(fixture("d3_good.html"))
        self.assertTrue(result.applicable)
        self.assertEqual(result.defects, [], msg=[d.message for d in result.defects])

    def test_flags_missing_cdn_or_render_call(self):
        found = codes(fixture("d3_broken_no_cdn.html"))
        self.assertTrue(
            {"d3-missing-cdn", "d3-missing-render-call"} & found,
            msg=f"expected a CDN or render-call defect, got {found}",
        )

    def test_flags_scrolljacking(self):
        self.assertIn("html-scroll-containment", codes(fixture("d3_broken_scrolljack.html")))

    def test_flags_interactive_marks_without_keyboard_wiring(self):
        self.assertIn("html-keyboard-wiring", codes(fixture("d3_broken_no_keyboard.html")))


class MermaidChecks(unittest.TestCase):
    def test_good_mermaid_html_is_clean(self):
        result = check_render.check_file(fixture("mermaid_good.html"))
        self.assertTrue(result.applicable)
        self.assertEqual(result.defects, [], msg=[d.message for d in result.defects])

    def test_good_mermaid_markdown_is_clean(self):
        result = check_render.check_file(fixture("mermaid_good.md"))
        self.assertTrue(result.applicable)
        self.assertEqual(result.defects, [], msg=[d.message for d in result.defects])

    def test_flags_unrecognized_or_unbalanced_source(self):
        found = codes(fixture("mermaid_broken_source.md"))
        self.assertTrue(
            {"mermaid-unknown-diagram", "mermaid-unbalanced"} & found,
            msg=f"expected an unknown-diagram or unbalanced defect, got {found}",
        )

    def test_flags_html_bundle_missing_mermaid_wiring(self):
        self.assertIn("mermaid-missing-wiring", codes(fixture("mermaid_broken_no_wiring.html")))


class RenderBlockingVerdict(unittest.TestCase):
    """A result exposes whether any reported defect is render-blocking, which the
    CLI maps to its exit code."""

    def test_clean_good_artifact_is_not_render_blocking(self):
        result = check_render.check_file(fixture("vega_good.vg.json"))
        self.assertFalse(result.has_render_blocking())

    def test_broken_artifact_is_render_blocking(self):
        result = check_render.check_file(fixture("vega_broken_missing_field.vg.json"))
        self.assertTrue(result.has_render_blocking())


if __name__ == "__main__":
    unittest.main()
