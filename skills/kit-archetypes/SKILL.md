---
name: kit-archetypes
description: A gallery of nine proven shapes of an agent team for a LADO kit — Solo, Solo + reviewer, feature with design gate, research and report, parallel fan-out, triage, docs and content, incident and ops, bug hunt — each with its roles, flow, when to take it and its complexity. Use when a human starts a kit from scratch, or to check a transferred process against a simpler known shape; for the interview itself use kit-interview.
---

# Kit archetypes

Start from the simplest shape that does the task, and add a part only when a requirement
needs it. Offer **Solo** first, every time, and argue for it; then at most two more that fit
the task. Multi-agent teams cost more tokens and fail in more ways (lost hand-offs, vague
roles, endless loops), so each extra role must buy something the human asked for.

Complexity is worker roles / work steps / gates; the supervisor is not counted.

Never offer a group chat (agents talking freely in one channel) or a swarm without a lead:
they are hard to steer and to stop. Build one only when the human asks for it by name, and
then write the risk into the blueprint.

## 0. Solo — 1 / 1 / 0–1

- **Team**: one worker.
- **Flow**: `work` → (gate `approve`, only before something hard to undo) → end. Or no flow:
  the supervisor hands tasks to the worker directly.
- **Take it when**: one person could do the task in one sitting, a good prompt and the
  right skills are what is missing. The default.
- **Not when**: the human needs an independent check before the result is used.

## 1. Solo + reviewer — 2 / 2 / 1

- **Team**: worker, reviewer (read-only).
- **Flow**: `implement` → `review` (`max_visits: 3`, changes → implement) → gate `approve` → end.
- **Take it when**: mistakes are costly and a fresh look catches them (code, contracts,
  anything merged or shipped).
- **Not when**: the result is checked by a test or a command anyway; then Solo with that
  check in its "done" is enough.

## 2. Feature with design gate — 3 / 3 / 2

- **Team**: designer (or the supervisor designs), implementer, reviewer.
- **Flow**: `design` → gate `design_ok` → `implement` → `review` (loop, `max_visits: 3`) →
  gate `merge_ok` → end.
- **Take it when**: the human wants to agree on the approach before work starts (larger
  changes, architecture, public interfaces).
- **Not when**: tasks are small and their acceptance criteria are known up front; use 1.

## 3. Research and report — 2 / 4 / 1

- **Team**: researcher (several in parallel if parts are independent), writer or
  fact-checker.
- **Flow**: `plan` → gate `scope` (choice) → `research` → `synthesize` → `fact_check` → end.
- **Take it when**: the result is a document built from many sources, and facts must be
  checked against them.
- **Not when**: one source answers the question; use Solo.

## 4. Parallel fan-out — 2 / 4 / 1

- **Team**: worker (one per part, started in parallel), integrator or reviewer.
- **Flow**: `split` → `work` (per part) → `integrate` → `review` → gate `approve` → end.
- **Take it when**: the task splits into parts that share no files and no decisions
  (independent modules, documents, data sets).
- **Not when**: parts share code or context; parallel workers then conflict. Use 1 or 2.

## 5. Triage — 2–3 / 2 / 0–1

- **Team**: triager, one specialist per category (one to two).
- **Flow**: `triage` → `handle` (the specialist for the category) → end; a choice gate only
  when the triager is unsure.
- **Take it when**: many incoming items (issues, tickets, emails) of a few clear kinds,
  each handled differently.
- **Not when**: all items are handled the same way; use Solo.

## 6. Docs and content — 2 / 3 / 2

- **Team**: writer, editor.
- **Flow**: `outline` → gate `outline_ok` → `draft` → `edit` (`max_visits: 2`, changes →
  draft) → gate `publish_ok` → end.
- **Take it when**: text is published under the human's name, and its structure must be
  agreed first.
- **Not when**: internal notes or drafts; use Solo.

## 7. Incident and ops — 2 / 3 / 2

- **Team**: investigator, operator.
- **Flow**: `diagnose` → gate `action` (choice: mitigate, roll back, escalate) → `fix` →
  `verify` → gate `deploy_ok` → end.
- **Take it when**: production is affected and every change to it must be the human's call.
- **Not when**: nothing runs in production; use 8.

## 8. Bug hunt — 2 / 3 / 1

- **Team**: debugger (reproduces and fixes), reviewer.
- **Flow**: `reproduce` → `fix` → `review` (loop, `max_visits: 3`) → gate `merge_ok` → end.
- **Take it when**: the bug must be reproduced by a failing test before it is fixed.
- **Not when**: the cause is already known; use 1.

## Checking a shape

Whatever the shape, before it goes into the blueprint:
- every role has a clear output and its own rights or context, and acts in at least one step;
- every step says when it is done and when each outcome applies;
- an independent check comes before the end when the result is used by others;
- every loop has `max_visits`; at most two gates per flow, each before something hard to
  undo or only the human's call;
- the measures are inside `kit-budget`'s green zone, or the blueprint says why not.
