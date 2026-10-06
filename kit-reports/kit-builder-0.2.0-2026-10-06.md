# Kit report: kit-builder 0.2.0

- Date: 2026-10-06
- Kit: the repository root of kit-builder (path given), branch `lado/kit-builder/v02-final`
- Commit: 3411844 (the candidate for 0.2.0; `kit.yaml` still says 0.1.1, the version is set
  at release)
- Evaluated by: kit-builder critic (layers a and b), run by hand on kit-builder itself
  following `agents/critic.md`, `kit-rubric` and the `do` of `flows/evaluate.yaml`
- Mode: re-evaluation against `kit-reports/kit-builder-0.1.0-2026-10-06.md`,
  `git diff aa557b2 -- . ':!kit-reports'` (the base is the commit in that report's "Kit:"
  line; `docs/`, `tests/` and `BACKLOG.md` are not kit text and were left out of the review)
- Passes: three independent sub-agents, each with `kit-rubric`, the kit files and the diff;
  pass 1 started from kit.yaml and the roles, pass 2 from the flows step by step, pass 3
  from the skills, then the roles in reverse order. A fourth sub-agent did the cut-rule
  check over the word diff. The diff touches every role, flow and skill (703 lines added,
  272 removed), so "the changed text and its surroundings" was the whole kit. Findings were
  merged by place and reason; where passes filed one problem under different criteria, it
  sits under the criterion most passes chose, or the one closest to the fix on a tie.
  3 one-pass findings dropped, 4 kept as confirmed.

Findings are candidates for the human to weigh, not a pass/fail grade.

## Card

| Layer | Result |
|---|---|
| a. `lado kits check` | OK; 0 warnings |
| a. Budget | green; no measure over green, no similar paragraphs |
| b. Rubric | 15 findings (1 high, 6 medium, 8 low); 4 of 12 criteria without findings |
| Stop rule | not: 1 high and 6 medium in the changed text |

### `lado kits check .`

```
kit-builder: OK (2 agents, 12 skills, 1 packs and 3 flows)
```

### Budget script (exit status 0)

```
# Complexity budget: kit-builder 0.1.1

| Measure | Where | Value | Green / yellow up to | Zone |
|---|---|---|---|---|
| Worker roles (not supervisor) | kit | 2 | 3 / 5 | green |
| Work steps in a flow | flows/create.yaml | 4 | 5 / 8 | green |
| Work steps in a flow | flows/evaluate.yaml | 1 | 5 / 8 | green |
| Work steps in a flow | flows/improve.yaml | 5 | 5 / 8 | green |
| Gates in a flow | flows/create.yaml | 2 | 2 / 3 | green |
| Gates in a flow | flows/evaluate.yaml | 0 | 2 / 3 | green |
| Gates in a flow | flows/improve.yaml | 2 | 2 / 3 | green |
| Words in a role prompt | agents/author.md | 633 | 800 / 1500 | green |
| Words in a role prompt | agents/critic.md | 714 | 800 / 1500 | green |
| Words in the lead's prompt | agents/supervisor.md | 960 | 1000 / 1500 | green |
| Own skills | kit | 5 | 5 / 10 | green |
| MCP servers | kit | 0 | 2 / 4 | green |

## Similar paragraphs (one rule, one place; 55% similar or more)

none

Overall: green
```

## Fix first

1. Let `improve.build` take what a later visit brings: the critic's findings on the change,
   a reject reason, a failed release, a revised plan after `blocked` (F5.1, F8.1).
2. Tell the author to merge the start branch and resolve the conflict after a failed
   release, or report `blocked` (F7.1).
3. Fix the base of a re-evaluation in `improve` in the plan, not in a report file the
   critic rewrites (F2.1).
4. Name what the human can do when a run stops at the loop limit (F7.2).
5. Let `improve` start from the last report of the kit's content, not of the version in
   its file name, and give the human's own requests a place in the plan (F2.2, F2.3).

## Findings

