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
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_gap_u1_circle_pythagorean_half_exponent_obstruction`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_u1_selector_split_real_zero_divisors_and_cayley_unit_circle`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_u1_transport_n_torsion_and_sign_separation`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011Circle.lean::sign_fails_connectedness_shadow`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011U1SelectorBoundary.lean::u1_selector_boundary`](../../code/lean4/)
- [`not located`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/holonomy_interference.rs::gauge_equivalence`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs::evaluate_qm207_holonomy_bridge`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/u1_gauge_triviality.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/u1_graph_connection.rs::U1Connection`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche9_bloch_gap_cayley_u1_hadamard_coherence_and_destructive_interference_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/amplitude_bridge.rs::half_exponent_obstruction`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0055](tfq_0055_each_language_must_carry_no_rational_homomorphism_supplies_the_missing_square_root.md)
- [TFQ-0056](../15_finite_qed/tfq_0056_each_language_must_carry_clifford_admission_slash_square_exact_solution_rank_and_a.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
