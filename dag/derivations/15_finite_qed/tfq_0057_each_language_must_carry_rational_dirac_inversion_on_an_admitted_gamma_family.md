# [TFQ-0057] Each language must carry: rational Dirac inversion on an admitted gamma family,

> **Stage**: `FINITE_QED` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `2986c36f-8684-5c0f-91ba-76a66f02c068`  
> **Parent Derivation**: [TFQ-0056](tfq_0056_each_language_must_carry_clifford_admission_slash_square_exact_solution_rank_and_a.md)

---

## 1. Abstract & Formal Statement

The charged finite Dirac carrier is the admitted 4 by 4 family together with a graph connection, not a spinor field on a smooth manifold. dirac_ward_takahashi_finite_map.md records S_F(p)^(-1) = slash(p) - m I and S_F(p) = (slash(p) + m I)/(p^2 - m^2), with the product equal to I_4 when the denominator is invertible in Q(i). Dressing along a spanning tree is Psi_v = u_T(v)^(-1) psi_v, where u_T is the path holonomy in the unit Gaussian rationals. On the 4-vertex diamond the dressed two-point is invariant under vertex gauges that fix the root, across the eight spanning trees, while a tree change multiplies by.

### Governing Obligation
Each language must carry: rational Dirac inversion on an admitted gamma family, and spanning-tree dressing whose two-point is vertex-gauge invariant while tree change is a cycle holonomy.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `completion to R/C, Stone, period integrals (lift)`
- **Admitted**: `each row s5.2 "Residual import" column (assumption)`
- **Admitted**: `finite oriented graph (assumption)`
- **Admitted**: `non-triviality and order N of the edge phase cochain (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> All finite rational/integer control theorems for QM-207..231 are mechanized; continuum completions in QM-207..211 remain priced as explicit imports.

> [!WARNING]
> Finite N-torsion gauge invariance and sign-group separation are mechanized; completion to R/Z remains in FQ-GAP-U1-CIRCLE.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:376085dc410bbb86117c8efb40f2280ed15cb5734a22d050f6e1718aef3be579`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/dirac_ward_takahashi_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0058](tfq_0058_each_language_must_carry_u_g_equals_the_scaled_principal_minor_of_the.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:0fb81f77bbeba84143f574b5a4bc956196140991`
