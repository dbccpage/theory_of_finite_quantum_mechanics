# [TFQ-0056] Each language must carry: Clifford admission, slash-square, exact solution rank, and a

> **Stage**: `FINITE_QED` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `61116771-2c93-543e-98c4-b5361571383b`  
> **Parent Derivation**: [TFQ-0054](../14_finite_gauge/tfq_0054_each_language_must_carry_pure_gauge_iff_every_off_forest_edge_is_1.md)

---

## 1. Abstract & Formal Statement

dirac_gamma_admission.rs admits a declared family of square gamma matrices over Q(i) with a diagonal metric of entries +1 or -1. CliffordFamily::admit checks every anticommutator against 2 eta I and names the first failing pair. dirac and weyl are the signature (+,-,-,-) families built from the Pauli matrices in omega_lie_theory. slash(p) squares to (p·p) I. solution_dimension is N minus the exact rank of slash(p) - m I. has_dirac_adjoint checks gamma^0 (gamma^mu)* gamma^0 = gamma^mu separately: the anticommutators do not imply that adjoint. Momenta, masses and spin-element parameters stay rational and declared.

### Governing Obligation
Each language must carry: Clifford admission, slash-square, exact solution rank, and a separate Dirac-adjoint check that anticommutators do not imply.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `completion to R/C, Stone, period integrals (lift)`
- **Admitted**: `complex field C (assumption)`
- **Admitted**: `continuum Hilbert space (assumption)`
- **Admitted**: `each row s5.2 "Residual import" column (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> All finite rational/integer control theorems for QM-207..231 are mechanized; continuum completions in QM-207..211 remain priced as explicit imports.

> [!WARNING]
> Z[i] non-field obstruction and discriminant-5 spectral exit from Q(i) are mechanized; continuum Hilbert completion remains an explicit import.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/dirac_gamma_admission.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0057](tfq_0057_each_language_must_carry_rational_dirac_inversion_on_an_admitted_gamma_family.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
