# [TFQ-0079] Each language must carry: Weyl gamma5 square and trace, chiral projector algebra,

> **Stage**: `FINITE_ELECTROWEAK` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `297685d4-bf9d-5333-85ed-9ef3185b9df0`  
> **Parent Derivation**: [TFQ-0078](tfq_0078_each_language_must_carry_the_four_anomaly_polynomials_vanish_at_n_c.md)

---

## 1. Abstract & Formal Statement

QM-227 in qed_weak_hadronic_finite_maps.rs builds the weak finite shadow on the Weyl-basis gammas. gamma5 is diag(-1,-1,1,1), its square is I, and its trace is 0. The projectors (I minus or plus gamma5)/2 are idempotent, orthogonal and complete, and the vector-minus-axial current kills a right-handed test spinor. The muon phase-space polynomial f0(x) = 1 - 8x + 8x^3 - x^4 has f0(0) = 1, f0(1) = 0, and a recorded factorization. The one-loop bracket is only a sign check once pi^2 is replaced by a rational interval.

### Governing Obligation
Each language must carry: Weyl gamma5 square and trace, chiral projector algebra, f0 endpoints and factorization, the sign of the one-loop bracket, and the Fermi window only where the language actually computes it.

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
- [`absent: no local rust twin located for external:sha256:b2756728a2444a8202ad7ab9078b63b94e2b41bb2addc311e7a2b1bebd8d9f44`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/qed_weak_hadronic_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0080](tfq_0080_rust_and_python_must_carry_exact_two_sided_unitarity_d_b_triangle_closure_and.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:0fb81f77bbeba84143f574b5a4bc956196140991`
