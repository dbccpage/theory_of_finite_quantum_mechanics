# PROD-P2-NEXT-1

Goal id: PROD-P2-NEXT-1

Selected scope for PROD-P2-NEXT-1 is recorded in this note.

## Selected scope

`WdpOutputGate` adapter (`omega_engine_applications/wdp_products/p2_provenance_gate/adapter.py`) implementing the `OutputGate` protocol (`omega_engine_applications/wdp_products/p2_provenance_gate/contracts.py`) over `witnessed_difference.observation.classify_observation`, `witnessed_difference.witness.verify_witness`, `witnessed_difference.measurement.measure`, and `WdpReceiptIssuer`, evaluated across all twelve WDP Appendix G.5 validator steps in canonical order (`omega_engine_applications/tests/test_p1_p2_adapters.py`).

## Hypotheses

H1. The twelve `G5Step` values (`IDS`, `RAW_RECORD_HASH`, `WITNESS_SEMANTICS`, `RE_ACCESS`, `LADDER_ACCEPT`, `MEASURAND`, `UNIT_SCALE`, `CALIBRATION_RANGE`, `UNCERTAINTY`, `PROVENANCE_CHAIN`, `TRACEABILITY`, `AUTHORITY_SEPARATE`) partition the preconditions of Appendix G.5 into twelve ordered checks.

H2. A `ValidationReport` emits a claim (`emitted == True`) if and only if `failures == ()` and `receipt` is a `ReceiptRecord` whose `claim_ids` contains `claim_id`; whenever `failures` is non-empty, `receipt is None`.

H3. Each of the twelve `G5Step` checks admits an orthogonal single-step mutation (`mutate_for_g5_step(step)`) of `valid_candidate_record()` that causes `WdpOutputGate.gate` to fail exclusively at `step` (`tuple(f.step for f in report.failures) == (step,)`).

## Derivation

1. **Twelve-step Appendix G.5 evaluation**:
   - Step 1 (`IDS`): checks mark-capable `Interaction`, retained `Registration`, and `interaction.registration_carrier_id == registration.carrier_id`.
   - Step 2 (`RAW_RECORD_HASH`): checks `record.raw_record_digest == payload_digest(registration.mark)`.
   - Step 3 (`WITNESS_SEMANTICS`): checks non-empty `witness_target` (named among `interaction.poles`) and `witness_context`.
   - Step 4 (`RE_ACCESS`): checks `witness.registration == registration` and `verify_witness(witness, record.observed_mark)`.
   - Step 5 (`LADDER_ACCEPT`): checks `evaluator_result.status == ACCEPT`, `standing == ACCEPTING`, `evaluator_id == witness.reaccess.evaluator_id`, and `classify_observation(observation_receipt)`.
   - Step 6 (`MEASURAND`): checks `MeasurandSpecification`, distinct `ReportedValue` carrier, `IndicationValueMap` carrier binding, and exact rational relation `gain * indication + offset == raw_value`.
   - Step 7 (`UNIT_SCALE`): checks `NumericScale` non-empty `scale_id` and `unit`, `lower <= upper`, and `resolution > 0`.
   - Step 8 (`CALIBRATION_RANGE`): checks `Calibration` binding (`scale_id`, `evaluator_id`), `lower <= raw_value + correction <= upper`, and resolution grid alignment `((corrected - lower) / resolution).denominator == 1`.
   - Step 9 (`UNCERTAINTY`): checks named `error_procedure` and non-negative exact rational `uncertainty`.
   - Step 10 (`PROVENANCE_CHAIN`): checks non-empty `Provenance` entries.
   - Step 11 (`TRACEABILITY`): checks `_validate_traceability(calibration, traceability)` when `traceability_claimed` is `True`.
   - Step 12 (`AUTHORITY_SEPARATE`): checks `authority_decision_inline is False` and `authority_effect == AuthorityEffect.NONE`.

2. **Reference measurement & receipt issuance on pass**:
   - When `failures == ()`, `WdpOutputGate.gate` runs `classify_observation` and `measure` to produce the exact `Measurement` artifact and issues a `ReceiptRecord` via `WdpReceiptIssuer.issue(subject="p2_output_gate", ..., claim_ids=(claim_id,))`.

## Claims this note does not make

- It does not assign operational authority (`authority_effect` is fixed to `"None"`).
- It does not conflate WDP artifact provenance (`Provenance`) with VIM metrological traceability (`MetrologicalTraceability`).
- It does not treat a passing `ValidationReport` as a proof of external truth beyond the checked observation and measurement contracts.
