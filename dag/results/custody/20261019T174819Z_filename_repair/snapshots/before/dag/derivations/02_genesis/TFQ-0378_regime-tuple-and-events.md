# [TFQ-0378] regime-tuple-and-events

> **Stage**: `GENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `19d39f52-4c98-56a2-a56f-322ef9c7a0c7`  
> **Parent Derivation**: [TFQ-0377](TFQ-0377_mss0-only-inscription.md)

---

## 1. Abstract & Formal Statement

PG-GEN-REGIME-EVENTS and ledger row WDP-P000-006 describe a Genesis regime as admitted data, forms, instances, rules, and requirements, with state changes only through admission events or impose. Supply stays an external presentation event. Genesis paper.md section 6 is the heading. Derivation/Inertia.lean, which was opened, defines genesis as a regime with five empty or zero fields. The finite statement still required is those five fields and the named event families, with positive form arities and deduplicating token admissions kept as extra clauses from the ledger, not as consequences of the inscription.

### Governing Obligation
A Genesis regime is five admitted components, and the regime changes only by admission events or impose, while supply stays external.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> none for the definition. Mapping of these events to obligation-vector morphisms is not derived (PG-GAP-EVENT-OBLIGATION).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`declaration obligation: genesis as the five-field empty regime, events still to be matched to the ledger families`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean::supply_no_op`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/genesis_construction.rs::interpret_event`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/genesis_construction.rs::interpret_regime`](../../code/rust/src/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/event.rs`](../../code/rust/src/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/regime.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: model.py was listed and not opened; the five regime fields still need a local check against WDP-P000-006`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/model.py`](../../code/python/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0379](TFQ-0379_supply-does-not-admit.md)
- [TFQ-0387](TFQ-0387_irreflexive-endpoints-distinct.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/floor.yaml`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-GEN-REGIME-EVENTS`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-GEN-REGIME-EVENTS` (`GENESIS` / `DEFINITION`)
- **Mined Operad Family (`M2`)**: `OP-GENESIS-PG-GEN-REGIME-EVENTS`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [510, -1020, 765]`, `chord_potential = 765`, `holonomy_gamma2 = 1020`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-GEN-REGIME-EVENTS): 4*idx(51) + 3*stage_rank(2) + route_degree(8) == 218` ($\text{value} = 218$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-GEN-REGIME-EVENTS): R_raw(112) - G_cob(55) - S_decoy(2) == 55 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 55$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = a0fff983bb56b7c86377021f8aa8cbe76529ef223ebea8a0707e15309bf02637`
