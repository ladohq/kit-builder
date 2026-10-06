---
name: kit-interview
description: How to interview a human about the LADO kit they need — the branches (transfer an existing process, start from scratch, or improve an existing kit by the critic's report, restoring its BLUEPRINT.md), a question bank, the round format, how to turn their material (CLAUDE.md, their skills, a process description, tracker statuses) into roles, steps and gates, and the BLUEPRINT.md template. Use when designing a new kit or planning changes to one; for choosing among ready team shapes use kit-archetypes, for the kit file format use lado-kit-format.
---

# Kit interview

The interview ends with requirements R1..Rn in the human's words and a kit shape where every
part traces to one of them. It is not a questionnaire: ask only what changes the kit, and
find the rest yourself.

## Round format

A round is one message. Each decision in it gets its own block, in this order:

```
**Question.** <one question, answerable in a sentence>
**Context.** <why it matters for the kit; what you already found, with where>
**Recommendation.** <your answer and why; usually the simpler option>
```

Put several questions in one round when none of their answers changes another; number
them, so the human can answer "1 yes, 2 as you recommend". A question whose sense or
options depend on an earlier answer waits for that answer, in a round of its own.
Write each answer down as a requirement (R-number) or as a decision in the blueprint at
once, so nothing lives only in the chat. When an answer contradicts an earlier one, say so
and ask which holds.

## Branches

For a new kit the first question is always: "Do you already have a process you want to
bring over?" For a kit that exists, take the branch "Existing kit".

**Transfer** (yes). The process exists; the kit should follow it, not improve it behind the
human's back.
1. Ask for the material: where it lives, which parts are binding. Read it all before the
   next question (section "Reading the human's material").
2. Restate the process as a list of steps with who does each and what each hands on. Done
   when the human agrees or corrects it.
3. Ask only about gaps: a step with no clear "done", a hand-off with no artifact, a
   decision nobody owns, a loop with no limit.
4. Propose the mapping (steps to flow states, people to roles, sign-offs to gates). Where
   the process has more parts than its task needs, say so and recommend merging them, but
   the human decides.

**From scratch** (no). The human needs a working kit, not a lesson in multi-agent design.
1. Ask what one task they will give the kit looks like, start to finish, and what "done"
   means for it.
2. Offer archetypes from `kit-archetypes`: Solo first, then at most two that fit the task.
3. Adapt the chosen archetype only where an answer requires it.

A narrow, specialised kit (a domain such as data pipelines or legal review) goes through
either branch, then the domain questions below.

**Existing kit** (the flow `improve`). The kit and the critic's report of its current
version are given; the human decides what changes, and the blueprint records why.
1. Read every file of the kit and the whole report before the first question.
2. No `BLUEPRINT.md`: restore it from the template, so that the critic stops reporting
   yellow measures nothing justifies. Requirements are what the README, the roles and the
   flows make the kit do, each with the file it comes from; section 2 is the nearest
   archetype or the process the roles describe; section 3 traces every element; section 4
   is the budget script's output. Ask the human only about what the kit cannot tell you,
   in one round: a requirement you inferred and are unsure of, an element no requirement
   covers (cut it, or keep it with which reason), each measure over green (its reason, or
   cut).
3. Go through the report in rounds: each finding with your recommendation (fix, or leave
   with a reason), each of its "Questions for the human", each measure over green that
   keeps its place (the human's reason goes into section 4), then each change the human
   asks for that no finding covers. A finding that changes a
   requirement or adds or drops an element changes sections 1 and 3 too.
4. Add a row to section 5 per change: the planned version, the change, and the report and
   finding it comes from. Commit the blueprint.
5. Write the plan, the note the author and the critic work from:

```
Kit <name> <version now> → <planned version>; report <path> (commit <the commit it evaluated>); blueprint <commit>
Fix: - <finding id and title>: <what to change, in which file>
Change: - <the human's request no finding covers>: <what to change, in which file>
Leave: - <finding id>: <the human's reason>
Answers: - <question>: <answer>
Blueprint: <what changed in sections 1–4, or "unchanged">
```

The planned version is a patch when only text changes, a minor when a role, step, gate,
skill or flow is added or dropped or the kit's behaviour changes for its user.

## Question bank

Pick what the answers so far leave open; skip what the material already says.

- **Task.** What does one task look like, from request to result? What is "done"?
- **Volume.** How many tasks a day or week? Do tasks share code or files?
- **People.** Which decisions are only yours? What must never happen without you?
- **Risk.** What is hard to undo: merge, deploy, publish, send, delete, spend money?
- **Checking.** Who checks the work today, against what? What does a bad result look like?
- **Loops.** When a check fails, what happens? How many tries before you want to step in?
- **Tools.** Which commands, test suites, services or MCP servers does the work need?
- **Domain.** Which rules, terms or standards must every agent know? Where are they written?
- **Existing kit.** Do you already use a kit? What does it lack or do badly?
- **Size.** Would one agent with good instructions do? If not, what breaks?

## Reading the human's material

Read everything first, then map. For each element, note the source (file and line or
section) so the blueprint can cite it.

| Material | What to take | Becomes |
|---|---|---|
| `CLAUDE.md`, `AGENTS.md`, contributor docs | standing rules, commands, conventions | the repository's own file stays where it is; a rule every role needs goes into a skill, not into each role |
| the human's own skills or prompt files | reusable know-how | a kit skill (copied when it is theirs) or a `dependencies.skills` entry (when it is published) |
| a written process (wiki, runbook, checklist) | steps, owners, artifacts, sign-offs | flow states, roles, notes, gates |
| tracker statuses (e.g. To do, In progress, Review, QA, Done) | the states work passes through and who moves it | a status where someone works is a work state; a status where someone signs off is a gate or a review state; a status nobody acts in (Blocked, Backlog) is not a state |
| team roles (developer, QA, tech lead) | who does what with which rights | a role only if its work, rights or context differ; same work, different person is one role |

Rules of the mapping:
- A step needs a role only when its actor needs other rights, other instructions or a fresh
  look (an independent check). Otherwise the previous role does it.
- A gate goes before what is hard to undo or leaves the machine, and where only the human
  can decide (`lado-kit-format`, "Gates"). A sign-off that is a formality becomes nothing.
- A loop (review, fix, review) gets `max_visits` and a way to the human.
- What the material says only once and one role needs stays in that role or step.

## The blueprint

Write `BLUEPRINT.md` at the kit repository's root from `${SKILL_DIR}/blueprint-template.md`;
during a run that root is the run's worktree, because the author works there.
All five sections are required; section 5 starts empty for a new kit and gets a row per
change in `improve`. Every element of the
kit appears in section 3 with the requirements it covers; an element with none is cut
before the blueprint goes to the human, or kept with a written reason.
