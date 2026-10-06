---
name: kit-rubric
description: Rubric for reviewing the text of a LADO kit — 12 criteria with what counts as a violation, the finding format with a quote, the three-pass rule and the report template. Use when evaluating a kit's roles, flows and skills after `lado kits check` and the budget script, or when writing or re-checking a kit report.
---

# Kit rubric

The static checks (`lado kits check`, the `kit-budget` script) count and prove what can be
counted. This rubric covers what only reading shows: whether the roles, steps and skills
will make agents do the right thing. Its findings are candidates for the human, never a
pass/fail grade.

## Three passes

An LLM review varies from run to run; a finding that shows up once may be noise. So:

1. Make three passes over the whole kit, each covering all 12 criteria. Start each pass
   from a different place (pass 1: kit.yaml and the roles; pass 2: the flows, step by
   step; pass 3: the skills, then back to the roles), and write down each pass's findings
   before the next pass begins, without copying from the earlier lists. If you can start
   independent sub-agents, give each pass to a fresh one with this skill and the kit
   folder only.
2. Two findings are the same when they name the same criterion and the same place (file
   and line, or state) for the same reason.
3. The report keeps only findings seen in at least two of the three passes, with their
   count ("passes: 2/3"). Say in the report how the passes ran and how many one-pass
   findings were dropped.

## Finding format

```markdown
- **F<criterion>.<n>** [high | medium | low] `<file>:<line>` (state `<state>` for a flow)
  > <exact quote>
  <What is wrong and what it makes an agent do, in one or two sentences.>
  Fix: <the smallest change that removes it.> Passes: <2/3 | 3/3>
```

- `<file>` is relative to the kit folder.
- The quote is copied word for word: one line, or a few consecutive lines each copied
  whole. Before writing the report, search each quoted line in its file (for example
  `grep -nF '<line>' <file>`) and correct the line number; a quote that is not found is
  fixed or dropped.
- Impact: **high**: a run can go wrong, loop, lose work or do something hard to undo;
  **medium**: agents will act differently from run to run or waste a step; **low**:
  wording or length.

A criterion with no finding gets one line: what you checked and, where the kit has one,
the quote that shows it is handled. "Not applicable" when the kit has nothing it applies
to (for example criterion 8 for a kit without loops).

## The 12 criteria

**1. Role boundaries.** Each role says what it does and what it leaves to others; its
rights (read-only, writes where, commits, merges) are stated.
Violation: two roles own the same action; a role does what another role owns; a
read-only role is told to write or commit; a role's rights are not stated.

**2. Handoffs between steps.** A step gets the previous step's note and the notes of the
states in its `needs`, nothing else; after a gate, the previous note also carries the note
that led to the gate (`lado-kit-format`). The step that produces a note says what goes
into it.
Violation: a step works from something ("the design", "the plan") that is neither in the
previous note nor in a `needs` state; a `do` does not say what its note holds; a note a
later step needs is allowed to say "as above" or "see the chat".

**3. Done and outcomes.** Each work state's `do` says when the step is done and the
condition for each outcome.
Violation: a `do` without a done condition; an outcome with no condition for choosing it;
two outcomes whose conditions overlap.

**4. Independent verification.** Before a flow ends or does something hard to undo,
someone other than the author checks the work: another role or a human gate that shows the
evidence.
Violation: the only check is the author's own; a review step can be skipped; a gate asks
the human to approve without showing what to approve (`needs`).

**5. Contradictions.** Instructions can all be followed at once: within a role, between a
role and a step's `do`, between two roles, and with LADO's own instructions to agents
(outcomes are reported with `flow_advance`, gates are the human's, only the lead talks to
the human unless the kit says otherwise).
Violation: two instructions that cannot both hold; a role telling an agent to answer a
gate, to skip `flow_advance` in a run, or to do what LADO does itself.

**6. Duplication.** One rule, one place: the role if it holds in every step, the `do` if
it belongs to one step, a skill if several roles need it. The budget script lists
paragraphs that match word for word; this criterion covers the same meaning in other
words.
Violation: a rule restated in two roles, in a role and a `do`, or in two `do`s, beyond a
short pointer to its one place; two copies that already differ.

**7. When to call the human.** The kit says which decisions are the human's and how they
reach the human (a gate, the lead, a question in the note), and what an agent does when
blocked.
Violation: a decision only the human can make with no path to the human; a worker told
to ask the human directly when the lead holds that conversation; no rule for being
blocked or for a review loop that does not converge.

**8. Loops on a later visit.** A state that a flow can enter again says what changes on
the later visit; a reviewing state on a loop needs itself and marks its previous findings
RESOLVED or STILL OPEN; a work state on a loop whose note a gate or a later step needs
needs itself and writes that note whole on every visit (`lado-kit-format`, "Notes and
`needs`"); the loop is bounded (`max_visits` or a gate).
Violation: a looping `do` silent about later visits; a reviewer on a loop without its own
state in `needs`; a needed work state on a loop without itself in `needs`, or whose later
note lists only the fixes; the fixing step not told where the findings to fix are.

**9. Concision and why.** Every sentence changes what an agent does; a rule an agent
might break carries its reason.
Violation: a sentence an agent obeys by default (a no-op); filler, history or exposition
in a prompt; a non-obvious rule without its why; a prompt over its word budget through
restatement.

**10. Skill descriptions.** Each own skill's `description` says what it holds and when to
use it, and how it differs from a neighbour that could be confused with it; each skill a
role lists is one the role needs.
Violation: a description without "when"; two skills whose descriptions trigger on the
same case; a skill in a role's `skills:` that nothing in the role or its steps calls for;
a skill's text pasted into a prompt instead of listed.

**11. Provider neutrality.** The kit runs under any agent CLI LADO supports (see
`lado-kit-format`).
Violation: one CLI's tool names, slash commands, model names or config files; a path to a
kit file not through `${KIT_DIR}` / `${SKILL_DIR}`; an instruction that only one CLI can
follow. LADO's own tools (`flow_advance`, `send_message`, `spawn_worker`) are neutral.

**12. Safety and scope.** Nothing hard to undo or leaving the machine (merge to main,
push, tag, publish, delete, a paid run, a message outside the session) happens without a
gate or the human's explicit yes; each role knows the limits of its task.
Violation: such an action with no gate or yes before it; a destructive command without
its condition; a role invited to change things outside its task.

When the kit has a `BLUEPRINT.md`, also list under "Not traced" each role, step, gate,
skill or MCP server that no requirement R names, and each yellow or red budget measure
the blueprint does not justify.

## Report

The report is one file, `kit-reports/<kit>-<version>-<YYYY-MM-DD>.md` at the root of the
repository you work in, with the kit's `name` and `version` from its `kit.yaml`. Copy the
template `${SKILL_DIR}/report-template.md` and fill every section; delete only the lines
its comments say may go. "Fix first" holds at most 5 items: the highest-impact
findings, a red budget measure, an error of `lado kits check`, each pointing to its
finding id.
