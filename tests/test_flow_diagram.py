"""Tests of skills/kit-budget/scripts/flow_diagram.py on small fixture flows and on
kit-builder's own flows and BLUEPRINT.md.

Run: uv run --with pyyaml python -m unittest discover -s tests -v
"""

import importlib.util
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "kit-budget" / "scripts" / "flow_diagram.py"
spec = importlib.util.spec_from_file_location("flow_diagram", SCRIPT)
flow_diagram = sys.modules["flow_diagram"] = importlib.util.module_from_spec(spec)
spec.loader.exec_module(flow_diagram)

LOOP = textwrap.dedent("""\
    name: loop
    start: write
    states:
      write:
        agent: author
        do: Write it.
        outcomes: {done: review}
      review:
        agent: critic
        max_visits: 3
        outcomes: {approved: ok, changes: write}
      ok:
        gate: approval
        ask: Ship it?
        outcomes: {approved: done, rejected: write}
      done:
        end: true
    """)

PLAIN = LOOP.replace("    do: Write it.\n", "").replace("    ask: Ship it?\n", "")  # a skeleton


def skeleton(text):
    return f"# Blueprint\n\nText.\n\n```yaml\n{text}```\n\nMore text.\n"


class Files(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.path = Path(self.dir.name)

    def write(self, name, text):
        path = self.path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path


class Parse(Files):
    def test_flow_file(self):
        [flow] = flow_diagram.load(self.write("flows/loop.yaml", LOOP))
        self.assertEqual(flow.name, "loop")
        self.assertEqual(flow.start, "write")
        self.assertEqual([s.kind for s in flow.states.values()], ["work", "work", "gate", "end"])
        self.assertEqual(flow.states["review"].detail, "critic")
        self.assertEqual(flow.states["review"].max_visits, 3)
        self.assertEqual(flow.states["ok"].outcomes, {"approved": "done", "rejected": "write"})

    def test_kit_folder_reads_its_flows(self):
        self.write("kit.yaml", "name: k\n")
        self.write("flows/b.yaml", LOOP.replace("name: loop", "name: b"))
        self.write("flows/a.yaml", LOOP.replace("name: loop", "name: a"))
        self.assertEqual([f.name for f in flow_diagram.load(self.path)], ["a", "b"])

    def test_markdown_skeletons_only_yaml_blocks_with_states(self):
        text = skeleton(PLAIN)
        text += "\n```yaml\nname: not-a-flow\n```\n\n```\nstates: plain block\n```\n"
        [flow] = flow_diagram.load(self.write("BLUEPRINT.md", text))
        self.assertEqual(flow.name, "loop")
        self.assertIn("BLUEPRINT.md:5", flow.source)

    def test_markdown_two_skeletons(self):
        text = skeleton(PLAIN) + skeleton(PLAIN.replace("name: loop", "name: other"))
        self.assertEqual([f.name for f in flow_diagram.load(self.write("B.md", text))], ["loop", "other"])


class Errors(Files):
    def error(self, text, name="f.yaml"):
        with self.assertRaises(flow_diagram.FlowError) as caught:
            flow_diagram.load(self.write(name, text))
        return str(caught.exception)

    def test_unknown_target(self):
        message = self.error(LOOP.replace("{done: review}", "{done: reviw}"))
        self.assertIn("unknown state 'reviw'", message)
        self.assertIn("'write'", message)

    def test_unreachable_state(self):
        self.assertIn("unreachable from 'write': lost", self.error(LOOP + "  lost:\n    agent: x\n    outcomes: {done: done}\n"))

    def test_no_end(self):
        text = LOOP.replace("  done:\n    end: true\n", "  done:\n    agent: x\n    outcomes: {again: write}\n")
        self.assertIn("no end state", self.error(text))

    def test_bad_start(self):
        self.assertIn("start 'nowhere' is not a state", self.error(LOOP.replace("start: write", "start: nowhere")))

    def test_state_with_two_kinds(self):
        self.assertIn("exactly one of agent, gate", self.error(LOOP.replace("    gate: approval\n", "    gate: approval\n    agent: x\n")))

    def test_state_without_outcomes(self):
        self.assertIn("no outcomes and not an end", self.error(LOOP.replace("    outcomes: {done: review}\n", "")))

    def test_skeleton_with_do_is_rejected(self):
        self.assertIn("a skeleton holds only", self.error(skeleton(LOOP), "BLUEPRINT.md"))

    def test_markdown_without_skeleton(self):
        self.assertIn("no ```yaml block", self.error("# Blueprint\n\nNo flows.\n", "BLUEPRINT.md"))

    def test_not_a_mapping(self):
        self.assertIn("expected a YAML mapping", self.error("- a\n- b\n"))

    def test_missing_input(self):
        with self.assertRaises(flow_diagram.FlowError):
            flow_diagram.load(self.path / "nothing.yaml")


class Render(Files):
    def test_same_input_same_bytes(self):
        path = self.write("loop.yaml", LOOP)
        first = flow_diagram.render(flow_diagram.load(path)[0])
        second = flow_diagram.render(flow_diagram.load(path)[0])
        self.assertEqual(first, second)

    def test_states_edges_and_labels(self):
        svg = flow_diagram.render(flow_diagram.load(self.write("loop.yaml", LOOP))[0])
        for name in ("write", "review", "ok", "done"):
            self.assertIn(f'data-state="{name}"', svg)
        for label in (">done<", ">approved<", ">changes<", ">rejected<", "max_visits 3", "gate: approval"):
            self.assertIn(label, svg)
        self.assertEqual(svg.count('stroke-dasharray="5 3" marker-end'), 2)  # changes, rejected

    def test_outcomes_to_one_target_share_an_edge(self):
        text = LOOP.replace("{approved: ok, changes: write}", "{approved: ok, minor: ok, changes: write}")
        svg = flow_diagram.render(flow_diagram.load(self.write("f.yaml", text))[0])
        self.assertIn(">approved | minor<", svg)

    def test_ends_on_the_last_row(self):
        text = LOOP.replace("{done: review}", "{done: review, nothing: done}")
        flow = flow_diagram.load(self.write("f.yaml", text))[0]
        cells = flow_diagram.layout(flow)
        self.assertEqual(cells["done"][0], max(row for row, _ in cells.values()))
        kinds = {(e.source, e.target): e.kind for e in flow_diagram.edges(flow, cells)}
        self.assertEqual(kinds[("write", "done")], "long")
        self.assertEqual(kinds[("review", "write")], "back")


class Compare(Files):
    def test_same(self):
        flows = flow_diagram.load(self.write("f.yaml", LOOP))
        self.assertEqual(flow_diagram.compare(flows, flows), [])

    def test_every_kind_of_difference(self):
        plan = flow_diagram.load(self.write("plan.yaml", LOOP))
        built = LOOP.replace("agent: critic", "agent: reviewer").replace("{approved: done, rejected: write}", "{approved: done, rejected: review}")
        built = built.replace("max_visits: 3", "max_visits: 2") + "  extra:\n    agent: x\n    outcomes: {done: done}\n"
        built = built.replace("{done: review}", "{done: review, more: extra}")
        diffs = flow_diagram.compare(flow_diagram.load(self.write("f.yaml", built)), plan)
        self.assertIn("flow loop: state review: agent reviewer, planned agent critic", diffs)
        self.assertIn("flow loop: state ok, outcome rejected: review, planned write", diffs)
        self.assertIn("flow loop: state review: max_visits 2, planned 3", diffs)
        self.assertIn("flow loop: state extra: built, not in the plan", diffs)
        self.assertIn("flow loop: state write, outcome more: extra, planned none", diffs)

    def test_flows_missing_on_either_side(self):
        a = flow_diagram.load(self.write("a.yaml", LOOP.replace("name: loop", "name: a")))
        b = flow_diagram.load(self.write("b.yaml", LOOP.replace("name: loop", "name: b")))
        self.assertEqual(flow_diagram.compare(a, b), ["flow a: built, not in the plan", "flow b: planned, not built"])


class OwnFlows(unittest.TestCase):
    """kit-builder's own three flows render, and match the skeletons in its BLUEPRINT.md."""

    def test_render_all_three(self):
        flows = flow_diagram.load(ROOT)
        self.assertEqual([f.name for f in flows], ["create", "evaluate", "improve"])
        for flow in flows:
            svg = flow_diagram.render(flow)
            self.assertTrue(svg.startswith("<svg"))
            for name in flow.states:
                self.assertIn(f'data-state="{name}"', svg)

    def test_blueprint_skeletons_match_the_flows(self):
        planned = flow_diagram.load(ROOT / "BLUEPRINT.md")
        self.assertEqual(flow_diagram.compare(flow_diagram.load(ROOT), planned), [])

    def test_committed_svgs_are_current(self):
        for flow in flow_diagram.load(ROOT / "BLUEPRINT.md"):
            committed = ROOT / "blueprint-flows" / f"{flow.name}.svg"
            self.assertEqual(committed.read_text(encoding="utf-8"), flow_diagram.render(flow), committed)


class Run(Files):
    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)

    def test_out_writes_one_svg_per_flow_byte_for_byte(self):
        self.write("flows/loop.yaml", LOOP)
        out = self.path / "svg"
        first = self.run_script(self.path, "--out", out)
        self.assertEqual(first.returncode, 0, first.stderr)
        data = (out / "loop.svg").read_bytes()
        self.run_script(self.path, "--out", out)
        self.assertEqual((out / "loop.svg").read_bytes(), data)

    def test_invalid_flow_exits_2(self):
        result = self.run_script(self.write("f.yaml", LOOP.replace("{done: review}", "{done: nowhere}")), "--out", self.path)
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown state 'nowhere'", result.stderr)

    def test_compare_exits_1_on_a_difference(self):
        plan = self.write("plan.yaml", LOOP)
        built = self.write("built.yaml", LOOP.replace("agent: critic", "agent: reviewer"))
        result = self.run_script(built, "--compare", plan)
        self.assertEqual(result.returncode, 1)
        self.assertIn("agent reviewer, planned agent critic", result.stdout)
        self.assertEqual(self.run_script(plan, "--compare", plan).returncode, 0)


if __name__ == "__main__":
    unittest.main()
