# Kit report: <kit> <version>

- Date: <YYYY-MM-DD>
- Kit: <folder>, <how it was found: path given, or `lado kits show <name>`>
- Evaluated by: kit-builder critic (layers a and b)
- Passes: <how the three passes ran>; <n> one-pass findings dropped

Findings are candidates for the human to weigh, not a pass/fail grade.

## Card

| Layer | Result |
|---|---|
| a. `lado kits check` | <OK, or the number of errors>; <n> warnings |
| a. Budget | <overall zone>; <each yellow or red measure with its value> |
| b. Rubric | <n> findings (<h> high, <m> medium, <l> low); <k> of 12 criteria without findings |

### `lado kits check <folder>`

```
<whole output>
```

### Budget script (exit status <n>)

```
<whole output>
```

## Fix first

<!-- At most 5 items, most harmful first. Each: one line, what to change, and the finding
id, budget measure or check error it comes from. -->

1. <...> (F<id>)

## Findings

<!-- One subsection per criterion, all 12, in this order. A criterion without findings
gets one line: what was checked and the quote that shows it is handled, or "Not
applicable" and why. Finding format: see the kit-rubric skill. -->

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

<!-- Only on a later visit: each finding of the previous report, RESOLVED or STILL OPEN,
with the quote or output that shows it. Otherwise delete this section. -->

## Questions for the human

<!-- Decisions only the human can make, numbered, each with a recommended answer. Delete
the section when there are none. -->

## Found on the way

<!-- Problems outside the kit, such as LADO itself (mark them `[lado]`). Delete the section
when there are none. -->
