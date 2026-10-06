# Kit report: lado-dev 0.9.1

- Date: 2026-10-06
- Kit: /Users/aleksejkolesnikov/.lado/cache/kit-lado-dev-4f0aa9be/v0.9.1, found with
  `lado kits show lado-dev` (the installed release v0.9.1)
- Evaluated by: kit-builder critic (layers a and b)
- Passes: three independent sub-agents, each with the `kit-rubric` skill and the kit folder
  only; pass 1 started from kit.yaml and the roles, pass 2 from the flows, pass 3 from the
  skill and the roles in reverse order. 9 one-pass findings dropped. 3 findings that all
  three passes made were dropped after checking LADO's code (see "Found on the way").

Findings are candidates for the human to weigh, not a pass/fail grade.

## Card

| Layer | Result |
|---|---|
| a. `lado kits check` | OK; 0 warnings |
| a. Budget | yellow; words in `agents/developer.md` 904, in `agents/supervisor.md` 1273; 1 duplicate paragraph (`merge` in both flows) |
| b. Rubric | 10 findings (0 high, 7 medium, 3 low); 5 of 12 criteria without findings |

### `lado kits check /Users/aleksejkolesnikov/.lado/cache/kit-lado-dev-4f0aa9be/v0.9.1`

```
lado-dev: OK (3 agents, 71 skills, 4 packs and 2 flows)
```

### Budget script (exit status 0)

```
# Complexity budget: lado-dev 0.9.1

| Measure | Where | Value | Green / yellow up to | Zone |
|---|---|---|---|---|
| Worker roles (not supervisor) | kit | 3 | 3 / 5 | green |
| Work steps in a flow | flows/feature.yaml | 5 | 5 / 8 | green |
| Work steps in a flow | flows/fix.yaml | 3 | 5 / 8 | green |
| Gates in a flow | flows/feature.yaml | 2 | 2 / 3 | green |
| Gates in a flow | flows/fix.yaml | 1 | 2 / 3 | green |
| Words in a role prompt | agents/architect.md | 589 | 800 / 1500 | green |
| Words in a role prompt | agents/developer.md | 904 | 800 / 1500 | yellow |
| Words in a role prompt | agents/reviewer.md | 790 | 800 / 1500 | green |
| Words in a role prompt | agents/supervisor.md | 1273 | 800 / 1500 | yellow |
| Own skills | kit | 1 | 5 / 10 | green |
| MCP servers | kit | 0 | 2 / 4 | green |

## Duplicate paragraphs (one rule, one place)

- yellow: "Record what the review found on the way, then check the branch together with the current main bef..." in flows/feature.yaml: state "merge"; flows/fix.yaml: state "merge"

Overall: yellow
```

## Fix first

