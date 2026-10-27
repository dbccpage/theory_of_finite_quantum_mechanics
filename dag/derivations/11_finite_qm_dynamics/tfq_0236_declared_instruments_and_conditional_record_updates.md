# [TFQ-0236] Declared instruments and conditional record updates

> **Stage**: `FINITE_QM_DYNAMICS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `6672005d-e1b6-5ff2-bb3c-da0b1c3e8937`  
> **Parent Derivation**: [TFQ-0235](tfq_0235_selective_measurement_update_as_idempotent_conditioning.md)

---

## 1. Abstract & Formal Statement

Finite Quantum Mechanics section 13.3, after the Hilbert carrier is supplied, obliges an instrument to be a family of completely positive maps indexed by record labels, with Kraus operators summing to the identity in the adjoint form stated there. Outcome weights use the supplied trace pairing, and the conditional state is the branch divided by a positive probability. A zero-probability branch has no normalized state. Projective instruments recover a Luders update and an idempotent non-selective dephasing channel; general instruments need not be projective, repeatable, or idempotent.

### Governing Obligation
Record conditional updating from a declared instrument and pairing, without treating that update as the occurrence of one event.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `declared outcome partition (observer-relative) (assumption)`
- **Admitted**: `probability pairing and normalization (assumption)`
- **Admitted**: `projection postulate / spectral structure (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean mechanization targeted, not delivered (PL-QM037-1); incompatible measurements out of scope (C9).

> [!WARNING]
> Overlaps L1_TO_L2 Born nodes (QM_020, other fragment).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm021_idempotent_conditioning_and_order_sensitivity`](../../code/lean4/)
- [`lean4/quantum_mechanics/GleasonTheorem.lean::d2_binary_non_bornian_obstruction`](../../code/lean4/)
- [`lean4/quantum_mechanics/H013BornPairingBoundary.lean::born_pairing_boundary`](../../code/lean4/)
- [`sources/atlas/papers/finite_quantum_mechanics/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:6391572c23248195d97785667c444e6f67da73cab83285825dc16d94e998598b`](../../code/rust/src/)
- [`external:sha256:4fbc6b0667894450336cabb7dd92392cca1592abb3feb809e1fff47ee1281cec`](../../code/rust/src/)
- [`external:sha256:32bcf706711e8c0460831c97a9d55d8e64bb3ba66c27d70d4d64695823902525`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_ds_qm_dynamics_structure_and_majorana_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`sources/atlas/papers/finite_quantum_mechanics/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0237](tfq_0237_measurement_problem_slot_left_undeclared.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT` (`FINITE_QM_STRUCTURE` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-DS-PROJECTION-POSTULATE-BOUNDARY`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [170, -340, 255]`, `chord_potential = 255`, `holonomy_gamma2 = 340`
- **Finite Shadow Exact Witness (`M4`)**: `idempotent_repeat_stability: E(E(v)) == E(v) with trace 1 + 0 == 1` ($\text{value} = 1$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `sequential_order_sensitivity_defect: |(P_z P_x - P_x P_z)|_entry_sq == 4 (order sensitivity requires non-commuting projector algebra)` ($\text{value} = 4$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 2c867b3d2d5a91a4dc5e8116fad497573f2f6864492728764f1585f9d9216c7e`
