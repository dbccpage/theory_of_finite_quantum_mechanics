# [TFQ-0065] Each language must carry: transverse projector identities, the bubble trace match, U=1

> **Stage**: `FINITE_QED` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `a93ad5b0-0bf0-5e64-a0b4-42e54aab4903`  
> **Parent Derivation**: [TFQ-0064](tfq_0064_each_language_must_carry_exact_cancellation_of_the_declared_infrared_cutoff_between.md)

---

## 1. Abstract & Formal Statement

vacuum_polarization_lamb_shift.rs checks the transverse projector P_T = eta - q q / q^2 on a non-null rational four-momentum. The test requires q_mu P = 0, idempotence, and trace 3. The 4 by 4 Clifford trace of the fermion bubble numerator is compared with the tensor polynomial 4[k^mu (k+q)^nu + (k+q)^mu k^nu - eta (k·(k+q) - m^2)] and must match. On the bubble with Feynman parameters x and 1-x, U equals 1 and F equals m^2 - x(1-x) q^2. BPHZ subtraction at q^2 = 0 is required to cancel the cutoff and to give Pi_R(0) = 0.

### Governing Obligation
Each language must carry: transverse projector identities, the bubble trace match, U=1 and F=m^2-x(1-x)q^2, moment coefficients 1/15, 1/140, 1/945, and contact total 91/120 as the executable value.

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
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/vacuum_polarization_lamb_shift.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/vacuum_polarization_lamb_shift_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0066](tfq_0066_each_language_must_carry_the_twelve_digit_prefixes_for_pi_r_9_m_2_4_the_running.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
