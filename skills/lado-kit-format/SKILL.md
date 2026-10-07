---
name: lado-kit-format
description: The LADO kit format and the rules a kit must follow that `lado kits check` does not prove — provider neutrality, skills from outside the kit, paths, one lead, artifacts (produces, reads, artifact or note), gates, max_visits — what to do when a check fails, and how a kit is released and published. Use when writing kit.yaml, a role, a flow or a skill of a kit, or checking it against the format, or releasing it; for judging a kit's text against review criteria use kit-rubric.
---

# LADO kit format

## The source of truth is `lado kits check`

```bash
lado kits check <kit folder>                 # while working
lado kits check <kit folder> --tag vX.Y.Z    # before a release tag: what `lado kits add` will say
```

It checks the format of every file, the skill packs, hardcoded paths in roles, MCP commands
and SKILL.md files, and the graph of each flow (unreachable states, traps, cycles without
`max_visits` or a gate, `reads` of a name no state before it produces, roles that act in
no step). An
error there is a bug in the kit; read each `warning:` line and fix it or say in the
blueprint why it stays. Do not re-check by hand what the command checks; when this skill and
the command disagree, the command is right. The format itself is in the "Kits" section of
LADO's README and in `lado kits show <kit>`.

A kit, in short:

```
kit.yaml              name, version, description, supervisor, dependencies (lado, skills)
agents/<role>.md      frontmatter name, description, skills, mcp; the body is the role prompt
flows/<name>.yaml     states: work (agent, do, outcomes, reads, produces), gate (reads), end
skills/<name>/        SKILL.md and its files, always moved as a whole
BLUEPRINT.md          not LADO's: why each part exists, with flow skeletons (kit-interview)
blueprint-flows/      the skeletons drawn as SVG by the kit-budget flow script
```

## Rules the command does not prove

**Provider neutrality.** A kit runs under any agent CLI LADO supports. Name actions, not one
CLI's tools, slash commands, models or config files: "run the tests", "read the file", not a
tool name. Skills come in through `skills:` and MCP servers through `mcp:`; never paste a
skill's text into a prompt.

**Skills from outside the kit.** `kit.yaml` cannot list the kit's own skills: LADO finds
them in `skills/`. So every other skill a role lists in `skills:` is declared in
`dependencies.skills`, by its own folder (the one holding its SKILL.md) in `folders`, from
a pack pinned to a tag or commit. A folder above the skill installs every skill under it,
and the ones no role uses only add noise to the session.

**Paths.** Roles and MCP commands reach kit files through `${KIT_DIR}`; a skill reaches its
own files through `${SKILL_DIR}` (only inside a skill). The command scans only SKILL.md of a
skill, so keep scripts and other files of a skill free of absolute and home paths too.

**One lead.** Only a kit that leads a whole session has `supervisor:` in kit.yaml. A kit
that adds roles or skills to another kit has no supervisor, so adding it never changes who
leads. A supervisor's step in a flow goes to whoever leads the session.

**Artifacts: `produces`, `reads`, artifact or note.** LADO 0.27 has no `needs`; a step's
result reaches later steps and the human as an artifact.
- Artifact or note. An artifact is a step's result that someone reads later: a later step,
  or the human at a gate, also from afar in LADO's UI (a design, a plan, a review, a
  report). A note is the short message about the step to whoever acts next: the verdict,
  the questions for the human, what changed. A result never goes into the note's body, and
  nobody is handed a local path: the human may not reach this machine.
- A work state's `produces` names the artifacts its step must write. LADO refuses every
  outcome until each is written in the current visit, so it holds whatever the outcome:
  the `do` says what the artifact holds when there is no result (nothing to change,
  blocked). Name only what is always there; what a step writes only sometimes (a diagram,
  a log) it attaches to its note with `flow_advance`'s `artifacts` when it exists. Gates
  and ends produce nothing.
- A work state's or a gate's `reads` names artifacts of the run that the step or the gate
  shows: only names a state before it produces, never its own; a step on a loop sees its
  own `produces` on a later visit without them.
- A name is 1-64 characters of a-z, 0-9, `.`, `_` and `-`, produced by one state of its
  flow. Take the names from the user's words for their process, not from another kit.
- An agent writes an artifact with `write_artifact` and reads one with `read_artifact`: a
  worker of the run by the bare name, the lead by `<run>/<name>`.
- When the result is also a file of the repository (it ships with the tag, a later run
  reads it), the file is the source: commit it, then write the artifact from it (`file`),
  last before reporting. Whoever commits a change to such a file writes its artifact again
  at once, so no later step or gate sees an older text. A relative `file` is resolved from
  where the agent started: a worker starts in the run's worktree, the lead in its own
  repository, so the lead passes the absolute path in the run's worktree (`flow_status`).
- A step gets the note of the step before it, with the artifacts attached to it. After a
  gate, the note is the human's answer together with the note the gate showed them. A
  human's comment at a gate reaches only the next step: what later steps need goes into an
  artifact.
- On a loop, a reviewing state produces its review and, on a later visit, marks its
  previous findings RESOLVED or STILL OPEN; a work state the loop sends back to writes its
  artifact whole on every visit, not only what changed, because readers get only its
  latest record.

