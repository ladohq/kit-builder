---
name: kit-budget
description: Complexity budget of a LADO kit — a script that counts roles, flow steps, gates, prompt words, skills, MCP servers and similar paragraphs and gives each a green, yellow or red zone — and a script that draws each flow as an SVG graph and compares the built flows with the blueprint's flow skeletons. Use when evaluating a kit, when a blueprint needs its budget section or its flow diagrams, or before adding a role, step, gate or skill.
---

# Kit budget

The simplest kit that solves the task wins. The budget makes "simple" a number: every part
over green needs a reason written in the kit's `BLUEPRINT.md` (section "Complexity budget").

## Run it

The script is `scripts/kit_budget.py` in this skill's folder (the folder this SKILL.md is
in). Your agent CLI may expand `${SKILL_DIR}` to that folder; if it does not, put the
folder's path there yourself:

```bash
uv run --script ${SKILL_DIR}/scripts/kit_budget.py <kit folder>
```

For an installed kit, `lado kits show <name>` prints its folder. The script needs only `uv`
(it declares PyYAML itself). Quote its output as it is; do not recount by hand.

Exit status: `0` green or yellow, `1` at least one measure is red, `2` the folder is not a
kit (no or empty `kit.yaml`), or a kit.yaml, flow or role frontmatter is not valid YAML or
not a mapping.

## Measures and zones

| Measure | Counted per | Green | Yellow | Red |
|---|---|---|---|---|
| Worker roles (not supervisor) | kit | ≤ 3 | 4–5 | > 5 |
| Work steps in a flow | flow | ≤ 5 | 6–8 | > 8 |
| Gates in a flow | flow | ≤ 2 | 3 | > 3 |
| Words in a role prompt | role | ≤ 800 | 801–1500 | > 1500 |
| Words in the lead's prompt | lead | ≤ 1000 | 1001–1500 | > 1500 |
| Own skills | kit | ≤ 5 | 6–10 | > 10 |
| MCP servers | kit | ≤ 2 | 3–4 | > 4 |

How each is counted:
- **Worker roles**: files `agents/*.md`, minus the agent named by `supervisor:` in
  `kit.yaml` and minus an agent named `supervisor` (LADO reserves that name for the lead).
- **Work steps**: states of one `flows/*.yaml` that have `agent:`; gates and ends are not
  steps. Each flow gets its own row and zone.
- **Gates**: states of one flow that have `gate:` (approval or choice).
- **Words in a role prompt**: the body of `agents/<role>.md` after the YAML frontmatter,
  split on whitespace. Every worker role gets its own row.
- **Words in the lead's prompt**: the same count for the lead (the supervisor, as in
  "Worker roles"). The lead gets a higher green limit: it runs the session and the flows
  and talks to the human, so it carries more rules than one worker.
- **Own skills**: folders `skills/<name>/` that hold a `SKILL.md`. Skills from
  `dependencies.skills` are not counted: they are shared, not the kit's text.
- **MCP servers**: distinct server names under `mcp:` in the frontmatter of all
  `agents/*.md` (the only place a kit declares MCP servers); a server two roles use counts once.

A flow-less or role-less kit gets one row with value 0 for those measures. The overall zone
is the worst row.

## Similar paragraphs

One rule, one place. A paragraph is a block between blank lines in a role prompt or in a
flow state's `do`. The script compares every two paragraphs in different places (roles,
states, or a role and a state) and lists each pair at 55% similar or more, most similar
first, with both places. A repeat inside one place is not listed.

Similarity is the Jaccard index of the two paragraphs' content words: the distinct words
both have, divided by the distinct words either has. Words are lowercased, punctuation is
dropped, and common function words ("the", "you", "when") are left out, since any two
English paragraphs share them. The same paragraph, ignoring case and spacing, is 100%.
The list of function words is English only: in a kit written in another language they
stay in, and similarity comes out too high. The method catches close repeats of a whole
paragraph; a rule repeated inside a longer paragraph scores lower and is left to rubric
criterion 6 (`kit-rubric`).

Paragraphs under 8 words are not compared. A short paragraph is most often a pointer
("Follow `lado-checks`, "Merging a run's branch"."), which is the fix, not the repeat; and
in a few words one shared term moves the score a lot. Point to a rule in under 8 words.

The 55% was calibrated on lado-dev 0.9.1–0.9.4 and kit-builder 0.1.1. Whole-paragraph
repeats scored 57% (a merge step reworded in one flow) to 100%. Below the line are repeats
the script misses: the roles' "Most tasks come as a step of a flow run..." openings, worded
apart (48–52%), and rules repeated inside longer paragraphs (the verdict and
`flow_advance` rule of architect and reviewer, 41–45%; RESOLVED / STILL OPEN, 38%).
Different paragraphs scored lower; kit-builder's highest pair was 28%.

Each pair is yellow: it makes the overall zone at least yellow but never red. Fix it by
keeping the rule where it belongs (the role if it holds in every step, the `do` if it
belongs to one step, a skill if several roles need it) and pointing to it from the others.
Rewording a repeat until it scores under 55% does not fix it.

## Reading the result

- Green: nothing to justify.
- Yellow: allowed when `BLUEPRINT.md` says which requirement needs it and why a simpler
  shape does not work.
- Red: cut it before release (merge roles or steps, move text into a skill). The thresholds
  are starting values: if a red measure truly cannot be cut, tell the human; changing a
  threshold is a change to kit-builder, not to the kit.

## Flow diagram

The budget counts the shape; the diagram shows it. `scripts/flow_diagram.py` in this
skill's folder draws each flow as a graph: work steps (with their agent), gates and ends in
their own colours, an edge per outcome labelled with its name, `max_visits` on the state.
Run from the same folder as the budget:

```bash
uv run --script ${SKILL_DIR}/scripts/flow_diagram.py <input> --out <folder>
uv run --script ${SKILL_DIR}/scripts/flow_diagram.py <kit folder> --compare <kit folder>/BLUEPRINT.md
```

`<input>` is a flow file, a kit folder (its `flows/*.yaml`) or a Markdown file: in
`BLUEPRINT.md` every fenced `yaml` block with `states:` is a flow skeleton (the template in
`kit-interview` shows one). `--out` writes `<flow name>.svg` per flow, the same bytes for
the same flow, so a committed diagram changes only when its flow does. `--compare` prints
each difference between the built flows and the skeletons: a flow, state, agent, gate,
outcome or planned `max_visits` that one has and the other does not. The built flows and
the blueprint must agree: when they differ, one of them is wrong.

Exit status: `0` done, or no difference; `1` the flows differ from the skeletons; `2` an
input is missing or a flow is not valid (an outcome to an unknown state, a state not
reachable from `start`, no `end: true` state, a skeleton state with keys other than
`agent`, `gate`, `end`, `outcomes` and `max_visits`). The error names the file and state.

The drawing is ported from the Tessera kit-builder's `render_workflow_diagram.py`.
