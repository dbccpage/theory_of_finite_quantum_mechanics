# [TFQ-0549] wdp-degree-k-torsion-balance

> **Stage**: `WDP` | **Status**: `SOURCE_RECORD`  
> **UUID**: `efae4646-2dbd-5c7a-8e23-071f2c56783b`  
> **Parent Derivation**: [TFQ-0004](tfq_0004_witnessed_difference_degree_1_window.md)

---

## 1. Abstract & Formal Statement

WDP-CH05-P03: on a finite oriented simplicial complex δ^{k+1}δ^k = 0 for every k, since each k-face of a (k+2)-simplex arises by deleting two vertices in either order with opposite signs; each triple (C^{k−1}, C^k, C^{k+1}) with a norm meeting the §4.8 hypothesis is then a window with κ^k well defined on Q^k, 0 → H^k → Q^k → im δ^k → 0 exact, and Γ_{k+1} ≤ ‖δ^k‖_{J→1}Φ_k. WDP-CH05-P06: the six-vertex, fifteen-edge, ten-triangle triangulation of RP² has rank_ℚ δ¹ = 10 and rank_{F₂} δ¹ = 9, so H²(K; ℚ) = 0 while H²(K; F₂) ≅ F₂; the single-triangle indicator is exact over ℚ (Φ₂ = 0) with only non-integral rational repairs. WDP-CH05-P04: on every finite oriented graph Σ_v (d₀*x)(v) = 0, so d₀*x = ρ needs Σ_v ρ(v) = 0 (necessary, not sufficient, and with no closedness or boundary condition); a functional invariant under A ↦ A + d₀λ descends uniquely to Q¹, so the pairing with a 1-cycle is invariant; and δ²δ¹ = 0 on complexes with 3-simplices.

### Governing Obligation
Verify δ^{k+1}δ^k = 0 exactly on each declared simplicial complex, reproduce the RP² ranks 10 over ℚ and 9 over F₂, and check the zero-sum balance and 1-cycle pairing invariance on finite graphs, stating the coefficient field with every answer.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared finite oriented simplicial complex with a total vertex order and a declared coefficient field (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Written proofs with Python checks and no Lean declaration; the coefficient field is part of the window, the degree-k extension says nothing about cup products or continuum forms, and the balance identities are not physical conservation laws.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: the claim map records WDP-CH05-P03, P04 and P06 as prose-only`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust binding for the degree-k window, the RP2 torsion witness or the balance identities`

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/simplicial.py::gauss_law_solvable`](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/simplicial.py)
- [`atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/simplicial.py::rp2_torsion_witness`](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/simplicial.py)
- [`atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/simplicial.py::verify_nilpotence`](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/simplicial.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:2277-2292`
  - `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:2306-2327`
  - `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:2331-2350`