**Gates.** A gate is the human's decision. Put one before anything that is hard to undo or
leaves the machine (merge, tag, push, publish) and where only the human can decide; not
after every step. A gate `reads` what the human approves: it shows them the note that led
to it and those artifacts.

**`max_visits`.** On a reviewing state that can send work back, use a small number such as
3, and say in its `do` what changes on a later visit.

**Each `do`** says when the step is done and when to report each outcome.

## When a check or command fails

This is the one rule for every role. Find the cause before you act on a failure of
`lado kits check`, a kit-builder script or `git`. An error the kit's files cause is the
kit's: a finding, a fix, `changes` or `failed`, as your step says. A cause outside the
kit's files (no network to fetch a skill pack, a missing `uv` or `lado`, uncommitted
changes in the way, another branch checked out) says nothing about the kit, so it is not a
finding, not a verdict either way and not `blocked`, and the author cannot fix it:
- a worker sends the supervisor the command and its whole output with `send_message`,
  waits, and runs it again once the supervisor answers;
- the supervisor shows the human the command and its output and waits; it runs it again
  once they say it is settled, and after a second failure from the same cause leaves it to
  them.

Never change the kit to get past such a failure, and never stash, reset or clean the
human's checkout.

## Releasing

The supervisor's step `release` of `create` and `improve`, in this order. "The start
branch" is the branch the run started from, checked out in the supervisor's repository
(main, or master after a plain `git init`).
1. Settle the version with the human; on a later visit keep the one in `kit.yaml` unless
   they change it. Set it in `kit.yaml` in the run's worktree and commit on the run's
   branch. A tag that already exists for it later means the version is wrong: settle it
   again here.
2. In the run's worktree, note `git rev-parse HEAD`, then merge the start branch into the
   run's branch. On a conflict, `git merge --abort` and report `failed` with the
   conflicting files. When the merge brought in changes to the kit's text
   (`git diff --name-only <the noted commit> HEAD` lists a file of the kit's text,
   `kit-rubric` "Re-evaluation" 1, or of `blueprint-flows/`), report `failed` with that
   list: neither the critic nor the human has seen the merged kit, and a clean merge can
   still join two texts that contradict each other. Then run
   `lado kits check . --tag vX.Y.Z` there; it must print OK.
3. In the supervisor's repository, on the start branch, `git merge --ff-only <the run's
   branch>`, so that branch only ever moves to a checked commit. If it cannot fast-forward
   because the start branch gained commits, go back to step 2, at most twice; then ask the
   human. Then `git tag vX.Y.Z` there. Never move or delete a tag that exists.
4. Ask whether to push the branch and the tag, then whether to open a marketplace pull
   request, with its text ready ("Publishing"). Each leaves the machine and needs the
   human's yes in the chat, in this session. Without a yes, the release ends at the local
   tag; say what is left for the human to do.

Report `failed` only for a fault in the kit's files, with the command and its whole
output in note_body (the release produces no artifact); the author fixes it on the run's
branch and runs the command again as the note gives it, `--tag` included, since its own
check runs without `--tag`. On a merge conflict the author merges the start branch into
the run's branch, resolves the conflicts and commits; a conflict between two decisions on
content is the human's (`blocked`). Kit text the merge brought in the author leaves as it
is: when it contradicts the blueprint or adds an element the blueprint does not name, it
reports `blocked` with the list, since which one changes is the human's decision. A
failure from outside the kit's files follows "When a check or command fails". When it is left to the human, or step 3 reaches
its bound, the run stays in `release`, never `failed`: tell the human which of steps 2–4
are left and how to go on: you retry once they say it is settled, or they finish by hand
and run `lado flow-set <session> <run> done`, or they cancel the run.

Report `released` once the tag is on the start branch: note_summary is the tag; note_body
the check's output and what the human chose about push and pull request, or what is left.

**A report-only run.** A run of `evaluate`, or of `improve` that ended in `nothing`, adds
only a report. When it ends, merge its branch into the start branch only if
`git diff --name-only <start branch>...<the run's branch>` lists nothing outside
`kit-reports/`. When it lists more (a blueprint `triage` restored), show the human the
list and that text whole; with their yes merge the branch. Otherwise take only the run's
own report files, the `kit-reports/` paths of that list: ask the human first when one of
them has local changes or the start branch changed it since the run began, then
`git checkout <the run's branch> -- <those paths>` and `git commit -m "<report>" --
<those paths>`, so nothing else they staged goes in. On a merge conflict, `git merge
--abort` and show the human the files; any other failure follows "When a check or command
fails". The run has ended, so there is no outcome to report.

## Publishing

A kit reaches a marketplace by a pull request to the marketplace's repository, after the
kit's branch and tag are pushed: the marketplace's CI checks the kit's latest tag. The
pull request needs:

- the line for `marketplace.yaml`: `<name>: <git url of the kit's repository>`, the name as
  in `kit.yaml`;
- the row for the marketplace README's table:
  `` | `<name>` | [<owner>/<repo>](<https url>) | <one sentence: what it is for> | ``;
- a title and a short body: what the kit does, its flows, the output of
  `lado kits check . --tag vX.Y.Z`.

Name the kit's repository `lado-kit-<name>` and give it the GitHub topic `lado-kit`, so
people find it.
