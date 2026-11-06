# [TFQ-0563] wd2-shortest-separating-word

> **Stage**: `WDP` | **Status**: `PROVED_LEAN`  
> **UUID**: `b944c3d0-0e4e-5b68-beb1-19144a399f20`  
> **Parent Derivation**: [TFQ-0562](tfq_0562_wd2_no_escape_update_congruence.md)

---

## 1. Abstract & Formal Statement

A state pair belonging to R_n but excluded from R_{n+1} has a shortest separating input word of length n + 1 (WD2-T4).

### Governing Obligation
Mechanize Theorem WD2-T4 on shortest separating word length in Lean 4.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Establishes in Lean 4 that every state pair in R_n \ R_{n+1} is unseparated at lengths <= n and has a separating word over the declared alphabet of length n + 1; tie-breaking among multiple shortest words requires an external alphabet order.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean::Wd2.shortest_separating_word`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/FiniteDistinction.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: verified directly in Lean 4 and Python`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py::shortest_separating_length`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/finite_distinction.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0564](tfq_0564_wd2_factored_report_preservation.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/01_substantiated/wd2_claim_ledger.md:9`
