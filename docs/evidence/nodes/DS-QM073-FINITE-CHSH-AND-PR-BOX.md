# DS-QM073-FINITE-CHSH-AND-PR-BOX

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Every deterministic row, weighted correlation and PR entry is exact; deterministic CHSH and generic convex absolute bound are kernel checked.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Formalize the concrete table-to-general convex theorem transport and any full Fine converse or quantum realization. Product/separable for a bare classical table has a different meaning from quantum separability. The broader source statement is kept in pfp_review.prior_statement.

## Source status

P8-C3 single-table local rank-1 decomposition, P8-C6 16-vertex deterministic CHSH ceiling (|S|=2), P8-C7 PR-box S=4 non-extension, and P8-C8 rational/Tsirelson CHSH hierarchy (100 \< 196 \< 200 \< 400) mechanized in DerivationDagQMClosure.lean and mirrored in 006_finite_qm

## Review

- PFP review: [dag/results/DS-QM073-FINITE-CHSH-AND-PR-BOX/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM073-FINITE-CHSH-AND-PR-BOX/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Every deterministic row, weighted correlation and PR entry is exact; deterministic CHSH and generic convex absolute bound are kernel checked.
  - does not support: Formalize the concrete table-to-general convex theorem transport and any full Fine converse or quantum realization. Product/separable for a bare classical table has a different meaning from quantum separability.
  - next test: Formalize the concrete table-to-general convex theorem transport and any full Fine converse or quantum realization. Product/separable for a bare classical table has a different meaning from quantum separability.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ContextualityObstruction.lean`

- file: [lean4/ContextualityObstruction.lean](../../../lean4/ContextualityObstruction.lean)
- sha256 (`bytes`): `712a6a817e5b6991910e8e6ed1a394997262e62b71fc89908426866e60773627`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `ContextualityObstruction`): recorded sha256 `712a6a817e5b6991910e8e6ed1a394997262e62b71fc89908426866e60773627` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ContextualityObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `x1_has_no_global_section` | yes | yes | yes | Quot.sound, propext | `#print axioms x1_has_no_global_section` |
- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0259 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm073_074_chsh_pr_box_and_no_signaling_marginal` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm073_074_chsh_pr_box_and_no_signaling_marginal` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm073_bare_table_separability_single_joint_bound_and_pr_box_obstruction` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm073_bare_table_separability_single_joint_bound_and_pr_box_obstruction` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm073_bell_chsh_pythagorean_tsirelson_vs_pr_box_and_local_bound` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm073_bell_chsh_pythagorean_tsirelson_vs_pr_box_and_local_bound` |
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

### Rust: `omega_engine/crates_rs/tests/omega_quantum_physics/finite_bell_extension.rs`

- file: `omega_engine/crates_rs/tests/omega_quantum_physics/finite_bell_extension.rs`
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

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0259_finite_chsh_ceiling_on_one_global_joint_table.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0259_finite_chsh_ceiling_on_one_global_joint_table.md](../../../dag/derivations/12_finite_qm_structure/tfq_0259_finite_chsh_ceiling_on_one_global_joint_table.md)
- sha256 (`lf-normalised`): `b2177f05c11715d1dec037d5488c6c1e891d6c536e6fb4c875616087051c4c65`
- generated view: listed, not counted
- cited in: record TFQ-0259 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/073_correlation_separability_finite_bell/qm_073_correlation_separability_finite_bell_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/073_correlation_separability_finite_bell/qm_073_correlation_separability_finite_bell_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0259 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm
- TFQ-0259 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/finite_chsh_correlations.rs

## Routes

Incoming (1):

- `DS-R-ENTANGLEMENT-TO-BELL` `DERIVED_LEAN`: [DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS](DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS.md) (PROVED_LEAN)

Outgoing (2):

- `DS-R-BELL-THEOREM` `DERIVED_LEAN`: [DS-QM073-BELL-THEOREM-OBSTRUCTED](DS-QM073-BELL-THEOREM-OBSTRUCTED.md) (PROVED_LEAN)
- `DS-R-BELL-TO-NOSIGNALING` `DERIVED_LEAN`: [DS-QM074-NO-SIGNALING-MARGINAL](DS-QM074-NO-SIGNALING-MARGINAL.md) (PROVED_LEAN)
