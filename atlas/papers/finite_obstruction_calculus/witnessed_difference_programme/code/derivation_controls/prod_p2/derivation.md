# PROD-P2

## Target
Bind the **P2 Provenance-Gated Output Layer** (`PROD-P2`) to `omega_engine_cognitive_operations` via `evaluate_provenance_output_gate` and `WdpProvenanceOutputGateAdapter`. Every numerical or observational output must pass interaction/witness registration, metrological scale and uncertainty validation (`REV-SMRM-P2-NUMERAL`), and multi-stage affine calibration replay before emission.

## Mathematical Formulation

Let $R_{\text{obs}} = (\text{Interaction}, \text{Registration}, \text{Witness}, \text{EvaluatorResult})$ be an observation receipt and let $M = (\text{spec}, v_{\text{rep}}, \text{scale}, \text{cal}, u_{\text{stated}}, \text{prov}, \text{trace}, \text{vmap})$ be a measurement tuple.
1. **Observation & Numeral Gate (`WdpOutputGate`)**: Refuses any negative/non-rational uncertainty (`INVALID_UNCERTAINTY`) or unmapped indication key (`UNMAPPED_INDICATION`).
2. **Composed Enclosure Replay (`replay_composed_measurement`, `verify_measurement_replay`)**: Verifies the exact rational enclosure `BoundedReading(-12, Fraction(3, 2))` across the 2-stage affine calibration chain and attaches a `PROD-KERNEL` SHA-256 receipt.

## Verification Summary
- `evaluate_provenance_output_gate` in `omega_engine_cognitive_operations` accepts calibrated measurements with verified replay enclosures and refuses negative uncertainty or unmapped indication keys.
