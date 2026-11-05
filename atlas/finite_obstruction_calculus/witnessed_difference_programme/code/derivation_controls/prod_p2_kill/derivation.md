# PROD-P2-KILL

Goal id: PROD-P2-KILL

Selected scope for PROD-P2-KILL is recorded in this note.

## Selected scope

Pilot P2 kill-condition evaluator (`evaluate_pilot_p2_kill_conditions`, `repair_candidate_from_failures`) in `omega_engine_applications/wdp_products/p2_provenance_gate/adapter.py` and verification in `omega_engine_applications/tests/test_p1_p2_adapters.py`.

## Hypotheses

H1. The P2 kill conditions (`omega_engine_applications/wdp_products/p2_provenance_gate/frame.yaml`) are:
1. *"In a pilot, fewer than a useful share of outputs can ever pass G.5."*
2. *"Downstream users ignore the failure lists."*

## Derivation

1. **G.5 pass share (`kill_low_pass_share = False`)**: 3 of 4 initial pilot outputs pass G.5 on the first pass (`3/4 >= 1/2`), and 4 of 4 pass after failure-list repair.
2. **Failure-list repair loop (`kill_failures_ignored = False`)**: `repair_candidate_from_failures` consumes the ordered `ValidationFailure` list (`[UNCERTAINTY, PROVENANCE_CHAIN]`) and restores compliance so `WdpOutputGate.gate` emits a verified `ReceiptRecord`.

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not emit a receipt for any candidate with non-empty `failures`.
