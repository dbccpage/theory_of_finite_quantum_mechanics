# PROD-P5-KILL

Goal id: PROD-P5-KILL

Selected scope for PROD-P5-KILL is recorded in this note.

## Selected scope

Pilot P5 kill-condition evaluator (`evaluate_pilot_p5_kill_conditions`) in `omega_engine_applications/wdp_products/p5_claim_certification/adapter.py` and verification in `omega_engine_applications/tests/test_p3_p5_adapters.py`.

## Hypotheses

H1. The P5 kill conditions (`omega_engine_applications/wdp_products/p5_claim_certification/frame.yaml`) are:
1. *"Authors maintain the claim ledger manually instead of running `CertificationService.certify` in CI."*
2. *"Proved is ever emitted for a claim with a missing D.3 pointer."*

## Derivation

1. **Automated CI certification (`kill_1_manual_maintenance = False`)**: `evaluate_pilot_p5_kill_conditions` runs `WdpCertificationService.certify` in topological dependency order (`21.11`).
2. **D.3 pointer completeness (`kill_2_proved_with_missing_d3 = False`)**: Any `ClaimNode` marked `Status.PROVED` whose `EvidencePointers.missing()` is non-empty is demoted to `Status.UNDETERMINED`, leaving zero `PROVED` claims with missing D.3 pointers.

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not allow `PROVED` to survive an incomplete D.3 pointer tuple.
