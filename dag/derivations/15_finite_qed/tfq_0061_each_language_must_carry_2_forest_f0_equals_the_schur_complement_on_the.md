# [TFQ-0061] Each language must carry: 2-forest F0 equals the Schur complement on the

> **Stage**: `FINITE_QED` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `2ea75fc2-cbea-5afe-af4c-55422af38073`  
> **Parent Derivation**: [TFQ-0060](tfq_0060_each_language_must_carry_c1_1_2_exactly_and_higher_coefficients_only.md)

---

## 1. Abstract & Formal Statement

symanzik_two_forest_bphz_finite_map.md and evaluate_qm214_symanzik_two_forest_bphz compute the second Symanzik polynomial as a sum over spanning 2-forests plus the mass term U_G times sum alpha_e m_e^2. On the bubble, the triangle and the 2-loop diamond the forest sum matches the Kirchhoff-Schur complement over Q. A spanning-tree routing p_T satisfies d0 of p_T equal to the external momenta and vanishes on cotree chords. Changing tree changes p_T by a cycle, and the loop-intersection completion returns the same F0 for every tree, with det of the intersection matrix equal to U_G.

### Governing Obligation
Each language must carry: 2-forest F0 equals the Schur complement on the three declared graphs, tree change is a cycle, and the 4-forest subtraction leaves z^2 at the origin, with D and m imported.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `completion to R/C, Stone, period integrals (lift)`
- **Admitted**: `declared discrete Lagrangian and weights (assumption)`
- **Admitted**: `each row s5.2 "Residual import" column (assumption)`
- **Admitted**: `time slicing (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> All finite rational/integer control theorems for QM-207..231 are mechanized; continuum completions in QM-207..211 remain priced as explicit imports.

> [!WARNING]
> Lean file for ENC-1072 not verified by me.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/symanzik_two_forest_bphz_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0062](tfq_0062_each_language_must_carry_a_truncated_intermediate_normalization_series_a.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
