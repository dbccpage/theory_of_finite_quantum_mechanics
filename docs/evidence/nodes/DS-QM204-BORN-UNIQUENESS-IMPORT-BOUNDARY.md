# DS-QM204-BORN-UNIQUENESS-IMPORT-BOUNDARY

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Born-quadratic uniqueness (Gleason) is imported; L^p pairings for p != 2 are valid in L1 measure theory. The dedicated 204 slot is empty.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Gleason-type uniqueness hypotheses (assumption)

## Bottleneck

No derivation of quadratic uniqueness from L1 additivity.

## Source status

QM_204 ledger: stub "Band slot reserved" (QM_204-C0); content carried by QM-210-C3 and QM206-C5 \[STANDARD\]

## Review

- PFP review: [dag/results/DS-QM204-BORN-UNIQUENESS-IMPORT-BOUNDARY/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/DS-QM204-BORN-UNIQUENESS-IMPORT-BOUNDARY/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Exact normalized alternative profiles, quadratic rotation identity and a genuine Born/quartic divergence are kernel/native checked on the declared rational carrier.
  - does not support: Supply frame-function/effect/continuity/dimension hypotheses and a uniqueness theorem. Bare normalization does not derive Born pairing.
  - next test: Supply frame-function/effect/continuity/dimension hypotheses and a uniqueness theorem. Bare normalization does not derive Born pairing.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1043
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall` |
- counts toward the grade: yes

### Lean: `lean4/GleasonTheorem.lean`

- file: [lean4/GleasonTheorem.lean](../../../lean4/GleasonTheorem.lean)
- sha256 (`bytes`): `881e01ee20e9af8f1d0f184edb5062447928fc98916c7a18f546d700fc839343`
- cited in: node.lean, record TFQ-1043
- replay: `none`
- check: `cd lean4 && lake build GleasonTheorem`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `d2_binary_non_bornian_obstruction` | yes | yes | yes | - | `#print axioms d2_binary_non_bornian_obstruction` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1043
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_1043_ds_qm204_born_uniqueness_import_boundary.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_1043_ds_qm204_born_uniqueness_import_boundary.md](../../../dag/derivations/12_finite_qm_structure/tfq_1043_ds_qm204_born_uniqueness_import_boundary.md)
- sha256 (`lf-normalised`): `b635491a2c7c79e97d8e06e501d4004ba89a67d86c64a34155e54a43513da471`
- generated view: listed, not counted
- cited in: record TFQ-1043
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/204_born_uniqueness_import_boundary/qm_204_born_uniqueness_import_boundary_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/204_born_uniqueness_import_boundary/qm_204_born_uniqueness_import_boundary_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/206_universal_boundary_synthesis_and_cochain_lift/qm_206_universal_boundary_synthesis_and_cochain_lift_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/206_universal_boundary_synthesis_and_cochain_lift/qm_206_universal_boundary_synthesis_and_cochain_lift_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/210_born_rule_postulate_and_state_effect_pairing/qm_210_born_rule_postulate_and_state_effect_pairing_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/210_born_rule_postulate_and_state_effect_pairing/qm_210_born_rule_postulate_and_state_effect_pairing_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (0):


Outgoing (2):

- `DS-R-BORN-IMPORT` `DERIVED_LEAN`: [DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT](DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT.md) (IMPORTED_ASSUMPTION)
- `DS-R-FIVE-IMPORT` `COMPUTED`: [DS-QM207-211-FIVE-IMPORT-CASCADE](DS-QM207-211-FIVE-IMPORT-CASCADE.md) (COMPUTATIONALLY_CHECKED)

No incoming route.
