# [TFQ-0562] wd2-no-escape-update-congruence

> **Stage**: `WDP` | **Status**: `PROVED_LEAN`  
> **UUID**: `8bb8aa0c-b72b-5cc7-b34c-f5c5923273c1`  
> **Parent Derivation**: [TFQ-0561](tfq_0561_wd2_sharp_stabilization_bound.md)

---

## 1. Abstract & Formal Statement

The initial observation kernel R_0 is an update congruence if and only if R_1 = R_0, R_infinity = R_0, and no pair in R_0 admits a separating input word (WD2-T3).

### Governing Obligation
Mechanize the four-way no-escape equivalence theorem WD2-T3 in Lean 4.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Establishes the four-way equivalence between update congruence of R_0, R_1 = R_0, R_n = R_0 for all n, and absence of separating words in Lean 4; pairs that escape R_0 are classified by shortest separating words in TFQ-0563.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean::Wd2.isUpdateCongruence_iff_r1_eq_r0`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean::Wd2.no_escape_equivalence`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: verified directly in Lean 4 and Python`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py::no_escape_profile`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0563](tfq_0563_wd2_shortest_separating_word.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/01_substantiated/wd2_claim_ledger.md:8`
