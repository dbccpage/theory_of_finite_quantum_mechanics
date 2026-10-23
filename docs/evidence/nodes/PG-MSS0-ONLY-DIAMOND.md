# PG-MSS0-ONLY-DIAMOND

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Genesis stage MSS-0: the only admissible node at stage 0 is the inscription \<\>; every other node needs stage \>= 1. The gate returns STRUCTURAL_ONLY, never mathematical or empirical certification.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Python profile gate only; no Rust or Lean counterpart found for 'MSS-0' (grep returned only Python and archive docs). The Rust analogue is GenesisConstruction::pre_genesis.

## Source status

MSS-0 admits only \<\> (Python tower profile gate)

## Review

- PFP review: [dag/results/PG-MSS0-ONLY-DIAMOND/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/PG-MSS0-ONLY-DIAMOND/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `consistent`; prior status `DEFINITION`; qualifies for E4: yes.
  - narrowest claim: Exact declared stage-zero/node eligibility controls and an explicit structural-only authority ceiling are kernel/native checked.
  - does not support: Connect these tags to the actual profile registry and separate real mathematical/empirical validation. This structural rule supplies no physical, proof or authority certificate.
  - next test: Connect these tags to the actual profile registry and separate real mathematical/empirical validation. This structural rule supplies no physical, proof or authority certificate.

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
| `QuantumMechanics.DerivationDagQMClosure.pg_gen_rewriting_commutation_and_obstruction_persistence` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_gen_rewriting_commutation_and_obstruction_persistence` |
| `QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation` |
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

### Python: `omega_engine_pfp/domain/tower/profile.py`

- file: `omega_engine_pfp/domain/tower/profile.py`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0377_mss0_only_inscription.md`

- file: [dag/derivations/02_genesis/tfq_0377_mss0_only_inscription.md](../../../dag/derivations/02_genesis/tfq_0377_mss0_only_inscription.md)
- sha256 (`lf-normalised`): `8564b7e593adaebe2309645580e778f9980141052d1cba432d2c5491a5d634cc`
- generated view: listed, not counted
- cited in: record TFQ-0377
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0377 lean4: missing declaration obligation: no MSS-0 name was seen in the opened Inertia.lean header
- TFQ-0377 lean4: no local lean twin located for lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean
- TFQ-0377 python: missing obligation: the tower profile cited by the DAG was not opened; a local stage-0 check is still required in 000_genesis_19l57g1/code/genesis_checks.py
- TFQ-0377 rust: missing obligation: an MSS-0 symbol was not confirmed in omega_ooutwire_primitives
- TFQ-0377 rust: no local rust twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/profile.rs

## Routes

Incoming (1):

- `PG-R-DIAMOND-TO-MSS0` `DERIVED_LEAN`: [PG-INERT-DIAMOND](PG-INERT-DIAMOND.md) (DEFINITION)

Outgoing (2):

- `PG-R-MSS0-TO-REGIME` `DERIVED_LEAN`: [PG-GEN-REGIME-EVENTS](PG-GEN-REGIME-EVENTS.md) (DEFINITION)
- `PGW-R-MSSN-ROWS-1-TO-6-SPECIFIED` `DERIVED_PROSE`: [PGW-MSSN-ROWS-1-TO-6-SPECIFIED](PGW-MSSN-ROWS-1-TO-6-SPECIFIED.md) (DEFINITION)
