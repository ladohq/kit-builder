# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml>=6"]
# ///
"""Draw the flows of a LADO kit as SVG, and compare built flows with planned ones.

Usage:
  uv run --script flow_diagram.py <input> --out <folder>     one <flow name>.svg per flow
  uv run --script flow_diagram.py <input> --compare <plan>   differences, flow by flow

<input> and <plan> are a flow file (flows/<name>.yaml), a folder (its flows/*.yaml, or
*.yaml when it has no flows/), or a Markdown file (BLUEPRINT.md) whose ```yaml blocks with
`states:` are flow skeletons. Exit status: 0 done, 1 the flows differ from the plan,
2 an input is missing or a flow is not valid. A state's `produces` and `reads` are not
drawn or checked (`lado kits check` does that); `needs`, gone since LADO 0.27, is refused.
The layout is ported from the Tessera
kit-builder's render_workflow_diagram.py: layered, deterministic, no other dependencies.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

import yaml

NODE_W, NODE_H, NODE_RX = 180, 46, 8
ROW_GAP = 76  # from one row's top to the next row's top, minus NODE_H
COL_GAP = 40  # between two nodes of one row
PAD = 30
TOP = 40  # room above the first row for the start marker
LANE = 18  # between two side lanes (back edges on the left, long edges on the right)
FONT = "system-ui, -apple-system, sans-serif"
CHAR_W = 6.2  # approximate width of a label character at 11px
EDGE = "#6b7280"
LABEL = "#4b5563"
# kind -> (fill, stroke, text)
COLORS = {
    "work": ("#ffffff", "#9ca3af", "#1b2236"),
    "gate": ("#fdf0e7", "#d06a2c", "#a0522d"),
    "end": ("#e8f6ee", "#36a86e", "#2a7a50"),
}
SKELETON_KEYS = {"agent", "gate", "end", "outcomes", "max_visits"}


class FlowError(Exception):
    pass


@dataclass
class State:
    name: str
    kind: str  # work, gate or end
    detail: str  # the agent, the gate's type, or "end"
    outcomes: dict[str, str] = field(default_factory=dict)
    max_visits: int | None = None


@dataclass
class Flow:
    name: str
    source: str
    start: str
    states: dict[str, State]


# Reading


def load(path: Path) -> list[Flow]:
    """The flows of a flow file, a folder or a Markdown file, validated."""
    if path.is_dir():
        folder = path / "flows" if (path / "flows").is_dir() else path
        files = sorted(folder.glob("*.yaml"))
        if not files:
            raise FlowError(f"{path}: no flow files (*.yaml)")
        return [parse(_read(f), f.as_posix()) for f in files]
    if not path.is_file():
        raise FlowError(f"{path}: no such file or folder")
    if path.suffix.lower() in (".md", ".markdown"):
        return skeletons(_read(path), path.as_posix())
    return [parse(_read(path), path.as_posix())]


def skeletons(markdown: str, source: str) -> list[Flow]:
    """The flow skeletons of a Markdown file: its ```yaml blocks that have `states:`."""
    flows = []
    for match in re.finditer(r"^```ya?ml[ \t]*\n(.*?)^```", markdown, re.M | re.S):
        line = markdown.count("\n", 0, match.start()) + 1
        try:
            data = yaml.safe_load(match.group(1))
        except yaml.YAMLError as exc:
            raise FlowError(f"{source}:{line}: not valid YAML: {exc}") from exc
        if isinstance(data, dict) and "states" in data:
            flows.append(parse(data, f"{source}:{line}", skeleton=True))
    if not flows:
        raise FlowError(f"{source}: no ```yaml block with states:")
    names = [f.name for f in flows]
    for name in names:
        if names.count(name) > 1:
            raise FlowError(f"{source}: two skeletons named {name!r}")
    return flows


