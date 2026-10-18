# [TFQ-0293] Complex field as a declared carrier

> **Stage**: `L1_TO_L2` | **Status**: `GAP`  
> **UUID**: `df25fd2a-a9a7-58b1-880a-f11321a15b8d`  
> **Parent Derivation**: [TFQ-0292](TFQ-0292_square-root_field_for_amplitude_coordinates.md)

---

## 1. Abstract & Formal Statement

A complex field for sector amplitudes is an import. qm_122_finite_hilbert_boundary_from_primitive_difference.md records Gaussian integers as a finite stand-in and states that they are not a field, since one plus i has no inverse there. The finite obligation is to keep Q(i), when used, as a declared coefficient pack rather than a consequence of primitive difference. complex_structure_selector.rs checks pairings on Gaussian rationals under the identity or conjugation. That is a pairing check, not a construction of the continuum complex field. derivation_dag.json records the id L1-IMP-COMPLEX-FIELD.

### Governing Obligation
Declare any complex coefficient pack and do not read it off the report fiber.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `complex field C: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> No derivation of C from <> or from the window in the sources read. See route L1-R-COMPLEX-GAP.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/H007Complexification.lean::gi_not_embedded`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/complex_realification.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/complex_structure_selector.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0294](TFQ-0294_circle_phases_as_an_imported_unit_group.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`, `F002`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
  - `omega_engine_atlas/coda_atlas/F002_continuum/floor.yaml`
