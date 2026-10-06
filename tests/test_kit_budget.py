"""Tests of skills/kit-budget/scripts/kit_budget.py on small fixture kits.

Each test writes a fixture kit into a temporary folder: kit.yaml, agents/*.md,
flows/*.yaml and skills/<name>/SKILL.md, only what the case needs.
Run: uv run --with pyyaml python -m unittest discover -s tests -v
"""

import importlib.util
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

import yaml

SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "kit-budget" / "scripts" / "kit_budget.py"
spec = importlib.util.spec_from_file_location("kit_budget", SCRIPT)
kit_budget = sys.modules["kit_budget"] = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kit_budget)


def words(n, word="word"):
    return " ".join(f"{word}{i}" for i in range(n))


def agent(name, body="You do the work.", mcp=None):
    meta = {"name": name, "description": f"The {name}.", "skills": []}
    if mcp:
        meta["mcp"] = {server: {"command": ["npx", server]} for server in mcp}
    return f"---\n{yaml.safe_dump(meta)}---\n{body}\n"


def flow(name, work=1, gates=0, do=None):
    """A chain of `work` work states and `gates` approval gates, then an end."""
    names = [f"step{i}" for i in range(work)] + [f"gate{i}" for i in range(gates)]
    states = {}
    for i, state in enumerate(names):
        after = names[i + 1] if i + 1 < len(names) else "done"
        if state.startswith("gate"):
            states[state] = {
                "gate": "approval",
                "ask": "OK?",
                "outcomes": {"approved": after, "rejected": names[0]},
            }
        else:
            text = (do or {}).get(state, f"Do {state}.")
            states[state] = {"agent": "worker", "do": text, "outcomes": {"done": after}}
    states["done"] = {"end": True}
    return yaml.safe_dump({"name": name, "description": "A flow.", "start": names[0], "states": states})


class Kit:
    def __init__(self, test, agents=None, flows=None, skills=(), supervisor="supervisor"):
        self.dir = tempfile.TemporaryDirectory()
        test.addCleanup(self.dir.cleanup)
        root = self.path = Path(self.dir.name)
        meta = {"name": "fixture", "version": "0.1.0", "description": "A fixture kit."}
        if supervisor:
            meta["supervisor"] = supervisor
        (root / "kit.yaml").write_text(yaml.safe_dump(meta))
        agents = {"worker": agent("worker")} if agents is None else agents
        for name, text in agents.items():
            (root / "agents").mkdir(exist_ok=True)
            (root / "agents" / f"{name}.md").write_text(text)
        for name, text in (flows or {}).items():
            (root / "flows").mkdir(exist_ok=True)
            (root / "flows" / f"{name}.yaml").write_text(text)
        for name in skills:
            (root / "skills" / name).mkdir(parents=True)
            (root / "skills" / name / "SKILL.md").write_text(f"---\nname: {name}\n---\nA skill.\n")

    def measure(self, measure):
        """The rows of one measure, as {where: (value, zone)}."""
        report = kit_budget.measure(self.path)
        return {r.where: (r.value, r.zone) for r in report.rows if r.measure == measure}


def roles(n, supervisor=True):
    found = {f"worker{i}": agent(f"worker{i}") for i in range(n)}
    if supervisor:
        found["supervisor"] = agent("supervisor")
    return found


class WorkerRoles(unittest.TestCase):
    def test_green_and_supervisor_not_counted(self):
        kit = Kit(self, agents=roles(3))
        self.assertEqual(kit.measure("worker_roles"), {"kit": (3, "green")})

    def test_yellow(self):
        self.assertEqual(Kit(self, agents=roles(4)).measure("worker_roles"), {"kit": (4, "yellow")})
        self.assertEqual(Kit(self, agents=roles(5)).measure("worker_roles"), {"kit": (5, "yellow")})

    def test_red(self):
        self.assertEqual(Kit(self, agents=roles(6)).measure("worker_roles"), {"kit": (6, "red")})

    def test_supervisor_named_in_kit_yaml_not_counted(self):
        agents = roles(3, supervisor=False)
        agents["lead"] = agent("lead")
        kit = Kit(self, agents=agents, supervisor="lead")
        self.assertEqual(kit.measure("worker_roles"), {"kit": (3, "green")})


class WorkSteps(unittest.TestCase):
    def test_zones_per_flow(self):
        kit = Kit(self, flows={"a": flow("a", work=5, gates=2), "b": flow("b", work=6), "c": flow("c", work=9)})
        self.assertEqual(
            kit.measure("work_steps"),
            {"flows/a.yaml": (5, "green"), "flows/b.yaml": (6, "yellow"), "flows/c.yaml": (9, "red")},
        )

    def test_eight_is_yellow(self):
        kit = Kit(self, flows={"a": flow("a", work=8)})
        self.assertEqual(kit.measure("work_steps"), {"flows/a.yaml": (8, "yellow")})

    def test_no_flows(self):
        self.assertEqual(Kit(self).measure("work_steps"), {"no flows": (0, "green")})


