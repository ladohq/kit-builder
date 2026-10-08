# Backlog

Found while building kit-builder, outside the task at hand. Items marked `[lado]` are bugs or
friction in LADO itself, to move to the LADO repository.

- `[lado]` `lado kits check` scans only SKILL.md of a skill for hardcoded paths, not the
  skill's other files (scripts, references), although they travel with the kit.
- `[lado]` A work step after a gate gets the human's answer together with the note that led
  to the gate ("Note before the gate", `runs._answer_note`), but the README's Kits section
  and the docstring of `lado/flows.py` say only that a step gets the previous step's note.
  All three rubric passes on lado-dev read that as "the note is lost at a gate" (3 false
  findings). `lado-kit-format` now states it; LADO's docs should too.
- `[lado]` A run's `human_language` reaches only the notes ("Write note_summary and
  note_body in …", `runs.py`); files written for the human, such as a report, get no hint.
  In a `ru` run of `evaluate` over lado-dev the first report came in English, following the
  English template. `kit-rubric` now says the report takes the notes' language; LADO could
  say it for every file the step writes for the human. With LADO 0.27 the report is also
  the artifact the human reads (`evaluation`, `assessment`), so the hint belongs with the
  artifacts a step must write ("This step must write: ...") as well.
- `[lado]` A relative `file` of `write_artifact` is resolved from where the agent
  started: for the lead that is its own repository, not the run's worktree, so in a run's
  step a lead that writes `file=BLUEPRINT.md` publishes the start branch's copy, and
  `produces` counts it. kit-builder's supervisor passes the absolute path in the run's
  worktree (0.5.0); any kit whose lead writes a file of the run has the same trap. LADO
  could resolve a lead's relative `file` from the run's worktree inside a run's step, or
  say so in the step's text.
- Re-evaluation (`kit-rubric`) ran once, by hand, on kit-builder 0.2.0 against the 0.1.0
  report (`kit-reports/kit-builder-0.2.0-2026-10-06.md`): the cut-rule check found two lost
  rules, but the diff covered the whole kit, so "Missed earlier" was empty by construction
  and the stop rule was not tested over rounds. Still to do: a second round after the fixes,
  and a run of `improve` over lado-dev, to see the stop rule hold after one or two rounds
  with a small "Missed earlier".
- Rubric criterion 6 is the only check for a rule restated inside a longer paragraph
  (`kit-budget` misses them, 38–45% similar). If such repeats keep coming back in reports,
  try comparing sentences, not only paragraphs.

### The human's notes on the lado-dev session (2026-10-06), what is left

Closed in 0.2.0: 1 (flow `improve`), 2 (re-evaluation, stop rule), 3 (lead limit, cut table,
cut-rule check, a restored blueprint to justify yellow), 5 ("Existing kit"), 6 (one-pass
findings confirmed), 7 in the kit (the report in the notes' language; the `[lado]` part is
above). Reports in `kit-reports/` (item 8) stay published with the kit, as decided in 0.2.0.
Open:

- Item 2: convergence is unproven on a real run (above).
- Item 4: similar paragraphs are found now, but a rule restated inside a longer paragraph
  still is not (above).
- Item 8: `${SKILL_DIR}` is not set for every agent; `kit-budget` now tells the agent to put
  the skill's folder there itself. `[lado]` A `lado kits budget <folder>` (or an exported
  path to the kit's skills) would remove the guess.

### End-to-end run of `create` (AC4.4, 2026-10-06)

Sandbox: empty repository, own `LADO_HOME` and `LADO_TMUX_SOCKET`, kit-builder at c9651f5,
LADO 0.23.1, Claude Code, permission mode `auto`. The kit `docs-fixer` ("solo + reviewer"
for typos and broken links in docs) went from interview to `done` in 35 minutes, 19 of
them waiting at the two gates; `evaluate` ran twice (8 findings, then approved with one
low); `lado kits check . --tag v0.1.0` printed OK. Found on the way:

- `[lado]` A fresh repository blocks the supervisor on Claude Code's "Do you trust this
  folder?" dialog. `lado ls` shows `starting` with no hint; only `lado attach` (or the
  tmux window) shows why. Workers in the session's worktrees did not hit it. `lado start`
  could detect the dialog and say so, or `lado ls` could name it.
