# [TFQ-0054] Each language must carry: pure gauge iff every off-forest edge is 1,

> **Stage**: `FINITE_GAUGE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `74ba6866-9cde-55d3-a499-183d3c39fad1`  
> **Parent Derivation**: [TFQ-0053](tfq_0053_each_language_must_carry_a_unit_gaussian_edge_connection_covariant_difference_vertex.md)

---

## 1. Abstract & Formal Statement

u1_gauge_triviality.rs decides whether a declared connection is pure gauge. trivializing_gauge uses the spanning-forest gauge fixing from holonomy_interference: the connection is the gauge transform of the trivial connection exactly when every edge off the forest is left at 1. Otherwise it returns the fundamental cycle of the first edge left at another value, together with that holonomy, which is not 1. The walk and holonomy are ordinary OrientedWalk and U1Connection values, so the refusal can be replayed. The module says nothing about an additive cochain the connection may have come from.

### Governing Obligation
Each language must carry: pure gauge iff every off-forest edge is 1, else a replayable cycle whose holonomy is not 1; coboundary agreement is withheld unless the scale has infinite order.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `circle group U(1) (assumption)`
- **Admitted**: `continuity of one-parameter phase group (assumption)`
- **Admitted**: `finite oriented graph (assumption)`
- **Admitted**: `non-triviality and order N of the edge phase cochain (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Finite N-torsion gauge invariance and sign-group separation are mechanized; completion to R/Z remains in FQ-GAP-U1-CIRCLE.

> [!WARNING]
> Algebraic non-square obstruction in Q(i) and rational Cayley punctured-circle parameterization are mechanized; compact continuous R/Z completion remains a declared external import.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:e86ad3309b090c78f09e92fa9833a87b325a0513396663cbf2bd5c2ea1fd0c7b`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0055](tfq_0055_each_language_must_carry_no_rational_homomorphism_supplies_the_missing_square_root.md)
- [TFQ-0056](../15_finite_qed/tfq_0056_each_language_must_carry_clifford_admission_slash_square_exact_solution_rank_and_a.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:0fb81f77bbeba84143f574b5a4bc956196140991`
