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


SHAPED = {
    "flow": ("--shape", "sankey", "--source", "from", "--target", "to", "--value", "visits"),
    "calls": (
        "--shape",
        "network",
        "--source",
        "caller",
        "--target",
        "callee",
        "--value",
        "calls",
        "--nodes",
        FIXTURES / "services.csv",
        "--node-group",
        "team",
    ),
    "internet": ("--shape", "choropleth", "--region", "country", "--value", "share"),
    "wards": (
        "--shape",
        "choropleth",
        "--region",
        "ward",
        "--value",
        "trees",
        "--geojson",
        FIXTURES / "wards.geojson",
        "--feature-id",
        "code",
        "--feature-name",
        "name",
    ),
}


class ShapedWorkspace(Workspace):
    def prepare(self, source, *args) -> subprocess.CompletedProcess:
        return run("prepare_data.py", source, *args, "--out", self.dir / "prepared.json")

    def prepared(self, name: str) -> Path:
        result = self.prepare(FIXTURES / f"{name}.csv", *SHAPED[name])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return self.dir / "prepared.json"

    def build(self, spec, data) -> subprocess.CompletedProcess:
        return run("build_page.py", spec, "--data", data, "--out", self.dir / "page.html")

    def page(self, name: str) -> Path:
        result = self.build(FIXTURES / f"{name}.spec.json", self.prepared(name))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return self.dir / "page.html"

    def edited(self, name: str, old: str, new: str) -> Path:
        text = self.page(name).read_text(encoding="utf-8")
        self.assertIn(old, text)
        return self.write("edited.html", text.replace(old, new))

    def spec_without(self, name: str, section: str, key: str) -> Path:
        spec = json.loads((FIXTURES / f"{name}.spec.json").read_text(encoding="utf-8"))
        del spec[section][key]
        return self.write("spec.json", json.dumps(spec))


class PreparingFlowsAndNetworks(ShapedWorkspace):
    def test_a_balanced_flow_comes_out_as_nodes_and_links(self):
        prepared = json.loads(self.prepared("flow").read_text(encoding="utf-8"))
        self.assertEqual(len(prepared["nodes"]), 5)
        self.assertEqual(len(prepared["links"]), 6)
        self.assertEqual(
            prepared["links"][0], {"source": "Landing", "target": "Sign-up", "value": 620}
        )

    def test_a_stage_that_sends_out_less_than_it_takes_in_stops_the_run(self):
        source = self.write("leak.csv", "from,to,visits\nA,B,10\nB,C,7\n")
        result = self.prepare(source, *SHAPED["flow"])
        self.assertEqual(result.returncode, 1)
        self.assertEqual(codes(result), {"unbalanced-node"})
        self.assertFalse((self.dir / "prepared.json").exists())

    def test_a_flow_that_loops_back_stops_the_run(self):
        source = self.write("loop.csv", "from,to,visits\nA,B,5\nB,C,5\nC,A,5\n")
        self.assertEqual(codes(self.prepare(source, *SHAPED["flow"])), {"cycle"})

    def test_a_flow_of_zero_stops_the_run(self):
        source = self.write("zero.csv", "from,to,visits\nA,B,0\n")
        self.assertEqual(codes(self.prepare(source, *SHAPED["flow"])), {"not-positive"})

    def test_a_link_to_a_node_the_nodes_file_lacks_stops_the_run(self):
        source = self.write("calls.csv", "caller,callee,calls\nweb,api,9\napi,cache,4\n")
        result = self.prepare(source, *SHAPED["calls"])
        self.assertEqual(result.returncode, 1)
        self.assertEqual(codes(result), {"unknown-node"})

    def test_the_same_pair_linked_in_both_directions_stops_a_network(self):
        source = self.write("calls.csv", "caller,callee,calls\nweb,api,9\napi,web,4\n")
        self.assertEqual(codes(self.prepare(source, *SHAPED["calls"])), {"duplicate-key"})

    def test_a_node_linked_to_itself_stops_a_network(self):
        source = self.write("calls.csv", "caller,callee,calls\nweb,web,9\n")
        self.assertEqual(codes(self.prepare(source, *SHAPED["calls"])), {"self-link"})

    def test_network_nodes_keep_their_group(self):
        prepared = json.loads(self.prepared("calls").read_text(encoding="utf-8"))
        self.assertEqual(prepared["groupValues"], ["Front", "Platform", "Commerce"])
        self.assertEqual(prepared["nodes"][0], {"id": "web", "label": "web", "group": "Front"})


