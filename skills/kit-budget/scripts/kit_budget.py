# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml>=6"]
# ///
"""Count a LADO kit against the complexity budget of kit-builder (SKILL.md says how).

Usage: uv run --script kit_budget.py <kit folder>
Exit status: 0 green or yellow, 1 red, 2 not a kit.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# measure -> (green up to, yellow up to); above is red
LIMITS = {
    "worker_roles": (3, 5),
    "work_steps": (5, 8),
    "gates": (2, 3),
    "prompt_words": (800, 1500),
    "lead_prompt_words": (1000, 1500),
    "own_skills": (5, 10),
    "mcp_servers": (2, 4),
}
LABELS = {
    "worker_roles": "Worker roles (not supervisor)",
    "work_steps": "Work steps in a flow",
    "gates": "Gates in a flow",
    "prompt_words": "Words in a role prompt",
    "lead_prompt_words": "Words in the lead's prompt",
    "own_skills": "Own skills",
    "mcp_servers": "MCP servers",
}
ZONES = ("green", "yellow", "red")
LEAD = "supervisor"  # the name LADO reserves for a kit's lead
MIN_PARAGRAPH_WORDS = 8  # shorter paragraphs (a pointer, "Be brief.") are not compared
# Two paragraphs are similar from this Jaccard similarity of their content words on.
# Calibrated on lado-dev 0.9.1-0.9.4 and kit-builder (SKILL.md): whole-paragraph repeats
# scored 0.57 and up; repeats worded apart or inside longer paragraphs, 0.52 and less,
# are left to rubric criterion 6.
SIMILAR_FROM = 0.55
# Function words: shared by any two English paragraphs, so they would only add noise.
STOP_WORDS = frozenset("""
a about after all also an and any are as at be been before both but by can could did do
does each either every for from had has have he her here his how i if in into is it its
just may me more most must my no nor not now of on once one only or other our out over own
same she should so some such than that the their them then there these they this those to
too under until up very was we were what when where which while who whom why will with
would you your
""".split())


class NotAKit(Exception):
    pass


@dataclass
class Row:
    measure: str
    where: str
    value: int

    @property
    def zone(self) -> str:
        green, yellow = LIMITS[self.measure]
        return "green" if self.value <= green else "yellow" if self.value <= yellow else "red"


@dataclass
class Similar:
    similarity: float  # Jaccard similarity of the content words, 0..1
    places: tuple[str, str]
    texts: tuple[str, str]


@dataclass
class Report:
    name: str
    version: str
    rows: list[Row] = field(default_factory=list)
    similar: list[Similar] = field(default_factory=list)

    @property
    def zone(self) -> str:
        zones = [r.zone for r in self.rows] + (["yellow"] if self.similar else [])
        return max(zones, key=ZONES.index, default="green")


def measure(kit: Path) -> Report:
    if not (kit / "kit.yaml").is_file():
        raise NotAKit(f"{kit}: no kit.yaml")
    meta = _mapping(_read(kit / "kit.yaml"), kit / "kit.yaml")
    if not meta:
        raise NotAKit(f"{kit / 'kit.yaml'}: empty")
    report = Report(str(meta.get("name", "?")), str(meta.get("version", "?")))
    lead = meta.get("supervisor") or LEAD
    agents = {p: _frontmatter(p) for p in sorted((kit / "agents").glob("*.md"))}
    flows = {p: _states(p) for p in sorted((kit / "flows").glob("*.yaml"))}
    rel = lambda p: p.relative_to(kit).as_posix()  # noqa: E731

    workers = [p for p, (m, _) in agents.items() if m.get("name", p.stem) not in (lead, LEAD)]
    report.rows.append(Row("worker_roles", "kit", len(workers)))
    for kind, key in (("work_steps", "agent"), ("gates", "gate")):
        for path, states in flows.items():
            count = sum(1 for s in states.values() if isinstance(s, dict) and key in s)
            report.rows.append(Row(kind, rel(path), count))
        if not flows:
            report.rows.append(Row(kind, "no flows", 0))
    leads = [p for p in agents if p not in workers]
    for kind, paths, empty in (("prompt_words", workers, "no roles"), ("lead_prompt_words", leads, "no lead role")):
        for path in paths:
            report.rows.append(Row(kind, rel(path), len(agents[path][1].split())))
        if not paths:
            report.rows.append(Row(kind, empty, 0))
    skills = [p for p in (kit / "skills").glob("*/SKILL.md")]
    report.rows.append(Row("own_skills", "kit", len(skills)))
    servers = {name for m, _ in agents.values() for name in (m.get("mcp") or {})}
    report.rows.append(Row("mcp_servers", "kit", len(servers)))

    texts = [(rel(p), body) for p, (_, body) in agents.items()]
    for path, states in flows.items():
        for state, s in states.items():
            if isinstance(s, dict) and isinstance(s.get("do"), str):
                texts.append((f'{rel(path)}: state "{state}"', s["do"]))
    report.similar = _similar(texts)
    return report


def content_words(text: str) -> set[str]:
    """The distinct words of a text, lowercased, without punctuation and STOP_WORDS."""
    return set(re.findall(r"[a-z0-9]+(?:['_-][a-z0-9]+)*", text.lower())) - STOP_WORDS


def similarity(a: str, b: str) -> float:
    """Jaccard similarity of two texts' content words: shared / all, 0..1."""
    wa, wb = content_words(a), content_words(b)
    return len(wa & wb) / len(wa | wb) if wa | wb else 0.0


