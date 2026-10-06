# kit-builder

A LADO kit that builds and evaluates LADO kits.

- **Create** a kit for your own work. A supervisor interviews you, either about a process you
  already have or from scratch with a gallery of proven team shapes. It writes a
  `BLUEPRINT.md` that says why each part of the kit exists. An author writes the kit, and a
  critic checks it against a complexity budget and a 12-criterion rubric. You approve the
  blueprint and the release, and the supervisor tags it.
- **Improve** a kit you already have, from the critic's report to a new tag. You decide
  with the supervisor which findings to fix. A kit without a `BLUEPRINT.md` gets one
  restored from its roles and flows on the way.
- **Evaluate** any kit, yours or someone else's, before you put it to work. The critic runs
  `lado kits check` and the budget script and reviews the text against the rubric, with
  the text of the skills each role depends on and a checklist of holes earlier reviews
  missed. It writes a report with quoted findings and the few things to fix first.

The rule behind all three is the simplest kit that solves your task. A role, step, gate or
skill goes into the kit only when one of your requirements needs it.

Requires LADO 0.23 or newer (`lado kits check` checks flow graphs from 0.23 on).

## Install and start

```bash
lado kits add kit-builder -m official
mkdir my-kit && cd my-kit && git init && git commit --allow-empty -m init
lado start . --kit kit-builder
```

Then talk to the supervisor in LADO's UI or terminal. Its first question is whether you
already have a process you want to bring over.

In a fresh repository the agent CLI may first ask whether you trust the folder. If
`lado ls` shows the supervisor in `starting` for long, run `lado attach` and confirm.

### Evaluate someone else's kit

Start a session in any repository and name the kit, either its installed name or the
absolute path to its folder:

```bash
lado start . --kit kit-builder
# then tell the supervisor: "evaluate the kit lado-dev" (or "... the kit in ~/src/my-team")
```

The report lands in `kit-reports/<kit>-<version>-<date>.md` of that repository.

To check a kit again after changes, name its previous report ("evaluate lado-dev again
against kit-reports/lado-dev-0.9.1-2026-10-06.md"). The critic then reviews only what
changed since that report: it marks the old findings resolved or still open, checks that
no rule was lost in cut text, lists findings in untouched text apart as "Missed earlier",
and says whether the stop rule holds (no high or medium finding in the changed text). When
it holds, another round would mostly find what earlier rounds missed; when it does not, it
is advice for you, not a block. The report's card says what its count covers, the whole
kit or only the change, so compare counts only between reports of the same coverage.

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
  `changes`, at most three times; `changes` while a high finding is open (medium ones are
  for you to weigh at the release gate). If the loop hits
  its limit, the supervisor shows you the open findings and you answer the loop gate:
  `continue` (the critic checks once more) or `cancel`; to release as it is, run
  `lado flow-set <session> <run> release_ok --reason "<why>"`.
- `release`: sets the version, checks `lado kits check . --tag vX.Y.Z`, merges the run's
  branch and tags locally. Pushing and a marketplace pull request happen only after you say
  yes, and the supervisor gives you the pull request text.

**`improve`**: change a kit in the session's repository and release it. Take it when you
want an existing kit better, or when an `evaluate` report has findings you want fixed (name
the report, so the same kit is not evaluated again). Every change to a kit goes through a
run, so the critic's check and your gates come before the tag.

```
assess (critic) → triage (supervisor) → plan_ok (gate: approval)
  → build (author) → evaluate (critic, max_visits 3; changes → build)
  → release_ok (gate: approval) → release (supervisor) → done
```

- `assess`: a full evaluation of the whole current version, or the full report you named
  for it. Later checks review only the change, so this one sets what the run looks at.
- `triage`: you and the supervisor go through the findings, the critic's questions and
  any change you want that no finding covers; it restores `BLUEPRINT.md` if the kit has
  none and writes the plan of changes. Rejecting the plan at `plan_ok` sends it back with
  your reason.
- `build`, `evaluate`, `release`: as in `create`, by the plan; the plan names the version,
  and `evaluate` reviews the change against the report, then, before it approves, makes
  one more pass over the whole of every file the change touched.

**`evaluate`**: one step: the critic evaluates the kit the task names and writes the report.
The supervisor merges the run's branch, which brings the report into your repository.

## Where things are

- `BLUEPRINT.md`: kit-builder's own blueprint, with its requirements, the trace of every
  role, step, gate and skill to them, and its complexity budget (green limits: 800 words
  for a worker role, 1000 for the lead, five work steps and two gates per flow). A kit built with
  kit-builder gets its own `BLUEPRINT.md` in the same shape.
- `kit-reports/`: evaluation reports, including kit-builder's evaluation of itself.
- `agents/`, `flows/`, `skills/`: the roles, the three flows and the kit's own skills
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
