---
name: kit-rubric
description: Rubric for reviewing the text of a LADO kit — 12 criteria with what counts as a violation, known holes checked by name, reading dependency skills, the finding format with a quote, the three-pass rule, re-evaluation against a previous report, the verdict and stop rule, and the report template. Use when evaluating a kit's roles, flows and skills after `lado kits check` and the budget script, when writing or re-checking a kit report, or when fixing or weighing findings named by criterion.
---

# Kit rubric

The static checks (`lado kits check`, the `kit-budget` script) count and prove what can be
counted. This rubric covers what only reading shows: whether the roles, steps and skills
will make agents do the right thing. Its findings are candidates for the human, never a
pass/fail grade: each carries the quote that shows it, so the human can judge it without
trusting the critic.

## Three passes

An LLM review varies from run to run; a finding that shows up once may be noise. So:

1. Make three passes over the whole kit, each covering all 12 criteria and every known
   hole (below), and each reading the dependency skills (below) as well as the kit's own
   text. Start each pass from a different place (pass 1: kit.yaml and the roles; pass 2:
   the flows, step by step; pass 3: the skills, then back to the roles), and write down
   each pass's findings before the next pass begins, without copying from the earlier
   lists. If you can start independent sub-agents, give each pass to a fresh one with this
   skill, the kit folder and the dependency skills' folders only.
2. Two findings are the same when they name the same place (file and line, or state) for
   the same reason. When passes give one finding different impacts or criteria, take the
   higher impact and the criterion closest to the fix, and say so in the finding.
3. The report keeps findings seen in at least two of the three passes, with their count
   ("Passes: 2/3"). A finding seen in one pass stays only when you confirm it in the files
   yourself: its quote is there, and the files or `git` show the harm it names, not just
   reasoning about it. Mark it "Passes: 1/3, confirmed" and put that evidence (a second
   quote or the command output) into the finding: it rests on one pass and your check, so
   the human weighs it with less confidence and sees what confirmed it. Drop the other
   one-pass findings; a real one lost to the vote costs the human more than one marked as
   less certain.
   Say in the report how the passes ran, how many one-pass findings were dropped and how
   many were kept as confirmed.

## Dependency skills

A role does what the skills it lists tell it, so a skill from `dependencies.skills` is
part of the role's text: a pass that skips it misses what it makes the role do. Read the
`SKILL.md` of each one a role lists, and the files it points to. For an installed kit,
`lado kits show <kit>` prints each skill's folder under "Skills:", after the last ": ".
For a kit given as a folder, the pack's clone is in LADO's git cache once the kit was
checked or installed: the folder `cache` of LADO's home (`$LADO_HOME`, by default `.lado`
in your home folder), as `<repository name>-<hash>`, then the `<ref>` after the `@` of the
pack's `from`. The skill is in one of the `folders` its `dependencies.skills` entry
names. A skill from `expects.skills` is part of the role's text too: read it in the kit the
README names as bringing it, through `lado kits show <that kit>` when it is installed. A
dependency or expected skill you cannot find: say so under "Passes" and in criterion 10.

## Known holes

Holes that earlier reviews missed on some runs and found on others. Every pass checks each
one by name; the report's "Known holes" table gives, for each, the finding id or the quote
that shows the kit handles it.

1. A red check (tests, build, `lado kits check`, a merge) sent back to the author as a bug
   in the work, with no step telling a fault of the work from one of the environment
   (a missing tool, the network, a dirty worktree). Criterion 3.
2. Work outside a flow: a role told to make or merge changes, or run read-only work, with
   no run around it; a merge with no gate or human yes before it. Criteria 4, 12.
3. A path to a file outside the run's worktree: the main checkout, a home folder, a
   relative path that means something else in the worktree. Criteria 11, 12.
4. A reviewer's verdict with no severity threshold: nothing says which level of finding
   blocks and which does not. Criterion 3.
5. A dependency skill that writes files, commits or asks the user, listed on a role that
   must not (a read-only role, a worker when only the lead talks to the human).
   Criteria 1, 5.
