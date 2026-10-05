# Research: archetypes of agent teams (2026-10-06)

No single standard catalogue. De facto common ground: Anthropic "Building effective agents"
(chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer), Azure AI agent
orchestration patterns (sequential, concurrent, group chat/maker-checker, handoff, magentic;
complexity ladder), Google ADK multi-agent patterns (most complete list), LangGraph
(supervisor, hierarchical, swarm), OpenAI practical guide (single agent first; manager vs
handoffs; HITL on failure thresholds / high-risk actions), CrewAI, MetaGPT/ChatDev (SOP roles),
surveys 2402.01680, 2501.06322, MAST 2503.13657 (14 failure modes), Cognition "Don't build
multi-agents". Anthropic/OpenAI/LangGraph/CrewAI URLs not re-fetched: verify before citing.

Consensus set: single agent with tools; sequential; routing; parallel fan-out/gather;
orchestrator-workers; evaluator-optimizer (maker-checker); handoff (hard to control); HITL.

Gallery (worker roles / work states / gates):
1. Solo + reviewer: implement -> review (loop, max 3) -> approve. 2/2/1
2. Feature pipeline with design gate: design -> gate -> implement -> review -> gate. 3/3/2
3. Research and report: plan -> scope choice gate -> research fan-out -> synthesize -> fact-check. 2/4/1
4. Parallel fan-out: split -> parallel items -> integrate -> review -> gate (only independent parts). 2/4/1
5. Triage / routing: triage -> specialist per category; gate on low confidence. 2-3/2/0-1
6. Docs / content: outline -> gate -> draft -> edit (loop 2) -> publish gate. 2/3/2
7. Ops / incident: diagnose -> choice gate (mitigate/rollback/escalate) -> fix -> verify -> deploy gate. 2/3/2
8. Bug hunt: reproduce -> fix -> review (loop) -> gate. 2/3/1
9. Solo baseline: lead + one worker, no flow or one state + gate. 1/1/0-1 — default to argue for first.

Pitfalls to check: over-engineering (start simplest, add by measurement); token cost (~15x
for multi-agent research); split shared-context coding work; MAST coordination failures
(crisp output contract per role, done criterion per state, verifier before end, max_visits on
loops); vague/overlapping roles, role in no flow, state without clear outcome; unbounded
loops; HITL only on irreversible actions (<=2 gates per flow heuristic, approval fatigue);
avoid group chat/swarm unless asked; every step reports a note.
