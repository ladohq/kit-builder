---
name: lado-kit-format
description: The LADO kit format and the rules a kit must follow that `lado kits check` does not prove — provider neutrality, paths, one lead, needs, gates, max_visits. Use when writing kit.yaml, a role, a flow or a skill of a kit, or checking it against the format; for judging a kit's text against review criteria use kit-rubric.
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
```

## Rules the command does not prove

**Provider neutrality.** A kit runs under any agent CLI LADO supports. Name actions, not one
CLI's tools, slash commands, models or config files: "run the tests", "read the file", not a
tool name. Skills come in through `skills:` and MCP servers through `mcp:`; never paste a
skill's text into a prompt.

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
