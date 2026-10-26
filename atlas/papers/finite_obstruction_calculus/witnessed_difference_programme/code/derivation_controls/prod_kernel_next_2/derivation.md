# PROD-KERNEL-NEXT-2

Goal id: PROD-KERNEL-NEXT-2

Selected scope for PROD-KERNEL-NEXT-2 is recorded in this note.

## Selected scope

Pilot agent loop finite belief arena declaration (`declare_pilot_agent_loop_arena`, `PILOT_ARENA_TASK_ID`, `PILOT_ARENA_USABLE_BUDGET`) in `omega_engine_applications/wdp_products/kernel/adapter.py` and verification in `omega_engine_applications/tests/test_kernel_adapter.py`.

## Hypotheses

H1. Under `WDP-CHS-D01`, an agent loop is declared as a finite belief arena (`schema = "wdp-finite-belief-model-v1"`) over a finite state carrier, action set, transition relation, post-state observation table, exact positive rational action costs, and resolution table with `authorization = {"effect": "None"}`.

H2. The first kernel kill condition (`omega_engine_applications/wdp_products/kernel/frame.yaml`) states: *"No pilot workflow can be declared as a finite arena with a usable budget."*

H3. For the pilot G.5 provenance-repair loop (`draft -> {gated, rejected} -> verified`), the minimax worst-case cost from initial belief `["draft"]` is $1 + \max(1, 1 + 1) = 3$, which resolves within `PILOT_ARENA_USABLE_BUDGET = "3"`.

## Derivation

1. **Arena declaration (`declare_pilot_agent_loop_arena`)**:
   - Declares states `("draft", "gated", "rejected", "verified")`, initial belief `["draft"]`, target `[["verified"]]`, and actions `("issue_receipt", "manual_audit", "repair_provenance", "run_g5_gate")`.
   - Compiles cleanly under `certified_progress.model.compile_model`.

2. **Usable budget verification**:
   - Solving and checking the arena via `WdpCertificateChecker.check` yields `accepted=True`, `claim="WIN_OPTIMAL"`, and `initial_value="3"`.
   - Under `PILOT_ARENA_USABLE_BUDGET = "3"`, `derive_label` emits `TerminationLabel.RESOLVED_WITHIN_BUDGET`; under tighter budget `"2"`, it emits `TerminationLabel.EXHAUSTED`.

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not claim original-world validation outside the declared finite arena (`WDP-CHS-O02`).
