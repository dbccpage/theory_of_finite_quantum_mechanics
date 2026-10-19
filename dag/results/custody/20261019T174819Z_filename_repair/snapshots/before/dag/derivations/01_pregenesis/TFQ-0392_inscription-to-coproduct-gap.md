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

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-INERT-DIAMOND`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-INERT-DIAMOND` (`PREGENESIS` / `DEFINITION`)
- **Mined Operad Family (`M2`)**: `OP-PREGENESIS-PG-INERT-DIAMOND`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [370, -740, 555]`, `chord_potential = 555`, `holonomy_gamma2 = 740`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-INERT-DIAMOND): 4*idx(37) + 3*stage_rank(1) + route_degree(3) == 154` ($\text{value} = 154$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-INERT-DIAMOND): R_raw(79) - G_cob(39) - S_decoy(1) == 39 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 39$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = e0c9784cc655825ca2c144b9fda4055a20bf16bdfab616cda6f84de22acf6b67`

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-ROOT-DIFF-STRUCTURE`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-ROOT-DIFF-STRUCTURE` (`PREGENESIS` / `ADMITTED_PRIMITIVE`)
- **Mined Operad Family (`M2`)**: `OP-PREGENESIS-PG-ROOT-DIFF-STRUCTURE`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [360, -720, 540]`, `chord_potential = 540`, `holonomy_gamma2 = 720`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-ROOT-DIFF-STRUCTURE): 4*idx(36) + 3*stage_rank(1) + route_degree(4) == 151` ($\text{value} = 151$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-ROOT-DIFF-STRUCTURE): R_raw(77) - G_cob(38) - S_decoy(1) == 38 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 38$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche16_master_177_node_172_route_dag_completeness_and_operad_audit_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 99dcda861d27c22f53e0bc2d9bf8a58cc8ee851f5c84a144b3301fc634ca4eba`
