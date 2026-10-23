# DS-QM090-093-O022-REGISTRY-RELATIVE-MINIMALITY

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The complex-Hilbert CPTP row meets the declared audit conditions and is minimal within the frozen seven-row O022 registry (six weaker candidates fail or refuse). MinimalInterface(R,F,w) does not imply minimality over all registries; witness \[5,7\].

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

None (O022 7-row registry-relative minimality and \[5, 7\] super-registry non-transfer witness mechanized in ds_qm090_093_o022_registry_minimality_and_tier3_pr_box_bridge and ds_qm090_093_o022_seven_row_registry_relative_minimality).

## Source status

O022 7-row capability registry unique selection of Row 6 (complex-Hilbert CPTP), \[5, 7\] super-registry non-transfer witness, and 24-ray (16 local + 8 PR-box) Tier-3 uniqueness boundary mechanized in DerivationDagQMClosure.lean and mirrored in 006_finite_qm

## Review

- PFP review: [dag/results/DS-QM090-093-O022-REGISTRY-RELATIVE-MINIMALITY/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/DS-QM090-093-O022-REGISTRY-RELATIVE-MINIMALITY/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: The frozen row conjunction and failure of rank minimality to transfer to an expanded registry are exact; the limited list/rank and Boolean statements are kernel checked.
  - does not support: Establish semantic capability evidence and a justified interface ordering before any physical minimality theorem. No all-registry or unique-QM minimality is proved.
  - next test: Establish semantic capability evidence and a justified interface ordering before any physical minimality theorem. No all-registry or unique-QM minimality is proved.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0273 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_o022_registry_minimality_and_tier3_pr_box_bridge` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_o022_registry_minimality_and_tier3_pr_box_bridge` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_o022_seven_row_registry_relative_minimality` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_o022_seven_row_registry_relative_minimality` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche18_ds_qm063_072_073_090_holonomy_bit_shadow_chsh_and_o022_closure_witness` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0273_finite_descent_of_an_imported_quantum_interface.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0273_finite_descent_of_an_imported_quantum_interface.md](../../../dag/derivations/12_finite_qm_structure/tfq_0273_finite_descent_of_an_imported_quantum_interface.md)
- sha256 (`lf-normalised`): `1463ba1ada7b6d51c89a0588d1ffffb7bc50584dcebf8eda5434b97e3fd2f715`
- generated view: listed, not counted
- cited in: record TFQ-0273 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/090_interpretations_as_authority_shadows/qm_090_interpretations_as_authority_shadows_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/090_interpretations_as_authority_shadows/qm_090_interpretations_as_authority_shadows_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/092_qm_typed_authority_boundary_suite/qm_092_qm_typed_authority_boundary_suite_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/092_qm_typed_authority_boundary_suite/qm_092_qm_typed_authority_boundary_suite_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/093_from_q_to_gtfoc_finite_descent_of_quantum_structure/qm_093_from_q_to_gtfoc_finite_descent_of_quantum_structure_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/093_from_q_to_gtfoc_finite_descent_of_quantum_structure/qm_093_from_q_to_gtfoc_finite_descent_of_quantum_structure_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `DS-R-AUTHORITY-TO-REGISTRY` `DERIVED_LEAN`: [DS-QM090-092-AUTHORITY-FIREWALL](DS-QM090-092-AUTHORITY-FIREWALL.md) (COMPUTATIONALLY_CHECKED)

Outgoing (2):

- `DS-R-SURVIVAL` `COMPUTED`: [DS-QM093-SURVIVAL-THEOREM](DS-QM093-SURVIVAL-THEOREM.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-UNIQUENESS` `DERIVED_LEAN`: [DS-QM090-093-QM-UNIQUENESS-TIER3](DS-QM090-093-QM-UNIQUENESS-TIER3.md) (PROVED_LEAN)
