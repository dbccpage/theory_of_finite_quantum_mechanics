# [TFQ-0081] Each language must carry: S(N_c) = N_c/3, the values 1 and 1/3,

> **Stage**: `FINITE_ELECTROWEAK` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `e800e136-3d49-5405-af70-7be5928dbe27`  
> **Parent Derivation**: [TFQ-0080](tfq_0080_rust_and_python_must_carry_exact_two_sided_unitarity_d_b_triangle_closure_and.md)

---

## 1. Abstract & Formal Statement

The hadronic finite map begins with the Adler-Bell-Jackiw colour factor, as a rational prefactor rather than a continuum decay amplitude. abj_colour_factor returns N_c (Q_u^2 - Q_d^2). With the charges from the Gell-Mann-Nishijima table this is N_c/3, so the value is 1 at three colours and 1/3 at one colour, and the rate ratio between those colour counts is 9. pion_two_photon_rate_ev encloses the declared formula alpha^2 m_pi^3 S^2 / (64 pi^3 f_pi^2). The note records the N_c = 3 window [7.690, 7.882] eV and the N_c = 1 window [0.854, 0.875] eV against a stated experimental band.

### Governing Obligation
Each language must carry: S(N_c) = N_c/3, the values 1 and 1/3, and the exact factor 9 between the two colour counts, with the electron-volt windows tied to the declared inputs.

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

- [TFQ-0082](tfq_0082_each_language_must_carry_the_octet_and_decuplet_relations_as_polynomial_identities.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
