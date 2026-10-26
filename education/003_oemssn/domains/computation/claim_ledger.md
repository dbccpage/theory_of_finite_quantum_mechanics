# Claim Ledger for Theoretical Computer Science & Automata Theory

**Domain Key:** `computation`  
**AuthorityEffect:** `None`  

| coverage_id | operation | disposition | admitted_steps | basis | what_does_not_follow |
| --- | --- | :---: | :---: | --- | --- |
| `cov_computation_create_structure` | `create_structure` | `admitted` | `2, 4, 6, 8, 10, 12, 14, 16` | Scaffolds constructive computation distinctions and relational complexes. | Does not imply universal empirical truth or unproved continuity. |
| `cov_computation_remove_obstruction` | `remove_obstruction` | `admitted` | `3, 5, 7, 9, 11, 13, 15` | Discharges active structural constraints, deadlock, and symmetry ambiguities. | Does not eliminate fundamental recovery gaps or unproved conjectures. |
| `cov_computation_wir_prenatal_transposition` | `prenatal_transposition_antisymmetry` | `admitted` | `1-5` | Root W irreflexive setting (X, R, a, b), transposition operator sigma(a, b) = (b, a), oriented 1-chain boundary sign flip partial_1(sigma(e)) = -partial_1(e), tie-retention dual-branch tracking [branch_D2, branch_S2], and exact integer matrix boundary nilpotency B_1 B_2 = 0. | Does not imply continuous tape space or physical quantum computation without discrete mapping. |
| `cov_computation_fuel_bounded_turing` | `turing_execution_and_cycle_detection` | `admitted` | `6-16` | Discrete deterministic Turing machine execution and Graph Reduction Monad under strict fuel budgets, certified step receipts, Floyd/hash periodic cycle detection, and HaltingObstruction generation. | Does not solve the general Turing halting problem or circumvent Rice's theorem; holds strictly within declared fuel bounds. |
| `cov_computation_simplicial_boundary_nilpotency` | `boundary_closure_nilpotency` | `admitted` | `7` | Exact integer simplicial boundary matrices B_1 and B_2 with verified vanishing product B_1 * B_2 = 0 on computational state complex triangles. | Does not derive smooth Riemannian manifolds or continuous differential equations. |

## Verification Status
- Scenario Schema: Strictly validated (16 steps with 14-field specification).
- Code Tests: Pytest unit suite passing (19/19 tests passing in 4_computation/tests).
- Formal Model: Lean 4 kernel checked under `{propext, Quot.sound}` (`computation_core.lean`).
