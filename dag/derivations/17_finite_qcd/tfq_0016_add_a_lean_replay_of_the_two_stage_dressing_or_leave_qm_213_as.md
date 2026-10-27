# [TFQ-0016] Add a Lean replay of the two-stage dressing or leave QM-213 as

> **Stage**: `FINITE_QCD` | **Status**: `PROVED_LEAN`  
> **UUID**: `e48544d7-d14e-5ebc-8e7e-ca7fdf7232a2`  
> **Parent Derivation**: [TFQ-0015](tfq_0015_keep_the_substantial_versus_artificial_split_on_b_2_q_not_on_su_3.md)

---

## 1. Abstract & Formal Statement

Narrowed to the Lean model in B2SemidirectDressing.lean. Invertible upper-triangular 2x2 matrices over Q are modelled as triples (d1, b, d2) with product (d1 d1', d1 b' + b d2', d2 d2'). Each invertible x equals torusProj x times unipotentPart x, with torusProj x diagonal and unipotentPart x unit upper-triangular, the factorization is unique, and the unit upper-triangular matrices are closed under conjugation by invertible ones. On the graph with vertices 0 to 3, edges (0,1), (1,2), (0,2), (2,3), (1,3) and tree edges (0,1), (0,2), (2,3), take any assignment of one invertible matrix to each edge. The explicit stage-one dressing u_N(v) = (1, -b/d2, 1), read off the tree transport T(v) of the vertex v, leaves the tree edges diagonal and preserves torusProj on all five edges. Stage-two dressing by the inverse of the diagonal part of T(v) turns the stage-one connection into U_full(e) = T(target e)^-1 U_e T(source e) on all five edges. For any commutative ring R and any 1-cochain A as a function R to R to R, bA(u,v,w) = -A(u,w) and (A cup A)(u,v,w) = A(u,v) A(v,w) are defined, and K = bA + A cup A satisfies b(bA) = 0, the identity bK + A cup K - K cup A = 0, and gauge covariance. Lean does not identify the triple model with the QM-213 map, does not show u_N is a conjugate of the tree unipotent, does not identify U_full with tree_gauge_indexed.residual, has no poset P_5, and has no non-commutative coefficients in the curvature statements. The Lean module records that the natural numbers 2 and 3 differ and does not prove a color-transport statement. checks/independent/tfq-0016.py searches FiniteQM.lean for the substrings qm213, two_stage, and borel and does not find them.

### Governing Obligation
Not proved in Lean: that the triple model is the QM-213 map; that u_N is a conjugate of the tree unipotent; that U_full is tree_gauge_indexed.residual; the curvature statements on the extended diamond poset P_5 and with non-commutative (matrix) coefficients, which checks/independent/tfq-0016.py tests with SymPy only; any color-transport statement.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`B2SemidirectDressing.two_stage_factorization`](../../lean4/B2SemidirectDressing.lean)
- [`B2SemidirectDressing.UpperTri2.b2_semidirect_factorization`](../../lean4/B2SemidirectDressing.lean)
- [`B2SemidirectDressing.UpperTri2.b2_factorization_unique`](../../lean4/B2SemidirectDressing.lean)
- [`B2SemidirectDressing.UpperTri2.unipotent_subgroup_normal`](../../lean4/B2SemidirectDressing.lean)
- [`B2SemidirectDressing.stage1_tree_edges_diagonal`](../../lean4/B2SemidirectDressing.lean)
- [`B2SemidirectDressing.stage1_preserves_quotient_projection`](../../lean4/B2SemidirectDressing.lean)
- [`B2SemidirectDressing.stage2_reproduces_residual`](../../lean4/B2SemidirectDressing.lean)
- [`B2SemidirectDressing.b_squared_zero`](../../lean4/B2SemidirectDressing.lean)
- [`B2SemidirectDressing.discrete_bianchi_identity`](../../lean4/B2SemidirectDressing.lean)
- [`B2SemidirectDressing.curvature_gauge_covariance`](../../lean4/B2SemidirectDressing.lean)
- [`B2SemidirectDressing.b2_color_dimension_mismatch`](../../lean4/B2SemidirectDressing.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`checks/independent/tfq-0016.py`](../../checks/independent/tfq-0016.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0017](tfq_0017_do_not_promote_the_su_2_quaternion_shadow_to_su_3_c.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
