# [TFQ-0077] Each language must carry: Q = T3 + Y on the Standard

> **Stage**: `FINITE_ELECTROWEAK` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `28bcb59a-7caf-5441-9cf6-17735b652c94`  
> **Parent Derivation**: [TFQ-0076](tfq_0076_each_language_must_carry_det_of_the_neutral_mass_matrix_is_0.md)

---

## 1. Abstract & Formal Statement

Gell-Mann-Nishijima is a rational charge table on the dressed fermions. With hypercharges (1/6, 2/3, -1/3, -1/2, -1) the charges are Q_u = 2/3, Q_d = -1/3, Q_nu = 0 and Q_e = -1, and the left and right charges match for u, d and e. Composite arithmetic gives Q(p) = 2 Q_u + Q_d = 1, Q(n) = Q_u + 2 Q_d = 0, and Q(p)+Q(e) = 0. FiniteQM.lean states this as sm_gell_mann_nishijima_charge_identities. The executable Rust and Python controls recompute the charges from T3+Y rather than reading a stored flag. Nothing here produces a running electric charge or a continuum current.

### Governing Obligation
Each language must carry: Q = T3 + Y on the Standard Model hypercharge list gives charges 2/3, -1/3, 0, -1, with proton charge 1, neutron charge 0, and proton plus electron charge 0.

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
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/electroweak_dfm_weinberg_control.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/electroweak_dfm_weinberg_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0078](tfq_0078_each_language_must_carry_the_four_anomaly_polynomials_vanish_at_n_c.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
