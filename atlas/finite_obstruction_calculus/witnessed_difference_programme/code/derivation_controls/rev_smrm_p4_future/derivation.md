# REV-SMRM-P4-FUTURE

## Target
Implement **Realizable Future-Distinction Observation Design** (`REV-SMRM-P4-FUTURE`, unblocking 3 downstream nodes in `goal_dag.jsonl`). Using `realizable_observation.core`, `realizable_observation.checker`, and `realizable_observation.replay`, we synthesize minimal-cost realizable observation suites that separate future-divergent state pairs, verify construction optimality against the fixed suite baseline (`fixed_suite_cost`), and validate full replay (`replay`), mapped onto `omega_engine_cognitive_operations`.

## Mathematical Formulation

Let $S$ be a finite state space with future-behavior map $F : S \to \mathcal{B}$ and candidate tests $\mathcal{T}$ with positive costs $c : \mathcal{T} \to \mathbb{Z}_{>0}$.
1. **Future-Distinction Requirement**: Every pair of states $(s, s') \in S \times S$ with distinct future behaviors $F(s) \ne F(s')$ must be separated by at least one selected test $t \in \Sigma \subseteq \mathcal{T}$ ($t(s) \ne t(s')$).
2. **Realizable Synthesis (`construct`)**: Selects a test suite $\Sigma^* \subseteq \mathcal{T}$ minimizing $\sum_{t \in \Sigma} c(t)$ subject to separating all future-divergent pairs, strictly improving on `fixed_suite_cost` when redundant sensors are present.
3. **Construction & Replay Verification (`check_construction`, `replay`)**: Independently verifies pair coverage, cost optimality, coordinate-projection separation (`coordinate_example`), and deterministic bundle replay.

## Verification Summary
- `check_construction` and `replay` pass on the synthesized observation suite.
- The synthesized suite cost is strictly less than `fixed_suite_cost`.