1. Give the supervisor a rule for a worker's NEEDS_CONTEXT or BLOCKED message inside a run
   (answer, ask the human, or cancel on the human's word), so a blocked run cannot stall
   (F7.1).
2. Put the human's yes before the two outward or paid actions that lack it: publishing a
   mockup page and a paid `make test-live` during a run (F12.1, F12.2).
3. Settle whether a non-code-only change needs `make check` or `make lint` and say it in one
   place (F5.1).
4. Drop `finishing-a-development-branch` from the supervisor and `requesting-code-review`
   from the reviewer: nothing calls for them, and the first competes with the `merge`
   step (F10.1, F10.2).
5. Move the merge-step "skip `make check`" rule into `lado-checks` only and point to it from
   the reviewer role and both `merge` steps; this also clears the budget's duplicate
   paragraph (F6.1).

## Findings

### 1. Role boundaries

- **F1.1** [medium] `agents/supervisor.md:65` (state `design` of `feature`)
  > A UI design starts from `docs/design/ui.md` in the LADO repo and updates it with what the
  The supervisor, who otherwise designs and merges but writes no product files, is told to
  edit a tracked file during the design step without saying on which branch or who
  commits it: it may land on main outside review, or stay uncommitted in the run's
  worktree. Fix: make the ui.md update part of the design, carried out and committed by
  the developer on the run's branch. Passes: 2/3

### 2. Handoffs between steps

No finding. All three passes questioned `implement` and `merge` getting the architect's and
the reviewer's notes after a gate; LADO passes the note that led to a gate on with the
human's answer, and the step says so: `flows/feature.yaml:64`
> worktree, test-first, as your role describes. The architect's review comes with the

### 3. Done and outcomes

No finding. Every work state's `do` has a done condition and a condition per outcome, for
example `flows/feature.yaml:48`
> Done when every point of your review has a verdict with its evidence. Report

### 4. Independent verification

No finding. Every branch goes through `review` (another role) and the `merge_ok` gate
before `merge`; `agents/supervisor.md:112`
> - Every branch is reviewed before it is merged, however small; never skip a flow's review.

### 5. Contradictions

- **F5.1** [medium] `skills/lado-checks/SKILL.md:19` and `skills/lado-checks/SKILL.md:31`
  > | The change is ready | `make check` | Developer: always, last, before you report done. Reviewer and merge step: as the rules below say. It runs all four above. |

  > - A change only to non-code paths (defined below) needs `make lint` only; a change to a
  The `implement` steps side with the first line (`flows/fix.yaml:16`: "Run `make check`
  after your last change and commit on the run's branch."), so for a docs-only `fix` the
  developer gets two answers and runs will differ. Fix: say in line 19 whether the
  non-code exception applies to the developer, and make the `implement` steps point to
  that rule. Passes: 3/3

### 6. Duplication

- **F6.1** [low] `agents/reviewer.md:35`, `flows/feature.yaml:110`, `flows/fix.yaml:53`
  > `git diff --name-only <that commit> HEAD` is a non-code path as `lado-checks` defines

  > 3. Skip `make check` only when both hold (`lado-checks`, "Run as little as proves
  The re-review and merge-step rules for skipping `make check` are written out in full in
  `lado-checks` (from line 43: "- The merge step skips `make check` only when both hold:
  `git merge main` brought nothing"), in the reviewer role and in both `merge` steps; four
  copies of one rule will drift. Fix: keep it in `lado-checks` and leave one-line pointers.
  Passes: 3/3
- **F6.2** [low] `agents/developer.md:43` and `flows/fix.yaml:17` (state `implement`)
  > it tests. Done when every AC is covered by a test you saw fail and then pass.

  > Done when every AC about behaviour is covered by a test you saw fail and then pass,
  The done rule lives in the role and in both `implement` steps, and the copies already
  differ ("every AC" against "every AC about behaviour"): a wording AC may get a contrived
  test or none. Fix: keep the done rule in the `do` only. Passes: 2/3

### 7. When to call the human

- **F7.1** [medium] `agents/developer.md:88`
  > BLOCKED do not finish a step: send them to the supervisor with `send_message` and leave
  > the run where it is. The body is the full report:
  The supervisor role has no rule for such a message inside a run (answer it, ask the
  human, or cancel), and `implement` has only the outcome `done`, so a blocked run may sit
  with no next action. Fix: a supervisor working rule: answer with `send_message` when the
  decision is yours, otherwise ask the human; cancel the run only on the human's word.
  Passes: 3/3

### 8. Loops on a later visit

- **F8.1** [low] `flows/feature.yaml:68` and `flows/fix.yaml:12` (state `implement`)
  > step's note says what to fix: review findings, a conflict with main (merge main into

  > later visit the note says what to fix: review findings, a conflict with main (merge
  `implement` is also entered from `merge_ok: rejected`, where the note is the human's
  reason; the list leaves that case out. Fix: add "or the human's reason for rejecting the
  merge". Passes: 3/3

### 9. Concision and why

No repeated finding: each pass named a different sentence. The rules carry their reasons,
for example `skills/lado-checks/SKILL.md:51`
> - Never pipe a check whose result gates something (`make check | tail` hides a red exit

### 10. Skill descriptions

- **F10.1** [medium] `agents/supervisor.md:9`
  > - finishing-a-development-branch
  Nothing in the role or its steps calls for this skill, and its own options (push, PR,
  discard, worktree cleanup) compete with the `merge` step and with LADO removing the
  run's worktree. Fix: remove it from `skills:`. Passes: 3/3
- **F10.2** [medium] `agents/reviewer.md:6`
  > - requesting-code-review
  The skill is for the author asking for a review; the reviewer role never calls for it.
  Fix: remove it from `skills:`. Passes: 3/3

### 11. Provider neutrality

No repeated finding. No CLI tool names, slash commands or model names; `PROVIDER=claude` is
a target of LADO's own Makefile. One pass questioned `agents/developer.md:25`
> 2. Change files with your editing tools (edit, write), one readable change at a time. Do

### 12. Safety and scope

- **F12.1** [medium] `agents/supervisor.md:68`
  > `.lado/mockups/<run>/`, not committed. If your environment can publish a page for the human
  > to open, publish it and give the link. The design names where the approved mockups are,
  Publishing a page takes unreleased design work off the machine without the human's yes.
  Fix: "offer to publish it; publish only on the human's yes". Passes: 3/3
- **F12.2** [medium] `skills/lado-checks/SKILL.md:20`
  > | A real agent CLI still works | `make test-live PROVIDER=claude` or `PROVIDER=kilo` | After changing a provider, and on main before a release. Ask the supervisor first for Claude: it uses a paid model. |
  The supervisor's rule to ask the human before a paid run covers only releases
  (`agents/supervisor.md:103`: "main (`lado-checks`; ask the human first for Claude, it
  uses a paid model) and green CI on"), so during a run it may allow a paid run alone.
  Fix: a supervisor working rule that a worker's request for a paid `make test-live` goes
  to the human. Passes: 2/3

## Found on the way

- `[lado]` A work step after a gate gets the human's answer together with "Note before the
  gate" (`runs._answer_note`), but neither the README's Kits section nor the docstring of
  `lado/flows.py` says so; it says only that a step gets the previous step's note. All
  three rubric passes read that as "the note is lost at a gate". kit-builder's
  `lado-kit-format` now states it.
