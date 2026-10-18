# [TFQ-0342] Do not treat Genesis events or S(n) maps as obligation-monoid morphisms until

> **Stage**: `MSSN_SN` | **Status**: `GAP`  
> **UUID**: `3bacec47-5461-5c31-ba47-95841ac1503a`  
> **Parent Derivation**: [TFQ-0341](TFQ-0341_refuse_unrestricted_old-image_recovery_and_the_advertised_sncarrier_cardinalities_until_a.md)

---

## 1. Abstract & Formal Statement

The pregenesis segment note in derivation_dag.json still says no source opened there derives Genesis events or S(n) maps as morphisms carrying generated and discharged obligation vectors in the free commutative monoid. The monoid is present as Rust in omega_kernel/src/obligation.rs: Obligations is a BTreeMap of ObligationId to positive counts, with empty, single, of, and combine, and ObligationError for never-generated and over-discharge. Node PG-OBLIGATION-MONOID says Genesis morphisms are meant to carry those vectors. The later route label is not adopted; the join stays open.

### Governing Obligation
Do not treat Genesis events or S(n) maps as obligation-monoid morphisms until generated and discharged vectors are derived, not only implemented.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Classical.choice in old_image_base (assumption: found in axiom report, against the Fable 05 expectation)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Mechanized for finite Genesis event traces and the commutative 3-counter obligation monoid.

> [!WARNING]
> none for the definition. Mapping of these events to obligation-vector morphisms is not derived (PG-GAP-EVENT-OBLIGATION).

> [!WARNING]
> Off-image refusal and the advertised carrier cardinalities are not established (PG-SN-OFF-IMAGE-REFUSAL).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.declare_then_assert_cost_floor`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.traceObligation_append`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean::supply_no_op`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/SnCarrier.lean::BasePresentation`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/SnCarrier.lean::RetractOutcome`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/SnCarrier.lean::retractionDownMap`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/SnCarrier.lean::sectionLift`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/SnTheorems.lean::ground_carrier_empty`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/SnTheorems.lean::old_image_base`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_category_theory/src/mssn_functor_bridge.rs::MssnFunctorBridge`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_kernel/src/obligation.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_kernel/src/obligation.rs::ObligationError`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_kernel/src/obligation.rs::ObligationId`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_kernel/src/obligation.rs::Obligations`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_wdp_obligations_and_growth_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/genesis_construction.rs::interpret_event`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/genesis_construction.rs::interpret_regime`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0343](../06_wdp/TFQ-0343_leave_gen-wdp-o01_through_o05_open_carrier_floor_preservation_maps_higher_fillers_hilbert.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
