# [TFQ-0586] wdp-meron-m5-toric-noise-repair

> **Stage**: `WDP` | **Status**: `PROVED_LEAN`  
> **UUID**: `59002dd1-015b-55cd-8136-71c40fc55992`  
> **Parent Derivation**: [TFQ-0585](tfq_0585_wdp_meron_m4_native_adapters.md)

---

## 1. Abstract & Formal Statement

Meron Field-Limit Target M5 (Chapter 23): the primal-dual completion criterion ((E - E) intersect ker Q_D subset B) characterizes exact recovery, the 4-vertex star syndrome on a square cycle has rank 3 and is injective on tree-supported errors while vanishing on the 4-edge cycle, and worst-case adaptive transcripts cannot distinguish errors differing by an undetected logical cycle.

### Governing Obligation
Formalize the corrected finite toric-code syndrome kernel, restricted-error tree injectivity, and worst-case adaptive non-improvement in Lean 4 and Python.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Mechanized in Lean 4 (toric_completion_criterion_iff, toric_star_syndrome_sum_zero, toric_restricted_tree_error_injective, toric_cycle_error_in_syndrome_kernel, and toric_adaptive_transcript_indistinguishable in WdpBatch6.lean) and checked in Python plan_odm_toric_boundary.py.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean::WitnessedDifference.WdpBatch6.toric_adaptive_transcript_indistinguishable`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean::WitnessedDifference.WdpBatch6.toric_completion_criterion_iff`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean::WitnessedDifference.WdpBatch6.toric_cycle_error_in_syndrome_kernel`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean::WitnessedDifference.WdpBatch6.toric_restricted_tree_error_injective`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean::WitnessedDifference.WdpBatch6.toric_star_syndrome_sum_zero`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch6.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: checked by Lean 4 theorems and Python toric boundary witness`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/plan_odm_toric_boundary.py::toric_boundary_witness`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/plan_odm_toric_boundary.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0587](tfq_0587_wdp_meron_spacetime_limit.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/meron_field_limit_derivations/README.md:34-35`
