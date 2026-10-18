# [TFQ-0299] Orthogonal additivity is an extra frame law

> **Stage**: `L1_TO_L2` | **Status**: `GAP`  
> **UUID**: `65d3c091-46e3-5ddd-b05d-09cecdab4f99`  
> **Parent Derivation**: [TFQ-0298](../09_finite_hilbert/TFQ-0298_bra-ket_section_remains_non-canonical.md)

---

## 1. Abstract & Formal Statement

Orthogonal additivity is an import. In qm_020_born_normalization_and_conditional_hilbert_lift.md the section labeled Theorem 6 lists it among the representation assumptions that l1 sector additivity does not supply: additivity over orthogonal sectors, and a projection or frame function if a Gleason route is invoked. The finite obligation is to keep l1 additivity on one declared sector basis distinct from additivity across every orthogonal decomposition. qm_122_finite_hilbert_boundary_from_primitive_difference.md records a weak unit-effect contract on which two pairings share the total and still disagree.

### Governing Obligation
Import orthogonal frame additivity separately from additivity on one fixed sector basis.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `orthogonality relation: assumption`
- **Admitted**: `projection measures / frames: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> No derivation of orthogonality from the l1 carrier. H013 headers say Candidate only.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/FiniteQM.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::quartic_rival`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013FrameAdditivity.lean`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013SameContract.lean::two_effect_rules_share_unit_total_and_disagree`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/frame_function_polytope.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0300](TFQ-0300_descent-compatible_maps_stay_row-sparse.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
