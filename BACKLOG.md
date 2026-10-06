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
- An `evaluate` run ends with the critic's report committed on the run's branch, which is
  not merged, so LADO keeps the worktree and asks the supervisor to merge it. The
  supervisor role (T3) should say to merge that branch so the report lands in the
  session's repository.