def _similar(texts: list[tuple[str, str]]) -> list[Similar]:
    """Pairs of paragraphs (blocks between blank lines) in different places whose similarity
    is SIMILAR_FROM or more, most similar first; paragraphs under MIN_PARAGRAPH_WORDS words
    are skipped."""
    paragraphs = [
        (place, " ".join(p.split()))
        for place, text in texts
        for p in re.split(r"\n\s*\n", text)
        if len(p.split()) >= MIN_PARAGRAPH_WORDS
    ]
    found = []
    for i, (place_a, a) in enumerate(paragraphs):
        for place_b, b in paragraphs[i + 1:]:
            if place_a == place_b:
                continue
            score = 1.0 if a.lower() == b.lower() else similarity(a, b)
            if score >= SIMILAR_FROM:
                found.append(Similar(score, (place_a, place_b), (a, b)))
    return sorted(found, key=lambda s: -s.similarity)


def _read(path: Path) -> str:
    """A file's text without a byte order mark and with \n line ends."""
    text = path.read_text(encoding="utf-8-sig")
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _mapping(text: str, path: Path) -> dict:
    """YAML text that must be a mapping (or empty); anything else is NotAKit."""
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise NotAKit(f"{path}: not valid YAML: {exc}") from exc
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise NotAKit(f"{path}: expected a YAML mapping")
    return data


def _states(path: Path) -> dict:
    """The states of a flow file."""
    states = _mapping(_read(path), path).get("states") or {}
    if not isinstance(states, dict):
        raise NotAKit(f"{path}: states must be a mapping")
    return states


def _frontmatter(path: Path) -> tuple[dict, str]:
    """An agent file's frontmatter and its body (the role prompt)."""
    text = _read(path)
    match = re.match(r"---\n(.*?)\n---[ \t]*(?:\n|$)", text, re.S)
    if not match:
        return {}, text
    return _mapping(match.group(1), path), text[match.end():]


def render(report: Report) -> str:
    lines = [
        f"# Complexity budget: {report.name} {report.version}",
        "",
        "| Measure | Where | Value | Green / yellow up to | Zone |",
        "|---|---|---|---|---|",
    ]
    for row in report.rows:
        green, yellow = LIMITS[row.measure]
        lines.append(f"| {LABELS[row.measure]} | {row.where} | {row.value} | {green} / {yellow} | {row.zone} |")
    lines += ["", f"## Similar paragraphs (one rule, one place; {SIMILAR_FROM:.0%} similar or more)", ""]
    if not report.similar:
        lines.append("none")
    short = lambda t: t if len(t) <= 80 else t[:77] + "..."  # noqa: E731
    for s in report.similar:
        (place_a, place_b), (a, b) = s.places, s.texts
        lines.append(
            f"- yellow: {s.similarity:.0%} similar: {place_a}: \"{short(a)}\" ~ {place_b}: \"{short(b)}\""
        )
    lines += ["", f"Overall: {report.zone}"]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: kit_budget.py <kit folder>", file=sys.stderr)
        return 2
    try:
        report = measure(Path(argv[0]))
    except NotAKit as exc:
        print(exc, file=sys.stderr)
        return 2
    print(render(report))
    return 1 if report.zone == "red" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