class PreparingRegions(ShapedWorkspace):
    def test_a_country_code_and_a_country_name_both_join_the_atlas(self):
        prepared = json.loads(self.prepared("internet").read_text(encoding="utf-8"))
        keys = {region["key"] for region in prepared["regions"]}
        self.assertLessEqual({"United States of America", "Norway"}, keys)
        self.assertEqual(len(prepared["regions"]), 9)

    def test_a_region_the_atlas_lacks_stops_the_run(self):
        source = self.write("bad.csv", "country,share\nNorway,99\nAtlantis,50\n")
        result = self.prepare(source, *SHAPED["internet"])
        self.assertEqual(result.returncode, 1)
        self.assertEqual(codes(result), {"unknown-region"})

    def test_one_country_given_by_name_and_by_code_stops_the_run(self):
        source = self.write("twice.csv", "country,share\nNorway,99\n578,98\n")
        self.assertEqual(codes(self.prepare(source, *SHAPED["internet"])), {"duplicate-key"})

    def test_a_region_the_geojson_lacks_stops_the_run(self):
        source = self.write("bad.csv", "ward,trees\nN,410\nQ,5\n")
        self.assertEqual(codes(self.prepare(source, *SHAPED["wards"])), {"unknown-region"})

    def test_counterclockwise_rings_come_out_clockwise(self):
        given = json.loads((FIXTURES / "wards.geojson").read_text(encoding="utf-8"))
        prepared = json.loads(self.prepared("wards").read_text(encoding="utf-8"))
        ring = given["features"][0]["geometry"]["coordinates"][0]
        self.assertEqual(prepared["features"][0]["geometry"]["coordinates"][0], ring[::-1])

    def test_a_geojson_point_stops_the_run(self):
        geojson = json.loads((FIXTURES / "wards.geojson").read_text(encoding="utf-8"))
        geojson["features"][0]["geometry"] = {"type": "Point", "coordinates": [13.3, 52.5]}
        args = list(SHAPED["wards"])
        args[args.index("--geojson") + 1] = self.write("points.geojson", json.dumps(geojson))
        source = self.write("wards.csv", "ward,trees\nS,265\nE,120\n")
        self.assertEqual(codes(self.prepare(source, *args)), {"not-a-region"})


class BuildingShapedPages(ShapedWorkspace):
    def test_each_kind_builds_a_page_that_passes_the_output_check(self):
        for name in SHAPED:
            with self.subTest(name):
                result = run("check_output.py", self.page(name))
                self.assertEqual(result.returncode, 0, result.stdout)
                self.assertEqual(codes(result), set())

    def test_a_chart_kind_is_refused_data_of_another_shape(self):
        for spec, data in (("flow", "calls"), ("calls", "internet"), ("internet", "flow")):
            with self.subTest(spec=spec, data=data):
                result = self.build(FIXTURES / f"{spec}.spec.json", self.prepared(data))
                self.assertEqual(result.returncode, 1)
                self.assertEqual(codes(result), {"chart-data-mismatch"})
                self.assertFalse((self.dir / "page.html").exists())

    def test_a_bar_chart_is_refused_network_data(self):
        result = self.build(FIXTURES / "coffee.spec.json", self.prepared("calls"))
        self.assertEqual(codes(result), {"chart-data-mismatch"})

    def test_a_flow_without_a_unit_is_refused(self):
        result = self.build(self.spec_without("flow", "value", "unit"), self.prepared("flow"))
        self.assertEqual(codes(result), {"spec-missing"})

    def test_a_map_without_a_unit_is_refused(self):
        spec = self.spec_without("internet", "value", "unit")
        self.assertEqual(codes(self.build(spec, self.prepared("internet"))), {"spec-missing"})

    def test_a_network_past_the_readable_node_count_is_refused(self):
        links = "".join(f"hub,leaf{index},1\n" for index in range(61))
        source = self.write("big.csv", "caller,callee,calls\n" + links)
        prepared = self.prepare(
            source, "--shape", "network", "--source", "caller", "--target", "callee"
        )
        self.assertEqual(prepared.returncode, 0, prepared.stdout)
        spec = self.write(
            "spec.json",
            json.dumps(
                {"title": "t", "summary": "s", "chart": "network", "nodes": {"label": "Service"}}
            ),
        )
        self.assertEqual(codes(self.build(spec, self.dir / "prepared.json")), {"too-many-nodes"})

    def test_a_map_where_every_region_holds_one_value_is_refused(self):
        source = self.write("flat.csv", "country,share\nNorway,50\nChad,50\n")
        self.assertEqual(self.prepare(source, *SHAPED["internet"]).returncode, 0)
        result = self.build(FIXTURES / "internet.spec.json", self.dir / "prepared.json")
        self.assertEqual(codes(result), {"constant-values"})


class CheckingShapedPages(ShapedWorkspace):
    def test_a_link_to_a_node_the_page_lacks_is_reported(self):
        page = self.edited("flow", '"target": "Paid"', '"target": "Refunded"')
        self.assertEqual(codes(run("check_output.py", page)), {"link-unknown-node"})

    def test_a_network_page_that_lost_its_link_table_is_reported(self):
        text = self.page("calls").read_text(encoding="utf-8")
        start = text.index("<table>", text.index("</table>"))
        end = text.index("</table>", start) + len("</table>")
        page = self.write("edited.html", text[:start] + text[end:])
        self.assertIn("no-table", codes(run("check_output.py", page)))

    def test_an_atlas_at_another_version_is_reported(self):
        page = self.edited("internet", "world-atlas@2.0.2", "world-atlas@2.0.1")
        self.assertEqual(codes(run("check_output.py", page)), {"foreign-import"})

    def test_a_projection_import_outside_a_map_page_is_reported(self):
        page = self.edited(
            "flow", "const data =", "await import('https://esm.sh/d3-geo@3.1.1')\nconst data ="
        )
        self.assertEqual(codes(run("check_output.py", page)), {"foreign-import"})

    def test_a_region_with_no_shape_on_the_map_is_reported(self):
        page = self.edited("wards", '"key": "N"', '"key": "Q"')
        self.assertEqual(codes(run("check_output.py", page)), {"region-unmatched"})

    def test_a_ramp_too_flat_to_rank_regions_is_reported(self):
        page = self.edited(
            "internet", '"ramp": ["#deebf7", "#08519c"]', '"ramp": ["#deebf7", "#c6dbef"]'
        )
        self.assertEqual(codes(run("check_output.py", page)), {"ramp-flat"})


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