def parse(data, source: str, skeleton: bool = False) -> Flow:
    """A Flow from YAML text or data; FlowError when it is not a valid flow."""
    if isinstance(data, str):
        try:
            data = yaml.safe_load(data)
        except yaml.YAMLError as exc:
            raise FlowError(f"{source}: not valid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise FlowError(f"{source}: expected a YAML mapping")
    name, start, raw = data.get("name"), data.get("start"), data.get("states")
    if not name:
        raise FlowError(f"{source}: no name")
    if not isinstance(raw, dict) or not raw:
        raise FlowError(f"{source}: states must be a non-empty mapping")
    states = {}
    for key, s in raw.items():
        key = str(key)
        where = f"{source}: state {key!r}"
        if not isinstance(s, dict):
            raise FlowError(f"{where}: expected a mapping")
        if "needs" in s:
            raise FlowError(
                f"{where}: needs is gone since LADO 0.27; a step names the artifacts it reads in "
                "reads and the ones it writes in produces"
            )
        kinds = [k for k in ("agent", "gate", "end") if s.get(k)]
        if len(kinds) != 1:
            raise FlowError(f"{where}: needs exactly one of agent, gate or end: true")
        if skeleton and set(s) - SKELETON_KEYS:
            extra = ", ".join(sorted(set(s) - SKELETON_KEYS))
            raise FlowError(f"{where}: a skeleton holds only agent, gate, end, outcomes, max_visits (not {extra})")
        outcomes = s.get("outcomes") or {}
        if not isinstance(outcomes, dict):
            raise FlowError(f"{where}: outcomes must be a mapping")
        kind = {"agent": "work", "gate": "gate", "end": "end"}[kinds[0]]
        detail = "end" if kind == "end" else str(s[kinds[0]])
        if kind != "end" and not outcomes:
            raise FlowError(f"{where}: no outcomes and not an end")
        if kind == "end" and outcomes:
            raise FlowError(f"{where}: an end has no outcomes")
        visits = s.get("max_visits")
        states[key] = State(key, kind, detail, {str(o): str(t) for o, t in outcomes.items()}, visits)
    flow = Flow(str(name), source, str(start), states)
    _validate(flow)
    return flow


def _validate(flow: Flow) -> None:
    where = f"{flow.source}: flow {flow.name!r}"
    if flow.start not in flow.states:
        raise FlowError(f"{where}: start {flow.start!r} is not a state")
    for s in flow.states.values():
        for outcome, target in s.outcomes.items():
            if target not in flow.states:
                raise FlowError(f"{where}: state {s.name!r}, outcome {outcome!r} goes to unknown state {target!r}")
    if not any(s.kind == "end" for s in flow.states.values()):
        raise FlowError(f"{where}: no end state (end: true)")
    reached = set(_ranks(flow))
    lost = [n for n in flow.states if n not in reached]
    if lost:
        raise FlowError(f"{where}: unreachable from {flow.start!r}: {', '.join(lost)}")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


# Layout


def _ranks(flow: Flow) -> dict[str, int]:
    """Breadth-first depth of every state reached from start, outcomes in their order."""
    ranks = {flow.start: 0}
    queue = deque([flow.start])
    while queue:
        name = queue.popleft()
        for target in flow.states[name].outcomes.values():
            if target not in ranks:
                ranks[target] = ranks[name] + 1
                queue.append(target)
    return ranks


def layout(flow: Flow) -> dict[str, tuple[int, int]]:
    """(row, column) of every state: rows by depth from start, ends on the last row."""
    ranks = _ranks(flow)
    last = max([r for n, r in ranks.items() if flow.states[n].kind != "end"], default=-1) + 1
    rows: dict[int, list[str]] = {}
    for name in sorted(ranks, key=lambda n: (ranks[n], list(flow.states).index(n))):
        row = last if flow.states[name].kind == "end" else ranks[name]
        rows.setdefault(row, []).append(name)
    return {name: (row, col) for row, names in rows.items() for col, name in enumerate(names)}


@dataclass
class Edge:
    source: str
    target: str
    label: str
    kind: str = ""  # down (to the next row), long (further down), back (up or same row), self


def edges(flow: Flow, cells: dict[str, tuple[int, int]]) -> list[Edge]:
    """One edge per (source, target), its outcomes joined in the label."""
    found: dict[tuple[str, str], Edge] = {}
    for s in flow.states.values():
        for outcome, target in s.outcomes.items():
            if (s.name, target) in found:
                found[(s.name, target)].label += " | " + outcome
                continue
            e = found[(s.name, target)] = Edge(s.name, target, outcome)
            gap = cells[target][0] - cells[s.name][0]
            e.kind = "self" if s.name == target else "down" if gap == 1 else "long" if gap > 1 else "back"
    return list(found.values())


# Drawing


def _text_w(text: str) -> float:
    return len(text) * CHAR_W


def render(flow: Flow) -> str:
    """The SVG of one flow; the same flow always gives the same bytes."""
    cells = layout(flow)
    all_edges = edges(flow, cells)
    rows: dict[int, list[str]] = {}
    for name, (row, _) in cells.items():
        rows.setdefault(row, []).append(name)
    widest = max(len(names) for names in rows.values())
    body_w = widest * NODE_W + (widest - 1) * COL_GAP
    back = [e for e in all_edges if e.kind == "back"]
    right = [e for e in all_edges if e.kind in ("long", "self")]
    label_w = lambda es: max([_text_w(e.label) for e in es], default=0)  # noqa: E731
    left_gutter = (label_w(back) + 16 + LANE * len(back)) if back else 0
    right_gutter = (label_w(right) + 16 + LANE * len(right)) if right else 0
    x0 = PAD + left_gutter
    width = x0 + body_w + right_gutter + PAD

    pos: dict[str, tuple[float, float]] = {}
    for row, names in rows.items():
        row_w = len(names) * NODE_W + (len(names) - 1) * COL_GAP
        left = x0 + (body_w - row_w) / 2
        for col, name in enumerate(names):
            pos[name] = (left + col * (NODE_W + COL_GAP) + NODE_W / 2, PAD + TOP + row * (NODE_H + ROW_GAP) + NODE_H / 2)
    legend_y = PAD + TOP + len(rows) * (NODE_H + ROW_GAP) - ROW_GAP + 30
    height = legend_y + 14 + PAD

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" role="img" aria-label={quoteattr("Flow " + flow.name)}>',
        f"  <title>Flow {escape(flow.name)}</title>",
        "  <defs>",
        '    <marker id="arrow" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto" markerUnits="userSpaceOnUse">',
        f'      <polygon points="0 0, 8 4, 0 8" fill="{EDGE}"/>',
        "    </marker>",
        "  </defs>",
        f'  <rect width="{width:.0f}" height="{height:.0f}" fill="#ffffff"/>',
        f'  <text x="{PAD}" y="{PAD + 4}" font-family="{FONT}" font-size="15" font-weight="600" '
        f'fill="#1b2236">{escape(flow.name)}</text>',
    ]
    sx, sy = pos[flow.start]
    top = sy - NODE_H / 2
    out.append(f'  <circle cx="{sx:.1f}" cy="{top - 26:.1f}" r="6" fill="#1b2236"/>')
    out.append(_line(sx, top - 20, sx, top, dashed=False))

    # the shortest edges get the lanes nearest the nodes, so fewer lines cross
    span = lambda e: (abs(cells[e.source][0] - cells[e.target][0]), all_edges.index(e))  # noqa: E731
    lane_of = {id(e): i for group in (back, right) for i, e in enumerate(sorted(group, key=span))}
    downs: dict[str, list[Edge]] = {}
    for e in all_edges:
        if e.kind == "down":
            downs.setdefault(e.source, []).append(e)
    for e in all_edges:
        (fx, fy), (tx, ty) = pos[e.source], pos[e.target]
        if e.kind == "down":
            sibs = downs[e.source]
            fx += (sibs.index(e) - (len(sibs) - 1) / 2) * 14
            y1, y2 = fy + NODE_H / 2, ty - NODE_H / 2
            if abs(fx - tx) < 1:
                out.append(_line(fx, y1, tx, y2, dashed=False))
            else:
                mid = (y1 + y2) / 2
                out.append(_path(f"M {fx:.1f} {y1:.1f} C {fx:.1f} {mid:.1f}, {tx:.1f} {mid:.1f}, {tx:.1f} {y2:.1f}", dashed=False))
            out.append(_label((fx + tx) / 2 + 6, (y1 + y2) / 2 + 4, e.label, "start"))
        elif e.kind == "back":
            lane = x0 - 16 - LANE * lane_of[id(e)]
            x1, x2 = fx - NODE_W / 2, tx - NODE_W / 2
            lx = lane - label_w(back) - 4
            out.append(_path(f"M {x1:.1f} {fy:.1f} L {lx:.1f} {fy:.1f} L {lx:.1f} {ty + 6:.1f} L {x2:.1f} {ty + 6:.1f}", dashed=True))
            out.append(_label(x1 - 4, fy - 4, e.label, "end"))
        else:
            lane = x0 + body_w + 16 + LANE * lane_of[id(e)]
            x1, x2 = fx + NODE_W / 2, tx + NODE_W / 2
            lx = lane + label_w(right) + 4
            ty_in = ty - 6 if e.kind == "long" else fy + 8
            fy_out = fy if e.kind == "long" else fy - 8
            out.append(_path(f"M {x1:.1f} {fy_out:.1f} L {lx:.1f} {fy_out:.1f} L {lx:.1f} {ty_in:.1f} L {x2:.1f} {ty_in:.1f}", dashed=False))
            out.append(_label(x1 + 4, fy_out - 4, e.label, "start"))

    for name in flow.states:
        out.append(_node(flow.states[name], *pos[name]))
    out.append(_legend(PAD, legend_y))
    out.append("</svg>")
    return "\n".join(out) + "\n"


