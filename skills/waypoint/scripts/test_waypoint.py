#!/usr/bin/env python3
"""Tests for the waypoint CLI.

Zero-dependency: stdlib unittest only. Run from the skill directory with:

    python3 -m unittest scripts/test_waypoint.py

The tests pin the contract the rest of the skill depends on — ID determinism,
comment-syntax resolution, block composition in both single- and multi-flow
shapes, lenient parsing of the legacy `Map:` blocks that already exist in real
repos, drift detection, ID-correction output, and manifest rendering.
"""

from __future__ import annotations

import hashlib
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import waypoint  # noqa: E402


class TestComputeId(unittest.TestCase):
    """The waypoint ID is the first 8 hex chars of SHA-256 of the path string."""

    def test_matches_sha256_prefix(self):
        path = "config/rspack/browser/browser.plugins.ts"
        expected = hashlib.sha256(path.encode()).hexdigest()[:8]
        self.assertEqual(waypoint.compute_id(path), expected)

    def test_is_eight_hex_chars(self):
        wp_id = waypoint.compute_id("a/b/c.py")
        self.assertEqual(len(wp_id), 8)
        self.assertTrue(all(c in "0123456789abcdef" for c in wp_id))

    def test_deterministic(self):
        self.assertEqual(waypoint.compute_id("x/y.go"), waypoint.compute_id("x/y.go"))

    def test_path_sensitive(self):
        self.assertNotEqual(waypoint.compute_id("a/x.py"), waypoint.compute_id("b/x.py"))


class TestRelPath(unittest.TestCase):
    """Paths are normalized relative to the git root before hashing."""

    def test_strips_root_prefix(self):
        rel = waypoint.to_relpath("/repo/src/app.ts", "/repo")
        self.assertEqual(rel, "src/app.ts")

    def test_already_relative_passthrough(self):
        # A path already relative to root resolves to itself.
        rel = waypoint.to_relpath("/repo/a/b.py", "/repo")
        self.assertEqual(rel, "a/b.py")


class TestCommentStyle(unittest.TestCase):
    """Extension determines comment syntax deterministically."""

    def test_hash_languages(self):
        for name in ["x.py", "x.sh", "x.rb", "x.yml", "x.yaml", "x.toml", "Dockerfile", "Makefile"]:
            self.assertEqual(waypoint.comment_style(name), ("line", "#"), name)

    def test_slash_languages(self):
        for name in [
            "x.js",
            "x.ts",
            "x.tsx",
            "x.jsx",
            "x.go",
            "x.rs",
            "x.java",
            "x.c",
            "x.cpp",
            "x.h",
        ]:
            self.assertEqual(waypoint.comment_style(name), ("line", "//"), name)

    def test_dash_languages(self):
        for name in ["x.sql", "x.lua"]:
            self.assertEqual(waypoint.comment_style(name), ("line", "--"), name)

    def test_block_css(self):
        self.assertEqual(waypoint.comment_style("x.css"), ("block", ("/*", "*/")))
        self.assertEqual(waypoint.comment_style("x.scss"), ("block", ("/*", "*/")))

    def test_block_markup(self):
        for name in ["x.html", "x.xml", "x.vue", "x.md"]:
            self.assertEqual(waypoint.comment_style(name), ("block", ("<!--", "-->")), name)

    def test_fallback_is_hash(self):
        self.assertEqual(waypoint.comment_style("x.weirdext"), ("line", "#"))

    def test_override(self):
        self.assertEqual(waypoint.comment_style("x.py", override="//"), ("line", "//"))


def _single_flow_spec():
    # docker-compose.ci.yml resolves to the `#` comment leader, which the
    # single-flow composition tests assert against.
    return {
        "file": "docker-compose.ci.yml",
        "flows": [
            {
                "pipeline": "sourcemap-upload",
                "role": "uploads browser sourcemaps to Sentry so minified errors resolve to source",
                "reference": ".ai/waypoints/sourcemap-upload.md",
                "neighbors": [
                    {
                        "dir": "from",
                        "id": "4263ae66",
                        "path": "docker-compose.ci.yml",
                        "desc": "passes the release version into this build",
                    },
                    {
                        "dir": "into",
                        "id": "80e5dc26",
                        "path": "browser.plugins.ts",
                        "desc": "uploads browser sourcemaps to Sentry",
                    },
                ],
            }
        ],
    }


def _multi_flow_spec():
    return {
        "file": "shared/version.ts",
        "flows": [
            {
                "pipeline": "sourcemap-upload",
                "role": "uploads browser sourcemaps to Sentry",
                "reference": ".ai/waypoints/sourcemap-upload.md",
                "neighbors": [
                    {
                        "dir": "from",
                        "id": "4263ae66",
                        "path": "docker-compose.ci.yml",
                        "desc": "passes the release version in",
                    },
                ],
            },
            {
                "pipeline": "changeset-release",
                "role": "bumps versions and tags the release",
                "reference": ".ai/waypoints/changeset-release.md",
                "neighbors": [
                    {
                        "dir": "into",
                        "id": "1a2b3c4d",
                        "path": "publish.yml",
                        "desc": "publishes the tagged packages to npm",
                    },
                ],
            },
        ],
    }