class Gates(unittest.TestCase):
    def test_zones_per_flow(self):
        kit = Kit(self, flows={"a": flow("a", gates=2), "b": flow("b", gates=3), "c": flow("c", gates=4)})
        self.assertEqual(
            kit.measure("gates"),
            {"flows/a.yaml": (2, "green"), "flows/b.yaml": (3, "yellow"), "flows/c.yaml": (4, "red")},
        )


class PromptWords(unittest.TestCase):
    def test_zones_per_role_and_frontmatter_not_counted(self):
        kit = Kit(
            self,
            agents={
                "supervisor": agent("supervisor", words(10)),
                "w": agent("w", words(800)),
                "a": agent("a", words(801)),
                "b": agent("b", words(1500)),
                "c": agent("c", words(1501)),
            },
        )
        self.assertEqual(
            kit.measure("prompt_words"),
            {
                "agents/w.md": (800, "green"),
                "agents/a.md": (801, "yellow"),
                "agents/b.md": (1500, "yellow"),
                "agents/c.md": (1501, "red"),
            },
        )

    def test_lead_has_its_own_limits(self):
        cases = {1000: "green", 1001: "yellow", 1500: "yellow", 1501: "red"}
        for n, zone in cases.items():
            with self.subTest(n=n):
                kit = Kit(self, agents={"supervisor": agent("supervisor", words(n))})
                self.assertEqual(kit.measure("lead_prompt_words"), {"agents/supervisor.md": (n, zone)})
                self.assertEqual(kit.measure("prompt_words"), {"no roles": (0, "green")})

    def test_lead_named_in_kit_yaml(self):
        kit = Kit(self, agents={"lead": agent("lead", words(1000))}, supervisor="lead")
        self.assertEqual(kit.measure("lead_prompt_words"), {"agents/lead.md": (1000, "green")})

    def test_no_lead_role(self):
        self.assertEqual(Kit(self).measure("lead_prompt_words"), {"no lead role": (0, "green")})

    def test_crlf_and_bom_frontmatter_not_counted(self):
        text = "\ufeff" + agent("a", words(10)).replace("\n", "\r\n")
        kit = Kit(self, agents={"a": text})
        self.assertEqual(kit.measure("prompt_words"), {"agents/a.md": (10, "green")})


class OwnSkills(unittest.TestCase):
    def test_zones(self):
        cases = {5: "green", 6: "yellow", 10: "yellow", 11: "red"}
        for n, zone in cases.items():
            with self.subTest(n=n):
                kit = Kit(self, skills=[f"skill-{i}" for i in range(n)])
                self.assertEqual(kit.measure("own_skills"), {"kit": (n, zone)})

    def test_folder_without_skill_md_not_counted(self):
        kit = Kit(self, skills=["one"])
        (kit.path / "skills" / "notes").mkdir()
        self.assertEqual(kit.measure("own_skills"), {"kit": (1, "green")})


class McpServers(unittest.TestCase):
    def test_distinct_servers_across_roles(self):
        kit = Kit(self, agents={"a": agent("a", mcp=["one", "two"]), "b": agent("b", mcp=["two"])})
        self.assertEqual(kit.measure("mcp_servers"), {"kit": (2, "green")})

    def test_yellow_and_red(self):
        kit = Kit(self, agents={"a": agent("a", mcp=["s1", "s2", "s3"])})
        self.assertEqual(kit.measure("mcp_servers"), {"kit": (3, "yellow")})
        kit = Kit(self, agents={"a": agent("a", mcp=[f"s{i}" for i in range(5)])})
        self.assertEqual(kit.measure("mcp_servers"), {"kit": (5, "red")})


RULE = "Run the checks yourself after your last change and quote their output in your report."
# the same rule reworded: most content words stay
REWORDED = "When your last change is in, run the checks yourself and put their output in the report."
OTHER = "Write the design into the note and ask the human to approve it before anyone builds."
POINTER = 'Follow `lado-checks`, "Merging a run\'s branch".'