def _line(x1: float, y1: float, x2: float, y2: float, dashed: bool) -> str:
    return _path(f"M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}", dashed)


def _path(d: str, dashed: bool) -> str:
    dash = ' stroke-dasharray="5 3"' if dashed else ""
    return f'  <path d="{d}" fill="none" stroke="{EDGE}" stroke-width="1.2"{dash} marker-end="url(#arrow)"/>'


def _label(x: float, y: float, text: str, anchor: str) -> str:
    return (
        f'  <text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="11" fill="{LABEL}" '
        f'text-anchor="{anchor}">{escape(text)}</text>'
    )


def _node(s: State, x: float, y: float) -> str:
    fill, stroke, ink = COLORS[s.kind]
    sub = {"work": s.detail, "gate": f"gate: {s.detail}", "end": "end"}[s.kind]
    if s.max_visits is not None:
        sub += f" · max_visits {s.max_visits}"
    return "\n".join([
        f"  <g data-state={quoteattr(s.name)} data-kind={quoteattr(s.kind)}>",
        f'    <rect x="{x - NODE_W / 2:.1f}" y="{y - NODE_H / 2:.1f}" width="{NODE_W}" height="{NODE_H}" '
        f'rx="{NODE_RX}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>',
        f'    <text x="{x:.1f}" y="{y - 3:.1f}" text-anchor="middle" font-family="{FONT}" font-size="13" '
        f'font-weight="600" fill="{ink}">{escape(s.name)}</text>',
        f'    <text x="{x:.1f}" y="{y + 13:.1f}" text-anchor="middle" font-family="{FONT}" font-size="11" '
        f'fill="{ink}">{escape(sub)}</text>',
        "  </g>",
    ])


