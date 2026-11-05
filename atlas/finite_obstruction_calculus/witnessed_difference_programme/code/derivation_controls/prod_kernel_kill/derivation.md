# PROD-KERNEL-KILL

Goal id: PROD-KERNEL-KILL

Selected scope for PROD-KERNEL-KILL is recorded in this note.

## Selected scope

Pilot kernel kill-condition evaluator (`evaluate_pilot_kernel_kill_conditions`, `pilot_agent_loop_certificate`) in `omega_engine_applications/wdp_products/kernel/adapter.py` and verification in `omega_engine_applications/tests/test_kernel_adapter.py`.

## Hypotheses

H1. The kernel kill conditions (`omega_engine_applications/wdp_products/kernel/frame.yaml`) are:
1. *"No pilot workflow can be declared as a finite arena with a usable budget."*
2. *"Receipts are not read or replayed by anyone downstream."*

H2. Under `WDP-CHS-P18`, a replay checker never calls the producer and verifies the static `WIN_OPTIMAL` certificate against `declare_pilot_agent_loop_arena()` at minimax budget `"3"`.

## Derivation

1. **Kill Condition 1 (`kill_no_finite_arena = False`)**:
   - `WdpCertificateChecker.check` replays `pilot_agent_loop_certificate` against `declare_pilot_agent_loop_arena()` and accepts `claim == "WIN_OPTIMAL"` with `initial_value == "3" == PILOT_ARENA_USABLE_BUDGET`.
2. **Kill Condition 2 (`kill_receipts_unreplayed = False`)**:
   - `WdpReceiptIssuer.issue` issues a canonical `ReceiptRecord` binding the arena and check receipt under `("WDP-CHS-P04", "WDP-CHS-P18")`, and `WdpReceiptIssuer.verify` replays the digest offline (`True`).

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not claim original-world validation outside the declared finite arena.