6. Commands out of step with `expects.commands` (`lado-kit-format`, "Commands from outside
   the kit"); the `expects …` lines of `lado kits check` list what the kit declares:
   (a) a command the kit's roles or skills always run, or its README requires, that
   `expects.commands` lacks (sdlc 0.1.1 with `openspec`), criterion 10; (b) a command in `expects.commands` that only some projects need
   (`gh` when the code host comes from the project's settings): every other project gets a
   false start error, criterion 11; (c) `expects.commands` with `dependencies.lado` below
   `">=0.30"`, criterion 10.

## Finding format

```markdown
- **F<criterion>.<n>** [high | medium | low] `<file>:<line>` (state `<state>` for a flow)
  > <exact quote>
  <What is wrong and what it makes an agent do, in one or two sentences.>
  Fix: <the smallest change that removes it.> Passes: <2/3 | 3/3 | 1/3, confirmed | full pass, confirmed | cut-rule check>
```

- `<file>` is relative to the kit folder.
- The quote is copied word for word: one line, or a few consecutive lines each copied
  whole. Before writing the report, search each quoted line in its file (for example
  `grep -nF '<line>' <file>`) and correct the line number; a quote that is not found is
  fixed or dropped. A lost rule ("Re-evaluation") quotes the removed line as `git diff`
  shows it, with its file and line at the base commit.
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

**2. Handoffs between steps.** A step works from the previous step's note, the artifacts
attached to it and the artifacts its `reads` names, nothing else; after a gate, the note
also carries the note that led to the gate (`lado-kit-format`, "Artifacts"). A result a
later step or the human reads is an artifact in its state's `produces`, not the text of a
note and not a path; the state that produces it says what it holds.
Violation: a step works from something ("the design", "the plan") that is neither in the
previous note nor in its `reads`; a result a later step or a gate needs handed on as note
text, "as above", "see the chat" or a local path; a `do` silent on what its artifact
holds, or on what it holds for an outcome without a result. A flow with `needs` does not
load in LADO 0.27 or newer: a high finding, fix: replace `needs` with `reads` of the artifacts the
step works from, and name them in `produces` of the states that write them.

**3. Done and outcomes.** Each work state's `do` says when the step is done and the
condition for each outcome.
Violation: a `do` without a done condition; an outcome with no condition for choosing it;
two outcomes whose conditions overlap.

**4. Independent verification.** Before a flow ends or does something hard to undo,
someone other than the author checks the work: another role or a human gate that shows the
evidence.
Violation: the only check is the author's own; a review step can be skipped; a gate asks
the human to approve what it does not show: an artifact missing from its `reads`.

**5. Contradictions.** Instructions can all be followed at once: within a role, between a
role and a step's `do`, between two roles, and with LADO's own instructions to agents
(outcomes are reported with `flow_advance`, gates are the human's, only the lead talks to
the human unless the kit says otherwise).
Violation: two instructions that cannot both hold; a role telling an agent to answer a
gate, to skip `flow_advance` in a run, or to do what LADO does itself.

**6. Duplication.** One rule, one place: the role if it holds in every step, the `do` if
it belongs to one step, a skill if several roles need it. The budget script lists
pairs of paragraphs that share 55% or more of their content words; this criterion covers
repeats it misses: a rule restated inside a longer paragraph or in other words.
Violation: a rule restated in two roles, in a role and a `do`, or in two `do`s, beyond a
short pointer to its one place; two copies that already differ.

**7. When to call the human.** The kit says which decisions are the human's and how they
reach the human (a gate, the lead, a question in the note), and what an agent does when
blocked.
Violation: a decision only the human can make with no path to the human; a worker told
to ask the human directly when the lead holds that conversation; no rule for being
blocked or for a review loop that does not converge.

**8. Loops on a later visit.** A state that a flow can enter again says what changes on
the later visit; a reviewing state on a loop has its review in `produces` and on a later
visit marks its previous findings RESOLVED or STILL OPEN; a work state on a loop writes its
artifact whole on every visit (`lado-kit-format`, "Artifacts"); the loop is bounded
(`max_visits` or a gate).
Violation: a looping `do` silent about later visits; a reviewer on a loop without its own
artifact in `produces`; a work state on a loop whose later artifact lists only the fixes;
the fixing step not told where the findings to fix are.

**9. Concision and why.** Every sentence changes what an agent does; a rule an agent
might break carries its reason.
Violation: a sentence an agent obeys by default (a no-op); filler, history or exposition
in a prompt; a non-obvious rule without its why; a prompt over its word budget through
restatement.

**10. Skill descriptions.** Each own skill's `description` says what it holds and when to
use it, and how it differs from a neighbour that could be confused with it; each skill a
role lists is one the role needs.
Violation: a description without "when"; two skills whose descriptions trigger on the
same case; a skill in a role's `skills:` that nothing in the role or its steps calls for; a skill
from outside the kit not declared by its own folder, or a declared folder no role uses
(`lado-kit-format`);
a skill in `expects.skills` whose kit the README does not name, one that is in fact
published as a package (it belongs in `dependencies.skills`), or `expects.skills` with
`dependencies.lado` below `">=0.29"` (`lado-kit-format`, "Skills from outside the kit");
a skill's text pasted into a prompt instead of listed. A role's skill that no kit declares
(a skill of another kit missing from `expects.skills`) is `lado kits check`'s to report,
not yours to check by hand: quote its line (`skill "<name>" is not visible to agent
"<role>"`) as the finding's evidence.

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
skill or MCP server that no requirement R names, each yellow or red budget measure
the blueprint does not justify, and each difference the flow script's `--compare` prints
between the flows and the blueprint's skeletons: the kit drifted from what the human
approved, or the blueprint was not updated; a difference blocks `approved` ("Verdict"). A
blueprint without skeletons: say so there.

## Re-evaluation

Use it when there is a previous report of this kit (the critic's role says when). Fresh
passes over the whole kit find new small things on every round, many of them there from
the start, and the human cannot tell when to stop; so review the change, not the kit again.

1. The kit's text is `kit.yaml`, `README.md`, `BLUEPRINT.md`, `agents/`, `flows/` and
   `skills/`; other files of the repository (`kit-reports/`, `BACKLOG.md`, `docs/`,
   `tests/`) are not part of the change. The base is the commit the change starts from, so
   that text the run itself wrote is never "Missed earlier". In `create` the whole kit is
   new: all its text counts as changed, and the check of cut rules (3) uses the diff from
   the previous report's commit. In `improve` the base is the commit the plan names for
   its report, on every visit. Otherwise it is the commit in the previous report's header
   ("Commit:", or "(commit …)" in its "Kit:" line); without one, the parent of the commit
   that added the report (`git log --diff-filter=A -1 --format=%H -- <report>`, then
   `<that>^`). The change is `git diff <base> -- kit.yaml README.md BLUEPRINT.md agents
   flows skills` in the kit folder. When the folder is not a git repository, evaluate in
   full and say why under "Passes".
2. Mark each finding of the previous report, and each finding and change the plan lists,
   RESOLVED or STILL OPEN, with the quote or command output that shows it; check the
   author's fixed / not fixed list against the files. A finding keeps its section: a STILL
   OPEN one from "Missed earlier" stays there, the others stay findings.
3. Check every rule in a removed line of the diff: find where it is now, starting from the
   author's table "cut → where the rule is now", and check that this place holds the rule
   itself, not only its topic. Compare by paragraph (`git diff --word-diff`): rewrapping
   moves lines that lose nothing. A rule found nowhere is lost: a finding under the
   criterion it served, "Passes: cut-rule check", with its impact by what agents may do
   without it. Shortening text is where rules go missing, and the author's own check is
   the one that missed them. You do it after the passes; with sub-agents, a fourth one
   gets `git diff --word-diff` and the author's table.
4. Make the three passes over the changed text and its surroundings only: the section of a
   role or skill, or the flow state, that holds a change, and the places the changed text
   points to or that point to it. Each pass still covers all 12 criteria and the known
   holes; a sub-agent for a pass also gets the diff.
5. In a step that asks for a verdict, once the three passes leave no blocking finding
   ("Verdict"), make one full pass before you report `approved`: all 12 criteria and the
   known holes over the whole of every file the diff touches, not only its changed
   sections. A re-evaluation reads only the change, so what the first assessment missed is
   never looked for again without it. Confirm each of its findings in the files as a
   one-pass finding is confirmed ("Passes: full pass, confirmed"). In `create` all the
   text is changed, so the three passes already were full: skip it.
6. A new finding (in neither the previous report nor the plan) in text the diff does not
   touch was missed by an earlier round, not caused by this change: list it under "Missed
   earlier", in the same format, the full pass's included. It does not block a verdict and
   does not count for the stop rule.

## Verdict

This is the one rule for a step that asks for a verdict (the critic's `evaluate` in
`create` and `improve`). `approved` when `lado kits check` has no error, no budget measure
is red, every yellow measure is justified in the blueprint, the flow script's `--compare`
prints no difference and no high finding is open; otherwise `changes`. Medium and low
findings, findings under "Missed earlier" and those the plan leaves with the human's
reason ("Left by the plan") do not block. A pair of similar paragraphs the budget script
lists is not a measure: it is a finding under criterion 6, and its impact decides.
A check that fails for a cause outside the kit's files gives no verdict either way
(`lado-kit-format`, "When a check or command fails").

Stop rule, in a re-evaluation: no high and no medium finding in the changed text, lost
rules included. It is advice for the human at the release gate, not a block: a report can
be `approved` with the stop rule not met, and the card's row "Stop rule" says so. When it
holds, another round would mostly find what earlier rounds missed, and what is left is the
human's to weigh.

## Report

The report is one file, `kit-reports/<kit>-<version>-<YYYY-MM-DD>.md` at the root of the
repository you work in, with the kit's `name` and `version` from its `kit.yaml`; in
`improve`, after `assess`, the planned version the plan names, so the report before the
change and the one after it are different files. Its flow
diagrams go into the folder of the same name without `.md`, one `<flow>.svg` per flow,
drawn by the `kit-budget` flow script with `--out`. Copy the
template `${SKILL_DIR}/report-template.md` and fill every section; delete only the lines
its comments say may go. "Fix first" holds at most 5 items: the highest-impact
findings, a red budget measure, an error of `lado kits check`, each pointing to its
finding id.

Write the report in the language the step asks for its notes (the run's human language),
or else the language of the task: the human reads both. The template's English does not
set the language; translate its headings, and keep finding ids, levels, RESOLVED / STILL
OPEN and quotes as they are.