### 1. Role boundaries

No finding. The critic writes only its report (`agents/critic.md:10`, "You change no file
of the kit you evaluate; the only file you write is the report."), the author only what the
blueprint or plan names (`agents/author.md:12`), the supervisor no role, flow or skill
(`agents/supervisor.md:14`). The one action nobody owns, resolving a release conflict, is
F7.1.

### 2. Handoffs between steps

- **F2.1** [medium] `skills/kit-rubric/SKILL.md:152` (flow `improve`, state `evaluate`)
  > commit. In `improve` the base is the commit the plan's report evaluated, on every
  The plan names the report by path only (`skills/kit-interview/SKILL.md:75`, "report
  <path>"), and the version in the report's name changes only at `release`, so on the same
  day `improve.evaluate` writes to the same path and is told to rewrite it
  (`agents/critic.md:74`):
  > text. Rewrite the same report file when its name is
  On visit 2 or 3 the "Commit:" in that file is the author's first-round commit; the base
  moves forward, first-round text counts as unchanged, and its new findings fall into the
  non-blocking "Missed earlier".
  Fix: the plan's first line records the report's commit, and the rubric takes the base
  from the plan. Passes: 3/3
- **F2.2** [medium] `agents/supervisor.md:31`
  > report of this version (in `kit-reports/`, merged), so the critic does not evaluate again.
  The critic's last report in a run carries the version before the release (the version is
  set in `release`, `agents/supervisor.md:64`), and `assess` treats a report of another
  version as background (`flows/improve.yaml:20`, "A report of another version is only
  background: evaluate anew."). So after any release no report "of this version" exists,
  and every `improve` starts with a full evaluation. This repository shows it: the report
  for 0.2.0 is written against a `kit.yaml` that says 0.1.1.
  Fix: name the latest report whose commit the kit has not changed since, other than the
  version in `kit.yaml`; `assess` uses it on that condition. Passes: 1/3, confirmed
- **F2.3** [medium] `skills/kit-interview/SKILL.md:76`
  > Fix: - <finding id and title>: <what to change, in which file>
  The supervisor sends a human who wants to "improve it with or without a `BLUEPRINT.md`" to
  `improve` (`agents/supervisor.md:30`), but the branch "Existing kit" goes only through the
  report's findings, questions and measures, and the plan has no line for a change the
  human asks for that no finding covers. Supervisors will invent a finding id, drop the
  request or send it to `create`.
  Fix: in step 3 add the human's own requests, and a `Change:` line to the plan form.
  Passes: 1/3, confirmed
- **F2.4** [low] `agents/critic.md:64`
  > those in the report under "Left by the plan". You still write findings, not
  `skills/kit-rubric/report-template.md` has no such section (`grep -c "Left by the plan"`
  gives 0), and the rubric says to fill the template's sections, so where the list goes
  varies by run.
  Fix: add the section to the template, improve only. Passes: 2/3

### 3. Done and outcomes

- **F3.1** [low] `flows/create.yaml:50` (state `evaluate`; also `improve.evaluate`)
  > Check the kit against its blueprint (the note from design).
  The role promises the opposite (`agents/critic.md:14`):
  > In a run, the step's `do` says what to evaluate and which outcome to report; this role
  The verdict rule is in the role (`agents/critic.md:56`), so critics manage, but the two
  texts disagree on where to look.
  Fix: in the role, "the step's `do` says what to evaluate; this role says how, which
  outcome to report, when you are done and what goes into the note". Passes: 3/3

### 4. Independent verification

No finding. In `create` and `improve` the critic's `evaluate` (`max_visits: 3`) comes
before `release_ok`, and `release_ok` before any merge or tag; the release re-runs
`lado kits check . --tag vX.Y.Z` after merging the start branch (`agents/supervisor.md:70`).

### 5. Contradictions

- **F5.1** [high] `flows/improve.yaml:50` (state `build`)
  > Change only what the plan (the note from triage) lists; a finding it leaves is not
  `improve.build` is entered again after the critic's `changes`, a reject at `release_ok` and
  a failed `release`, and the author's role then says to fix the critic's findings or the
  release failure (`agents/author.md:39`). A new finding the author's own change caused, a
  reject reason or a merge conflict is in no plan, so the `do` forbids it. An author that
  obeys the `do` marks it "not in the plan", the critic answers `changes` again, and the
  loop runs to `max_visits`.
  Fix: "and on a later visit what the previous note asks"; a finding the plan leaves stays
  not yours. Passes: 2/3
- **F5.2** [low] `agents/author.md:34`
  > Replace the planned values in section 4 of `BLUEPRINT.md` with the script's output, keeping
  In `improve` the `do` allows only what the plan lists (F5.1), and the plan does not list
  section 4, so some authors leave the blueprint's budget stale. This repository shows the
  result: section 4 of `BLUEPRINT.md` is the 0.1.1 output (F9.1).
  Fix: let the `do` of `improve.build` keep the role's section 4 rule. Passes: 1/3, confirmed

### 6. Duplication

- **F6.1** [low] `agents/supervisor.md:49`
  > In `design` your first question is always: "Do you already have a process you want to
  The same rule is in `skills/kit-interview/SKILL.md:31`, which the line before points to,
  and the copies already differ ("In `design`" against "For a new kit").
  Fix: delete the role's copy. Passes: 3/3

### 7. When to call the human

- **F7.1** [medium] `agents/supervisor.md:69`
  > conflict, `git merge --abort` and report `failed` with the conflicting files. Then run
  The run goes to `build`, but nothing tells the author to merge the start branch into the
  run's branch and resolve the conflict, or to take a conflict that needs a content decision
  to the human (`agents/supervisor.md:71`, "The author fixes either on the run's branch.";
  the author's later visit is about findings). The author edits files without merging, the
  next `release` conflicts again, and the loop spends the visits of `evaluate`.
  Fix: one sentence in the author's later visit: merge the start branch, resolve, commit;
  `blocked` when a conflict needs the human. Passes: 3/3 (filed under criteria 1, 3 and 7)
- **F7.2** [medium] `agents/supervisor.md:88`
  > happens on reject. At `release_ok`, and when a run stops at the loop limit of `evaluate`,
  At the loop limit the human "decides", but no text says between what: another round
  (`lado flow-set <session> <run> build`), releasing with the open findings
  (`... release_ok`), or leaving the run and its branch. Each supervisor offers something
  else.
  Fix: name the options and that the human runs `lado flow-set` with a reason. Passes: 2/3
- **F7.3** [low] `agents/supervisor.md:77` at aa557b2 (removed line)
  > -what is left for the human to do.
  Lost: "Without a yes, the release ends at the local tag; say what is left for the human to
  do." Now only the first half is at `agents/supervisor.md:79`, and the release note has
  only what the human chose. A human who declines the push is not told what remains (push,
  the pull request text). Fix: append it again. Passes: cut-rule check

### 8. Loops on a later visit

- **F8.1** [medium] `agents/author.md:39` (flow `improve`, state `build` after `blocked`)
  > On a later visit the previous step's note says why you are back: the critic's report, or
  After `blocked` → `triage` → `plan_ok` the note is the revised plan. `create.build` names
  that case (`flows/create.yaml:41`, "After `blocked`, the previous step's note is the
  revised blueprint"), `improve.build` does not, so the author redoes the whole plan or
  guesses what changed. Fix: name it in the `do` of `improve.build`.
  Passes: 1/3, confirmed

### 9. Concision and why

- **F9.1** [low] `BLUEPRINT.md:166`
  > yellow and needs a reason here. The supervisor's prompt is near it (753 of 800 words).
  Section 4 is the 0.1.1 output: no rows for `flows/improve.yaml` (5 of 5 work steps, 2 of 2
  gates, both at the edge of green) and the supervisor counted as a role, not as the lead
  (960 of 1000). An agent planning a change from it misses that one more step in `improve`
  makes the kit yellow. Fix: paste the current output and update the sentence.
  Passes: 3/3

### 10. Skill descriptions

No finding. Each own skill says what it holds and when to use it; `kit-interview`,
`kit-archetypes` and `lado-kit-format` name the neighbour to use instead
(`skills/lado-kit-format/SKILL.md:3`, "for judging a kit's text against review criteria use
kit-rubric"). Each skill a role lists is used by it.

### 11. Provider neutrality

No finding. Skill files are reached through `${SKILL_DIR}` with a fallback
(`skills/kit-budget/SKILL.md:14`, "Your agent CLI may expand `${SKILL_DIR}` to that folder");
the commands are `lado`, `git` and `uv`; the tools named are LADO's.

### 12. Safety and scope

- **F12.1** [low] `flows/improve.yaml:39`
  > Report `nothing` when the human decides to change nothing; when the run ends, merge
  On `nothing`, a restored `BLUEPRINT.md` reaches the start branch with no gate and no check
  by the critic; the human answered only the uncertain parts. Fix: merge the restored
  blueprint only on the human's yes. Passes: 2/3
- **F12.2** [low] `agents/supervisor.md:75` at aa557b2 (removed line)
  > -Repository names follow the marketplace convention `lado-kit-<name>`, with the GitHub
  Lost: the repository name and the GitHub topic `lado-kit` are in no file now;
  `lado-kit-format` "Publishing" did not take them when the pull request text moved there.
  Fix: one line in "Publishing". Passes: cut-rule check

## Not traced

None. Every role, the three flows, each of their work steps and gates, the five own skills
and the dependency `mattpocock-skills` have a requirement in `BLUEPRINT.md` section 3; no
measure is over green. Section 4 itself is stale (F9.1).

## Previous findings

All 18 findings of `kit-builder-0.1.0-2026-10-06.md` are RESOLVED.

- **F1.1** RESOLVED. `agents/author.md:34`: "Replace the planned values in section 4 of
  `BLUEPRINT.md` with the script's output".
- **F2.1** RESOLVED. `flows/create.yaml:41`: "After `blocked`, the previous step's note is
  the revised blueprint".
- **F3.1** RESOLVED. `agents/critic.md:58-60`: "no high finding is open"; "Medium and low
  findings do not block".
- **F3.2** RESOLVED. `agents/supervisor.md:67-74`: the start branch is merged into the run's
  branch in the worktree, `git merge --abort` on a conflict, the start branch moves only by
  `git merge --ff-only`.
- **F4.1** RESOLVED. `flows/create.yaml:56-57`: "merges the run's branch into the branch the
  run started from and tags it locally".
- **F5.1** RESOLVED. The push and pull request questions are step 4 of the release, before
  `released` (`agents/supervisor.md:76-81`); "Ask once, after the release" is gone.
- **F5.2** RESOLVED. `agents/author.md:63-65`: `blocked` "when a warning or a measure over
  green is neither fixable nor justified in the blueprint".
- **F6.1** RESOLVED. The general later visit is in the role (`agents/author.md:39`), the
  `do` keeps only the `blocked` case.
- **F6.2** RESOLVED. The worktree root is in `flows/create.yaml:19` and
  `skills/kit-interview/SKILL.md:124`, not in the role.
- **F6.3** RESOLVED. `flows/create.yaml:50` points to the blueprint only; marking findings
  is in `kit-rubric` "Re-evaluation" step 2.
- **F6.4** RESOLVED. The done condition is only in `agents/author.md:57`.
- **F6.5** RESOLVED. The `blocked` rule is only in `agents/author.md:63-67`.
- **F7.1** RESOLVED. `agents/supervisor.md:88`: "when a run stops at the loop limit of
  `evaluate`" (what the human may then do is the new F7.2).
- **F8.1** RESOLVED. `agents/supervisor.md:64`: "on a later visit keep the one in `kit.yaml`";
  `flows/create.yaml:62-63`: "0.1.0 when the repository has no `v*` tag yet".
- **F9.1** RESOLVED. `flows/evaluate.yaml` no longer explains the merge.
- **F9.2** RESOLVED. `agents/critic.md:14`: "In a run, the step's `do` says…".
- **F9.3** RESOLVED. The sentence is gone from the role (its loss as a rule is F12.2).
- **F10.1** RESOLVED. `skills/lado-kit-format/SKILL.md:3`: "for judging a kit's text against
  review criteria use kit-rubric".

## Cut rules

| Removed rule (file:line at base) | Where it is now |
|---|---|
| `agents/supervisor.md:24-28` start `create`; "Building nothing is the right answer here." | `agents/supervisor.md:15-17`, `:26-37` (with `improve`) |
| `agents/supervisor.md:37-46` rounds, look facts up, stop when every requirement is written | `skills/kit-interview/SKILL.md:9-27` (rounds now batched, 0.1.1); `flows/create.yaml:15-22`; `flows/improve.yaml:35` |
| `agents/supervisor.md:50-57` blueprint at the worktree root, five sections, planned budget | `skills/kit-interview/SKILL.md:123-126`; `flows/create.yaml:19-20`; `agents/supervisor.md:59`; `skills/kit-interview/blueprint-template.md:39-40` |
| `agents/supervisor.md:61-73` release after the gate, push before pull request and why, pull request text | `agents/supervisor.md:63-82`; `skills/lado-kit-format/SKILL.md:66-77` |
| `agents/supervisor.md:75-76` repository name `lado-kit-<name>`, topic `lado-kit` | lost: F12.2 |
| `agents/supervisor.md:76-77` "say what is left for the human to do"; `flows/create.yaml:96` "or what is left for them to do" | lost: F7.3 |
| `agents/author.md:10-34` blueprint is the human's, `blocked` instead of guessing, errors and warnings fixed or justified | `agents/author.md:11-14`, `:55-67` ("say so in your note" became `blocked`, on purpose) |
| `agents/critic.md` "Most evaluations come as a step…", verdict, later visits | `agents/critic.md:14-16`, `:56-75`; `skills/kit-rubric/SKILL.md:143-179` (re-reviewing the whole kit replaced on purpose by the change) |
| `flows/create.yaml` `build`, `evaluate`, `release` `do`s | `agents/author.md`, `agents/critic.md` "5. Report", `agents/supervisor.md` "4. Release"; "no finding needs a change" replaced on purpose by "no high finding is open"; the ff fallback by merging the start branch first |
| `flows/evaluate.yaml` the merge after the run | `agents/supervisor.md:34-35` |
| `skills/kit-budget/SKILL.md:68-69` a red measure the blueprint justifies | replaced on purpose (d468d37, "red is cut"): `skills/kit-budget/SKILL.md:96-98` |
| `skills/kit-budget/SKILL.md` exact duplicates, every role a row | `skills/kit-budget/SKILL.md:46-50`, `:59-89` (similar paragraphs, lead row; task C) |
| `skills/kit-rubric/SKILL.md:25` only findings of two passes | `skills/kit-rubric/SKILL.md:25-33` (confirmed one-pass findings kept, on purpose) |
| the rest (`kit.yaml`, README, `kit-archetypes`, `lado-kit-format`, `BLUEPRINT.md`, report template) | rewording or extension; nothing lost |

## Missed earlier

None. The diff touches every file of the kit text, so no finding lies in unchanged text.

## Questions for the human

1. After a `nothing` in `improve`, should a restored `BLUEPRINT.md` be merged at all (F12.1)?
   Recommended: yes, on the human's explicit yes after they saw it; otherwise only the
   report.
2. Should kit-builder state the marketplace's naming convention again (F12.2)?
   Recommended: yes, one line in `lado-kit-format` "Publishing".
