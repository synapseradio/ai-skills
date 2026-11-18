"""Tests for the scripts in `scripts/`, driven through their command lines.

Run from this directory:

    uv run --no-project python -m unittest
"""

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

EVALS = Path(__file__).resolve().parent
SCRIPTS = EVALS.parent / "scripts"
FIXTURES = EVALS / "fixtures"


def run(script: str, *args) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *map(str, args)], capture_output=True, text=True
    )


def codes(result: subprocess.CompletedProcess) -> set:
    """The problem or defect codes a script printed, one per reported line."""
    found = set()
    for line in result.stdout.splitlines():
        match = re.match(r"^(?:problem|.+?\.(?:html|md)): ([a-z-]+): ", line)
        if match:
            found.add(match.group(1))
    return found


class Workspace(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.dir = Path(folder.name)

    def write(self, name: str, text: str) -> Path:
        path = self.dir / name
        path.write_text(text, encoding="utf-8")
        return path

    def prepared_coffee(self) -> Path:
        out = self.dir / "rows.json"
        result = run(
            "prepare_data.py",
            FIXTURES / "coffee.csv",
            "--x",
            "day",
            "--y",
            "cups",
            "--series",
            "person",
            "--out",
            out,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return out

    def coffee_page(self) -> Path:
        page = self.dir / "coffee.html"
        result = run(
            "build_page.py",
            FIXTURES / "coffee.spec.json",
            "--data",
            self.prepared_coffee(),
            "--out",
            page,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return page

    def edited_page(self, old: str, new: str) -> Path:
        text = self.coffee_page().read_text(encoding="utf-8")
        self.assertIn(old, text)
        return self.write("edited.html", text.replace(old, new))


class PreparingData(Workspace):
    def test_rows_come_out_typed_and_complete(self):
        prepared = json.loads(self.prepared_coffee().read_text(encoding="utf-8"))
        self.assertEqual(prepared["xType"], "date")
        self.assertEqual(prepared["seriesValues"], ["Ana", "Ben"])
        self.assertEqual(prepared["rows"][0], {"day": "2026-11-09", "cups": 2, "person": "Ana"})
        self.assertEqual(len(prepared["rows"]), 6)

    def test_a_measure_that_is_not_a_number_stops_the_run_and_writes_nothing(self):
        source = self.write("bad.csv", "day,cups\n2026-11-09,2\n2026-11-10,three\n")
        out = self.dir / "rows.json"
        result = run("prepare_data.py", source, "--x", "day", "--y", "cups", "--out", out)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(codes(result), {"not-a-number"})
        self.assertFalse(out.exists())

    def test_two_rows_for_one_position_stop_the_run(self):
        source = self.write("dup.csv", "day,cups\n2026-11-09,2\n2026-11-09,5\n")
        result = run(
            "prepare_data.py", source, "--x", "day", "--y", "cups", "--out", self.dir / "rows.json"
        )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(codes(result), {"duplicate-key"})

    def test_a_missing_value_stops_the_run_unless_dropping_is_asked_for(self):
        source = self.write("gap.csv", "day,cups\n2026-11-09,2\n2026-11-10,\n2026-11-11,4\n")
        out = self.dir / "rows.json"
        refused = run("prepare_data.py", source, "--x", "day", "--y", "cups", "--out", out)
        self.assertEqual(codes(refused), {"missing-value"})
        dropped = run(
            "prepare_data.py", source, "--x", "day", "--y", "cups", "--drop-missing", "--out", out
        )
        self.assertEqual(dropped.returncode, 0)
        self.assertEqual(len(json.loads(out.read_text(encoding="utf-8"))["rows"]), 2)


class BuildingPages(Workspace):
    def test_a_built_page_passes_the_output_check(self):
        result = run("check_output.py", self.coffee_page())
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(codes(result), set())

    def test_a_line_over_unordered_categories_is_refused(self):
        source = self.write("teams.csv", "team,points\nRed,3\nBlue,5\nGreen,4\n")
        rows = self.dir / "teams.json"
        run("prepare_data.py", source, "--x", "team", "--y", "points", "--out", rows)
        spec = self.write(
            "spec.json",
            json.dumps(
                {
                    "title": "Blue leads",
                    "summary": "Blue has 5 points.",
                    "chart": "line",
                    "x": {"label": "Team"},
                    "y": {"label": "Score", "unit": "points"},
                }
            ),
        )
        page = self.dir / "teams.html"
        result = run("build_page.py", spec, "--data", rows, "--out", page)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(codes(result), {"chart-data-mismatch"})
        self.assertFalse(page.exists())

    def test_a_spec_without_a_unit_is_refused(self):
        spec = json.loads((FIXTURES / "coffee.spec.json").read_text(encoding="utf-8"))
        del spec["y"]["unit"]
        result = run(
            "build_page.py",
            self.write("spec.json", json.dumps(spec)),
            "--data",
            self.prepared_coffee(),
            "--out",
            self.dir / "page.html",
        )
        self.assertEqual(codes(result), {"spec-missing"})


class CheckingPages(Workspace):
    def test_a_second_library_is_reported(self):
        page = self.edited_page(
            "const data =", "await import('https://esm.sh/lodash-es@4.17.21')\nconst data ="
        )
        self.assertEqual(codes(run("check_output.py", page)), {"foreign-import"})

    def test_an_unpinned_chart_library_is_reported(self):
        page = self.edited_page("@tanstack/charts@1.5.0/dom", "@tanstack/charts/dom")
        self.assertEqual(codes(run("check_output.py", page)), {"unpinned-import"})

    def test_a_table_that_lost_a_row_is_reported(self):
        page = self.edited_page(
            '<tr><td>2026-11-09</td><td>Ana</td><td class="num">2</td></tr>\n', ""
        )
        self.assertEqual(codes(run("check_output.py", page)), {"table-row-mismatch"})

    def test_two_series_colours_a_reader_cannot_tell_apart_are_reported(self):
        page = self.edited_page(
            '"colors": ["#0072b2", "#d55e00"]', '"colors": ["#0072b2", "#0072b3"]'
        )
        self.assertEqual(codes(run("check_output.py", page)), {"color-confusable"})

    def test_a_series_colour_too_pale_for_its_background_is_reported(self):
        page = self.edited_page(
            '"colors": ["#0072b2", "#d55e00"]', '"colors": ["#0072b2", "#ffff00"]'
        )
        self.assertEqual(codes(run("check_output.py", page)), {"color-low-contrast"})

    def test_a_page_without_a_text_summary_is_reported(self):
        page = self.edited_page(
            "Ben rose from 3 to 4 cups a day. Ana stayed between 1 and 3.</p>", "</p>"
        )
        self.assertIn("no-summary", codes(run("check_output.py", page)))


class CheckingMarkdown(unittest.TestCase):
    def test_a_well_formed_diagram_passes(self):
        self.assertEqual(run("check_output.py", FIXTURES / "mermaid_good.md").returncode, 0)

    def test_an_unknown_diagram_type_with_open_brackets_is_reported(self):
        result = run("check_output.py", FIXTURES / "mermaid_broken_source.md")
        self.assertEqual(codes(result), {"mermaid-unknown-type", "mermaid-unbalanced"})

    def test_bars_in_proportion_to_their_values_pass(self):
        self.assertEqual(run("check_output.py", FIXTURES / "bars_good.md").returncode, 0)

    def test_a_bar_drawn_longer_than_its_value_is_reported(self):
        self.assertEqual(
            codes(run("check_output.py", FIXTURES / "bars_broken.md")), {"bar-not-proportional"}
        )


if __name__ == "__main__":
    unittest.main()
