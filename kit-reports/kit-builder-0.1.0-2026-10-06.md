# Kit report: kit-builder 0.1.0

- Date: 2026-10-06
- Kit: the repository root of kit-builder (path given; branch `lado/kit-builder/t4-dev` at
  commit aa557b2, with `BLUEPRINT.md`)
- Evaluated by: kit-builder critic (layers a and b), run by hand on kit-builder itself
  following `agents/critic.md`, `kit-rubric` and the `do` of `flows/evaluate.yaml`
- Passes: three independent sub-agents, each with the `kit-rubric` skill and the kit files
  only (not `docs/`, `kit-reports/`, `BACKLOG.md`, `tests/`). Pass 1 started from kit.yaml
  and the roles, pass 2 from the flows step by step, pass 3 from the skills, then the roles
  in reverse order. Findings were merged by place and reason. Where passes filed the same
  problem under different criteria, it sits under the criterion most passes chose. 10
  one-pass findings were dropped.

Findings are candidates for the human to weigh, not a pass/fail grade.

## Card

| Layer | Result |
|---|---|
| a. `lado kits check` | OK; 0 warnings |
| a. Budget | green; no measure over green, no duplicate paragraphs |
| b. Rubric | 18 findings (1 high, 7 medium, 10 low); 2 of 12 criteria without findings |

### `lado kits check .`

```
kit-builder: OK (2 agents, 12 skills, 1 packs and 2 flows)
```

### Budget script (exit status 0)

```
# Complexity budget: kit-builder 0.1.0

| Measure | Where | Value | Green / yellow up to | Zone |
|---|---|---|---|---|
| Worker roles (not supervisor) | kit | 2 | 3 / 5 | green |
| Work steps in a flow | flows/create.yaml | 4 | 5 / 8 | green |
| Work steps in a flow | flows/evaluate.yaml | 1 | 5 / 8 | green |
| Gates in a flow | flows/create.yaml | 2 | 2 / 3 | green |
| Gates in a flow | flows/evaluate.yaml | 0 | 2 / 3 | green |
| Words in a role prompt | agents/author.md | 474 | 800 / 1500 | green |
| Words in a role prompt | agents/critic.md | 566 | 800 / 1500 | green |
| Words in a role prompt | agents/supervisor.md | 784 | 800 / 1500 | green |
| Own skills | kit | 5 | 5 / 10 | green |
| MCP servers | kit | 0 | 2 / 4 | green |

## Duplicate paragraphs (one rule, one place)

none

Overall: green
```

## Fix first

1. In `release`, never leave the start branch mid-merge or on a failing merge commit. Merge
   the start branch into the run's branch in the worktree, check there, and move the start
   branch only by fast-forward (F3.2).
2. Name in `create.evaluate` which findings make `changes` (for example, a high finding
   still open), so the verdict does not vary from run to run (F3.1).
3. Tell the supervisor what to do when the run stops at the loop limit of `evaluate` (F7.1).
4. Cover every later visit. In `build`, name the return after `blocked` with a revised
   blueprint. In `release`, keep the version already set (F2.1, F8.1).
5. Make the `release_ok` question say that approving also merges the run's branch into the
   start branch (F4.1).

## Findings

### 1. Role boundaries

- **F1.1** [medium] `skills/kit-interview/blueprint-template.md:40`
  > script's output after the kit is built.
  Section 4 of a built kit's blueprint is to be replaced by the script's output, but no role
  or step owns that. The supervisor writes the blueprint only in `design`, and the author
  treats the blueprint as the human's. So some runs keep a hand count, and in others the
  author edits the approved blueprint on its own initiative.
  Fix: give it to the author in one sentence: replace section 4 with the script's output
  and change nothing else in the blueprint. Passes: 2/3

### 2. Handoffs between steps

- **F2.1** [medium] `flows/create.yaml:42` (state `build`)
  > On a later visit the previous step's note is the critic's report, or why the release
  There is a third way back into `build`: `blocked` → `design` → `design_ok` → `build`. On
  that path the previous note is the human's approval with the revised blueprint, and
  there is no report. The author looks for findings that are not there and may miss what
  changed in the blueprint.
  Fix: name the case: after `blocked`, the note is the revised blueprint; build what
  changed. Passes: 3/3

