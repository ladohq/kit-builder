# Blueprint: kit-builder

A kit of the official LADO marketplace that helps a LADO user build a kit for their own
work, from "I know nothing about LADO" to a released tag, and evaluate any kit, theirs or
someone else's, before they put it to work. Users are anyone who runs LADO sessions; the
human talks only to the supervisor.

## 1. Requirements

What kit-builder must do, from its specification (`docs/spec.md`, stage 1 "MVP"). Later
stages (trial runs, metrics and `improve`, `extend`) are not requirements of this version.

- **R1** Create a kit: take the human from an interview to a kit in their repository,
  released with a local tag `vX.Y.Z`, with the human approving the design and the release.
  *Source:* spec 1 "create", 4 flow `create`, 8 stage 1.
- **R2** Interview in rounds (question, context, recommendation), starting with "Do you
  already have a process you want to bring over?" and following the branch: transfer an
  existing process (read the human's CLAUDE.md, skills, process description, tracker
  statuses and map them to roles, steps and gates) or start from scratch. *Source:* spec 2,
  4 `design`, skill `kit-interview` in 4.
- **R3** Offer known team shapes when starting from scratch: nine archetypes with their
  roles, flow, when to take them and complexity; Solo is offered first; a group chat or a
  leaderless swarm only when the human asks. *Source:* spec 7.
- **R4** Write `BLUEPRINT.md` at the root of the built kit: requirements, starting point,
  traceability of every part to a requirement, complexity budget, change log. It is the one
  place that says why each part exists, and the author and critic work from it.
  *Source:* spec 5.
- **R5** Measure complexity: a script counts the measures of the budget table (worker roles,
  work steps and gates per flow, words per role prompt, own skills, MCP servers) with a
  green, yellow or red zone each, plus paragraphs repeated across roles and steps; red fails.
  *Source:* spec 6a.
- **R6** Evaluate any kit, own or installed, given as a folder or an installed name:
  layer a (`lado kits check` and the budget) and layer b (a 12-criterion rubric, three
  passes, only repeated findings, each with a quote). Findings are candidates for the human,
  not pass/fail. *Source:* spec 2 S5, 4 flow `evaluate`, 6a, 6b.
- **R7** Report an evaluation as one file `kit-reports/<kit>-<version>-<date>.md`: a card
  (budget, result per layer), findings with quotes and files, "Fix first" with at most 5
  items. *Source:* spec 6 "Report".
- **R8** Release safely: set the version, pass `lado kits check . --tag vX.Y.Z`, commit and
  tag locally; push and a marketplace pull request only after the human's explicit yes,
  with the pull request text ready. *Source:* spec 4 `release`, 10.
- **R9** Simplicity: the simplest kit that solves the task. A part enters a built kit only
  when a requirement needs it, and kit-builder itself stays within its own budget.
  *Source:* spec 1 "main principle", 4 "kit-builder passes its own budget".
- **R10** A marketplace user installs and starts it from the README (`lado kits add
  kit-builder -m official`, `lado start . --kit kit-builder`); the kit is in English and
  runs under any agent CLI LADO supports. *Source:* spec 3, 8 stage 1 "instructions";
  decisions in `docs/mvp-brief.md`.

## 2. Starting point

Archetype 2 of `kit-archetypes`, **Feature with design gate** (3 / 3 / 2), adapted:

- The designer is the supervisor, not a worker role: the design is the interview, and only
  the lead talks to the human in the chat. The supervisor also releases, because tagging and
  asking for the push are the human's conversation.
- The implementer is the `author`, the reviewer is the `critic`, which reviews with the
  budget script and the rubric instead of a code review.
- The work steps are four (`design`, `build`, `evaluate`, `release`) rather than three,
  because the release is a step of its own after the human's release gate.

Evaluating a kit alone is the **Solo** archetype (1 / 1 / 0): the flow `evaluate` with the
critic and no gate, since it changes nothing but a report file.

## 3. Traceability

