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
  say it for every file the step writes for the human.
- Re-evaluation (`kit-rubric`) is untested on a real kit: run `improve` or `evaluate` with a
  previous report over lado-dev and check that the stop rule holds after one or two rounds,
  that "Missed earlier" stays small, and that the cut-rule table catches a lost rule.

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
- `[lado]` The first step after a gate gets the blueprint twice: once as "Note from
  design" (the step `needs: [design]`) and again as "Note before the gate", because the
  gate's note is the same design note. For `build` that is ~7 KB of duplicate context.
  Skip "Note before the gate" when it is the same note a `needs` entry already gives.
