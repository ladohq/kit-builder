# Backlog

Found while building kit-builder, outside the task at hand. Items marked `[lado]` are bugs or
friction in LADO itself, to move to the LADO repository.

- `kit-budget` finds duplicates per paragraph (blocks between blank lines). Two `do` texts
  without blank lines that differ in one sentence (lado-dev's `implement` in `feature` and
  `fix`) are not reported. If this proves to matter, compare by sentence or by line too.
- `[lado]` `lado kits check` scans only SKILL.md of a skill for hardcoded paths, not the
  skill's other files (scripts, references), although they travel with the kit.
- `[lado]` A work step after a gate gets the human's answer together with the note that led
  to the gate ("Note before the gate", `runs._answer_note`), but the README's Kits section
  and the docstring of `lado/flows.py` say only that a step gets the previous step's note.
  All three rubric passes on lado-dev read that as "the note is lost at a gate" (3 false
  findings). `lado-kit-format` now states it; LADO's docs should too.
- Self-evaluation 0.1.0 (`kit-reports/kit-builder-0.1.0-2026-10-06.md`), low findings left
  open: F6.4 (the author's check rule and the done condition of `build` say the same thing)
  and F6.5 (the `blocked` rule is in `build`'s `do` and twice in `agents/author.md`). They
  are wording only, and each copy now agrees with the others. Fold them into one place on
  the next change to `build`.

### End-to-end run of `create` (AC4.4, 2026-10-06)

Sandbox: empty repository, own `LADO_HOME` and `LADO_TMUX_SOCKET`, kit-builder at c9651f5,
LADO 0.23.1, Claude Code, permission mode `auto`. The kit `docs-fixer` ("solo + reviewer"
for typos and broken links in docs) went from interview to `done` in 35 minutes, 19 of
them waiting at the two gates; `evaluate` ran twice (8 findings, then approved with one
low); `lado kits check . --tag v0.1.0` printed OK. Found on the way:

- `docs/mvp-brief.md` (AC4.4) says `lado start <tmp> --kit <path to kit-builder>`, but
  `--kit` takes only a kit name (`kit "/tmp/…" not found`): add the folder first with
  `lado kits add <path>`, then `lado start <tmp> --kit kit-builder`. The README already
  says it this way; fix the brief's wording.
- The interview's rounds came as one question, then four questions at once (scope,
  reviewer, links, end of work), then the list R1..R7. The role says "rounds of one
  decision each". As the user it was quick and clear, so maybe allow a batch of
  independent questions in `kit-interview` explicitly instead of the supervisor breaking
  the rule.
- The supervisor starts the run (`flow_start`) right after the first question, before the
  kit has a name, so the run is called `create/docs-typo-fixer` and the kit `docs-fixer`.
  Cosmetic; starting the run after the name is agreed, or not naming the run after the kit,
  avoids it.
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
