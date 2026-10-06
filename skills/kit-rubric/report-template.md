# Kit report: <kit> <version>

- Date: <YYYY-MM-DD>
- Kit: <folder>, <how it was found: path given, or `lado kits show <name>`>
- Commit: <the commit evaluated, or "not a git repository">
- Evaluated by: kit-builder critic (layers a and b)
- Mode: <full, or re-evaluation against <previous report>, `git diff <base>`>
- Passes: <how the three passes ran>; <n> one-pass findings dropped, <k> kept as confirmed

Findings are candidates for the human to weigh, not a pass/fail grade.

## Card

| Layer | Result |
|---|---|
| a. `lado kits check` | <OK, or the number of errors>; <n> warnings |
| a. Budget | <overall zone>; <each yellow or red measure with its value> |
| b. Rubric | <n> findings (<h> high, <m> medium, <l> low); <k> of 12 criteria without findings |
| Stop rule | <re-evaluation only: holds, or not: <h> high and <m> medium in the changed text; delete the row in a full evaluation> |

### `lado kits check <folder>`

```
<whole output>
```

### Budget script (exit status <n>)

```
<whole output>
```

## Fix first

<!-- Most harmful first, as kit-rubric says. Each: one line, what to change, and the
finding id, budget measure or check error it comes from. -->

1. <...> (F<id>)

## Findings

<!-- One subsection per criterion, all 12, in this order. A criterion without findings
gets one line: what was checked and the quote that shows it is handled, or "Not
applicable" and why. Finding format: see the kit-rubric skill. In a re-evaluation,
only findings in the changed text, lost rules included. -->

### 1. Role boundaries

### 2. Handoffs between steps

### 3. Done and outcomes

### 4. Independent verification

### 5. Contradictions

### 6. Duplication

### 7. When to call the human

### 8. Loops on a later visit

### 9. Concision and why

### 10. Skill descriptions

### 11. Provider neutrality

### 12. Safety and scope

## Not traced

<!-- Only when the kit has BLUEPRINT.md: elements no requirement names, and yellow or red
measures it does not justify. Otherwise delete this section. -->

## Previous findings

<!-- Re-evaluation only (kit-rubric, "Re-evaluation"), as are the next two sections; in a
full evaluation delete all three. Each finding of the previous report, RESOLVED or STILL
OPEN, with the quote or output that shows it. -->

## Cut rules

<!-- Each rule in a removed line of the diff: where it is now (file:line), or "lost" with
the finding id. "None removed" when the diff removes no rule. -->

| Removed rule (file:line at base) | Where it is now |
|---|---|

## Missed earlier

<!-- Findings in text the diff does not touch, in the finding format. They do not block a
verdict. "None" when there are none. -->

## Left by the plan

<!-- improve only: findings the plan leaves, each with the human's reason from the plan.
Otherwise delete this section. -->

## Questions for the human

<!-- Decisions only the human can make, numbered, each with a recommended answer. Delete
the section when there are none. -->

## Found on the way

<!-- Problems outside the kit, such as LADO itself (mark them `[lado]`). Delete the section
when there are none. -->
