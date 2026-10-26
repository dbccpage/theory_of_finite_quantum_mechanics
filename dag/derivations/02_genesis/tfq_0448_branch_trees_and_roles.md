# [TFQ-0448] branch-trees-and-roles

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `f84c2e4e-1bba-5847-9d33-7f821e484ca0`  
> **Parent Derivation**: [TFQ-0446](tfq_0446_pruning_lemmas_cost_two.md)

---

## 1. Abstract & Formal Statement

With the external continuation policy enabled, isomorphism-quotiented branch DAGs were exported for both readings and both measures within the declared bounds. Under mu2 there is no guard cutoff: the quotient tree to the requested 15 transition steps is finite and enumerated in full, 963 nodes for L and 1847 for F, conditional on the orbit policy losing no child classes, and its leaves are round-cut, carrying 10 or 11 separation responses in L and 10, 11 or 12 in F. Under mu1 the 1200-node pre-expansion guard cuts first at depth 6 (L) and 5 (F), leaving exact exported frontiers of 927 and 886 guard-cut nodes. Counted over accepted edges (L mu1, L mu2, F mu1, F mu2), the recurring roles are supply (195/111/233/413), discrimination by one new instance (1047/858/1001/1458), innovation by a fresh form plus instance (8/53/10/83) and double discrimination (6, F mu2 only); the auxiliary-witness shape never appears among accepted minima.

### Governing Obligation
Regenerate the four quotiented trees within the declared bounds and report their node counts, cut kinds, leaf response counts and role counts over accepted edges.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared resource bounds: at most 2 items, concrete arity at most 2, 15 transition steps, pre-expansion node guards 1200 (mu1) and 3000 (mu2) (assumption)`

### Further Prerequisites
- [TFQ-0447](tfq_0447_count_invariance_transport.md) count-invariance-transport

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Reaching the requested depth is not unboundedness and no unboundedness claim is made; mu2 completeness is conditional on CL-TREE-MU2-COMPLETE, the mu1 trees are guard-bounded, and behaviour past the exported depths is unresolved.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: no Lean statement of the exported trees; they are finite computations`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/role.rs::role` (private upstream source, not in this repository)
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/tree.rs::depth_fifteen_reading_f_mu2_is_1847_nodes_with_the_sealed_roles` (private upstream source, not in this repository)
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/tree.rs::depth_fifteen_reading_l_mu2_is_963_nodes_and_merges_carry_witnesses` (private upstream source, not in this repository)

### Python Oracles & Numerical Evaluators
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/engine.py::build_tree` (private upstream source, not in this repository)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:449-458`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:466-473`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:480-487`