- `[lado]` The human's chat has no CLI: writing to the supervisor and answering an
  `ask_human` question work only in the UI (or its HTTP API with the token). For this
  headless run the "user" called `lado.runtime.write_as_human` and `answer_question`
  from LADO's Python. A `lado say <session> [--to agent]` and `lado reply <session> <id>
  [choice] [-m text]` would make end-to-end runs scriptable. (`lado answer` refusing an
  agent is intended: gates are the human's.)
- Closed with kit-builder 0.5.0 (LADO 0.27): ~~`[lado]` The first step after a gate gets
  the blueprint twice, as "Note from design" (`needs`) and as "Note before the gate".~~ The
  blueprint is now the artifact `blueprint`; the note is short, and a step's text names a
  record attached to the previous note only there, not again for its `reads`.

### Experiment: kit-builder 0.1.0 against 0.2.0 on lado-dev (2026-10-06)

Same input for both: lado-dev 0.9.1 (`c8afb8f` in kit-lado-dev). With 0.1.0, three `improve`
cycles gave 0.9.4. With 0.2.0, one `improve` cycle gave 0.10.0 (branch `exp/from-0.9.1` in
kit-lado-dev, not released). Then the 0.2.0 critic evaluated both in full and independently.
Reports are in kit-lado-dev's `kit-reports/` on that branch: `lado-dev-0.9.1`, `-0.10.0`,
`-0.10.0-full` and `-0.9.4`.

Results:

| | 0.1.0, 3 cycles → 0.9.4 | 0.2.0, 1 cycle → 0.10.0 |
|---|---|---|
| First assessment of 0.9.1 | 13 findings, 0 high | 19 findings, 1 high |
| Full evaluation by the 0.2.0 critic | 11 findings (0 high / 5 medium / 6 low) | 20 findings (0 high / 13 medium / 7 low) |
| BLUEPRINT.md | none | restored, so yellow measures are justified |

- Better in 0.2.0: one cycle closed all 19 findings, and the cut-rule check found no lost
  rule. Four findings that 0.1.0 found only in cycles 2–3 came up in the first assessment.
  The `brainstorming` high was found at all; it is still in 0.9.4.
- Five findings of the 0.10.0 full report are already fixed in 0.9.4 (red check in `merge`
  not classified, relative mockup path, code outside a flow merged without a gate, "every AC
  about behaviour", the visit-limit rule). The 0.2.0 critic missed them in its first
  assessment of 0.9.1, and one cycle did not reach them.

What to fix in kit-builder (all done in 0.3.0, each marked below; still to see on a real
run whether recall evens out):

- **Critic recall varies more than the kits differ.** The same 0.2.0 critic found 11
  findings on 0.9.4 and 20 on 0.10.0, and most of the 20 apply to 0.9.4 as well. It found
  the `brainstorming` high on 0.9.1 but not on 0.9.4, where the same line still stands
  (`supervisor.md:43`). The 0.10.0-full passes read the dependency skills' texts in
  `~/.lado/cache` and the LADO repository; the 0.9.4 passes did not. Wanted: `kit-rubric`
  makes every pass read the text of each dependency skill a role lists, and gives the passes
  a checklist of known holes: a red check routed back as code although the cause is the
  environment; read-only work outside a flow and merges without a gate; a path to a file
  outside the run's worktree; a reviewer verdict with no severity threshold; a dependency
  skill that writes files or asks the user while its role must not.
  *Done in 0.3.0:* `kit-rubric`, "Dependency skills" and "Known holes"; the report has a
  "Known holes" table.
- **`approved` while the stop rule fails.** The `improve/evaluate` check of 0.10.0 reported
  `approved` with "stop rule not met: 1 medium" in the same report. Wanted: one rule in
  `kit-rubric` and the critic for when the verdict is `approved`, the same as the stop rule,
  or say explicitly that a medium is only advice at release.
  *Done in 0.3.0:* one rule, `kit-rubric` "Verdict"; the stop rule is advice for the release
  gate, and the card says so. The critic points to it.
- **A re-evaluation's count cannot be compared with a full evaluation's.** The re-evaluation
  of 0.10.0 looked only at changed text and reported 9 findings; the full evaluation of the
  same commit reported 20. Wanted: the report card says how much of the kit the count
  covers, so the human does not compare 9 with 11.
  *Done in 0.3.0:* the card's row "Covers" and a line that counts of different coverage are
  not comparable.
- **The first assessment sets the ceiling of an `improve` run.** What the critic misses
  there, no later step of the same run looks for, because re-evaluation reads only the diff.
  Wanted: either the first assessment of `improve` runs the full checklist above, or the
  critic at `release_ok` adds one full pass over the parts the diff touched.
  *Done in 0.3.0, both:* `improve.assess` is always a full evaluation; `kit-rubric`
  "Re-evaluation" 5 adds a full pass over every file the diff touches before `approved`.
- **Small:** BLUEPRINT §2 of a restored blueprint cites `kit-archetypes`, a kit-builder
  skill the kit's own readers may not have; `kit-interview` could say to name the archetype
  without the skill's name.
  *Done in 0.3.0:* the blueprint template's section 2.

#### Skills kit-builder 0.2.0 uses (checked 2026-10-06, `lado kits show kit-builder`)

| Skill | Source | Registered on (`skills:`) | Named in the text of |
|---|---|---|---|
| `kit-interview` | own | supervisor | supervisor; `create.design`, `improve.triage`; `kit-archetypes` |
| `kit-archetypes` | own | supervisor | supervisor; `create.design`; `kit-interview` and its blueprint template |
| `lado-kit-format` | own | supervisor, author, critic | all three roles; `kit-interview`, `kit-archetypes`, `kit-rubric` |
| `kit-budget` | own | supervisor, author, critic | all three roles; `kit-archetypes`, `kit-rubric`, blueprint template |
| `kit-rubric` | own | critic | critic; `improve.assess`; the descriptions of `kit-budget` and `lado-kit-format` |
| `grilling` | mattpocock-skills v1.2.3 | supervisor | supervisor |
| `writing-for-agents` | mattpocock-skills v1.2.3 | supervisor, author | supervisor, author |
| `grill-me`, `handoff`, `teach`, `to-questionnaire`, `wait-what` | mattpocock-skills v1.2.3 | none | nowhere |

Every skill that a role or one of its steps names is registered on that role, so nothing
is missing from `skills:`. All three points below are done in 0.3.0: `kit-rubric` is on the
author and the supervisor (their text points to it), `folders` names only `grilling` and
`writing-for-agents` (`lado kits check .` counts 7 skills, was 12), and `kit-rubric` says
where to find a dependency's text.

- `kit-rubric` is not on the author or the supervisor, although `kit-budget` (which both
  have) sends to "criterion 6 (`kit-rubric`)", and the description of `lado-kit-format` says
  "for judging a kit's text against review criteria use kit-rubric". The author fixes
  findings named by rubric criterion. The supervisor goes through them with the human in
  `triage` and checks the stop rule at `release_ok`. Neither can open the criterion's text.
  Decide: register `kit-rubric` on both, or make the report quote what each criterion
  means, so the reader does not need the skill.
- `dependencies.skills` pulls the whole `skills/productivity` folder, which installs 5
  skills no role uses. Narrow `folders` to `skills/productivity/grilling` and
  `skills/productivity/writing-for-agents`, if LADO takes skill-level folders.
- The critic reads the dependency skills of the kit it evaluates from `~/.lado/cache`
  (seen in the lado-dev reports). No skill or role says so. That is the gap behind the
  recall finding above: `kit-rubric` should say where to find a dependency's text
  (`lado kits show <kit>` prints each one's folder).
- `kit-budget`'s `flow_diagram.py` has no case for a kit without `flows/` (a skill-only
  kit such as tracker-jira-server): it globs the kit root, reads `kit.yaml` as a flow and
  exits 2 with `error: kit.yaml: states must be a non-empty mapping`, with `--out` and with
  `--compare`. It should say "no flows" and exit 0; the `create` step text could then
  drop the supervisor's "not applicable" ruling. Found in session kit-tracker-jira-server,
  run create/tracker-jira-server, 2026-10-08.
- `lado-kit-format` ("Publishing") says "Name the kit's repository `lado-kit-<name>`" with
  no exception, but the official marketplace's README ("Propose a kit", 4) names kits of
  the ladohq organisation `kit-<name>`. The critic took the rule as written and filed
  F12.4 "rename `ladohq/kit-tracker-jira-server` to `lado-kit-…`"; the supervisor
  accepted it, the author changed the README's URL, and the human withdrew it at the
  release step, which cost one more triage, build and evaluate round. The skill should
  quote the marketplace's rule whole, the ladohq exception included. Found in session
  kit-tracker-jira-server, run improve/tracker-jira-server, 2026-10-08.
