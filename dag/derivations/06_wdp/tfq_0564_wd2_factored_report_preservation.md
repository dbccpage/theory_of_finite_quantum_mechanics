# [TFQ-0564] wd2-factored-report-preservation

> **Stage**: `WDP` | **Status**: `PROVED_LEAN`  
> **UUID**: `27cd8a01-40c7-5492-99dd-51179ba695e2`  
> **Parent Derivation**: [TFQ-0563](tfq_0563_wd2_shortest_separating_word.md)

---

## 1. Abstract & Formal Statement

A step report that factors through the before-update and after-update state observations preserves every horizon relation R_n, whereas an unfactored report can split R_n classes (WD2-T5).

### Governing Obligation
Mechanize the WD2-T5 factored-report invariance theorem and unfactored counterexample in Lean 4.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Establishes in Lean 4 that endpoint-factored step reports preserve R_n and exhibits the two-state unfactored report counterexample; endpoint factorization is sufficient but not necessary at infinite horizon.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean::Wd2.factored_report_preserves_polyRelated`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean::Wd2.factored_report_preserves_related`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean::Wd2.unfactored_report_splits_r0`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: verified directly in Lean 4 and Python`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py::factored_report_profile`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0565](tfq_0565_wd2_minimal_deterministic_quotient.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/01_substantiated/wd2_claim_ledger.md:10`
