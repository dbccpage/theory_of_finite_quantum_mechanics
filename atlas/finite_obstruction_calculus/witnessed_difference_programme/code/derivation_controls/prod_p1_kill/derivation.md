# PROD-P1-KILL

Goal id: PROD-P1-KILL

Selected scope for PROD-P1-KILL is recorded in this note.

## Selected scope

Pilot P1 kill-condition evaluator (`evaluate_pilot_p1_kill_conditions`, `operator_decision_for_label`) in `omega_engine_applications/wdp_products/p1_abstention_governor/adapter.py` and verification in `omega_engine_applications/tests/test_p1_p2_adapters.py`.

## Hypotheses

H1. The P1 kill conditions (`omega_engine_applications/wdp_products/p1_abstention_governor/frame.yaml`) are:
1. *"Arenas for real tasks exceed the solver's practical size."*
2. *"Labels do not change any operator decision in a pilot."*
3. *"A LOSS certificate cannot be produced on real agent rollouts."*

## Derivation

1. **Practical size (`kill_exceeds_practical_size = False`)**: The pilot arena has 4 states ($\le 64$).
2. **Operator decision differentiation (`kill_labels_do_not_change_decision = False`)**: `ResolvedWithinBudget`, `Exhausted`, and `LosingInDeclaredArena` map to three distinct operator decisions (`proceed_to_emit`, `request_budget_or_prune`, `halt_and_escalate_arena_revision`).
3. **LOSS certificate verification (`kill_loss_cert_unavailable = False`)**: On the unrepaired rollout variant (`pilot-g5-unrepaired-rollout`), `solve_progress` produces a verified `LOSS` certificate containing initial belief `["draft"]` in its trap set.

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not emit `Impossible` without `task_admits_impossibility = True`.
