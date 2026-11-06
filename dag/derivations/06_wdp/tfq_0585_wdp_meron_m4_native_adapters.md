# [TFQ-0585] wdp-meron-m4-native-adapters

> **Stage**: `WDP` | **Status**: `PROVED_LEAN`  
> **UUID**: `e745660b-75ee-5f05-9789-8c3bec1bbfaf`  
> **Parent Derivation**: [TFQ-0584](tfq_0584_wdp_meron_m3_spectral_gap_bypass.md)

---

## 1. Abstract & Formal Statement

Meron Field-Limit Target M4: on the 3-rung two-plaquette bond window, the explicit native syndrome-to-repair adapter clears every plaquette defect using a physical bond operator of weight at most 1 and recovers every single-bond fault, while distinct physical operators in the same quotient class have unequal support weights.

### Governing Obligation
Build finite cochain adapter maps from lattice occupation/spin histories into the WDP repair quotient with verified syndrome-to-repair tables and prove quotient-vs-operator separation.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0567](tfq_0567_wdp_bridge_o02_observer_repair.md) wdp-bridge-o02-observer-repair

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Mechanized in Lean 4 (meron_plaquette_syndrome_adapter_sound, meron_single_bond_exact_recovery, and meron_quotient_class_ne_physical_operator in WdpBatch6.lean alongside decoder_iff in LocalObservationCompletion.lean); physical laboratory actuation remains external.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/LocalObservationCompletion.lean::decoder_iff`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/LocalObservationCompletion.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean::WitnessedDifference.WdpBatch6.meron_plaquette_syndrome_adapter_sound`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean::WitnessedDifference.WdpBatch6.meron_quotient_class_ne_physical_operator`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean::WitnessedDifference.WdpBatch6.meron_single_bond_exact_recovery`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: checked in Lean 4 and Python obstruction signature witnesses`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py::obstruction_signature`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0586](tfq_0586_wdp_meron_m5_toric_noise_repair.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/README.md:32-33`
