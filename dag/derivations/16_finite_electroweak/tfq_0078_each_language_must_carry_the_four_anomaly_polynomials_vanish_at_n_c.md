# [TFQ-0078] Each language must carry: the four anomaly polynomials vanish at N_c =

> **Stage**: `FINITE_ELECTROWEAK` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `f44e46cc-1bd0-5939-8b05-ad33e1a0c5a1`  
> **Parent Derivation**: [TFQ-0077](tfq_0077_each_language_must_carry_q_t3_y_on_the_standard.md)

---

## 1. Abstract & Formal Statement

Anomaly cancellation in this control is a polynomial identity over Q, not a continuum triangle integral. At N_c = 3 the four listed polynomials vanish together: the SU(3)^2 U(1), SU(2)^2 U(1) and gravitational ones are 0, and the cubic hypercharge split is -3/4 from quarks plus 3/4 from leptons. At N_c = 1 the SU(2) polynomial is -1/3 and the cubic total is 1/2. With the linear charge constraints and Y_u = Y_Q + delta, Y_d = Y_Q - delta, the cubic equation reduces to -3 delta^2 + 3/4 = 0, hence delta^2 = 1/4.

### Governing Obligation
Each language must carry: the four anomaly polynomials vanish at N_c = 3, fail at N_c = 1 by -1/3 and 1/2, and the cubic constraint is delta^2 = 1/4.

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

- [TFQ-0079](tfq_0079_each_language_must_carry_weyl_gamma5_square_and_trace_chiral_projector_algebra.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:0fb81f77bbeba84143f574b5a4bc956196140991`
