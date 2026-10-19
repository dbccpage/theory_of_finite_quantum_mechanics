# [TFQ-0055] Each language must carry: no rational homomorphism supplies the missing square root

> **Stage**: `FINITE_GAUGE` | **Status**: `GAP`  
> **UUID**: `67aa1b37-8f6d-5f0b-8c6a-34bafb4fab87`  
> **Parent Derivation**: [TFQ-0054](tfq_0054_each_language_must_carry_pure_gauge_iff_every_off_forest_edge_is_1.md)

---

## 1. Abstract & Formal Statement

The finite U(1) data stop at Gaussian rational units and N-torsion holonomy. FQ-GAP-U1-CIRCLE records that the circle group is not constructed on the finite host: in Q(i), u = (3+4i)/5 has no square root and n -> u^n is injective, so no homomorphism from (Q,+) to the rational points sends 1 to u. F002.S001 is the empty shelf where a continuum shadow of that circle would have to be named later. Its shelf.yaml has books: [] and says a named adjoining record does not establish a bridge theorem. F002.S000 is only the interface inventory.

### Governing Obligation
Each language must carry: no rational homomorphism supplies the missing square root of (3+4i)/5, and F002.S001 remains an empty open bridge rather than a completed circle.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `circle group U(1) (assumption)`
- **Admitted**: `circle group U(1): assumption`
- **Admitted**: `complex field C (assumption)`
- **Admitted**: `continuity of one-parameter phase group (assumption)`
- **Admitted**: `continuum Hilbert space (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Algebraic non-square obstruction in Q(i) and rational Cayley punctured-circle parameterization are mechanized; compact continuous R/Z completion remains a declared external import.

> [!WARNING]
> See L1-U1-SELECTOR-OTHER-SEGMENT.

> [!WARNING]
> Z[i] non-field obstruction and discriminant-5 spectral exit from Q(i) are mechanized; continuum Hilbert completion remains an explicit import.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_gap_stone_rational_rotation_infinite_order_and_zi_non_field_obstruction`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_gap_u1_circle_pythagorean_half_exponent_obstruction`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_u1_selector_split_real_zero_divisors_and_cayley_unit_circle`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011Circle.lean::sign_excluded_circle_still_imported`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011U1SelectorBoundary.lean::selector_not_free`](../../code/lean4/)
- [`not located`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/complex_structure_selector.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs::UnitPhaseGroup`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/u1_gauge_triviality.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche8_tensor_stone_continuum_embedding_and_leftover_mnc_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche9_bloch_gap_cayley_u1_hadamard_coherence_and_destructive_interference_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/amplitude_bridge.rs::half_exponent_obstruction`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`, `F002.S001`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S001_continuum_finite_shadow_bridge`
