# PROD-P3-KILL

Goal id: PROD-P3-KILL

Selected scope for PROD-P3-KILL is recorded in this note.

## Selected scope

Pilot P3 kill-condition evaluator (`evaluate_pilot_p3_kill_conditions`) in `omega_engine_applications/wdp_products/p3_guard_transfer/adapter.py` and verification in `omega_engine_applications/tests/test_p3_p5_adapters.py`.

## Hypotheses

H1. The P3 kill conditions (`omega_engine_applications/wdp_products/p3_guard_transfer/frame.yaml`) are:
1. *"On pilot workloads no guard reaches strict benefit."*
2. *"Transfer soundness fails for the representation changes buyers care about."*

## Derivation

1. **Strict benefit (`kill_no_strict_benefit = False`)**: On the Appendix Q.4 workload ($N = 10000$, $v = 1$, $g = 1/1000$, $C_0 = 2$), the transferred `circulation` guard reaches strict benefit at $h = 13$ hits (`saving = "1"`).
2. **Transfer soundness (`kill_transfer_soundness_fails = False`)**: `WdpGuardTransferChecker.transfer` admits `circulation` under the declared adapter while refusing `unsafe-point` with `code = "transfer_unsafe"`.

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not claim transfer soundness without an explicit adapter and target validity check (`WDP-CHS-P05`).
