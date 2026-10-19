# [TFQ-0168] Keep finite joint tables and classical instruments exact, with no-signalling questions apart

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `7acbaa92-64ee-5f13-9305-5540beb57097`  
> **Parent Derivation**: [TFQ-0167](tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md)

---

## 1. Abstract & Formal Statement

Joint structure and classical instruments stay inside the same exact-rational crate and are not a quantum no-signalling theorem. The lib.rs module table assigns joint_table.rs to marginals, conditionals, independence tests, couplings, and Frechet bounds, and classical_instrument.rs to composition, coarse-graining, adaptive control, and conditional boxes, with no-signalling questions kept apart from hidden-variable questions. The obligation is to preserve that separation: a joint table on Fin n is a finite control, not an imported signalling principle and not a Born pairing.

### Governing Obligation
Keep finite joint tables and classical instruments exact, with no-signalling questions apart from hidden-variable questions.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`not located`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_finite_probability/src/classical_instrument.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_finite_probability/src/joint_table.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_finite_probability/src/lib.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/floor.yaml`
