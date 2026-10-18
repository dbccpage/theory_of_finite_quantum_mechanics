# [TFQ-0392] inscription-to-coproduct-gap

> **Stage**: `PREGENESIS` | **Status**: `GAP`  
> **UUID**: `8a681ea8-7206-52a3-8a47-7d89a93dfef8`  
> **Parent Derivation**: [TFQ-0361](TFQ-0361_inert-literal-inscription.md)

---

## 1. Abstract & Formal Statement

Route PG-R-GAP-DIAMOND-TO-ROOT in derivation_dag.json is marked GAP_NO_DERIVATION from PG-INERT-DIAMOND to PG-ROOT-DIFF-STRUCTURE. The opened reading note says no source derives the admitted root Difference joined with Structure from the inscription <>, and that the root is defined separately. Pre-Genesis paper.md section 1 states the opposite of that identification: the inscription stays inert. The finite statement still required is an explicit refusal, not a bridge term, between the host token for <> and any coproduct of two channels. This node does not supply that bridge.

### Governing Obligation
Leave open, with no mediating term, the passage from literal <> to Difference joined with Structure.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Primitive difference delta_0 (assumption: admitted primitive)`
- **Admitted**: `Structure carrier (assumption: declared, not derived)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The brief's identification '<> = admitted root Difference ⊔ Structure' has no derivation or definition in the Pre-Genesis/Genesis papers; they state the opposite (inert). See PG-GAP route and notes.

> [!WARNING]
> Admitted, not derived. Two sources mark the lineage withdrawn/unassigned (ENC-1138 layer_withdrawn 2026-08-18). The coproduct is not connected by any derivation to the literal inscription <> (see PG-INERT-DIAMOND).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation`](../../code/lean4/)
- [`missing declaration obligation: no arrow in 000_pre_genesis_to_mssn/lean4/Paper.lean from a literal inscription to a coproduct root`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/GenesisConstruction.lean::literalRoot`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/029_the_anomalon_boundary/lean4/OntologyBasic.lean::Real0`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: a refused conversion in omega_ooutwire_primitives from the inscription token to a Difference-Structure value`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_types/src/primitive_difference.rs::PrimitiveDifference`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/genesis_construction.rs::GenesisConstruction`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: a negative check that no function in 000_pre_genesis_to_mssn/code/preservation.py sends literal <> to a two-channel coproduct`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0393](TFQ-0393_admitted-root-coproduct.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000`, `F000.S000:000_from_primitive_difference_to_finite_obstruction_calculus`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F000_finite/S000_primitive_difference_and_finite_obstruction/000_from_primitive_difference_to_finite_obstruction_calculus/book/ch01_genesis_of_difference.md`
