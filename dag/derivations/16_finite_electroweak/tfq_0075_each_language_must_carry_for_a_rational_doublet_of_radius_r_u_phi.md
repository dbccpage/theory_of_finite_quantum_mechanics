# [TFQ-0075] Each language must carry: for a rational doublet of radius r, u(Phi)

> **Stage**: `FINITE_ELECTROWEAK` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `8423b877-21b3-5db3-a8e5-49211f1663b0`  
> **Parent Derivation**: [TFQ-0074](../15_finite_qed/tfq_0074_each_language_must_carry_klein_nishina_forward_value_1_thomson_shape_1_u_2_2_s_u.md)

---

## 1. Abstract & Formal Statement

electroweak_dfm_weinberg_control.rs starts the finite electroweak shadow with an SU(2) dressing over Q(i), not with spontaneous breaking on a lattice. su2_doublet_dressing_matrix builds u(Phi) from a doublet whose norm squares to r^2. The control requires det u = 1, u dagger u = I, left equivariance, and Phi dressed to the column (0, r). Dressed links and left-handed doublets are then invariant under the local SU(2) copy and transform only under the residual charge Q = T3 + Y. The note records that this avoids a gauge-fixing ghost and does not invoke a continuum vacuum manifold.

### Governing Obligation
Each language must carry: for a rational doublet of radius r, u(Phi) has determinant 1 and dresses Phi to (0, r), with residual charge Q = T3 + Y left as the next operator.

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
- [`absent: no local rust twin located for external:sha256:12edc74432418787b0ed633d04e6c77602431a6969b5172b53a4ffaf55e38d9f`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/electroweak_dfm_weinberg_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0076](tfq_0076_each_language_must_carry_det_of_the_neutral_mass_matrix_is_0.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:0fb81f77bbeba84143f574b5a4bc956196140991`