### 3. Done and outcomes

- **F3.1** [medium] `flows/create.yaml:65` (state `evaluate`)
  > measure is justified in the blueprint and no finding needs a change before release;
  Which findings "need a change before release" is left to the critic's judgement, while
  `agents/critic.md:55` expects the step to name them:
  > only says whether any finding the step names as blocking is left.
  The same kit can get `approved` in one run and `changes` in another, and low findings
  can use up the three visits.
  Fix: name the threshold, for example "no high finding is open"; medium and low findings
  reach the human in the report at `release_ok`. Passes: 3/3
- **F3.2** [high] `flows/create.yaml:87` (state `release`)
  > branch>` and run `lado kits check . --tag vX.Y.Z` again on the result; on a
  > conflict or a failed check, report `failed`. Then `git tag vX.Y.Z` there. Never
  On a conflict, the human's start branch (main) is left in the middle of a merge. On a
  failed check, a merge commit that fails the check stays on it. The run then goes to
  `build`, where the author works in the run's worktree and cannot repair the start
  branch.
  Fix: merge the start branch into the run's branch inside the worktree, run the check
  there, abort on a conflict, and move the start branch only by `--ff-only`.
  Passes: 3/3 (filed under criteria 3, 8 and 12)

### 4. Independent verification

- **F4.1** [medium] `flows/create.yaml:72` (state `release_ok`)
  > ask: Release the kit? The supervisor sets the version, checks it and tags it locally.
  Approving also merges the run's branch into the start branch (`release`, step 3), but the
  question does not say so. The human approves a merge onto main without being told.
  Fix: name the merge in `ask`. Passes: 2/3

### 5. Contradictions

- **F5.1** [low] `agents/supervisor.md:65`
  > tag, so a pull request before the push fails. Ask once, after the release, with this
  The step asks two questions inside `release`, before it reports `released`
  (`flows/create.yaml:90`):
  > 4. Ask the human whether to push the branch and the tag, and then whether to open a
  "Once, after the release" can be read as after the step, so its note would miss the
  human's choice.
  Fix: in the role, "Ask in the step `release`, after the tag". Passes: 3/3
- **F5.2** [medium] `agents/author.md:34`
  > justified in the blueprint; if neither, say so in your note.
  The `do` of `build` makes the same case not done (`flows/create.yaml:46`):
  > budget script over green is fixed or justified in the blueprint, and the work is
  The role lets the author report `done` with an unjustified measure, but the `do` does not
  count that as done, and no outcome covers it.
  Fix: in the role, "if neither, report `blocked`: the blueprint needs a reason only the
  human can give". Passes: 2/3

### 6. Duplication

- **F6.1** [low] `agents/author.md:16`
  > `design`; on a later visit the previous step's note is the critic's report, or why the
  This repeats `flows/create.yaml:42`, and both copies miss the case in F2.1.
  Fix: keep it in the `do` only. Passes: 2/3
- **F6.2** [low] `agents/supervisor.md:52`
  > a run, that root is the run's worktree (its path is in `flow_status` for the run), because
  "BLUEPRINT.md goes to the root of the run's worktree" is in three places: here,
  `flows/create.yaml:19` and `skills/kit-interview/SKILL.md:91`.
  Fix: keep it in the `design` `do` and in the skill; drop it from the role, which is at
  784 of 800 words. Passes: 3/3
- **F6.3** [low] `flows/create.yaml:61` (state `evaluate`)
  > findings RESOLVED or STILL OPEN first, checking the author's fixed / not fixed list
  This restates `agents/critic.md:60`:
  > previous report is the note from your state. First mark each of its findings RESOLVED or
  Fix: in the `do`, point to the role's "Later visits". Passes: 2/3
- **F6.4** [low] `agents/author.md:32`
  > Before you report, run `lado kits check .` and the `kit-budget` script on the worktree.
  The role restates the done condition of `build` (`flows/create.yaml:45`):
  > Done when `lado kits check .` shows no error, every warning and every measure of the
  The copies already differ (F5.2).
  Fix: keep the rule in the role and the done condition in the `do` as a pointer.
  Passes: 2/3
- **F6.5** [low] `flows/create.yaml:48` (state `build`)
  > Report `blocked` when the blueprint cannot be built as written, or a finding needs the
  The rule for `blocked` is in the `do` and twice in the author role
  (`agents/author.md:12`, `:47`), and the role's copy adds a case:
  > cannot be built as written (a contradiction, a gap, something `lado kits check` rejects),
  Fix: keep it in the role and point to it from the `do`. Passes: 2/3

### 7. When to call the human

- **F7.1** [medium] `flows/create.yaml:54` (state `evaluate`)
  > max_visits: 3
  Nothing says what happens when the loop between `build` and `evaluate` reaches its limit.
  The supervisor's rule covers only a worker that says it is blocked
  (`agents/supervisor.md:84`):
  > if it is yours to decide, otherwise ask the human, then answer the worker; the run waits
  The supervisor will improvise when the run stops for the human.
  Fix: one line in the supervisor's section 5. Show the human the critic's open findings
  and recommend continuing or cancelling. Passes: 3/3

### 8. Loops on a later visit

- **F8.1** [medium] `flows/create.yaml:78` (state `release`)
  > 1. Pick the version with the human: 0.1.0 for a first release unless they want
  `release` can be entered again (`failed` → `build` → … → `release`), but its `do` says
  nothing about a later visit. `kit.yaml` then already holds an untagged version, and
  "otherwise the next one" can turn the first release into 0.1.1.
  Fix: "On a later visit keep the version already set unless the human changes it";
  define a first release as "no `v*` tag yet". Passes: 3/3

### 9. Concision and why

- **F9.1** [low] `flows/evaluate.yaml:14` (state `evaluate`)
  > the run ends, LADO asks the supervisor to merge that branch, which brings the report
  The critic does nothing with this sentence; the supervisor role already owns the merge.
  Fix: delete it. Passes: 3/3
- **F9.2** [low] `agents/critic.md:14`
  > Most evaluations come as a step of a flow run (a message from `lado`): the step says what
  This is exposition: both flows start the critic only inside a run.
  Fix: "In a run, the step's `do` says what to evaluate, when you are done and what the
  note holds." Passes: 3/3
- **F9.3** [low] `agents/supervisor.md:75`
  > Repository names follow the marketplace convention `lado-kit-<name>`, with the GitHub
  No step creates or names a repository, since the kit's repository is the session's. The
  sentence changes nothing, and the prompt is at 784 of 800 words.
  Fix: delete it. Passes: 2/3

### 10. Skill descriptions

- **F10.1** [low] `skills/lado-kit-format/SKILL.md:3`
  > description: The LADO kit format and the rules a kit must follow that `lado kits check` does not prove — provider neutrality, paths, one lead, needs, gates, max_visits. Use when writing or reviewing kit.yaml, a role, a flow or a skill of a kit.
  "Reviewing" a kit also triggers `kit-rubric`, and this description does not say how the
  two differ; the other own skills name their neighbours.
  Fix: add "for judging a kit's text against review criteria use kit-rubric". Passes: 2/3

### 11. Provider neutrality

Checked roles, flows, skills and `kit_budget.py` for one CLI's tool names, slash commands,
model names, config files and absolute paths: none. The script is reached as
`${SKILL_DIR}/scripts/kit_budget.py` (`skills/kit-budget/SKILL.md:14`). `CLAUDE.md` appears
only as the human's material to read, and sub-agents are optional ("If you can start
independent sub-agents").

### 12. Safety and scope

Checked: the tag only after the `release_ok` gate, and "Never move or delete a tag that
exists." (`flows/create.yaml:88`). Push and pull request only after the human's yes
(`agents/supervisor.md:63`, "do them only after the human says yes to each in the chat").
The critic writes only its report, and the author adds nothing the blueprint does not name.
The one gap, a merge left on the start branch, is F3.2.

## Not traced

None. Every role, both flows, every work step and gate, the five own skills and the
dependency `mattpocock-skills` (`grilling`, `writing-for-agents`) have a requirement in
`BLUEPRINT.md` section 3, and the kit has no MCP server. All measures are green; the
blueprint notes the three at the green limit (gates in `create` 2/2, own skills 5/5, the
supervisor's prompt 784/800 words).
