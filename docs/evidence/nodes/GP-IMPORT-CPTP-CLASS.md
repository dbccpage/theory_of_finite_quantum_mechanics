# GP-IMPORT-CPTP-CLASS

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The class of completely positive trace-preserving maps. Collapse non-reversibility and failure of a same-basis isometry are not CPTP obstructions; exactly four reversible dilations of collapse exist under the declared convention that the ancilla starts at false.

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

- CPTP channel class: assumption
- ancilla prepared at false: declared convention

## Bottleneck

No derived channel class; QM_082 supplies stochastic-kernel population shadow only.

## Source status

imported; no channel class defined on the finite host

## Review

- PFP review: [dag/results/GP-IMPORT-CPTP-CLASS/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/GP-IMPORT-CPTP-CLASS/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Four actual reversible dilation maps/inverses and exact reset-channel Choi/TP/action arrays, with generic inverse and reset trace identities in Lean.
  - does not support: Prove the native-array-to-channel/dilation refinement and classify arbitrary CPTP maps under admitted complex Hilbert structure. The ancilla convention is essential.
  - next test: Prove the native-array-to-channel/dilation refinement and classify arbitrary CPTP maps under admitted complex Hilbert structure. The ancilla convention is essential.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1033
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries` |
- counts toward the grade: yes

### Lean: `lean4/H015CollapseDilations.lean`

- file: [lean4/H015CollapseDilations.lean](../../../lean4/H015CollapseDilations.lean)
- sha256 (`bytes`): `689bfa7562cf0a0205c346d902c8c2879b3ca0eaaee263a4fd4b4a3714f56bde`
- cited in: node.lean, record TFQ-1033
- replay: `none`
- check: `cd lean4 && lake build H015CollapseDilations`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `four_reversible_dilations_of_collapse` | yes | yes | yes | - | `#print axioms four_reversible_dilations_of_collapse` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1033
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1033_gp_import_cptp_class.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1033_gp_import_cptp_class.md](../../../dag/derivations/08_l1_to_l2/tfq_1033_gp_import_cptp_class.md)
- sha256 (`lf-normalised`): `62168678d1c7990bddc1cdb82ea0e24564a6d06628715e18085909b40d8a90fc`
- generated view: listed, not counted
- cited in: record TFQ-1033
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/claims/gap_register.yaml`

- file: `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/claims/gap_register.yaml`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/finite_hilbert_boundary_from_primitive_difference.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/finite_hilbert_boundary_from_primitive_difference.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (0):


Outgoing (2):

- `X-R-DROP-ONE-CENSUS` `DERIVED_LEAN`: [GP-DROP-ONE-CENSUS](GP-DROP-ONE-CENSUS.md) (PROVED_LEAN)
- `X-R-IMPORTS-TO-DECLARED-INTERFACE` `CONDITIONAL_ON_IMPORT`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

No incoming route.
