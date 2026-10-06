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
    "own_skills": (5, 10),
    "mcp_servers": (2, 4),
}
LABELS = {
    "worker_roles": "Worker roles (not supervisor)",
    "work_steps": "Work steps in a flow",
    "gates": "Gates in a flow",
    "prompt_words": "Words in a role prompt",
    "own_skills": "Own skills",
    "mcp_servers": "MCP servers",
}
ZONES = ("green", "yellow", "red")
LEAD = "supervisor"  # the name LADO reserves for a kit's lead
MIN_DUPLICATE_WORDS = 8  # shorter paragraphs ("Be brief.") are not counted as duplicates


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
class Duplicate:
    text: str
    places: list[str]


@dataclass
class Report:
    name: str
    version: str
    rows: list[Row] = field(default_factory=list)
    duplicates: list[Duplicate] = field(default_factory=list)

    @property
    def zone(self) -> str:
        zones = [r.zone for r in self.rows] + (["yellow"] if self.duplicates else [])
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
    for path, (_, body) in agents.items():
        report.rows.append(Row("prompt_words", rel(path), len(body.split())))
    if not agents:
        report.rows.append(Row("prompt_words", "no roles", 0))
    skills = [p for p in (kit / "skills").glob("*/SKILL.md")]
    report.rows.append(Row("own_skills", "kit", len(skills)))
    servers = {name for m, _ in agents.values() for name in (m.get("mcp") or {})}
    report.rows.append(Row("mcp_servers", "kit", len(servers)))

    texts = [(rel(p), body) for p, (_, body) in agents.items()]
    for path, states in flows.items():
        for state, s in states.items():
            if isinstance(s, dict) and isinstance(s.get("do"), str):
                texts.append((f'{rel(path)}: state "{state}"', s["do"]))
    report.duplicates = _duplicates(texts)
    return report


def _duplicates(texts: list[tuple[str, str]]) -> list[Duplicate]:
    """Paragraphs (blocks between blank lines) that appear in two or more places, compared
    case-blind with whitespace collapsed; paragraphs under MIN_DUPLICATE_WORDS are skipped."""
    seen: dict[str, Duplicate] = {}
    for place, text in texts:
        for paragraph in re.split(r"\n\s*\n", text):
            key = " ".join(paragraph.lower().split())
            if len(key.split()) < MIN_DUPLICATE_WORDS:
                continue
            found = seen.setdefault(key, Duplicate(" ".join(paragraph.split()), []))
            if place not in found.places:
                found.places.append(place)
    return [d for d in seen.values() if len(d.places) > 1]


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
    lines += ["", "## Duplicate paragraphs (one rule, one place)", ""]
    if not report.duplicates:
        lines.append("none")
    for d in report.duplicates:
        text = d.text if len(d.text) <= 100 else d.text[:97] + "..."
        lines.append(f"- yellow: \"{text}\" in {'; '.join(d.places)}")
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
