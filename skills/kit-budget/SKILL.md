---
name: kit-budget
description: Complexity budget of a LADO kit — a script that counts roles, flow steps, gates, prompt words, skills, MCP servers and duplicate paragraphs and gives each a green, yellow or red zone. Use when evaluating a kit, when a blueprint needs its budget section, or before adding a role, step, gate or skill.
---

# Kit budget

The simplest kit that solves the task wins. The budget makes "simple" a number: every part
over green needs a reason written in the kit's `BLUEPRINT.md` (section "Complexity budget").

## Run it

```bash
uv run --script ${SKILL_DIR}/scripts/kit_budget.py <kit folder>
```

For an installed kit, `lado kits show <name>` prints its folder. The script needs only `uv`
(it declares PyYAML itself). Quote its output as it is; do not recount by hand.

Exit status: `0` green or yellow, `1` at least one measure is red, `2` the folder is not a
kit (no `kit.yaml`) or a file is not valid YAML.

## Measures and zones

| Measure | Counted per | Green | Yellow | Red |
|---|---|---|---|---|
| Worker roles (not supervisor) | kit | ≤ 3 | 4–5 | > 5 |
| Work steps in a flow | flow | ≤ 5 | 6–8 | > 8 |
| Gates in a flow | flow | ≤ 2 | 3 | > 3 |
| Words in a role prompt | role | ≤ 800 | 801–1500 | > 1500 |
| Own skills | kit | ≤ 5 | 6–10 | > 10 |
| MCP servers | kit | ≤ 2 | 3–4 | > 4 |

How each is counted:
- **Worker roles**: files `agents/*.md`, minus the agent named by `supervisor:` in
  `kit.yaml` and minus an agent named `supervisor` (LADO reserves that name for the lead).
- **Work steps**: states of one `flows/*.yaml` that have `agent:`; gates and ends are not
  steps. Each flow gets its own row and zone.
- **Gates**: states of one flow that have `gate:` (approval or choice).
- **Words in a role prompt**: the body of `agents/<role>.md` after the YAML frontmatter,
  split on whitespace. Every role, the supervisor too, gets its own row.
- **Own skills**: folders `skills/<name>/` that hold a `SKILL.md`. Skills from
  `dependencies.skills` are not counted: they are shared, not the kit's text.
- **MCP servers**: distinct server names under `mcp:` in the frontmatter of all
  `agents/*.md` (the only place a kit declares MCP servers); a server two roles use counts once.

A flow-less or role-less kit gets one row with value 0 for those measures. The overall zone
is the worst row.

## Duplicate paragraphs

One rule, one place. A paragraph is a block between blank lines in a role prompt or in a
flow state's `do`. Two paragraphs are the same when they match ignoring case, line breaks
and spacing. Paragraphs under 8 words are skipped. A paragraph found in two or more places
(roles, states, or a role and a state) is listed with its places. A repeat inside one place
is not listed.

Each duplicate is yellow: it makes the overall zone at least yellow but never red. Fix it by
keeping the rule where it belongs (the role if it holds in every step, the `do` if it
belongs to one step, a skill if several roles need it) and pointing to it from the others.

## Reading the result

- Green: nothing to justify.
- Yellow: allowed when `BLUEPRINT.md` says which requirement needs it and why a simpler
  shape does not work.
- Red: cut it before release (merge roles or steps, move text into a skill). If it truly
  cannot be cut, the blueprint says why and the human decides. The thresholds are
  starting values.
