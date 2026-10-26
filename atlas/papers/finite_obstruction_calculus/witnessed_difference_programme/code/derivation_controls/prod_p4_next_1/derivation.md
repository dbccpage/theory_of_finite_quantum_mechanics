# PROD-P4-NEXT-1

Goal id: PROD-P4-NEXT-1

Selected scope for PROD-P4-NEXT-1 is recorded in this note.

## Selected scope

`WdpObservationPlanner` (`omega_engine_applications/wdp_products/p4_observation_budget/adapter.py`) implementing the `ObservationPlanner` protocol (`omega_engine_applications/wdp_products/p4_observation_budget/contracts.py`) over `finite_observation.solver.solve`, `finite_observation.solver.verify`, and `finite_observation.solver.unresolved_pairs` (`GEN-WDP-46`, `GEN-WDP-47`), plus `plan_distinct_image_shelf` over `observer_completion.distinct_image` (`WDP-DIM-1`), verified in `omega_engine_applications/tests/test_p4_adapter.py`.

## Hypotheses

H1. For a finite state carrier $X$, visible map $v : X \to Y$, query map $q : X \to Q$, and priced instruments $\{(I_k, c_k)\}_{k=1}^m$ with $c_k \in \mathbb{Q}_{>0}$, the unresolved pair set is $U = \{(x, y) : v(x) = v(y) \land q(x) \ne q(y)\}$ (`finite_observation.solver.unresolved_pairs`).

H2. A fixed suite $S \subseteq \{1, \dots, m\}$ is sufficient when for every $(x, y) \in U$ there exists $k \in S$ with $I_k(x) \ne I_k(y)$, and its exact cost is $\sum_{k \in S} c_k$ (`GEN-WDP-47`).

H3. When no instrument separates some $(x, y) \in U$, the menu is infeasible and the planner returns `SuiteVerdict(feasible=False, suite=(), cost=None, unresolved_pairs=...)` naming the unseparated pairs.

## Derivation

1. **Optimal sufficient suite (`WdpObservationPlanner.plan`)**:
   - Constructs a validated `finite_observation.solver.Instance`, runs `solve(instance)`, and replays the certificate via `verify(instance, cert)`.
   - On the three-state test shelf (`I_all_expensive` at cost `5`, `I_pair01` at cost `3/2`, `I_pair12` at cost `2`), selects `("I_pair01", "I_pair12")` with exact cost `"7/2" < "5"`.

2. **Infeasibility & independent verification (`WdpObservationPlanner.verify`)**:
   - When `I_partial` fails to separate `("s1", "s2")`, `plan` returns `SuiteVerdict(feasible=False, unresolved_pairs=(("s1", "s2"),))`.
   - `verify` accepts the optimal verdict and rejects suboptimal (`cost="5"`) or tampered verdicts.

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not claim evaluator self-witnessing or injectivity outside the declared carrier (`WDP-CH14-N01`, `WDP-CH14-N02`).