def _legend(x: float, y: float) -> str:
    items = [("work", "work step (agent)"), ("gate", "gate (human)"), ("end", "end")]
    out = []
    for i, (kind, text) in enumerate(items):
        fill, stroke, ink = COLORS[kind]
        ix = x + i * 150
        out.append(f'  <rect x="{ix:.1f}" y="{y:.1f}" width="14" height="14" rx="3" fill="{fill}" stroke="{stroke}"/>')
        out.append(f'  <text x="{ix + 20:.1f}" y="{y + 11:.1f}" font-family="{FONT}" font-size="11" fill="{ink}">{escape(text)}</text>')
    lx = x + len(items) * 150
    out.append(f'  <path d="M {lx:.1f} {y + 7:.1f} L {lx + 26:.1f} {y + 7:.1f}" stroke="{EDGE}" stroke-width="1.2" stroke-dasharray="5 3"/>')
    out.append(f'  <text x="{lx + 32:.1f}" y="{y + 11:.1f}" font-family="{FONT}" font-size="11" fill="{LABEL}">back to an earlier step</text>')
    return "\n".join(out)


# Comparing


def compare(built: list[Flow], planned: list[Flow]) -> list[str]:
    """Each difference between the built flows and the planned ones, as one line."""
    diffs = []
    by_name = {f.name: f for f in built}
    plan_names = {f.name for f in planned}
    for name in sorted(set(by_name) - plan_names):
        diffs.append(f"flow {name}: built, not in the plan")
    for plan in planned:
        flow = by_name.get(plan.name)
        if flow is None:
            diffs.append(f"flow {plan.name}: planned, not built")
            continue
        p = f"flow {plan.name}"
        if flow.start != plan.start:
            diffs.append(f"{p}: start is {flow.start}, planned {plan.start}")
        for name in plan.states:
            if name not in flow.states:
                diffs.append(f"{p}: state {name}: planned, not built")
        for name, s in flow.states.items():
            want = plan.states.get(name)
            if want is None:
                diffs.append(f"{p}: state {name}: built, not in the plan")
                continue
            if (s.kind, s.detail) != (want.kind, want.detail):
                diffs.append(f"{p}: state {name}: {_kind(s)}, planned {_kind(want)}")
            for outcome in sorted(set(s.outcomes) | set(want.outcomes)):
                got, exp = s.outcomes.get(outcome), want.outcomes.get(outcome)
                if got != exp:
                    diffs.append(f"{p}: state {name}, outcome {outcome}: {got or 'none'}, planned {exp or 'none'}")
            if want.max_visits is not None and s.max_visits != want.max_visits:
                diffs.append(f"{p}: state {name}: max_visits {s.max_visits}, planned {want.max_visits}")
    return diffs


def _kind(s: State) -> str:
    return {"work": f"agent {s.detail}", "gate": f"gate {s.detail}", "end": "end"}[s.kind]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Draw LADO flows as SVG, or compare them with a plan.")
    parser.add_argument("input", type=Path, help="a flow file, a kit or flows folder, or BLUEPRINT.md")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--out", type=Path, help="folder for one <flow name>.svg per flow")
    action.add_argument("--compare", type=Path, help="the plan: BLUEPRINT.md, a folder or a flow file")
    args = parser.parse_args(argv)
    try:
        flows = load(args.input)
        planned = load(args.compare) if args.compare else None
    except FlowError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if planned is not None:
        diffs = compare(flows, planned)
        for line in diffs:
            print(line)
        print(f"{len(diffs)} difference(s) from {args.compare}" if diffs else f"same as the plan in {args.compare}")
        return 1 if diffs else 0
    args.out.mkdir(parents=True, exist_ok=True)
    for flow in flows:
        target = args.out / f"{flow.name}.svg"
        target.write_text(render(flow), encoding="utf-8")
        print(target.as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
