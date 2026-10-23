# DS-QM094-EVERETT-RELATIVE-STATE-CONTACT

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Actual relative-state density, partial trace and expectation controls are exact; the scalar orthogonality and absolute-bound identities are kernel checked.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Prove the full tensor/partial-trace coordinate bridge and justify a physical record basis/probability rule. No branch selection or many-worlds ontology follows. The broader source statement is kept in pfp_review.prior_statement.

## Source status

QCE-C1..C12 Everett relative-state reduced-density record-overlap formula (off-diagonal c0*c1*r vanishing at r=0), Pythagorean isometric child-branch norm conservation, and global swap observable distinguishability vs diagonal collapse (4 != 2) mechanized in DerivationDagQMClosure.lean and mirrored in 006_finite_qm

## Review

- PFP review: [dag/results/DS-QM094-EVERETT-RELATIVE-STATE-CONTACT/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/DS-QM094-EVERETT-RELATIVE-STATE-CONTACT/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Actual relative-state density, partial trace and expectation controls are exact; the scalar orthogonality and absolute-bound identities are kernel checked.
  - does not support: Prove the full tensor/partial-trace coordinate bridge and justify a physical record basis/probability rule. No branch selection or many-worlds ontology follows.
  - next test: Prove the full tensor/partial-trace coordinate bridge and justify a physical record basis/probability rule. No branch selection or many-worlds ontology follows.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0276 (shared)
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm094_everett_reduced_state_overlap_isometric_refinement_and_collapse_refutation` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm094_everett_reduced_state_overlap_isometric_refinement_and_collapse_refutation` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm094_everett_relative_state_and_qm101_threshold_five_obligations` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm094_everett_relative_state_and_qm101_threshold_five_obligations` |
| `QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_phase_averaged_shadow_and_c10_pinching` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_phase_averaged_shadow_and_c10_pinching` |
- counts toward the grade: yes

### Lean: `sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`

- file: [sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean](../../../sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `a2ec0a203277c5c7b4bd71067351c574509c655c18bf0e08fe3c05a8005fc497`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm094_everett_reduced_state_overlap_isometric_refinement_and_collapse_refutation` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm094_everett_reduced_state_overlap_isometric_refinement_and_collapse_refutation` |
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
| `verify_tranche19_ds_qm062_094_101_206_u1_selector_everett_threshold_and_boundary_synthesis_witness` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/13_finite_qm_information/tfq_0276_everettian_relative_state_contact.md`

- file: [dag/derivations/13_finite_qm_information/tfq_0276_everettian_relative_state_contact.md](../../../dag/derivations/13_finite_qm_information/tfq_0276_everettian_relative_state_contact.md)
- sha256 (`lf-normalised`): `583ff49913bc4e3a3472d21eec5373c9d8e1894a59069f3181dd26c6557f4e41`
- generated view: listed, not counted
- cited in: record TFQ-0276 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/094_everettian_relative_state_contact/qm_094_everettian_relative_state_contact_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/094_everettian_relative_state_contact/qm_094_everettian_relative_state_contact_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0276 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm

## Routes

Incoming (1):

- `DS-R-EVERETT` `DERIVED_LEAN`: [DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE](DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE.md) (PROVED_LEAN), [DS-QM090-092-AUTHORITY-FIREWALL](DS-QM090-092-AUTHORITY-FIREWALL.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

