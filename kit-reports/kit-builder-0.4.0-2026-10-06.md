# Kit report: kit-builder 0.4.0

- Date: 2026-10-06
- Kit: the repository root of kit-builder (path given), branch `lado/kit-builder/critic`,
  with `lado/kit-builder/author` merged in. `kit.yaml` still says `version: 0.3.0`; the
  report is named for the planned 0.4.0 (the version is set at release).
- Commit: f43ad57 (the author's round-2 fixes; merged into the critic's branch)
- Evaluated by: kit-builder critic (layers a and b), run on kit-builder itself following
  `agents/critic.md` and `kit-rubric` as in the `evaluate` step of `improve`, outside a run
- Mode: re-evaluation, round 2, against this file's previous version (commit fb5db46):
  `git diff fb5db46..HEAD -- kit.yaml README.md BLUEPRINT.md agents flows skills`. That
  diff touches 8 files, with 80 lines added and 49 removed. Earlier versions of this file
  are in git: the full evaluation at 0456710 and round 1 at fb5db46.
- Passes: five independent sub-agents, each with `kit-rubric`, the kit folder, the
  dependency skills, the diff and the previous report:
  - pass 1 started from kit.yaml and the roles;
  - pass 2 started from the flows, state by state;
  - pass 3 started from the skills;
  - a fourth did the cut-rule check over the word diff;
  - a fifth did the full pass over the whole of the 8 touched files.

  Findings were merged by place and reason. Where passes gave different impacts, the
  higher was kept, and the finding says so. 0 one-pass findings dropped, 4 kept as
  confirmed (the full pass's included).
  The human's answers to round 1's three questions were all "as recommended".

Findings are candidates for the human to weigh, not a pass/fail grade.

**Verdict: `approved`.** `lado kits check` has no error, no measure is over green,
`--compare` prints no difference, and no high finding is open: all previous findings are
RESOLVED except F2.2, still open as a medium. The full pass found no high.
**Stop rule: not met.** The changed text holds 4 medium findings. This is advice for the
release gate, not a block.

## Card

| Layer | Result |
|---|---|
| a. `lado kits check` | OK; 0 warnings |
| a. Budget | green; no measure over green, no similar paragraphs |
| a. Flows | 3 drawn; same as the blueprint's skeletons (0 differences) |
| b. Rubric | 9 findings in the changed text (0 high, 4 medium, 5 low), F2.2 still open among them; 6 of 12 criteria without findings; 1 more under "Missed earlier" (low) |
| Covers | re-evaluation of the changed text (8 files), with a full pass over those 8 files |
| Stop rule | not met: 0 high, 4 medium — advice for the release gate, not a block |

The count covers only what the row "Covers" names: a count of a re-evaluation and one of a
full evaluation are not comparable.

### `lado kits check .`

```
kit-builder: OK (2 agents, 7 skills, 1 packs and 3 flows)
```

### Budget script (exit status 0)

```
# Complexity budget: kit-builder 0.3.0

| Measure | Where | Value | Green / yellow up to | Zone |
|---|---|---|---|---|
| Worker roles (not supervisor) | kit | 2 | 3 / 5 | green |
| Work steps in a flow | flows/create.yaml | 4 | 5 / 8 | green |
| Work steps in a flow | flows/evaluate.yaml | 1 | 5 / 8 | green |
| Work steps in a flow | flows/improve.yaml | 5 | 5 / 8 | green |
| Gates in a flow | flows/create.yaml | 2 | 2 / 3 | green |
| Gates in a flow | flows/evaluate.yaml | 0 | 2 / 3 | green |
| Gates in a flow | flows/improve.yaml | 2 | 2 / 3 | green |
| Words in a role prompt | agents/author.md | 788 | 800 / 1500 | green |
| Words in a role prompt | agents/critic.md | 674 | 800 / 1500 | green |
| Words in the lead's prompt | agents/supervisor.md | 768 | 1000 / 1500 | green |
| Own skills | kit | 5 | 5 / 10 | green |
| MCP servers | kit | 0 | 2 / 4 | green |

## Similar paragraphs (one rule, one place; 55% similar or more)

none

Overall: green
```

The author's prompt is at 788 of 800 words. The next rule added to it should push another
one into a skill.

### Flows

`uv run --script skills/kit-budget/scripts/flow_diagram.py . --out kit-reports/kit-builder-0.4.0-2026-10-06`
(exit status 0). No flow's shape changed, so the SVGs are byte-identical to the previous
ones.

![create](kit-builder-0.4.0-2026-10-06/create.svg)

![improve](kit-builder-0.4.0-2026-10-06/improve.svg)

![evaluate](kit-builder-0.4.0-2026-10-06/evaluate.svg)

`uv run --script skills/kit-budget/scripts/flow_diagram.py . --compare BLUEPRINT.md`:

```
same as the plan in BLUEPRINT.md (exit status 0)
```

## Fix first

Nothing blocks. The mediums, most harmful first:

1. A worker's environment failure has no bound and no exit once the supervisor "leaves it
   to them". The supervisor bullet also reads as if the supervisor reruns the worker's
   command in its own checkout (F7.3).
2. Put back "a wrong version from step 1 is yours". A `--tag` check that fails because
   `kit.yaml` disagrees now goes to the author, who edits a version the human settled
   (F3.11, a lost rule).
3. A push that fails after the tag is made matches both "stays in `release`" and "report
   `released`". Stay only while steps 2–3 are left (F3.13).
4. "Once the author has built a plan" is unclear after `blocked` on the first `build`. Say
   "worked from a plan (built it, or reported `blocked` on it)" (F2.2, still open).

## Findings

Findings in text the diff touches. Ids continue the previous reports' numbering.

### 1. Role boundaries

No finding. "Releasing" stays scoped to "The supervisor's step `release`"
(`skills/lado-kit-format/SKILL.md:93`). The author changes none of the merged text
(`agents/author.md:59`). The critic stays read-only (`agents/critic.md:10-11`).

### 2. Handoffs between steps

- **F2.2** STILL OPEN [medium] `flows/improve.yaml:38-39` (state `triage` on a later visit,
  then `build` after `blocked`)
  > the author has built a plan, each new plan starts with "Changed since the plan the

  `blocked` usually comes on the author's first `build` visit, when the plan "cannot be
  built as written" (`agents/author.md:14`). Has the author then "built a plan"? One
  triage leaves the list out, and another writes it against plan 1. `build` changes only
  "what its "Changed since the plan the author last built" lists" (`flows/improve.yaml:64-65`).
  Without a list, it rebuilds the whole plan over the partly built plan 1, or guesses.
  Pass 2 and pass 3 rated this low, the full pass medium; medium is kept, since runs
  differ.
  Fix: "Once the author has worked from a plan (built it, or reported `blocked` on it), …".
  Or give `improve.build` `needs: [triage, build]`, so it sees its own last note.
  Passes: 2/3 and the full pass

- **F2.3** [low] `flows/improve.yaml:40` (state `triage` after `plan_ok` → `rejected`)
  > author last built: …"; after a rejected plan, keep its list and add to it, since the

  The human's reason for rejecting a plan may be one of the items on its list. "Keep its
  list and add to it" then keeps an item that no longer differs from the built plan, so
  the list contradicts the plan body. The human sees the list at `plan_ok`, so the harm is
  small. If the item gets through, `build` changes what the list says.
  Fix: "after a rejected plan, write the list again against the plan the author last
  built".
  Passes: 1/3, confirmed. Evidence: the quoted line and `flows/improve.yaml:64-65`.

- **F2.4** [low] lost rule, `flows/improve.yaml:39` at fb5db46
  > new plan starts with "Changed since the previous plan: …", so the human and the

  Before the change, every revised plan carried a list, "so the human and the author see
  what differs". Now only plans after a build do. A plan the human rejects before any
  build gets no list, so at the next `plan_ok` the human cannot see what differs from the
  plan they rejected.
  Fix: covered by the fix of F2.2. Also start the plan after a rejection with "Changed
  since the rejected plan" when the author has built none.
  Passes: cut-rule check

### 3. Done and outcomes

- **F3.11** [medium] lost rule, `skills/lado-kit-format/SKILL.md:105-106` at fb5db46
  (state `release`)
  > never change the kit to get past such a failure. A wrong version from step 1 is yours:
  > correct it.

  Only the existing-tag case survives: "branch. A tag that already exists for it later
  means the version is wrong: settle it" (`skills/lado-kit-format/SKILL.md:98`). A `--tag`
  check that fails because `kit.yaml` does not say that version is the supervisor's slip
  in step 1. Now it reads as "an error the kit's files cause" (lines 77-78), so it goes to
  the author with `failed`. The author edits a version the human settled, and the run
  spends a `build`, an `evaluate` visit and `release_ok`.
  The cut-rule check and pass 2 rated this medium; pass 3 rated it low. Medium is kept.
  Fix: in step 1, "A tag that already exists, or a `--tag` check saying `kit.yaml` does
  not match, means the version from this step is wrong: settle and set it again here;
  never `failed`."
  Passes: cut-rule check; also passes 1, 2 and 3

- **F3.12** [low] `skills/lado-kit-format/SKILL.md:123` (state `release`)
  > and run `lado flow-set <session> <run> done`, or they cancel the run.

  `lado flow-set --help` prints "usage: lado flow-set [-h] --reason REASON session run
  state", so the command as written fails with a usage error. The supervisor's own copy is
  right: `release_ok --reason "<why>"` (`agents/supervisor.md:78-79`).
  Fix: `lado flow-set <session> <run> done --reason "<what was finished by hand>"`.
  Passes: 3/3 and the full pass

- **F3.13** [medium] `skills/lado-kit-format/SKILL.md:121` and `:125` (state `release`,
  step 4)
  > its bound, the run stays in `release`, never `failed`: tell the human which of steps 2–4
  > Report `released` once the tag is on the start branch: note_summary is the tag; note_body

  A push in step 4 that fails on the network, after the tag is made, matches both rules.
  Line 121 counts step 4 among the steps "left" and keeps the run in `release`; line 125,
  and "Without a yes, the release ends at the local tag" (lines 114-115), say to report
  `released`. One supervisor parks an already-tagged run, which the human must close with
  `flow-set`. A retry can then hit the existing tag, which step 1 now reads as "the
  version is wrong".
  Pass 1 rated this medium, pass 2 low; medium is kept.
  Fix: "…stays in `release` while steps 2–3 are left; once the tag is made, report
  `released` and say what is left of step 4."
  Passes: 2/3

### 4. Independent verification

No finding. Merged kit text goes back through the critic
(`skills/lado-kit-format/SKILL.md:100-106`), and the author changes none of it.

### 5. Contradictions

- **F5.4** [low] `skills/lado-kit-format/SKILL.md:117`
  > Report `failed` only for a fault in the kit's files, with the command and its whole

  Step 2 reports `failed` for two other cases: a merge conflict and merged kit text
  nobody has reviewed (lines 100-106). Neither is "a fault in the kit's files", and "the
  author fixes it … and runs the command again" does not fit merged text the author must
  leave alone. The specific step most likely wins, so the harm is small.
  Fix: "Report `failed` for the cases of step 2 and for a fault in the kit's files…".
  Passes: full pass, confirmed.

- **F5.5** [low] `agents/author.md:57` and `:59` (state `build` after `release` →
  `failed` on a conflict)
  > the run's branch, resolve the conflicts and commit; a conflict between two decisions on
  > When the merge brought in changed kit text, change none of it: when it contradicts the

  Resolving a conflict means editing text the merge brought in, and two lines later the
  author is told to "change none of it". One author resolves mechanical conflicts; another
  reports `blocked` on every conflict, at the cost of a trip through `design` or `triage`
  and a gate.
  Fix: "change none of it beyond resolving conflicts".
  Passes: full pass, confirmed.

### 6. Duplication

No finding. F6.2 is resolved: the environment rule lives once, at
`skills/lado-kit-format/SKILL.md:74-89` ("This is the one rule for every role."), and the
author, the critic, kit-rubric and the release only point to it.

### 7. When to call the human

- **F7.3** [medium] `skills/lado-kit-format/SKILL.md:82-86` (any worker step: `build`,
  `evaluate`, `assess`, `evaluate.evaluate`)
  > - a worker sends the supervisor the command and its whole output with `send_message`,
  >   waits, and runs it again once the supervisor answers;
  > - the supervisor shows the human the command and its output and waits; it runs it again
  >   once they say it is settled, and after a second failure from the same cause leaves it to

  The bound and the ways on exist only for `release` (lines 120-123).
  - The worker reruns on any answer, with no bound. Once the supervisor "leaves it to
    them", the worker has no outcome that fits: the failure is "not a finding, not a
    verdict either way and not `blocked`" (line 81), and the critic's steps have only
    `approved`/`changes` or `done`. So the run sits in a worker step, and nobody tells the
    human how it ends.
  - The supervisor's role handles only "When a worker writes that it is blocked"
    (`agents/supervisor.md:80`).
  - "It runs it again" reads as the supervisor rerunning the worker's `lado kits check` in
    its own checkout, not in the run's worktree (known hole 3).

  Fix: scope the supervisor bullet to its own commands, and add: "For a worker's failure,
  settle it with the human, then tell the worker to retry. When it is left to the human,
  tell them which run and step wait, and how it goes on: you tell the worker to retry, or
  they cancel the run."
  Passes: 2/3 and the full pass

### 8. Loops on a later visit

No finding beyond F2.2 and F7.3. The release's step 3 loop is bounded ("at most twice").

### 9. Concision and why

No finding. The new rules carry their reasons, for example "since which one changes is
the human's decision" (`agents/author.md:61`) and "so nothing else they staged goes in"
(`skills/lado-kit-format/SKILL.md:136`). One cosmetic point: line 119 of `lado-kit-format`
is not wrapped (108 characters).

### 10. Skill descriptions

No finding. `lado-kit-format`'s description adds "what to do when a check fails", and every
role that points to that section lists the skill.

### 11. Provider neutrality

No finding. "Look facts up yourself, never through a sub-agent or worker: that is work
outside a run." (`agents/supervisor.md:51-52`) overrides grilling's sub-agent dispatch.
The new text names only `git`, `lado`, `uv` and `send_message`.

### 12. Safety and scope

No finding. The report-only path checks out and commits only "the run's own report files"
and asks the human first when one of them has local changes
(`skills/lado-kit-format/SKILL.md:132-136`). Pass 3 reproduced it in a scratch repository:
a staged `other.txt` stayed out of the commit.

## Known holes

| Known hole | Finding, or how the kit handles it |
|---|---|
| 1. Red check sent back with no environment cause considered | Handled in one place: "This is the one rule for every role. Find the cause before you act on a failure of" (`skills/lado-kit-format/SKILL.md:76`), with pointers from the author (`agents/author.md:80-81`), the critic (`agents/critic.md:38-40`), the verdict and the release. Open: F7.3 (a worker's failure has no bound or exit), F3.11 (a version slip goes to the author). |
| 2. Work outside a flow, merge without a gate | "Look facts up yourself, never through a sub-agent or worker" (`agents/supervisor.md:51-52`). A report-only merge goes without a yes only when the run touches nothing outside `kit-reports/` (`skills/lado-kit-format/SKILL.md:129-131`); otherwise the human's yes, or only the run's own report paths. |
| 3. Path outside the run's worktree | The human's checkout is used deliberately, with path-limited commits (`skills/lado-kit-format/SKILL.md:135-136`) and "never stash, reset or clean the human's checkout" (lines 88-89). Open: F7.3 (the supervisor rerunning a worker's check in its own checkout). |
| 4. Verdict without a severity threshold | Handled: "prints no difference and no high finding is open; otherwise `changes`" (`skills/kit-rubric/SKILL.md:234`); an environment failure "gives no verdict either way" (line 238). |
| 5. Dependency skill that writes or asks where its role must not | Handled: grilling is on the lead only, its round format and scope yield to `kit-interview`, and its sub-agent dispatch is overridden (`agents/supervisor.md:50-52`). |

## Not traced

- Elements and measures: none untraced and none over green. `--compare` reports no
  difference. The R8 trace is fixed: `author` and `evaluate.evaluate` now cover R8
  (`BLUEPRINT.md:195`, `:213`).
- Blueprint lags the kit (low, full pass): R8 still lists "an existing tag" among
  environment failures (`BLUEPRINT.md:55` "tool, an existing tag, a dirty checkout,
  another branch checked out) goes to the human,"). The kit now treats an existing tag as
  a wrong version, settled again in step 1 (`skills/lado-kit-format/SKILL.md:98`). Drop it
  from R8's list.

## Previous findings

| Finding | Status | Evidence |
|---|---|---|
| F2.2 build after `blocked` (round 1, still open) | STILL OPEN | Now measured against "the plan the author last built" (`flows/improve.yaml:39`), but "built" is unclear after `blocked`; see F2.2 above |
| F3.5 release with no outcome after the bound | RESOLVED | "the run stays in `release`, never `failed`" (`skills/lado-kit-format/SKILL.md:121`); the command it gives is F3.12, and its overlap with `released` is F3.13 |
| F3.6 `docs/` and `tests/` counted as kit text | RESOLVED | "lists a file of the kit's text, `kit-rubric` "Re-evaluation" 1, or of `blueprint-flows/`" (`skills/lado-kit-format/SKILL.md:103-104`) |
| F3.7 existing tag in two rules | RESOLVED | Dropped from the outside causes (lines 79-80); "A tag that already exists for it later means the version is wrong" (line 98). Side effect: F3.11 |
| F3.8 failed report-only merge | RESOLVED | "On a merge conflict, `git merge --abort` and show the human the files; … The run has ended, so there is no outcome to report." (lines 136-138) |
| F5.3 grilling's sub-agent | RESOLVED | `agents/supervisor.md:51-52` |
| F6.2 two copies of the environment rule | RESOLVED | One section, `skills/lado-kit-format/SKILL.md:74-89`; kit-rubric keeps a pointer (line 238-239) |
| F7.2 author "as your own" | RESOLVED | "change none of it: … report `blocked` with the list" (`agents/author.md:59-61`); its clash with resolving conflicts is F5.5 |
| F12.2 `checkout -- kit-reports/` | RESOLVED | Only the run's own report paths, "`git commit -m "<report>" -- <those paths>`" (`skills/lado-kit-format/SKILL.md:135`); reproduced by pass 3 |
| F3.9 author's own checks (missed earlier) | RESOLVED | "A check failing for a cause outside the kit's files is not `blocked`" (`agents/author.md:80-81`) |
| F3.10 critic's `assess` (missed earlier) | RESOLVED | `agents/critic.md:38-40`, in layer a, so it covers every critic step |
| F12.3 README merge (missed earlier) | RESOLVED | "merges the run's branch when it adds only the report; anything more needs your yes" (`README.md:106-107`) |
| R8 trace mismatch (Not traced) | RESOLVED | `BLUEPRINT.md:195`, `:213`, `:234` |

## Cut rules

| Removed rule (file:line at fb5db46) | Where it is now |
|---|---|
| `skills/kit-rubric/SKILL.md:239-242` the environment paragraph of "Verdict" (says nothing about the kit; no verdict either way; send the supervisor the command, run again once it answers; a kit error counts) | `skills/lado-kit-format/SKILL.md:76-86`; the pointer at `skills/kit-rubric/SKILL.md:238-239` |
| `skills/lado-kit-format/SKILL.md:98-104` the failure paragraph (find the cause; `failed` only for a kit fault; outside causes to the human; second failure leaves it to them) | Lines 76-86 and 117-118 |
| `skills/lado-kit-format/SKILL.md:104-105` never stash, reset or clean; never change the kit to get past it | Lines 88-89 |
| `skills/lado-kit-format/SKILL.md:105-106` "A wrong version from step 1 is yours: correct it." | **lost** in its general form; only the existing-tag case is at line 98. See F3.11 |
| `skills/lado-kit-format/SKILL.md:101` "a tag that already exists" as an outside cause | Changed on purpose to a wrong version (line 98), as the human answered round 1's F3.7 |
| `agents/author.md:58-59` "run it again as the note gives it (`--tag` included)" | `skills/lado-kit-format/SKILL.md:118-119`, with a pointer at `agents/author.md:58` |
| `agents/author.md:59-60` check merged text "as your own" | Replaced by "change none of it … report `blocked`" (`agents/author.md:59-61`), as the human answered |
| `skills/lado-kit-format/SKILL.md:115-117` take only the report with `git checkout … -- kit-reports/` | Lines 132-136, narrowed to the run's own paths |
| `skills/lado-kit-format/SKILL.md:117` "A failed merge is read as above." | Lines 136-138 |
| `flows/improve.yaml:38-40` every revised plan starts with "Changed since the previous plan" | Lines 38-41, only once the author has built a plan; **lost** for a plan rejected before any build. See F2.4 |
| `README.md:106` the supervisor merges the run's branch | `README.md:106-107`, made conditional |

## Missed earlier

Findings in text the diff does not touch. They do not block and do not count for the stop
rule.

- **F3.14** [low] `README.md:75`
  > `changes`, at most three times; `changes` while a high finding is open (medium ones are

  The verdict is also `changes` on a `lado kits check` error, a red measure, an
  unjustified yellow one or a `--compare` difference (`skills/kit-rubric/SKILL.md:232-234`).
  A reader expects `approved` whenever no high finding is open.
  Fix: "`changes` while a high finding, a check error, a red measure or a flow differing
  from its skeleton is open".
  Passes: full pass, confirmed.

## Questions for the human

1. When a worker's check fails for an environment cause and you leave it unsettled, how
   should the run go on (F7.3)? Recommended: the run waits in its step; the supervisor tells
   you which run and step wait. You tell it to retry once it is settled, or you cancel the
   run.
2. A push that fails after the tag exists: report `released` with what is left, or keep the
   run open (F3.13)? Recommended: report `released` and say what is left of step 4.
