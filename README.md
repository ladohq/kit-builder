# kit-builder

A LADO kit that builds and evaluates LADO kits.

- **Create** a kit for your own work. A supervisor interviews you, either about a process you
  already have or from scratch with a gallery of proven team shapes. It writes a
  `BLUEPRINT.md` that says why each part of the kit exists. An author writes the kit, and a
  critic checks it against a complexity budget and a 12-criterion rubric. You approve the
  blueprint and the release, and the supervisor tags it.
- **Evaluate** any kit, yours or someone else's, before you put it to work. The critic runs
  `lado kits check` and the budget script and reviews the text against the rubric. It
  writes a report with quoted findings and the few things to fix first.

The rule behind both is the simplest kit that solves your task. A role, step, gate or skill
goes into the kit only when one of your requirements needs it.

Requires LADO 0.23 or newer (`lado kits check` checks flow graphs from 0.23 on).

## Install and start

```bash
lado kits add kit-builder -m official
mkdir my-kit && cd my-kit && git init && git commit --allow-empty -m init
lado start . --kit kit-builder
```

Then talk to the supervisor in LADO's UI or terminal. Its first question is whether you
already have a process you want to bring over.

### Evaluate someone else's kit

Start a session in any repository and name the kit, either its installed name or a path to
its folder:

```bash
lado start . --kit kit-builder
# then tell the supervisor: "evaluate the kit lado-dev" (or "... the kit in ../my-team")
```

The report lands in `kit-reports/<kit>-<version>-<date>.md` of that repository.

## Flows

**`create`**: from interview to a release tag. The kit's repository is the session's
repository.

```
design (supervisor) → design_ok (gate: approval)
  → build (author) → evaluate (critic, max_visits 3; changes → build)
  → release_ok (gate: approval) → release (supervisor) → done
```

- `design`: the interview in rounds (question, context, recommendation) and `BLUEPRINT.md`.
  Rejecting it at `design_ok` sends it back with your reason.
- `build`: the author writes the kit from the blueprint and, on later visits, fixes the
  critic's findings.
- `evaluate`: `lado kits check`, the budget and the rubric. It reports `approved` or
  `changes`, at most three times.
- `release`: sets the version, checks `lado kits check . --tag vX.Y.Z`, merges the run's
  branch and tags locally. Pushing and a marketplace pull request happen only after you say
  yes, and the supervisor gives you the pull request text.

**`evaluate`**: one step: the critic evaluates the kit the task names and writes the report.
The supervisor merges the run's branch, which brings the report into your repository.

## Where things are

- `BLUEPRINT.md`: kit-builder's own blueprint, with its requirements, the trace of every
  role, step, gate and skill to them, and its complexity budget. A kit built with
  kit-builder gets its own `BLUEPRINT.md` in the same shape.
- `kit-reports/`: evaluation reports, including kit-builder's evaluation of itself.
- `agents/`, `flows/`, `skills/`: the roles, the two flows and the kit's own skills
  (`kit-interview`, `kit-archetypes`, `lado-kit-format`, `kit-budget`, `kit-rubric`).
  `grilling` and `writing-for-agents` come from
  [mattpocock/skills](https://github.com/mattpocock/skills) as a dependency.

## Tests

The complexity budget script (`skills/kit-budget/scripts/kit_budget.py`) has tests on small
fixture kits. Run them from the repository root with `uv`:

```bash
uv run --with pyyaml python -m unittest discover -s tests -v
```

Run the script itself on any kit folder:

```bash
uv run --script skills/kit-budget/scripts/kit_budget.py <kit folder>
```
