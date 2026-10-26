# PROD-P4-KILL

Goal id: PROD-P4-KILL

Selected scope for PROD-P4-KILL is recorded in this note.

## Selected scope

Pilot instrument-menu kill-condition evaluation over `finite_observation.solver` (`solve`, `verify`), `finite_observation.replay_examples`, and `WdpObservationPlanner` in `omega_engine_applications/tests/test_wave1_derivations_and_architecture.py`.

## Hypotheses

H1. The P4 kill conditions (`omega_engine_applications/wdp_products/p4_observation_budget/frame.yaml`) are:
1. *"Pilot menus exceed what the exact solver finishes on."*
2. *"The planned suite never differs from what the buyer already uses."*

H2. Under `GEN-WDP-46`, `GEN-WDP-47`, and `WDP-DIM-1`, the exact solver computes and independently replays the minimum-cost sufficient suite on declared finite instrument menus.

## Derivation

1. **Kill Condition 1 (`kill_exceeds_solver_capacity = False`)**:
   - Across all 5 canonical `finite_observation.replay_examples` fixtures and the 3-instrument pilot menu (`I_buyer_monolithic` at price `5`, `I_pair01` at price `3/2`, `I_pair12` at price `2`), `solve` and `verify` finish deterministically in exact rational arithmetic.
2. **Kill Condition 2 (`kill_never_differs_from_buyer = False`)**:
   - Whereas the buyer baseline runs the monolithic probe `("I_buyer_monolithic",)` at cost `5` (or the full menu at cost `17/2`), the planner selects `("I_pair01", "I_pair12")` at exact minimum cost `7/2 < 5`, verified by `WdpObservationPlanner.verify`.

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not claim polynomial-time scaling on arbitrary combinatorial menus outside declared finite budgets.
