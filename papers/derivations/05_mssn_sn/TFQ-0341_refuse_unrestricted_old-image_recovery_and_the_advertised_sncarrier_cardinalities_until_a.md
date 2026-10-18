# [TFQ-0341] Refuse unrestricted old-image recovery and the advertised SnCarrier cardinalities until a

> **Stage**: `MSSN_SN` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `c9187b59-bdf9-5513-961b-7ef37d149674`  
> **Parent Derivation**: [TFQ-0335](TFQ-0335_from_typed_old-image_recovery_record_injectivity_of_the_lift_only_and_refuse.md)

---

## 1. Abstract & Formal Statement

WDP-P001-019 is a negative boundary: the pinned SnCarrier implementation does not establish unrestricted old-image recovery or its advertised carrier cardinalities. Domain restriction and a corrected cardinality theorem remain open. The ledger names SnCarrierDischarge.lean, which is present beside Paper001.lean, and says it imports the education SnCarrier module. DAG node PG-SN-CARRIER records the same tension: Pre-Genesis section 10 presents the education carrier as corrected, while this ledger row says it is defective. The node bottleneck leaves off-image refusal and the advertised cardinalities unestablished.

### Governing Obligation
Refuse unrestricted old-image recovery and the advertised SnCarrier cardinalities until a corrected finite cardinality statement is supplied.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Classical.choice in old_image_base (assumption: found in axiom report, against the Fable 05 expectation)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Off-image refusal and the advertised carrier cardinalities are not established (PG-SN-OFF-IMAGE-REFUSAL).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_to_sn_and_wdp_route_chain_composition`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/SnCarrier.lean::BasePresentation`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/SnCarrier.lean::RetractOutcome`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/SnCarrier.lean::retractionDownMap`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/SnCarrier.lean::sectionLift`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/SnTheorems.lean::ground_carrier_empty`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/SnTheorems.lean::old_image_base`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/SnCarrierDischarge.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_category_theory/src/mssn_functor_bridge.rs::MssnFunctorBridge`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/code/sn_mssn_checks.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0342](TFQ-0342_do_not_treat_genesis_events_or_s_n_maps_as_obligation-monoid_morphisms_until.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
