# [TFQ-0556] wdp-bridge-report-fiber-observer

> **Stage**: `WDP` | **Status**: `CONDITIONAL`  
> **UUID**: `5bab811b-025d-5577-bf50-db44169260a1`  
> **Parent Derivation**: [TFQ-0554](tfq_0554_wdp_genesis_bridges_ledger.md)

---

## 1. Abstract & Formal Statement

GEN-WDP-03: with actual cases X, a declared evaluation report E: X → Reports and a protected admission or permission decision A: X → Decisions, a decoder on the actual image of E exists exactly when E(x) = E(y) implies A(x) = A(y); necessity applies the decoder to equal reports, sufficiency assigns each occupied report the decision of any representative, and equal reports with unequal decisions forbid every decoder and every report-only postprocessor. GEN-WDP-06 records that event multisets can lose final state, final states can lose occurrence counts, and fresh hashes can bind false receipts. This is the fibre criterion of the S(n)/MSS-N hand-off (TFQ-0338) and of WDP adapter descent (TFQ-0553), so a protected question passes from the realized report to a WDP observer exactly when it is constant on the fibres of the declared report.

### Governing Obligation
Keep declared report and decision assumptions explicit; no permission or physical authenticity follows from this factorization criterion.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared report map from the S(n)/MSS-N realized report image to the WDP observer presentation, with the protected decision on the actual cases (assumption)`

### Further Prerequisites
- [TFQ-0553](tfq_0553_wdp_observer_quotient_passivity.md) wdp-observer-quotient-passivity

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The maps are declared. The result constructs no evaluator, permission grantor or physical authenticity test. The decoder is classical/noncomputable in general. Unused reports require no default value, and the empty case is included. Original target retained as an obligation: GEN-WDP-03: with actual cases X, a declared evaluation report E: X → Reports and a protected admission or permission decision A: X → Decisions, a decoder on the actual image of E exists exactly when E(x) = E(y) implies A(x) = A(y); necessity applies the decoder to equal reports, sufficiency assigns each occupied report the decision of any representative, and equal reports with unequal decisions forbid every decoder and every report-only postprocessor. GEN-WDP-06 records that event multisets can lose final state, final states can lose occurrence counts, and fresh hashes can bind false receipts. This is the fibre criterion of the S(n)/MSS-N hand-off (TFQ-0338) and of WDP adapter descent (TFQ-0553), so a protected question passes from the realized report to a WDP observer exactly when it is constant on the fibres of the declared report. Prior boundary: Conditional on the declared report and protected question; the criterion derives no evaluator, grantor or permission, and a successful evaluation alone does not determine authorization (GEN-WDP-04).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/ProposalAdmissionBridge.lean::factorization_iff_fiber_constancy`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/ProposalAdmissionBridge.lean)
- [`lean4/ReportFiberDescent.lean::ReportFiberDescent.joint_report_sufficient`](../../../lean4/ReportFiberDescent.lean)
- [`lean4/ReportFiberDescent.lean::ReportFiberDescent.lost_bit_obstruction`](../../../lean4/ReportFiberDescent.lean)
- [`lean4/ReportFiberDescent.lean::ReportFiberDescent.postprocess_obstruction`](../../../lean4/ReportFiberDescent.lean)
- [`lean4/ReportFiberDescent.lean::ReportFiberDescent.unique_decoder_iff`](../../../lean4/ReportFiberDescent.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `external:sha256:8f12bd5921d1b1e472ecaf9c5d7ccbc467a2b808ccd452c695dcfbac42e7bc55::ProposalAdmissionModel` (private upstream source, not in this repository)

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/proposal_admission_bridge.py::decision_decoder`](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/proposal_admission_bridge.py)
- [`checks/independent/pgw-wdp-bridge-report-fiber-observer.py`](../../../checks/independent/pgw-wdp-bridge-report-fiber-observer.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0557](tfq_0557_wdp_synthesis_trunk_tiers.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_bridge_register.md:14-17`
  - `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md:64-92`
  - `external:sha256:a11697dcdf5788b476d5c2e541b635a81c03e665684f69bd260bc463a03ee458:81-92`
  - `dag/derivations/independent/pgw-wdp-bridge-report-fiber-observer.md:5`
  - `dag/research/campaign_pgw-wdp-bridge-report-fiber-observer_lean_replay.json:7`
