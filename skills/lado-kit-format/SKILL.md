---
name: lado-kit-format
description: The LADO kit format and the rules a kit must follow that `lado kits check` does not prove — provider neutrality, paths, one lead, needs, gates, max_visits. Use when writing or reviewing kit.yaml, a role, a flow or a skill of a kit.
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

**One lead.** Only a kit that leads a whole session has `supervisor:` in kit.yaml, and the
name `supervisor` belongs to that agent alone. A kit that adds roles or skills to another kit
has no supervisor, so adding it never changes who leads. A supervisor's step in a flow goes
to whoever leads the session.

**Notes and `needs`.** A step gets the note of the step before it, nothing else, unless
`needs` names earlier states; then it also gets their latest notes. So a note that a later
step needs (a design, a blueprint) is written whole, never "as above". A reviewing state on
a loop needs itself, to mark its previous findings RESOLVED or STILL OPEN.

**Gates.** A gate is the human's decision: `approval` (exactly `approved`, `rejected`) or
`choice` (its outcome names). Put one before anything that is hard to undo or leaves the
machine (merge, tag, push, publish) and where only the human can decide; not after every
step. A gate with `needs` shows the human those notes.

**`max_visits`.** Every loop back (`changes` → an earlier step) needs a state with
`max_visits` on it, usually the reviewing state, with a small number such as 3. Its `do`
says what changes on a later visit.

**Each `do`** says when the step is done and when to report each outcome.