class Similar(unittest.TestCase):
    def similar(self, kit):
        """The similar pairs as (percent, place a, place b)."""
        return [(round(s.similarity * 100), *s.places) for s in kit_budget.measure(kit.path).similar]

    def test_verbatim_paragraph_in_two_roles_and_a_step(self):
        kit = Kit(
            self,
            agents={
                "a": agent("a", f"You are a.\n\n{RULE}"),
                # the same rule, wrapped and cased differently
                "b": agent("b", "You are b.\n\n" + textwrap.fill(RULE.upper(), 30)),
            },
            flows={"f": flow("f", do={"step0": f"Work.\n\n{RULE}"})},
        )
        self.assertEqual(
            self.similar(kit),
            [
                (100, "agents/a.md", "agents/b.md"),
                (100, "agents/a.md", 'flows/f.yaml: state "step0"'),
                (100, "agents/b.md", 'flows/f.yaml: state "step0"'),
            ],
        )

    def test_reworded_paragraph_above_threshold(self):
        kit = Kit(self, agents={"a": agent("a", RULE), "b": agent("b", REWORDED)})
        [(percent, a, b)] = self.similar(kit)
        self.assertEqual((a, b), ("agents/a.md", "agents/b.md"))
        self.assertGreaterEqual(percent / 100, kit_budget.SIMILAR_FROM)
        self.assertLess(percent, 100)

    def test_different_paragraphs_below_threshold(self):
        self.assertLess(kit_budget.similarity(RULE, OTHER), kit_budget.SIMILAR_FROM)
        kit = Kit(self, agents={"a": agent("a", RULE), "b": agent("b", OTHER)})
        self.assertEqual(self.similar(kit), [])

    def test_short_pointer_not_counted(self):
        kit = Kit(
            self,
            agents={"a": agent("a", f"Be brief.\n\n{POINTER}"), "b": agent("b", "Be brief.")},
            flows={"f": flow("f", work=2, do={"step0": POINTER, "step1": POINTER})},
        )
        self.assertEqual(self.similar(kit), [])

    def test_repeat_inside_one_place_not_counted(self):
        kit = Kit(self, agents={"a": agent("a", f"{RULE}\n\n{REWORDED}")})
        self.assertEqual(self.similar(kit), [])

    def test_similar_paragraphs_are_yellow_not_red(self):
        kit = Kit(self, agents={"a": agent("a", RULE), "b": agent("b", REWORDED)})
        report = kit_budget.measure(kit.path)
        self.assertEqual(report.zone, "yellow")

    def test_output_has_percent_and_places(self):
        kit = Kit(self, agents={"a": agent("a", RULE), "b": agent("b", REWORDED)})
        text = kit_budget.render(kit_budget.measure(kit.path))
        line = next(l for l in text.splitlines() if l.startswith("- yellow:"))
        percent = round(kit_budget.similarity(RULE, REWORDED) * 100)
        self.assertIn(f"{percent}% similar", line)
        self.assertIn("agents/a.md", line)
        self.assertIn("agents/b.md", line)


class Run(unittest.TestCase):
    def run_script(self, kit):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(kit.path)], capture_output=True, text=True
        )

    def test_green_kit_exits_0_and_prints_every_measure(self):
        result = self.run_script(Kit(self, agents=roles(1), flows={"f": flow("f")}))
        self.assertEqual(result.returncode, 0, result.stderr)
        for label in kit_budget.LABELS.values():
            self.assertIn(label, result.stdout)
        self.assertIn("Overall: green", result.stdout)

    def test_yellow_kit_exits_0(self):
        result = self.run_script(Kit(self, agents=roles(4)))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Overall: yellow", result.stdout)

    def test_red_kit_exits_1(self):
        result = self.run_script(Kit(self, flows={"f": flow("f", gates=4)}))
        self.assertEqual(result.returncode, 1)
        self.assertIn("Overall: red", result.stdout)

    def test_broken_frontmatter_exits_2(self):
        kit = Kit(self, agents={"a": "---\nname: [a\n---\nYou work.\n"})
        result = self.run_script(kit)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("agents/a.md", result.stderr)

    def test_flow_that_is_a_list_exits_2(self):
        kit = Kit(self, flows={"f": "- one\n- two\n"})
        result = self.run_script(kit)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("f.yaml", result.stderr)

    def test_flow_states_that_are_a_list_exits_2(self):
        kit = Kit(self, flows={"f": "name: f\nstates: [a, b]\n"})
        self.assertEqual(self.run_script(kit).returncode, 2)

    def test_empty_kit_yaml_exits_2(self):
        kit = Kit(self)
        (kit.path / "kit.yaml").write_text("")
        self.assertEqual(self.run_script(kit).returncode, 2)

    def test_frontmatter_that_is_a_list_exits_2(self):
        kit = Kit(self, agents={"a": "---\n- one\n---\nYou work.\n"})
        self.assertEqual(self.run_script(kit).returncode, 2)

    def test_not_a_kit_exits_2(self):
        with tempfile.TemporaryDirectory() as empty:
            result = subprocess.run(
                [sys.executable, str(SCRIPT), empty], capture_output=True, text=True
            )
        self.assertEqual(result.returncode, 2)
        self.assertIn("kit.yaml", result.stderr)


if __name__ == "__main__":
    unittest.main()
