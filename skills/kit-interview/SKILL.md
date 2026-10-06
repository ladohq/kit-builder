---
name: kit-interview
description: How to interview a human about the LADO kit they need — the two branches (transfer an existing process, or start from scratch), a question bank, the round format, how to turn their material (CLAUDE.md, their skills, a process description, tracker statuses) into roles, steps and gates, and the BLUEPRINT.md template. Use when designing a new kit; for choosing among ready team shapes use kit-archetypes, for the kit file format use lado-kit-format.
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

The first question is always: "Do you already have a process you want to bring over?"

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
All five sections are required; section 5 starts empty for a new kit. Every element of the
kit appears in section 3 with the requirements it covers; an element with none is cut
before the blueprint goes to the human, or kept with a written reason.