class TestComposeSingleFlow(unittest.TestCase):
    def setUp(self):
        self.spec = _single_flow_spec()
        self.wp_id = waypoint.compute_id(self.spec["file"])
        self.out = waypoint.compose_block(self.spec)

    def test_header_has_id_pipeline_reference(self):
        self.assertIn(
            f"# ── Waypoint {self.wp_id} · sourcemap-upload · reference: .ai/waypoints/sourcemap-upload.md",
            self.out,
        )

    def test_role_line(self):
        self.assertIn(
            "#    uploads browser sourcemaps to Sentry so minified errors resolve to source",
            self.out,
        )

    def test_neighbor_lines(self):
        self.assertIn(
            "#    ← 4263ae66  docker-compose.ci.yml — passes the release version into this build",
            self.out,
        )
        self.assertIn(
            "#    → 80e5dc26  browser.plugins.ts — uploads browser sourcemaps to Sentry", self.out
        )

    def test_closing_legend(self):
        self.assertIn(
            "# ── grep any 8-char ID to trace this pipeline · ← from  → into  ◁ reads  ▷ feeds",
            self.out,
        )

    def test_every_line_has_leader(self):
        for line in self.out.splitlines():
            self.assertTrue(line.startswith("#"), f"line missing comment leader: {line!r}")


class TestComposeSlashSyntax(unittest.TestCase):
    def test_slash_leader_used(self):
        spec = _single_flow_spec()
        spec["file"] = "config/rspack/browser/browser.plugins.ts"  # .ts -> //
        out = waypoint.compose_block(spec)
        for line in out.splitlines():
            self.assertTrue(line.startswith("//"), f"line missing // leader: {line!r}")


class TestComposeMultiFlow(unittest.TestCase):
    def setUp(self):
        self.spec = _multi_flow_spec()
        self.wp_id = waypoint.compute_id(self.spec["file"])
        self.out = waypoint.compose_block(self.spec)

    def test_multiflow_header(self):
        self.assertIn(
            f"// ── Waypoint {self.wp_id} · grep any 8-char ID to trace these pipelines ──",
            self.out,
        )

    def test_flow_subheaders(self):
        self.assertIn("//    sourcemap-upload — uploads browser sourcemaps to Sentry", self.out)
        self.assertIn("//    changeset-release — bumps versions and tags the release", self.out)

    def test_indented_neighbors(self):
        self.assertIn(
            "//      ← 4263ae66  docker-compose.ci.yml — passes the release version in", self.out
        )
        self.assertIn(
            "//      → 1a2b3c4d  publish.yml — publishes the tagged packages to npm", self.out
        )

    def test_per_flow_reference(self):
        self.assertIn("//      reference: .ai/waypoints/sourcemap-upload.md", self.out)
        self.assertIn("//      reference: .ai/waypoints/changeset-release.md", self.out)

    def test_closing_legend(self):
        self.assertIn("// ── ← from  → into  ◁ reads  ▷ feeds", self.out)


class TestComposeBlockComment(unittest.TestCase):
    """css/html-style blocks wrap the body between open/close delimiters."""

    def test_css_block_wrapping(self):
        spec = _single_flow_spec()
        spec["file"] = "styles/theme.css"
        out = waypoint.compose_block(spec)
        lines = out.splitlines()
        self.assertEqual(lines[0], "/*")
        self.assertEqual(lines[-1], "*/")
        self.assertIn("Waypoint", out)

    def test_html_block_wrapping(self):
        spec = _single_flow_spec()
        spec["file"] = "index.html"
        out = waypoint.compose_block(spec)
        lines = out.splitlines()
        self.assertEqual(lines[0], "<!--")
        self.assertEqual(lines[-1], "-->")


class TestParseLegacyBlocks(unittest.TestCase):
    """The parser must read existing real-repo blocks that use `Map:` and the
    two-line verbose closing, so scan/verify work without first migrating."""

    LEGACY = "\n".join(
        [
            "# ── Waypoint dd2c0eb6 ── sourcemap-upload ─────",
            "#    runs the rspack build and uploads sourcemaps",
            "#    ← 4263ae66  docker-compose.ci.yml — passes the release version into this build",
            "#    → 80e5dc26  browser.plugins.ts — uploads browser sourcemaps to Sentry",
            "#    Map: .ai/waypoints/sourcemap-upload.md",
            "# ── ← from · → into",
            "# ── search any ID to trace this pipeline across files.",
        ]
    )

    def test_finds_one_block(self):
        blocks = waypoint.parse_blocks(self.LEGACY)
        self.assertEqual(len(blocks), 1)

    def test_extracts_id(self):
        self.assertEqual(waypoint.parse_blocks(self.LEGACY)[0]["id"], "dd2c0eb6")

    def test_extracts_pipeline_from_map_line(self):
        self.assertIn("sourcemap-upload", waypoint.parse_blocks(self.LEGACY)[0]["pipelines"])

    def test_extracts_neighbors(self):
        neighbors = waypoint.parse_blocks(self.LEGACY)[0]["neighbors"]
        ids = sorted(n["id"] for n in neighbors)
        self.assertEqual(ids, ["4263ae66", "80e5dc26"])


