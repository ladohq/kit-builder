# Blueprint: <kit name>

<One paragraph: what the kit is for and who uses it.>

## 1. Requirements

What the human wants from the kit, in their words, then what the interview made precise.
Each one is checkable: someone can say whether the kit meets it.

- **R1** <requirement>. *Source:* <interview round, or file and section of the material>.
- **R2** ...

## 2. Starting point

Either the archetype (name from `kit-archetypes`, and what was changed and why), or the
transferred process: its steps, owners and sign-offs as the human described them, with
the source of each.

## 3. Traceability

Every part of the kit, and the requirements it covers. A part without a requirement is a
candidate for removal; keep it only with a reason in the last column.

| Element | Kind | Covers | Why it exists / why nothing simpler |
|---|---|---|---|
| `supervisor` | role (lead) | R1 | <...> |
| `<role>` | role | R2, R3 | <...> |
| `<flow>` | flow | R1 | <...> |
| `<flow>.<state>` | work step | R2 | <...> |
| `<flow>.<gate>` | gate | R4 | <what is irreversible or only the human's call> |
| `<skill>` | skill | R3 | <...> |
| `<server>` | MCP server | R5 | <...> |

Then the reverse check, one line per requirement: which elements cover it. A requirement
no element covers is a gap.

## 4. Complexity budget

The measures from `kit-budget`, planned (counted by hand) at design and replaced by the
script's output after the kit is built.

| Measure | Value | Zone | Reason, when not green |
|---|---|---|---|
| Worker roles (not supervisor) | | | |
| Work steps in `<flow>` | | | |
| Gates in `<flow>` | | | |
| Words in the longest role prompt | | | |
| Own skills | | | |
| MCP servers | | | |

Each yellow or red measure names the requirement that needs it and why a simpler shape
does not work.

## 5. Change log

How the kit changed and the fact that caused it, newest first. Empty for a new kit.

| Date | Version | Change | ← Fact (session, run, metric or report) |
|---|---|---|---|
