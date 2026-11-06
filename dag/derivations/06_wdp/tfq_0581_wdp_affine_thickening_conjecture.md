# [TFQ-0581] wdp-affine-thickening-conjecture

> **Stage**: `WDP` | **Status**: `PROVED_LEAN`  
> **UUID**: `02bef1b7-f6cf-5b09-87d8-63d1ae392322`  
> **Parent Derivation**: [TFQ-0580](tfq_0580_wdp_exact_scalar_hadamard_obstruction.md)

---

## 1. Abstract & Formal Statement

For rational affine support centers thickened by bounded measurement error epsilon > 0, the three-valued cell classifier with explicit ABSTAIN_NO_RULE abstention classifies separated cells without error, abstains on ambiguous overlap intervals rather than issuing a false decision, and bounds dyadic cell covering cost.

### Governing Obligation
Derive a dyadic cell partition and covering-number witness classifier with sound abstention tokens that bounds worst-case recovery cost under bounded noise epsilon > 0.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0573](tfq_0573_wdp_out_3_realizable_future_observation.md) wdp-out-3-realizable-future-observation

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Mechanized in Lean 4 (thickened_affine_cell_soundness, thickened_affine_boundary_abstains, thickened_affine_no_false_verdict, thickened_fiber_not_singleton, and thickened_affine_dyadic_covering_bound in WdpBatch6.lean); applies to bounded rational noise intervals and does not claim unbounded Gaussian tail recovery.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean::WitnessedDifference.WdpBatch6.thickened_affine_boundary_abstains`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean::WitnessedDifference.WdpBatch6.thickened_affine_cell_soundness`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean::WitnessedDifference.WdpBatch6.thickened_affine_dyadic_covering_bound`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean::WitnessedDifference.WdpBatch6.thickened_affine_no_false_verdict`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean::WitnessedDifference.WdpBatch6.thickened_fiber_not_singleton`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: checked in Lean 4 rational arithmetic and Python ExactField`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/exact_linear.py::ExactField`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/exact_linear.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0582](tfq_0582_wdp_meron_m1_correlation_estimates.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/affine_thickening_conjecture.md:15-18`
