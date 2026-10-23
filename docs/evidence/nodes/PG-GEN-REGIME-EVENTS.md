# PG-GEN-REGIME-EVENTS

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A Genesis regime is a tuple of admitted data, forms, instances, rules and requirements; state changes only through admission events or impose; supply is an external presentation event.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

none for the definition. Mapping of these events to obligation-vector morphisms is not derived (PG-GAP-EVENT-OBLIGATION).

## Source status

Regime R=(D,F,I,U,Q) and events supply/admitDatum/admitForm/admitInst/admitRuleAll/impose (Genesis §6)

## Review

- PFP review: [dag/results/PG-GEN-REGIME-EVENTS/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/PG-GEN-REGIME-EVENTS/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `consistent`; prior status `DEFINITION`; qualifies for E4: yes.
  - narrowest claim: Actual finite event/replay guards and complete state fields are retained; generic history composition and admitted-step evaluation are kernel checked.
  - does not support: Prove the full interpreter-to-source Regime equivalence and any event-to-obligation-vector transport. A declared event schema is not a derived physical or authority mechanism.
  - next test: Prove the full interpreter-to-source Regime equivalence and any event-to-obligation-vector transport. A declared event schema is not a derived physical or authority mechanism.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation` |
| `QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure` |
| `QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation` |
- counts toward the grade: yes

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean)
- sha256 (`bytes`): `9386f41cf6bbefae8ccb8fdae47f69a33140a0c45b3e6ca9a08f1e9596a922a7`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Inertia`): recorded sha256 `9386f41cf6bbefae8ccb8fdae47f69a33140a0c45b3e6ca9a08f1e9596a922a7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `supply_no_op` | yes | yes | yes | propext | `#print axioms supply_no_op` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/genesis_construction.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/genesis_construction.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0002_genesis_regime_events_as_a_separate_admission_record.md`

- file: [dag/derivations/02_genesis/tfq_0002_genesis_regime_events_as_a_separate_admission_record.md](../../../dag/derivations/02_genesis/tfq_0002_genesis_regime_events_as_a_separate_admission_record.md)
- sha256 (`lf-normalised`): `877686e085ad0b56189b726c321055eb7a37b30a3c74fa83a4319b2ab00bd04c`
- generated view: listed, not counted
- cited in: record TFQ-0002
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0378_regime_tuple_and_events.md`

- file: [dag/derivations/02_genesis/tfq_0378_regime_tuple_and_events.md](../../../dag/derivations/02_genesis/tfq_0378_regime_tuple_and_events.md)
- sha256 (`lf-normalised`): `c0c1350ab74a70fbfef1aff3948eeb360e6c203b2306ad63ed19cc96750d582e`
- generated view: listed, not counted
- cited in: record TFQ-0378
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0342_do_not_treat_genesis_events_or_s_n_maps_as_obligation_monoid_morphisms_until.md`

- file: [dag/derivations/05_mssn_sn/tfq_0342_do_not_treat_genesis_events_or_s_n_maps_as_obligation_monoid_morphisms_until.md](../../../dag/derivations/05_mssn_sn/tfq_0342_do_not_treat_genesis_events_or_s_n_maps_as_obligation_monoid_morphisms_until.md)
- sha256 (`lf-normalised`): `3c5506026eeada78ccc327f0bd2ee297d044bb4e3c6fc875975ee080d25bacb1`
- generated view: listed, not counted
- cited in: record TFQ-0342 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0342 rust: no local rust twin located for omega_engine/crates_rs/omega_kernel/src/obligation.rs
- TFQ-0378 lean4: declaration obligation: genesis as the five-field empty regime, events still to be matched to the ledger families
- TFQ-0378 lean4: no local lean twin located for lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean
- TFQ-0378 python: missing obligation: model.py was listed and not opened; the five regime fields still need a local check against WDP-P000-006
- TFQ-0378 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/model.py
- TFQ-0378 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py
- TFQ-0378 rust: no local rust twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/event.rs
- TFQ-0378 rust: no local rust twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/regime.rs

## Routes

Incoming (1):

- `PG-R-MSS0-TO-REGIME` `DERIVED_LEAN`: [PG-MSS0-ONLY-DIAMOND](PG-MSS0-ONLY-DIAMOND.md) (DEFINITION), [PG-SIX-OPERATIONS](PG-SIX-OPERATIONS.md) (DEFINITION)

Outgoing (11):

- `GTH-R-GTH-LANG-CORE` `GAP_NO_DERIVATION`: [GTH-LANG-CORE](GTH-LANG-CORE.md) (OPEN)
- `PG-R-FIRST-SEPARATION` `COMPUTED`: [PG-GEN-COLLAPSE-AND-FIRST-SEPARATION](PG-GEN-COLLAPSE-AND-FIRST-SEPARATION.md) (COMPUTATIONALLY_CHECKED)
- `PG-R-GAP-EVENT-OBLIGATION` `DERIVED_LEAN`: [PG-OBLIGATION-MONOID](PG-OBLIGATION-MONOID.md) (PROVED_LEAN)
- `PG-R-GENESIS-TO-WDP` `GAP_NO_DERIVATION`: [PG-WDP-GENESIS-BRIDGE-OBLIGATIONS](PG-WDP-GENESIS-BRIDGE-OBLIGATIONS.md) (OPEN)
- `PG-R-IRREFLEXIVE` `DERIVED_LEAN`: [PG-GEN-IRREFLEXIVE-DISTINCT](PG-GEN-IRREFLEXIVE-DISTINCT.md) (PROVED_LEAN)
- `PG-R-SIX-OPS-TO-SUPPLY` `DERIVED_LEAN`: [PG-GEN-SUPPLY-NO-OP](PG-GEN-SUPPLY-NO-OP.md) (PROVED_LEAN)
- `PG-R-SUPPLY-ERASURE` `DERIVED_LEAN`: [PG-GEN-SUPPLY-ERASURE](PG-GEN-SUPPLY-ERASURE.md) (PROVED_LEAN)
- `PGW-R-METATHEORY-OBJECT-LANGUAGE-SPLIT` `DERIVED_PROSE`: [PGW-METATHEORY-OBJECT-LANGUAGE-SPLIT](PGW-METATHEORY-OBJECT-LANGUAGE-SPLIT.md) (DEFINITION)
- `PGW-R-REGIME-ISOMORPHISM-UNORDERED-PAIRS` `DERIVED_PROSE`: [PGW-REGIME-ISOMORPHISM-UNORDERED-PAIRS](PGW-REGIME-ISOMORPHISM-UNORDERED-PAIRS.md) (DEFINITION)
- `UDG-R-TFQ-0003` `GAP_NO_DERIVATION`: [TFQ-0003](TFQ-0003.md) (OPEN)
- `UDG-R-TFQ-0319` `GAP_NO_DERIVATION`: [TFQ-0319](TFQ-0319.md) (OPEN)
