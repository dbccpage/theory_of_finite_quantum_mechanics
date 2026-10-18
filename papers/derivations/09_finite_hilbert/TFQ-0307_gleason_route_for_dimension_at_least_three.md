# [TFQ-0307] Gleason route for dimension at least three

> **Stage**: `FINITE_HILBERT` | **Status**: `GAP`  
> **UUID**: `1b78f444-5650-5192-b56b-a321c7702ee0`  
> **Parent Derivation**: [TFQ-0306](../08_l1_to_l2/TFQ-0306_born_uniqueness_stays_an_imported_boundary.md)

---

## 1. Abstract & Formal Statement

Gleason for dimension n at least 3 is an import. In qm_020_born_normalization_and_conditional_hilbert_lift.md the section labeled Theorem 6, part 2, cites a Gleason route under frame-function hypotheses and says dimension 2 needs a further POVM or continuity strengthening. qm_122_finite_hilbert_boundary_from_primitive_difference.md records that a two-label host fails the dimension extra and that uniqueness at n at least 3 stays imported. The claim ledger calls that a dim-2 obstruction, not a bridge to the full package. derivation_dag.json records L1-QM020-THM6-P2-GLEASON and FQ-GAP-BORN-UNIQUENESS-GLEASON.

### Governing Obligation
Import Gleason hypotheses for n at least 3 and keep the two-label host below that bar.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Gleason theorem for d >= 3 (assumption)`
- **Admitted**: `Gleason theorem: assumption`
- **Admitted**: `Hilbert space (assumption)`
- **Admitted**: `complex Hilbert space of dim >= 3: assumption`
- **Admitted**: `orthogonal additivity / frame functions: assumption`
- **Admitted**: `projection lattice (assumption)`
- **Admitted**: `reversible linear isometric dynamics: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Gleason is cited, not proved here. GleasonTheorem.lean states it is NOT a proof of Gleason's theorem. native/src/campaigns/born_gleason.rs exists under 006_finite_qm (accept dim3 / refuse dim2 / refuse real scalars per ledger; test names not checked).

> [!WARNING]
> Finite rational frame obstructions (Cabello 18-9, d=2 plane, and d=3 rotated frame eliminating the quartic rival) are mechanized; continuum Gleason frame additivity on S^{n-1} remains an external import.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/BornNormalization.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_gleason_d3_orthogonal_frame_additivity_eliminates_quartic_rival`](../../code/lean4/)
- [`lean4/quantum_mechanics/FiniteQM.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/GleasonTheorem.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013QuarticRivalSeparation.lean::frames_equinorm`](../../code/lean4/)
- [`lean4/quantum_mechanics/H017Gleason.lean::gleason_pack_uniqueness_still_imported`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/frame_function_polytope.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/pairing_audit.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche7_wdp_bridge_o03_o05_sector_orbit_and_gleason_rival_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0308](TFQ-0308_born-uniqueness_band_slot_is_still_a_stub.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/claims/gap_register.yaml`
