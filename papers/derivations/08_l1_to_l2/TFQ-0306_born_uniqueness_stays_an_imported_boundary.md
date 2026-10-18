# [TFQ-0306] Born uniqueness stays an imported boundary

> **Stage**: `L1_TO_L2` | **Status**: `GAP`  
> **UUID**: `fdc62c63-4fc3-575d-97a0-b3c5dc64ecf4`  
> **Parent Derivation**: [TFQ-0305](TFQ-0305_sector_weights_do_not_force_the_quadratic_form.md)

---

## 1. Abstract & Formal Statement

Born uniqueness is an import. qm_020_born_normalization_and_conditional_hilbert_lift.md says the quadratic form is selected only after the listed representation assumptions, and that l1 additivity alone does not force it. qm_204_born_uniqueness_import_boundary.md repeats the boundary in its title and, in the status box, says the draft does not derive continuum quantum mechanics. The finite obligation is to price uniqueness separately from the redundant normalization identity.

### Governing Obligation
Import Born uniqueness and do not read it off redundant normalization.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Gleason: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The file's own header says candidate only; the status PROVED_LEAN follows the ledger and the existence of named theorems, not a rebuild by me.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition`](../../code/lean4/)
- [`lean4/quantum_mechanics/FiniteQM.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::born_nonuniqueness_open`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::pairing_exists`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::quartic_rival`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::uniqueness_not_discharged`](../../code/lean4/)
- [`lean4/quantum_mechanics/H017Finish.lean::two_label_host_not_gleason_dimension`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/pairing_audit.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_state.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0307](../09_finite_hilbert/TFQ-0307_gleason_route_for_dimension_at_least_three.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
