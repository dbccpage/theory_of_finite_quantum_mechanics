# PROD-P1-NEXT-1

Goal id: PROD-P1-NEXT-1

Selected scope for PROD-P1-NEXT-1 is recorded in this note.

## Selected scope

`WdpAbstentionGovernor` adapter (`omega_engine_applications/wdp_products/p1_abstention_governor/adapter.py`) implementing the `AbstentionGovernor` protocol (`omega_engine_applications/wdp_products/p1_abstention_governor/contracts.py`) over `certified_progress.reporting.report_termination` and `WdpCertificateChecker`, together with round-trip tests across all eight `TerminationLabel` values and negative controls (`omega_engine_applications/tests/test_p1_p2_adapters.py`).

## Hypotheses

H1. Every termination outcome emitted by `certified_progress.reporting.report_termination` belongs to the seven certificate-backed labels (`RefusedCertificate`, `Stalled`, `Impossible`, `LosingInDeclaredArena`, `ResolvedWithinBudget`, `Exhausted`, `UndeterminedBudget`), and `TerminationLabel.REFUSED` represents a declared controller refusal action prior to certificate replay (`check = None`).

H2. For any checked `CheckReceipt`, non-negative exact rational `budget`, and explicit boolean `task_admits_impossibility`, `derive_label(check, budget, task_admits_impossibility=...)` reproduces the label assigned by `report_termination`.

H3. `TerminationLabel.IMPOSSIBLE` requires an accepted `LOSS` certificate with `initial_stalled = False` and `task_admits_impossibility = True`; when `task_admits_impossibility = False`, the same trapped `LOSS` certificate receives `TerminationLabel.LOSING_IN_DECLARED_ARENA`.

## Derivation

1. **Input validation (`TypedRefusal` gate)**:
   - `WdpAbstentionGovernor.report` checks `type(task_admits_impossibility) is bool` and validates `budget` via `is_rational_text` and `certified_progress.model.rational` (non-negative exact rational). Violation of either precondition returns `TypedRefusal(code="invalid_input", authority_effect="None")`.

2. **Declared controller refusal (`TerminationLabel.REFUSED`)**:
   - When `certificate is None` and a non-empty `refusal_action` (or `"refusal_action:..."` evidence reference) is supplied, `WdpAbstentionGovernor.report` returns `GovernorReport(label=TerminationLabel.REFUSED, check=None, ...)`. Passing both a certificate and a `refusal_action` returns `TypedRefusal(code="invalid_input", ...)`.

3. **Certificate-backed label parity and round-trip**:
   - For certificate-backed calls, `WdpAbstentionGovernor.report` invokes `report_termination(model, certificate, budget, task_admits_impossibility=task_admits_impossibility)`, converts `raw["receipt"]` via `to_check_receipt`, verifies `TerminationLabel(raw["termination"]) == derive_label(check_receipt, budget, task_admits_impossibility=task_admits_impossibility)`, and returns a frozen `GovernorReport` that round-trips identically through `model_dump_json()` and `model_validate_json()`.

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not infer impossibility from budget exhaustion (`Exhausted` and `UndeterminedBudget` require `WIN_OPTIMAL` / `WIN_FEASIBLE` certificates respectively, never `Impossible`).
- It does not treat arena-relative loss (`LosingInDeclaredArena`) as task-level impossibility when `task_admits_impossibility` is `False`.
