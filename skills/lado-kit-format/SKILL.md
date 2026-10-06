---
name: lado-kit-format
description: The LADO kit format and the rules a kit must follow that `lado kits check` does not prove — provider neutrality, skills from outside the kit, paths, one lead, needs, gates, max_visits — and how a kit is released and published. Use when writing kit.yaml, a role, a flow or a skill of a kit, or checking it against the format, or releasing it; for judging a kit's text against review criteria use kit-rubric.
---

# LADO kit format

## The source of truth is `lado kits check`

```bash
lado kits check <kit folder>                 # while working
lado kits check <kit folder> --tag vX.Y.Z    # before a release tag: what `lado kits add` will say
```

It checks the format of every file, the skill packs, hardcoded paths in roles, MCP commands
and SKILL.md files, and the graph of each flow (unreachable states, traps, cycles without
`max_visits` or a gate, `needs` that can never have a note, roles that act in no step). An
error there is a bug in the kit; read each `warning:` line and fix it or say in the
blueprint why it stays. Do not re-check by hand what the command checks; when this skill and
the command disagree, the command is right. The format itself is in the "Kits" section of
LADO's README and in `lado kits show <kit>`.

A kit, in short:

```
kit.yaml              name, version, description, supervisor, dependencies (lado, skills)
agents/<role>.md      frontmatter name, description, skills, mcp; the body is the role prompt
flows/<name>.yaml     states: work (agent, do, outcomes), gate, end
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

**Notes and `needs`.** A step gets the note of the step before it, nothing else, unless
`needs` names earlier states; then it also gets their latest notes. After a gate, the
step's note is the human's answer together with the note that led to the gate, the one the
gate showed the human. A note that a later step needs (a design, a blueprint) is written
whole, never "as above". A state on a loop needs itself: a reviewing state to mark its
previous findings RESOLVED or STILL OPEN; a work state the loop sends back to (implement,
fix, draft) when a gate or a later step needs its note, to see its own previous note. That
work state writes its note whole on every visit, not only what changed, because whoever
needs it gets only its latest note.

**Gates.** A gate is the human's decision. Put one before anything that is hard to undo or
leaves the machine (merge, tag, push, publish) and where only the human can decide; not
after every step. A gate with `needs` shows the human those notes.

**`max_visits`.** On a reviewing state that can send work back, use a small number such as
3, and say in its `do` what changes on a later visit.

**Each `do`** says when the step is done and when to report each outcome.

## Releasing

The supervisor's step `release` of `create` and `improve`, in this order. "The start
branch" is the branch the run started from, checked out in the supervisor's repository
(main, or master after a plain `git init`).
1. Settle the version with the human; on a later visit keep the one in `kit.yaml` unless
   they change it. Set it in `kit.yaml` in the run's worktree and commit on the run's
   branch.
2. In the run's worktree, note `git rev-parse HEAD`, then merge the start branch into the
   run's branch. On a conflict, `git merge --abort` and report `failed` with the
   conflicting files. When the merge brought in changes to the kit's text
   (`git diff --name-only <the noted commit> HEAD` lists any file outside `kit-reports/`
   and `BACKLOG.md`), report `failed` with that list: neither the critic nor the human has
   seen the merged kit, and a clean merge can still join two texts that contradict each
   other. Then run `lado kits check . --tag vX.Y.Z` there; it must print OK.
3. In the supervisor's repository, on the start branch, `git merge --ff-only <the run's
   branch>`, so that branch only ever moves to a checked commit. If it cannot fast-forward
   because the start branch gained commits, go back to step 2, at most twice; then ask the
   human. Then `git tag vX.Y.Z` there. Never move or delete a tag that exists.
4. Ask whether to push the branch and the tag, then whether to open a marketplace pull
   request, with its text ready ("Publishing"). Each leaves the machine and needs the
   human's yes in the chat, in this session. Without a yes, the release ends at the local
   tag; say what is left for the human to do.

When a command fails, find its cause before you report. Report `failed` only for a fault
in the kit's files, with the command and its whole output; the author fixes it on the
run's branch. A cause outside the kit's files (no network to fetch a skill pack, a missing
`uv` or `lado`, a tag that already exists, uncommitted changes in the way, another branch
checked out) is not the author's to fix: show the human the command and its output and
wait for them; run it again once they say it is settled, and after a second failure from
the same cause leave it to them. Never stash, reset or clean the human's checkout, and
never change the kit to get past such a failure. A wrong version from step 1 is yours:
correct it.

Report `released` once the tag is on the start branch: note_summary is the tag; note_body
the check's output and what the human chose about push and pull request, or what is left.

**A report-only run.** A run of `evaluate`, or of `improve` that ended in `nothing`, adds
only a report. When it ends, merge its branch into the start branch only if
`git diff --name-only <start branch>...<the run's branch>` lists nothing outside
`kit-reports/`. When it lists more (a blueprint `triage` restored),
show the human the list and that text whole; with their yes merge the branch, otherwise
take only the report: `git checkout <the run's branch> -- kit-reports/` on the start
branch and commit it. A failed merge is read as above.

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
