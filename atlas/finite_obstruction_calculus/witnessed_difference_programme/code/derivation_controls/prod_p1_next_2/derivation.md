# PROD-P1-NEXT-2

Goal id: PROD-P1-NEXT-2

Selected scope for PROD-P1-NEXT-2 is recorded in this note.

## Selected scope

Negative-control evaluation (`PROD-P1-NEXT-2`) for P1 `WdpAbstentionGovernor` (`omega_engine_applications/wdp_products/p1_abstention_governor/adapter.py` and `omega_engine_applications/tests/test_p1_p2_adapters.py`):
1. `Impossible` is withheld when `task_admits_impossibility` is `False` (governor emits `LosingInDeclaredArena` rather than `Impossible`, and `GovernorReport` raises `ValueError` if constructed directly with `AbstentionLabel.IMPOSSIBLE` and `task_admits_impossibility=False`).
2. Forged certificates (`task_id` mismatch or forged `WIN_OPTIMAL` witness that violates `verify_certificate`) are rejected (`RefusedCertificate`).

## Hypotheses

H1. Under WDP Appendix G.4 (`termination_certificates.certificate.verify_certificate`), a `LOSS` certificate certifies a closed losing trap set containing the initial belief $b_0$ in the declared arena (`LosingInDeclaredArena`).

H2. Promoting `LosingInDeclaredArena` to `Impossible` requires an explicit task-level policy (`task_admits_impossibility=True`) declaring that the arena exhausts all admissible task actions (`WDP-CHS-N07`).

H3. Any certificate whose `task_id` does not match `arena["task_id"]` or whose witness fails `verify_certificate` is rejected with `AbstentionLabel.REFUSED_CERTIFICATE`.

## Derivation

1. **Without task impossibility policy (`task_admits_impossibility=False`)**:
   - Evaluating `WdpAbstentionGovernor(task_admits_impossibility=False).evaluate(loss_arena, budget)` produces `report.label == AbstentionLabel.LOSING_IN_DECLARED_ARENA` and `report.verified is True`.
   - Direct construction of `GovernorReport(label=AbstentionLabel.IMPOSSIBLE, task_admits_impossibility=False, ...)` raises `ValueError("Impossible requires a task policy that admits impossibility")`.

2. **Forged certificate rejection**:
   - Mutating `cert["task_id"] = "forged-task-id"` causes `verify_certificate` to fail `"task_id matches arena"`, and `governor.verify(arena, forged_task_cert)` emits `AbstentionLabel.REFUSED_CERTIFICATE` (`verified=False`).
   - Mutating a `LOSS` certificate's `"outcome"` to `"WIN_OPTIMAL"` causes `verify_certificate` to fail the `WIN_OPTIMAL` checks, and `governor.verify(arena, forged_win_cert)` emits `AbstentionLabel.REFUSED_CERTIFICATE` (`verified=False`).

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not infer universal task impossibility from a losing finite arena without an explicit task policy.
