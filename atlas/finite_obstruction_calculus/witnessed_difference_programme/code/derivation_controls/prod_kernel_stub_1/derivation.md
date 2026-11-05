# PROD-KERNEL-STUB-1

Goal id: PROD-KERNEL-STUB-1

Selected scope for PROD-KERNEL-STUB-1 is recorded in this note.

## Selected scope

Adapter implementing the `CertificateChecker` protocol (`omega_engine_applications/wdp_products/kernel/contracts.py`) over `certified_progress.check_certificate` (`omega_engine_applications/wdp_products/kernel/adapter.py`), returning `CheckReceipt` without importing or calling `certified_progress.producer` and without substituting a solver's answer for a suboptimal or forged certificate.

## Hypotheses

H1. `certified_progress.check_certificate(model, certificate)` replays a submitted `wdp-progress-certificate-v1` object against the compiled finite belief arena `compile_model(model)`.

H2. An accepted `LOSS` certificate returns `{"accepted": True, "claim": "LOSS", "status": "Refuted", "termination": "Stalled" | "Trapped", "model_digest": ..., "authority_effect": "None"}`, where `"Stalled"` holds if and only if the initial belief has no admissible moves (`arena.initial in stalled`).

H3. An accepted `WIN_OPTIMAL` or `WIN_FEASIBLE` certificate returns `{"accepted": True, "claim": kind, "status": "Proved", "initial_value": str(values[arena.initial]), "model_digest": ..., "authority_effect": "None"}`.

H4. Any rejected certificate returns `{"accepted": False, "status": "Refused", "reason": str(error), "authority_effect": "None"}`.

## Derivation

1. **Mapping onto `CheckReceipt` (`to_check_receipt`)**:
   - When `accepted is False`, `to_check_receipt` emits `CheckReceipt(accepted=False, model_digest=..., certificate_digest=..., failures=(reason,), authority_effect="None")` with `claim=None, initial_value=None, initial_stalled=None`.
   - When `accepted is True` and `claim == "LOSS"`, `to_check_receipt` sets `initial_stalled = (termination == "Stalled")` and `initial_value = None`.
   - When `accepted is True` and `claim in ("WIN_OPTIMAL", "WIN_FEASIBLE")`, `to_check_receipt` sets `initial_value = raw["initial_value"]` (exact rational string) and `initial_stalled = None`.

2. **Non-invocation of producer and non-substitution of answers**:
   - `omega_engine_applications/wdp_products/kernel/adapter.py` never imports `certified_progress.producer` or `solve_progress`.
   - On `cheaper_route` (`s --direct(5)--> t`, `s --step(1)--> u --finish(1)--> t`), the optimal initial value is `"2"` (`WIN_OPTIMAL`), whereas the direct route has valid feasible value `"5"` (`WIN_FEASIBLE`). `WdpCertificateChecker.check` accepts the `WIN_FEASIBLE` certificate with `initial_value="5"` (never substituting `"2"`), and rejects the forged `WIN_OPTIMAL` certificate claiming `"5"` is optimal with `failures=("lower inequality failed: a cheaper action exists",)`.

3. **Parity with `report_termination` and P1 `derive_label`**:
   - Across all 15 offline replay records in `certified_progress/evidence/records.json` and all 7 certificate-backed `TerminationLabel` outcomes in `p1_abstention_governor`, `WdpCertificateChecker.check` reproduces `check_certificate` and drives `derive_label` in exact parity with `report_termination`.

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not claim original-world adequacy outside the declared finite belief arena (`WDP-CHS-O02`).
- It does not replace the open native Rust binding obligation for the full Python game checker (`WDP-CHS-O03`).
