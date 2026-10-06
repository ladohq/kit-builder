# Backlog

Found while building kit-builder, outside the task at hand. Items marked `[lado]` are bugs or
friction in LADO itself, to move to the LADO repository.

- `kit-budget` finds duplicates per paragraph (blocks between blank lines). Two `do` texts
  without blank lines that differ in one sentence (lado-dev's `implement` in `feature` and
  `fix`) are not reported. If this proves to matter, compare by sentence or by line too.
- `[lado]` `lado kits check` scans only SKILL.md of a skill for hardcoded paths, not the
  skill's other files (scripts, references), although they travel with the kit.
