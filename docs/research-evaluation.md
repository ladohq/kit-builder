# Research: evaluating a kit (2026-10-06)

Layers, cheapest first:
a) Static (free, deterministic): structure + LADO rules (kits.load, flows.py); flow graph:
   unreachable states, work states with no path to end, needs naming a state that can never
   precede, every cycle must contain max_visits or a gate (lado-dev: implement has no limit,
   cycle bounded by review max_visits 3); gate profile; role/flow consistency (role in no
   flow); prompt size (lado-dev supervisor ~1300 words); duplicated paragraphs across roles /
   flow `do`; each work state names done condition and every outcome.
b) LLM review against a rubric: per-criterion verdict + quoted evidence, 3 runs, keep repeated
   findings; candidates for a human, never pass/fail. Rubric: role boundaries; complete
   handoffs (note contents for `needs`); done criteria; built-in independent verification;
   no contradictions (incl. with LADO's own instructions); no duplication; escalation rules;
   loop behaviour on revisits (RESOLVED/STILL OPEN); concision + why; skill descriptions;
   provider neutrality; safety/scope.
c) Scenario runs: fixed tasks in sandbox repo, with-kit vs baseline (previous version or
   `default`), on the same provider/model; assertions first (hidden tests FAIL_TO_PASS /
   PASS_TO_PASS, trajectory: reached done, visits <= N, no flow-set), blind pairwise judge
   only for design quality (mask names). Gates need a scripted, deterministic answerer
   (tau-bench simulated user). Repeat k times: pass@k, pass^k. Refs: Inspect AI, promptfoo,
   LangSmith trajectory evals, Terminal-Bench, SWE-bench.
d) Operational metrics from lado.db: runs ended/cancelled/open, time start->end; visits per
   state, back-edge share, loop-limit gates; gate rejections, flow_set overrides (strongest
   misfit signal), ask_human count, human msgs/run, waiting time, gate open time; failed
   deliveries, `missing` replies, "no note yet" needs, thin note bodies; busy time per role
   (cost proxy; no tokens); attribution to state/role. Trends only, confounded.

From skill-creator take: baseline snapshot per iteration, iteration folders, assertions
drafted during runs, grader critiques assertions, analyst flags non-discriminating /
high-variance assertions, mean±sd + time deltas, blind A/B, human feedback step, improvement
rules (generalise, lean, explain why), description-trigger optimisation (also lead's routing).
Not transferable: run cost (few scenarios/repeats), human gates, branch+trajectory output,
failure attribution (MAST labels), model not pinned (results hold per provider/model),
blindness limited, Claude-only tooling.

Pitfalls: judge bias (swap order, per-criterion evidence, other model family, calibrate);
nondeterminism (epochs, pin sandbox/task/gate answers); small samples (std errors, paired
diffs, regression vs capability scenarios); cost (a->b->c order, c only on 3-5 scenarios);
overfitting (held-out scenarios).
Sources: MAST 2503.13657; Anthropic "Demystifying evals for AI agents"; tau-bench; Zheng 2306.05685;
Miller 2411.00640; Terminal-Bench; Inspect AI; promptfoo; LangSmith trajectory evals.
