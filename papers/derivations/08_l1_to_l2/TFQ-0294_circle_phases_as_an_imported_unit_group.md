# [TFQ-0294] Circle phases as an imported unit group

> **Stage**: `L1_TO_L2` | **Status**: `GAP`  
> **UUID**: `f30a6b2f-b24d-5cea-8112-9734ed29552e`  
> **Parent Derivation**: [TFQ-0293](TFQ-0293_complex_field_as_a_declared_carrier.md)

---

## 1. Abstract & Formal Statement

U(1) phases on sector amplitudes are an import. qm_122_finite_hilbert_boundary_from_primitive_difference.md says the mixing leftover already runs on plus and minus one, and that excluding the sign group needs an extra non-exponent-two condition. That exclusion does not construct the circle. The circle stays imported, and continuity of a one-parameter phase group stays a hypothesis. phase_blind_quotient.rs enumerates a declared finite unit group inside the Gaussian rationals. phase_averaged_shadow.rs says the continuous Haar average is not computed.

### Governing Obligation
Import circle phases, or name the finite unit group actually enumerated.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `circle group U(1) (assumption)`
- **Admitted**: `circle group U(1): assumption`
- **Admitted**: `continuity of one-parameter phase group (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> See L1-U1-SELECTOR-OTHER-SEGMENT.

> [!WARNING]
> Algebraic non-square obstruction in Q(i) and rational Cayley punctured-circle parameterization are mechanized; compact continuous R/Z completion remains a declared external import.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_gap_u1_circle_pythagorean_half_exponent_obstruction`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_u1_selector_split_real_zero_divisors_and_cayley_unit_circle`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011Circle.lean::sign_excluded_circle_still_imported`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011U1SelectorBoundary.lean::selector_not_free`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/complex_structure_selector.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_averaged_shadow.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs::UnitPhaseGroup`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche9_bloch_gap_cayley_u1_hadamard_coherence_and_destructive_interference_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/amplitude_bridge.rs::half_exponent_obstruction`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0295](TFQ-0295_born_readout_of_a_supplied_lift_is_redundant.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
