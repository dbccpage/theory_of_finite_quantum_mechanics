# [TFQ-0082] Each language must carry the octet and decuplet relations as polynomial identities

> **Stage**: `FINITE_ELECTROWEAK` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `54c759f7-a1c8-55b8-abf8-2500b2388b41`  
> **Parent Derivation**: [TFQ-0081](tfq_0081_each_language_must_carry_s_n_c_n_c_3_the_values_1_and_1_3.md)

---

## 1. Abstract & Formal Statement

The Gell-Mann-Okubo piece is a polynomial identity in three rational mass coefficients. su3_mass_coefficients reads isospin and hypercharge into the operator M0 + M1 Y + M2 (I(I+1) - Y^2/4). gmo_octet_relation_coefficients and gmo_decuplet_second_differences are the linear relations checked by passed(). The note says the octet and decuplet identities hold as polynomials in (M0, M1, M2). With the declared PDG-style masses the octet residual is recorded as 5.7e-3 and the Omega prediction as 1682.2 MeV against 1672.45 MeV. Those residuals are input-bound.

### Governing Obligation
Each language must carry the octet and decuplet relations as polynomial identities in (M0, M1, M2), and must keep the numerical residuals attached to the declared mass inputs.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `completion to R/C, Stone, period integrals (lift)`
- **Admitted**: `each row s5.2 "Residual import" column (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> All finite rational/integer control theorems for QM-207..231 are mechanized; continuum completions in QM-207..211 remain priced as explicit imports.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/qed_weak_hadronic_finite_maps.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/qed_weak_hadronic_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0083](tfq_0083_each_language_must_carry_an_explicit_gap_record_the_finite_gauge_dirac.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
