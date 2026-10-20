# [TFQ-0058] Each language must carry: U_G equals the scaled principal minor of the

> **Stage**: `FINITE_QED` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `921f7ac9-3783-5a07-9af3-f13e4281d062`  
> **Parent Derivation**: [TFQ-0057](tfq_0057_each_language_must_carry_rational_dirac_inversion_on_an_admitted_gamma_family.md)

---

## 1. Abstract & Formal Statement

Interaction begins as declared graph data, not as a continuum minimal coupling. dressed_graph_qed_g2_finite_map.md takes a finite connected graph, positive rational edge weights, and the first Symanzik polynomial U_G as the sum over spanning trees of the product of cotree weights. On the 4-vertex 5-edge diamond, eight of ten two-edge subsets are cotrees, U_G(1,1,1,1,1) = 8, and both the cotree sum and the scaled Kirchhoff minor equal 101 at weights (1,2,3,5,7). The triangle K3 has U = alpha_1 + alpha_2 + alpha_3. evaluate_qm212_dressed_qed_g2 and symanzik_u_polynomial compute that identity.

### Governing Obligation
Each language must carry: U_G equals the scaled principal minor of the weighted Laplacian on the declared graphs, with alpha, Clifford numerators and the subtraction point left as imports.

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
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/dressed_qed_g2_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0059](tfq_0059_each_language_must_carry_even_leg_wick_pairings_through_20_legs_a_hard.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
