# [TFQ-0234] Supplied Hilbert carrier after the conditional lift

> **Stage**: `FINITE_QM_CORE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `5c74553c-d178-5130-9430-ebc2a3c0e96f`  
> **Parent Derivation**: [TFQ-0006](../08_l1_to_l2/TFQ-0006_conditional_finite_hilbert_lift.md)

---

## 1. Abstract & Formal Statement

Once a Hilbert carrier is already in hand, finite quantum mechanics does not start again from primitive difference. Finite Quantum Mechanics section 1.1 calls the eight rungs an assumption audit: pairing, phase, tensor composition, reversible steps, instruments, and representation hypotheses stay extra structure. Section 5 leaves the continuum Hilbert lift open. Ledger row FQM-F3 separates the general trace identity from the narrower Lean model. The header opened in lean/FiniteQM.lean declares a narrow opening scope, a rational degree-4 readout identity and five 2x2 import-independence countermodels.

### Governing Obligation
Treat the Hilbert carrier, inner product, and Born pairing as supplied inputs for every later finite step.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `complex field C (assumption)`
- **Admitted**: `complex scalars with modulus: lift`
- **Admitted**: `continuum Hilbert space (assumption)`
- **Admitted**: `square root field: lift`
- **Admitted**: `unit phases: lift`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> No Lean theorem for |c|^2 normalization over C found; BornNormalization.lean treats discrete 2x2 density / POVM. Rust exact_amplitudes returns None unless every p_j is a rational square.

> [!WARNING]
> Z[i] non-field obstruction and discriminant-5 spectral exit from Q(i) are mechanized; continuum Hilbert completion remains an explicit import.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/BornNormalization.lean::born_normalization_redundancy`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_gap_stone_rational_rotation_infinite_order_and_zi_non_field_obstruction`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm020_thm4_hilbert_lift_redundancy`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/FiniteQM.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs::born_weights`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs::exact_amplitudes`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_l1_to_l2_bridges_and_ladder_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche8_tensor_stone_continuum_embedding_and_leftover_mnc_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0235](../11_finite_qm_dynamics/TFQ-0235_selective_measurement_update_as_idempotent_conditioning.md)
- [TFQ-0239](../11_finite_qm_dynamics/TFQ-0239_finite_path_sum_on_a_unique_intermediate_cut.md)
- [TFQ-0251](../12_finite_qm_structure/TFQ-0251_superposition_as_a_quotient_fiber.md)
- [TFQ-0256](../12_finite_qm_structure/TFQ-0256_product_defect_on_a_bipartite_weight_table.md)
- [TFQ-0262](../12_finite_qm_structure/TFQ-0262_cptp_class_recorded_as_a_definition.md)
- [TFQ-0272](../13_finite_qm_information/TFQ-0272_interpretations_as_authority_shadows.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