| Element | Kind | Covers | Why it exists / why nothing simpler |
|---|---|---|---|
| `supervisor` | role (lead) | R1, R2, R3, R4, R8 | Holds the conversation with the human: interview, blueprint, gates explained, release and the push question. LADO gives the chat to the lead only. |
| `author` | role | R1 | Writes the kit's files. A separate role so the critic's check is independent of the writer, and the supervisor stays the human's partner rather than a coder. |
| `critic` | role | R5, R6, R7 | Read-only evaluation with its own rights (writes only the report) and a fresh look; the same role serves `create` and `evaluate`. |
| `create` | flow | R1, R4, R8 | The path interview → approved blueprint → kit → check → approved release → tag. |
| `create.design` | work step | R2, R3, R4 | Interview and blueprint; its note is the whole blueprint, passed on with `needs`. |
| `create.design_ok` | gate | R1, R4 | The blueprint is the human's decision: nothing gets built that they did not approve. |
| `create.build` | work step | R1 | The author writes the kit; on a later visit fixes the critic's findings. |
| `create.evaluate` | work step | R6, R9 | Independent check before release, `max_visits: 3` so the loop with `build` ends. |
| `create.release_ok` | gate | R1, R8 | Tagging is the human's call; on reject the work goes back to the author. |
| `create.release` | work step | R8 | Version, `lado kits check --tag`, merge onto the start branch, local tag, then the push question. |
| `evaluate` | flow | R6, R7 | Evaluation alone, for a kit the human did not build here. |
| `evaluate.evaluate` | work step | R6, R7 | The one critic step; no gate, since it only adds a report file that the supervisor merges. |
| `kit-interview` | skill | R2, R4 | Round format, branches, question bank, mapping the human's material, the blueprint template. |
| `kit-archetypes` | skill | R3, R9 | The nine shapes, Solo first, and the checks every shape passes. |
| `lado-kit-format` | skill | R1, R6, R10 | The format and the rules `lado kits check` does not prove (provider neutrality, paths, one lead, notes and `needs`, gates, `max_visits`); every role writes or reads kits. |
| `kit-budget` | skill | R5, R9 | The budget table and the script `scripts/kit_budget.py`; used by the author before reporting, the critic in layer a and the supervisor for the planned budget. |
| `kit-rubric` | skill | R6, R7 | The 12 criteria, the finding format, the three-pass rule and the report template. |
| `mattpocock-skills` (`grilling`, `writing-for-agents`) | skill dependency | R1, R2 | `grilling` finds what is still the human's to decide in the interview; `writing-for-agents` makes the blueprint and the kit's prompts readable by agents that never saw the interview. Shared, so not copied (decision in `docs/mvp-brief.md`). |
| — | MCP server | — | None: the work is files and the `lado` and `git` commands. |

Reverse check:

- R1: `supervisor`, `author`, `create`, `create.design_ok`, `create.build`,
  `create.release_ok`, `lado-kit-format`, `writing-for-agents`.
- R2: `supervisor`, `create.design`, `kit-interview`, `grilling`.
- R3: `supervisor`, `create.design`, `kit-archetypes`.
- R4: `supervisor`, `create`, `create.design`, `create.design_ok`, `kit-interview`.
- R5: `critic`, `kit-budget`.
- R6: `critic`, `create.evaluate`, `evaluate`, `evaluate.evaluate`, `lado-kit-format`,
  `kit-rubric`.
- R7: `critic`, `evaluate`, `evaluate.evaluate`, `kit-rubric`.
- R8: `supervisor`, `create`, `create.release_ok`, `create.release`.
- R9: `create.evaluate`, `kit-archetypes`, `kit-budget`, and this blueprint's budget below.
- R10: `lado-kit-format` (provider neutrality); the README and `dependencies.lado: ">=0.23"`
  in `kit.yaml` (not kit elements in the sense of section 3).

## 4. Complexity budget

Output of `uv run --script skills/kit-budget/scripts/kit_budget.py .` at the repository
root (exit status 0), after the fixes from the self-evaluation
(`kit-reports/kit-builder-0.1.0-2026-10-06.md`):

```
# Complexity budget: kit-builder 0.1.0

| Measure | Where | Value | Green / yellow up to | Zone |
|---|---|---|---|---|
| Worker roles (not supervisor) | kit | 2 | 3 / 5 | green |
| Work steps in a flow | flows/create.yaml | 4 | 5 / 8 | green |
| Work steps in a flow | flows/evaluate.yaml | 1 | 5 / 8 | green |
| Gates in a flow | flows/create.yaml | 2 | 2 / 3 | green |
| Gates in a flow | flows/evaluate.yaml | 0 | 2 / 3 | green |
| Words in a role prompt | agents/author.md | 468 | 800 / 1500 | green |
| Words in a role prompt | agents/critic.md | 556 | 800 / 1500 | green |
| Words in a role prompt | agents/supervisor.md | 788 | 800 / 1500 | green |
| Own skills | kit | 5 | 5 / 10 | green |
| MCP servers | kit | 0 | 2 / 4 | green |

## Duplicate paragraphs (one rule, one place)

none

Overall: green
```

No measure is over green, so none needs a reason. Three sit at the edge of green: gates in
`create` (2 of 2), own skills (5 of 5) and the supervisor's prompt (788 of 800 words). A
new gate, skill or supervisor rule therefore makes the kit yellow and needs a reason here.

## 5. Change log

Filled by `improve` (stage 3); empty for this first version.

| Date | Version | Change | ← Fact (session, run, metric or report) |
|---|---|---|---|