class TestParseNewBlocks(unittest.TestCase):
    def test_roundtrip_single_flow(self):
        spec = _single_flow_spec()
        text = waypoint.compose_block(spec)
        blocks = waypoint.parse_blocks(text)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0]["id"], waypoint.compute_id(spec["file"]))
        self.assertIn("sourcemap-upload", blocks[0]["pipelines"])

    def test_roundtrip_multi_flow(self):
        spec = _multi_flow_spec()
        text = waypoint.compose_block(spec)
        blocks = waypoint.parse_blocks(text)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(set(blocks[0]["pipelines"]), {"sourcemap-upload", "changeset-release"})


class TestComputeDrift(unittest.TestCase):
    def test_verified_and_stale(self):
        manifest_rows = [
            {"id": "aaaaaaaa", "file": "a.py", "pipeline": "p"},
            {"id": "bbbbbbbb", "file": "b.py", "pipeline": "p"},
        ]
        code_blocks = [{"id": "aaaaaaaa", "file": "a.py", "pipelines": ["p"]}]
        drift = waypoint.compute_drift(manifest_rows, code_blocks)
        self.assertEqual([r["id"] for r in drift["verified"]], ["aaaaaaaa"])
        self.assertEqual([r["id"] for r in drift["stale"]], ["bbbbbbbb"])

    def test_orphaned(self):
        manifest_rows = [{"id": "aaaaaaaa", "file": "a.py", "pipeline": "p"}]
        code_blocks = [
            {"id": "aaaaaaaa", "file": "a.py", "pipelines": ["p"]},
            {"id": "cccccccc", "file": "c.py", "pipelines": ["p"]},
        ]
        drift = waypoint.compute_drift(manifest_rows, code_blocks)
        self.assertEqual([b["id"] for b in drift["orphaned"]], ["cccccccc"])


class TestComputeIdCorrections(unittest.TestCase):
    def test_flags_stale_id_with_new_value(self):
        nodes = [{"id": "00000000", "file": "a/b.py"}]
        corrections = waypoint.compute_id_corrections(nodes)
        self.assertEqual(len(corrections), 1)
        self.assertEqual(corrections[0]["old_id"], "00000000")
        self.assertEqual(corrections[0]["new_id"], waypoint.compute_id("a/b.py"))

    def test_correct_id_no_correction(self):
        good = waypoint.compute_id("a/b.py")
        nodes = [{"id": good, "file": "a/b.py"}]
        self.assertEqual(waypoint.compute_id_corrections(nodes), [])

    def test_reports_neighbor_references(self):
        nodes = [{"id": "00000000", "file": "a/b.py"}]
        references = [{"file": "other.py", "ref_id": "00000000"}]
        corrections = waypoint.compute_id_corrections(nodes, references)
        self.assertEqual(corrections[0]["referenced_by"], ["other.py"])


class TestRenderManifest(unittest.TestCase):
    def setUp(self):
        self.spec = {
            "pipeline": "build-release",
            "opening": "CI merges to main, builds the Docker image, then deploys it.",
            "nodes": [
                {
                    "id": "aaaaaaaa",
                    "file": "ci.yml",
                    "role": "triggers the build on merge",
                    "kind": "flow",
                },
                {
                    "id": "dddddddd",
                    "file": "rum.ts",
                    "role": "reads the release at runtime",
                    "kind": "sink",
                },
                {"id": "bbbbbbbb", "file": "build.sh", "role": "builds the image", "kind": "flow"},
            ],
            "topology": "aaaaaaaa → bbbbbbbb ▷ dddddddd",
        }
        self.out = waypoint.render_manifest(self.spec)

    def test_has_title(self):
        self.assertIn("# build-release", self.out)

    def test_has_opening_sentence(self):
        self.assertIn("CI merges to main, builds the Docker image, then deploys it.", self.out)

    def test_table_rows_present(self):
        self.assertIn("`aaaaaaaa`", self.out)
        self.assertIn("ci.yml", self.out)
        self.assertIn("triggers the build on merge", self.out)

    def test_sinks_ordered_last(self):
        # The sink row (rum.ts) must appear after both flow rows.
        self.assertLess(self.out.index("build.sh"), self.out.index("rum.ts"))
        self.assertLess(self.out.index("ci.yml"), self.out.index("rum.ts"))

    def test_topology_section(self):
        self.assertIn("## Topology", self.out)
        self.assertIn("aaaaaaaa → bbbbbbbb ▷ dddddddd", self.out)


if __name__ == "__main__":
    unittest.main()
