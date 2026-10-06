# Kit report: kit-builder 0.4.0

- Date: 2026-10-06
- Kit: the repository root of kit-builder (path given), branch `lado/kit-builder/critic`,
  with `lado/kit-builder/author` merged in. `kit.yaml` still says `version: 0.3.0`; the
  report is named for the planned 0.4.0 (the version is set at release).
- Commit: 2bc37d1 (the author's fixes; merged into the critic's branch)
- Evaluated by: kit-builder critic (layers a and b), run on kit-builder itself following
  `agents/critic.md` and `kit-rubric` as in the `evaluate` step of `improve`, outside a run
- Mode: re-evaluation against this file's previous version (commit 0456710, the full
  evaluation of d4868fe): `git diff 0456710..HEAD -- kit.yaml README.md BLUEPRINT.md agents
  flows skills`. That diff touches 10 files, with 137 lines added and 88 removed. The base
  is the commit of the previous report, because the kit's text at 0456710 is the text that
  report evaluated (d4868fe).
  This file replaces the previous version, since its name is unchanged; git keeps the
  earlier version.
- Passes: five independent sub-agents, each with `kit-rubric`, the kit folder, the two
  dependency skills' folders, the diff and the previous report:
  - pass 1 started from kit.yaml and the roles;
  - pass 2 started from the flows, state by state;
  - pass 3 started from the skills, then went back to the roles;
  - a fourth did the cut-rule check over `git diff --word-diff`;
  - a fifth did the full pass over the whole of the 10 files the diff touches.

  Findings were merged by place and reason. Where passes gave different impacts or
  criteria, the finding says which was kept. 0 one-pass findings dropped, 6 kept as
  confirmed (the full pass's findings included).
  The human's answers to the previous report's five questions were all "as recommended"
  (the supervisor's message).

Findings are candidates for the human to weigh, not a pass/fail grade.

**Verdict: `approved`.** `lado kits check` has no error, no budget measure is over green,
`--compare` prints no difference, and no high finding is open: all 15 previous findings
are RESOLVED, except F2.2, which is STILL OPEN as a medium. The full pass found no high.
**Stop rule: not met.** The changed text holds 7 medium findings. This is advice for the
release gate, not a block.

## Card

| Layer | Result |
|---|---|
| a. `lado kits check` | OK; 0 warnings |
| a. Budget | green; no measure over green, no similar paragraphs |
| a. Flows | 3 drawn; same as the blueprint's skeletons (0 differences) |
| b. Rubric | 9 findings in the changed text (0 high, 7 medium, 2 low), one of them F2.2 still open; 8 of 12 criteria without findings; 3 more under "Missed earlier" (1 medium, 2 low) |
| Covers | re-evaluation of the changed text (10 files), with a full pass over those 10 files |
| Stop rule | not met: 0 high, 7 medium — advice for the release gate, not a block |

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
| Words in a role prompt | agents/author.md | 769 | 800 / 1500 | green |
| Words in a role prompt | agents/critic.md | 651 | 800 / 1500 | green |
| Words in the lead's prompt | agents/supervisor.md | 752 | 1000 / 1500 | green |
| Own skills | kit | 5 | 5 / 10 | green |
| MCP servers | kit | 0 | 2 / 4 | green |

## Similar paragraphs (one rule, one place; 55% similar or more)

none

Overall: green
```

### Flows

`uv run --script skills/kit-budget/scripts/flow_diagram.py . --out kit-reports/kit-builder-0.4.0-2026-10-06`
(exit status 0). The fixes changed no flow's shape, so the SVGs are byte-identical to the
previous report's.

![create](kit-builder-0.4.0-2026-10-06/create.svg)

![improve](kit-builder-0.4.0-2026-10-06/improve.svg)

![evaluate](kit-builder-0.4.0-2026-10-06/evaluate.svg)

`uv run --script skills/kit-budget/scripts/flow_diagram.py . --compare BLUEPRINT.md`:

```
same as the plan in BLUEPRINT.md (exit status 0)
```

## Fix first

Nothing blocks. These are the mediums most worth fixing before the tag, since each one is
in the text the fixes just wrote:

1. Say how `release` ends when an environment failure is left to the human. It has only
   `released` and `failed`, and `failed` is now reserved for kit faults (F3.5).
2. Taking "only the report" with `git checkout <run> -- kit-reports/` overwrites the
   human's uncommitted reports and commits whatever they had staged. Take the run's own
   paths and commit only those (F12.2).
3. Release step 2 counts `docs/` and `tests/` as kit text, so a test-only commit on main
   sends the release back through build, evaluate and the gate. Use kit-rubric's list
   (F3.6).
4. "Changed since the previous plan" must be measured against the plan the author last
   built, not the last rejected one (F2.2, still open).
5. Merged kit text that contradicts the blueprint goes to the human (`blocked`). The
   author does not "check it as your own" and revert it (F7.2).

## Findings

Findings in text the diff touches. Ids continue the previous report's numbering.

### 1. Role boundaries

No finding. "Releasing" lives in `lado-kit-format`, which the author and the critic also
load, but it is scoped by its first line: "The supervisor's step `release` of `create` and
`improve`, in this order. "The start" (`skills/lado-kit-format/SKILL.md:76`). The critic's
rights stay in its opening (`agents/critic.md:10`).

### 2. Handoffs between steps

- **F2.2** STILL OPEN [medium] `flows/improve.yaml:38` (state `triage` on a later visit,
  then `build` after `blocked`)
  > human, starting from your own previous plan and the committed `BLUEPRINT.md`; the

  The fix makes the new plan start with "Changed since the previous plan: …"
  (`flows/improve.yaml:39`), and `build` changes only what that lists
  (`flows/improve.yaml:63-64`). Take this path:
  1. `build` reports `blocked`, and triage writes plan 2;
  2. the human rejects plan 2 at `plan_ok` (`rejected: triage`, `flows/improve.yaml:55`),
     and triage writes plan 3;
  3. the human approves plan 3, and the author builds it.

  Plan 3's list is measured against plan 2, which was never built. So the author skips
  what changed between plan 1 and plan 2, and the critic then sends it back, spending one
  of `evaluate`'s three visits.
  Fix: "Changed since the plan the author last built: …". Or give `improve.build`
  `needs: [triage, build]`.
  Passes: 3/3

### 3. Done and outcomes

- **F3.5** [medium] `skills/lado-kit-format/SKILL.md:103-104` (state `release` of `create`
  and `improve`)
  > wait for them; run it again once they say it is settled, and after a second failure from
  > the same cause leave it to them. Never stash, reset or clean the human's checkout, and

  The same gap is at line 91 ("go back to step 2, at most twice; then ask the"). `release`
  has only "outcomes: {released: done, failed: build}" (`flows/create.yaml:68`,
  `flows/improve.yaml:86`), and `failed` is now "only for a fault in the kit's files"
  (line 98-99). When the bound is reached, no outcome fits. One supervisor reports `failed`
  anyway, which sends an environment fault to the author, the harm F3.1 was about.
  Another leaves the run parked with the start branch perhaps fast-forwarded but untagged,
  and says nothing about what is left.
  Fix: "leave the run in `release`; tell the human which of steps 2–4 are left and how to
  go on: ask you to retry once it is settled, finish by hand and run `lado flow-set …
  done`, or cancel. Never report `failed` for it."
  Passes: 3/3 and the full pass

- **F3.6** [medium] `skills/lado-kit-format/SKILL.md:85-86` (state `release`, step 2)
  > (`git diff --name-only <the noted commit> HEAD` lists any file outside `kit-reports/`
  > and `BACKLOG.md`), report `failed` with that list: neither the critic nor the human has

  This test counts everything except `kit-reports/` and `BACKLOG.md` as "the kit's text".
  kit-rubric defines the kit's text as "`kit.yaml`, `README.md`, `BLUEPRINT.md`,
  `agents/`, `flows/` and" `skills/`, which leaves out `docs/` and `tests/`
  (`skills/kit-rubric/SKILL.md:189-191`). kit-builder's own repository tracks `docs/` and
  `tests/`. A start-branch commit that touches only those fails the release, then goes
  through `build` (nothing to fix), an `evaluate` visit (of 3) and `release_ok` again.
  Fix: "lists a file of the kit's text (`kit-rubric`, "Re-evaluation" 1, plus
  `blueprint-flows/`)".
  Passes: 3/3 and the full pass

- **F3.7** [low] `skills/lado-kit-format/SKILL.md:101`
  > `uv` or `lado`, a tag that already exists, uncommitted changes in the way, another branch

  An existing tag is listed as a cause outside the kit, for the human. But it usually
  means the version from step 1 is wrong, and line 105 says "A wrong version from step 1
  is yours:" / "correct it.". The two rules overlap, so supervisors will handle the same
  failure differently. Both paths reach the human, so the harm is small.
  Fix: "an existing tag: settle the version again with the human (step 1)", and drop it
  from the outside causes.
  Passes: 2/3

- **F3.8** [medium] `skills/lado-kit-format/SKILL.md:117` ("A report-only run": after
  `evaluate`, and after `improve.triage` → `nothing`)
  > branch and commit it. A failed merge is read as above.

  This merge runs in the human's checkout after the run has ended. "Above" says to `git
  merge --abort` and report `failed` for a kit fault, but there is no step left to report
  to. A conflict is likely here, because a re-evaluation rewrites a report file of the
  same name. The supervisor then has no rule: it leaves the checkout half-merged, or
  cleans it against "Never stash, reset or clean".
  Fix: "On a conflict, `git merge --abort` and show the human the files; any other failure
  goes to the human as a cause outside the kit (above)."
  Passes: 1/3, confirmed. Evidence: `flows/evaluate.yaml:15` "outcomes: {done: done}", and
  line 112 "When it ends, merge its branch".

### 4. Independent verification

No finding. F4.1 is resolved: kit text that the release merge brings in goes back through
the critic (`skills/lado-kit-format/SKILL.md:84-88`; the width of that test is F3.6). A
`--compare` difference now blocks `approved` (`skills/kit-rubric/SKILL.md:233-234`).
`plan_ok` shows a restored blueprint whole (`flows/improve.yaml:44-46`).

### 5. Contradictions

- **F5.3** [medium] `agents/supervisor.md:50-51` (states `design`, `triage`)
  > Use `grilling` to find what is still the human's to decide; where it differs from
  > `kit-interview` (the round's format, how far to ask), `kit-interview` wins. Never decide for

  The fix settles the round format and the scope, as the human answered. It leaves
  grilling's "When a frontier question needs a fact from the environment (filesystem,
  tools, etc.), dispatch a sub-agent to find it" (grilling `SKILL.md:20`), which the
  previous F5.1 named. That instruction is neither format nor scope, so `kit-interview`
  does not win on it. Two harms follow:
  - in LADO the lead may start an exploring worker with no run around it, against "never a
    worker or a" (`agents/supervisor.md:16`, known hole 2);
  - a CLI without sub-agents cannot follow it (criterion 11).

  Pass 2 and pass 3 read F5.1 as fully resolved. Pass 1 and the full pass found this part
  open; it is kept as confirmed.
  Fix: add "facts you look up yourself, never through a sub-agent or worker" to the
  parenthesis.
  Passes: 1/3 and the full pass, confirmed. Evidence: the grilling line quoted above.

### 6. Duplication

- **F6.2** [low] `skills/kit-rubric/SKILL.md:239-242` and
  `skills/lado-kit-format/SKILL.md:100-104`
  > A check that fails for a cause outside the kit's files (no network to fetch a skill pack,

  One rule, telling an environment failure from a kit fault, now has two copies, and they
  already differ. The release gives up after a second failure, while the critic is told
  to "the check again once it answers" with no bound (`skills/kit-rubric/SKILL.md:242`).
  Fix: keep the rule and its list of causes in `lado-kit-format`. kit-rubric points to it
  and keeps only "no verdict either way".
  Passes: 1/3, confirmed. Evidence: the two lines quoted.

### 7. When to call the human

- **F7.2** [medium] `agents/author.md:59-60` (state `build` after `release` → `failed` on
  merged kit text)
  > gives it (`--tag` included). When the merge brought in changed kit text, check that text
  > against the blueprint as your own, so the critic sees it next.

  The merged text is a commit by the human or by another run, and the blueprint does not
  name it. "As your own" invites the author to bring it in line with the blueprint, which
  reverts the human's change without asking. Meanwhile line 13 forbids keeping or
  dropping an element the blueprint does not name. Some runs will revert the change and
  others will report `blocked`, and no path to the human is named for the decision that
  is theirs: does the blueprint change, or the merged text?
  Fix: "Change none of the merged text; when it contradicts the blueprint or adds an
  element it does not name, report `blocked` with the list."
  Passes: 1/3 and the full pass, confirmed. Evidence: `agents/author.md:13` "so you do not
  add, drop or rename a role, step, gate, skill or MCP server they do not name."

### 8. Loops on a later visit

No finding beyond F2.2. The release's step 3 loop is bounded: "go back to step 2, at most
twice; then ask the" (`skills/lado-kit-format/SKILL.md:91`).

### 9. Concision and why

No finding. The history line is gone, and the calibration paragraph is down to two lines
(`skills/kit-budget/SKILL.md:79-80`). The new rules carry their reasons, for example
"neither the critic nor the human has seen the merged kit, and a clean merge can still
join two texts that contradict each other" (`skills/lado-kit-format/SKILL.md:86-88`).

### 10. Skill descriptions

No finding. `lado-kit-format`'s description adds "and how a kit is released and published
… or releasing it", and the skill is on the supervisor, which releases.

### 11. Provider neutrality

No finding in the kit's own text. The new text names only `git`, `lado`, `uv` and LADO's
tools. grilling's sub-agent dispatch is F5.3.

### 12. Safety and scope

- **F12.2** [medium] `skills/lado-kit-format/SKILL.md:116` (after `evaluate`, or after
  `improve.triage` → `nothing`, in the human's checkout)
  > take only the report: `git checkout <the run's branch> -- kit-reports/` on the start

  This runs without a yes, and it has three side effects:
  1. It overwrites any uncommitted edit the human has under `kit-reports/`.
  2. It reverts any report the start branch holds in a newer version, back to the run's
     copy.
  3. A bare "commit it" also commits whatever the human had staged.

  Pass 3 reproduced this in a scratch repository: after `echo "human edit" >>
  kit-reports/r.md; git add other.txt; git checkout run -- kit-reports/; git commit`, the
  edit was lost and the commit included `other.txt`. "Never stash, reset or clean the
  human's checkout" (line 104) does not cover it.
  Passes 1 and 3 rated this medium, the full pass low; medium is kept.
  Fix: take only the paths the run added (`git diff --name-only --diff-filter=A
  <start>...<run> -- kit-reports/`), ask first when any of them has local changes, and
  commit with `git commit -- <those paths>`.
  Passes: 2/3 and the full pass

## Known holes

| Known hole | Finding, or how the kit handles it |
|---|---|
| 1. Red check sent back with no environment cause considered | Release: "When a command fails, find its cause before you report. Report `failed` only for a fault" (`skills/lado-kit-format/SKILL.md:98`). Verdict: "A check that fails for a cause outside the kit's files (no network to fetch a skill pack," (`skills/kit-rubric/SKILL.md:239`). Open: F3.5 (no outcome after the bound), F3.6 (non-kit files counted as kit text). Missed earlier: F3.9 (the author's own checks), F3.10 (the critic's `assess`). |
| 2. Work outside a flow, merge without a gate | A report-only run merges without a yes only when it touches "nothing outside" `kit-reports/`; anything more is shown to the human (`skills/lado-kit-format/SKILL.md:112-116`). Open: F12.2 (how "only the report" is taken), F3.8 (a failed merge after the run), F5.3 (grilling's sub-agent). |
| 3. Path outside the run's worktree | The work in the human's checkout is deliberate and named: "branch" is the branch the run started from, "checked out in the supervisor's repository" (`skills/lado-kit-format/SKILL.md:77`), under "Never stash, reset or clean the human's checkout". Its harm to that checkout: F12.2. |
| 4. Verdict without a severity threshold | Handled: "prints no difference and no high finding is open; otherwise `changes`." (`skills/kit-rubric/SKILL.md:234`); a similar pair is "a finding under criterion 6, and its impact decides" (line 237). |
| 5. Dependency skill that writes or asks where its role must not | Handled: kit-budget's red measure goes "the lead takes it to the" human (`skills/kit-budget/SKILL.md:93`); `grilling` is on the lead only, and `kit-interview` wins on format and scope. |

## Not traced

- Elements: none untraced, and no measure over green. `--compare` reports no difference.
- Trace mismatch (low; confirmed by the critic, pass 1):
  - The reverse check for R8 lists `evaluate.evaluate` (`BLUEPRINT.md:233`), but that
    element's row covers only "R6, R7" (`BLUEPRINT.md:211`).
  - The `lado-kit-format` row says "the author reruns the release's failing command"
    (R8), but the `author` row covers "R1, R11, R12" (`BLUEPRINT.md:193`), and the
    reverse check for R8 does not list the author.

  Add R8 to both rows, or drop the element from the reverse check.
- Section 4 matches the script's output. Its header still says `kit-builder 0.3.0`, as
  `kit.yaml` does.

## Previous findings

| Finding | Status | Evidence |
|---|---|---|
| F3.1 [high] release `--tag` failure → author | RESOLVED | "Report `failed` only for a fault in the kit's files, with the command and its whole output" (`skills/lado-kit-format/SKILL.md:98-99`); the verdict paragraph at `skills/kit-rubric/SKILL.md:239`; "run it again as the note" (`agents/author.md:58`). Its weak spot after the retry bound is F3.5. |
| F2.1 blueprint without skeletons | RESOLVED | "A blueprint without skeletons, restored or written" (`skills/kit-interview/SKILL.md:136`); "give it flow skeletons when it has none" (`flows/improve.yaml:31`) |
| F2.2 build after `blocked` | STILL OPEN (in part) | See F2.2 above: "Changed since the previous plan" is measured against the last plan, not the built one |
| F3.2 refused ff-merge | RESOLVED | "because the start branch gained commits, go back to step 2, at most twice; then ask the" (`skills/lado-kit-format/SKILL.md:91`); other causes at lines 98-104 |
| F3.3 flow drift outside the verdict | RESOLVED | "prints no difference and no high finding is open" (`skills/kit-rubric/SKILL.md:234`) |
| F3.4 similar pair in the verdict | RESOLVED | "is not a measure: it is a finding under criterion 6" (`skills/kit-rubric/SKILL.md:237`) |
| F4.1 merged start branch tagged unchecked | RESOLVED | "When the merge brought in changes to the kit's text" (`skills/lado-kit-format/SKILL.md:84`); the width of that test is F3.6 |
| F4.2 restored blueprint not shown at `plan_ok` | RESOLVED | "`BLUEPRINT.md`, the note carries it whole after the plan" (`flows/improve.yaml:45`); the ask names it (line 53) |
| F5.1 grilling vs kit-interview | RESOLVED, as the human answered | "`kit-interview` (the round's format, how far to ask), `kit-interview` wins." (`agents/supervisor.md:51`); the sub-agent part left over is F5.3 |
| F5.2 kit-budget "tell the human" | RESOLVED | "the lead takes it to the" human (`skills/kit-budget/SKILL.md:93`) |
| F6.1 critic repeats | RESOLVED | The working-rules repeat is gone (`agents/critic.md:76`), and "candidates" lives in `skills/kit-rubric/SKILL.md:10-12` only |
| F7.1 critic cannot find the kit | RESOLVED | "corrected path or name, or ask the human to cancel the run" (`agents/supervisor.md:80`) |
| F9.1 Tessera history | RESOLVED | `grep -rn Tessera skills/*/SKILL.md` finds nothing; the credit stays in the script's docstring and BLUEPRINT |
| F12.1 report-only merge | RESOLVED | "**A report-only run.**" (`skills/lado-kit-format/SKILL.md:111-117`); its new side effects are F12.2 and F3.8 |

## Cut rules

The fourth sub-agent checked all 73 removed segments of the word diff; no rule is lost.
The main ones:

| Removed rule (file:line at base 0456710) | Where it is now |
|---|---|
| `agents/supervisor.md:60-79` the release procedure, steps 1–4 and "Report `released`…" | `skills/lado-kit-format/SKILL.md:74-109`, sentence by sentence, around "the start branch". Added: the merged-text check, the retry bound, and the failure paragraph |
| `agents/supervisor.md:65-66` "On a conflict, `git merge --abort` and report `failed` with the conflicting files." | `skills/lado-kit-format/SKILL.md:83-84`, word for word |
| `agents/supervisor.md:71-72` "Never move or delete a tag that exists." | `skills/lado-kit-format/SKILL.md:92` |
| `agents/supervisor.md:73-76` push and pull request each need the human's yes; otherwise the release ends at the local tag | `skills/lado-kit-format/SKILL.md:93-96` |
| `agents/supervisor.md:35` "merge its branch (it holds the report)" | `skills/lado-kit-format/SKILL.md:111-117`, narrowed to a content check |
| `flows/improve.yaml:43-44` a restored blueprint merged "only if the human, shown it whole, says yes (otherwise only the report)" | `skills/lado-kit-format/SKILL.md:114-117` |
| `flows/improve.yaml:59-60` "change what differs from the plan you built" | `flows/improve.yaml:63-64` "Changed since the previous plan"; the rule kept its topic but changed its reference point, which is F2.2 still open, not a lost rule |
| `agents/critic.md:12-13` "candidates … each one carries the quote …" | `skills/kit-rubric/SKILL.md:10-12` |
| `agents/critic.md:64` "You still write findings, not grades" | `agents/critic.md:62-63` and `skills/kit-rubric/SKILL.md:10-11` |
| `agents/critic.md:79` "change no file but your report and its diagrams" | `agents/critic.md:10-11` (it was a repeat) |
| `skills/kit-budget/SKILL.md:79-84` calibration examples | The numbers are at lines 79-80; the rule about repeats the script misses is at lines 71-73 and `skills/kit-rubric/SKILL.md:127-129` |
| `skills/kit-budget/SKILL.md:97` "tell the human" | `skills/kit-budget/SKILL.md:93-94`, routed through the lead |

## Missed earlier

Findings in text the diff does not touch. They do not block a verdict and do not count for
the stop rule.

- **F3.9** [medium] `agents/author.md:76` (state `build` of `create` and `improve`)
  > contradiction, a gap, something `lado kits check` rejects), when a warning or a measure

  This is known hole 1, on the author's side. The supervisor and the critic now tell an
  environment failure from a kit fault, but the author's own pre-report runs of `lado kits
  check .` and the scripts (`agents/author.md:32`) have no such rule. Without network or
  `uv`, the author reports `blocked`, which sends the run back to `design` or `triage`
  and through a gate.
  Fix: "a check that fails for a cause outside the kit's files: send the supervisor the
  command and its output with `send_message` and wait; it is not `blocked`."
  Passes: 1/3 and the full pass, confirmed.

- **F3.10** [low] `agents/critic.md:31` (states `assess` of `improve`, `evaluate` of
  `evaluate`)
  > 1. Run `lado kits check <folder>` and keep its whole output.

  The new environment rule sits in "Verdict", so it covers only steps that ask for a
  verdict. In `assess`, a network failure goes into the card as an error, and "Fix first"
  must list "an error of `lado kits check`" (`skills/kit-rubric/SKILL.md:260`). `triage`
  then plans a kit fix for a fault the kit does not have.
  Fix: move the environment paragraph out of "Verdict" so it covers every check the
  critic runs. That also settles F6.2 if it moves to `lado-kit-format`.
  Passes: 1/3, confirmed. Evidence: `skills/kit-rubric/SKILL.md:239` and `:260`.

- **F12.3** [low] `README.md:106`
  > The supervisor merges the run's branch, which brings the report into your repository.

  The merge is now conditional: when the run touches more than `kit-reports/`, the human
  is asked first. A reader of the README expects an unconditional merge.
  Fix: "…merges the run's branch when it adds only the report; anything more needs your
  yes."
  Passes: 1/3, confirmed.

## Questions for the human

1. When `release` stops on an environment failure the human must settle, how should the
   run end (F3.5)? Recommended: it stays in `release`; the supervisor tells the human
   what is left and offers to retry once it is settled. Otherwise the human runs `lado
   flow-set … done` after finishing by hand, or cancels.
2. Merged kit text that contradicts the blueprint: should the author change it, or send
   it to you (F7.2)? Recommended: send it to you (`blocked`); the author changes none of
   it.
3. Should the supervisor look facts up only itself during the interview, never through a
   sub-agent or worker (F5.3)? Recommended: yes.
