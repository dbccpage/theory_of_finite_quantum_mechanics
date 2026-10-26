# GP-IMPORT-CPTP-CLASS

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the labels false and true, collapse sends false to false and true to false, so those two labels have the same image. For every map inv on those labels, inv is not a two-sided inverse of collapse. For integers wF and wT, the mass image has first coordinate wF + wT and second coordinate 0, and those coordinates sum to wF + wT. If wF and wT are nonnegative, both image coordinates are nonnegative. The weights 2 and 3 have mass image (5, 0). The ancilla label is prepared at false. A reversible dilation is a pair of maps on label pairs that are mutual inverses and whose system coordinate on each prepared pair equals collapse of the system label. The four maps named by the Boolean swap pairs (false, false), (false, true), (true, false) and (true, true) are pairwise distinct. Each of those four maps is the forward map of a reversible dilation, and every reversible dilation agrees with one of those four maps at every label pair.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 22
- distinct cited Lean declarations covered by a current replay receipt: 11
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- CPTP channel class: assumption
- ancilla prepared at false: declared convention

## Bottleneck

The class of completely positive trace-preserving maps on a Hilbert space is not derived. Choi positivity, Kraus form and a Stinespring realization of that class stay imported. The Boolean collapse, the integer mass image and the four ancilla-false reversible dilations are one finite case. This mass image is a stochastic-kernel population shadow in the sense of QM_082, and it is not that channel class.

## Source status

imported; no channel class defined on the finite host

## Review

- PFP review: [dag/results/GP-IMPORT-CPTP-CLASS/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/GP-IMPORT-CPTP-CLASS/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Four actual reversible dilation maps/inverses and exact reset-channel Choi/TP/action arrays, with generic inverse and reset trace identities in Lean.
  - does not support: Prove the native-array-to-channel/dilation refinement and classify arbitrary CPTP maps under admitted complex Hilbert structure. The ancilla convention is essential.
  - next test: Prove the native-array-to-channel/dilation refinement and classify arbitrary CPTP maps under admitted complex Hilbert structure. The ancilla convention is essential.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignGpImportCptpClass.lean`

- file: [lean4/CampaignGpImportCptpClass.lean](../../../lean4/CampaignGpImportCptpClass.lean)
- sha256 (`bytes`): `5667a581f964eb7babec906cc92c49ea4dd4c859a71a49fdc4327c812fcf54b7`
- cited in: node.lean, receipt dag/research/campaign_gp-import-cptp-class_lean_replay.json (CampaignGpImportCptpClass), record TFQ-1033
- replay: `verified`
  - receipt [dag/research/campaign_gp-import-cptp-class_lean_replay.json](../../../dag/research/campaign_gp-import-cptp-class_lean_replay.json) (module `CampaignGpImportCptpClass`): recorded sha256 `5667a581f964eb7babec906cc92c49ea4dd4c859a71a49fdc4327c812fcf54b7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignGpImportCptpClass`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignGpImportCptpClass.collapseMass_coords` | yes | yes | yes | none | `#print axioms CampaignGpImportCptpClass.collapseMass_coords` |
| `CampaignGpImportCptpClass.collapseMass_nonneg` | yes | yes | yes | propext | `#print axioms CampaignGpImportCptpClass.collapseMass_nonneg` |
| `CampaignGpImportCptpClass.collapseMass_preserves_sum` | yes | yes | yes | none | `#print axioms CampaignGpImportCptpClass.collapseMass_preserves_sum` |
| `CampaignGpImportCptpClass.collapseMass_two_three` | yes | yes | yes | none | `#print axioms CampaignGpImportCptpClass.collapseMass_two_three` |
| `CampaignGpImportCptpClass.collapse_both_false` | yes | yes | yes | none | `#print axioms CampaignGpImportCptpClass.collapse_both_false` |
| `CampaignGpImportCptpClass.collapse_labels_agree` | yes | yes | yes | none | `#print axioms CampaignGpImportCptpClass.collapse_labels_agree` |
| `CampaignGpImportCptpClass.collapse_no_two_sided_inverse` | yes | yes | yes | none | `#print axioms CampaignGpImportCptpClass.collapse_no_two_sided_inverse` |
| `CampaignGpImportCptpClass.every_dilation_agrees` | yes | yes | yes | propext | `#print axioms CampaignGpImportCptpClass.every_dilation_agrees` |
| `CampaignGpImportCptpClass.four_maps_pairwise_unequal` | yes | yes | yes | none | `#print axioms CampaignGpImportCptpClass.four_maps_pairwise_unequal` |
| `CampaignGpImportCptpClass.four_named_are_dilations` | yes | yes | yes | none | `#print axioms CampaignGpImportCptpClass.four_named_are_dilations` |
| `CampaignGpImportCptpClass.prepared_is_false` | yes | yes | yes | none | `#print axioms CampaignGpImportCptpClass.prepared_is_false` |
| `collapseMass_coords` | yes | yes | yes | none | `#print axioms collapseMass_coords` |
| `collapseMass_nonneg` | yes | yes | yes | propext | `#print axioms collapseMass_nonneg` |
| `collapseMass_preserves_sum` | yes | yes | yes | none | `#print axioms collapseMass_preserves_sum` |
| `collapseMass_two_three` | yes | yes | yes | none | `#print axioms collapseMass_two_three` |
| `collapse_both_false` | yes | yes | yes | none | `#print axioms collapse_both_false` |
| `collapse_labels_agree` | yes | yes | yes | none | `#print axioms collapse_labels_agree` |
| `collapse_no_two_sided_inverse` | yes | yes | yes | none | `#print axioms collapse_no_two_sided_inverse` |
| `every_dilation_agrees` | yes | yes | yes | propext | `#print axioms every_dilation_agrees` |
| `four_maps_pairwise_unequal` | yes | yes | yes | none | `#print axioms four_maps_pairwise_unequal` |
| `four_named_are_dilations` | yes | yes | yes | none | `#print axioms four_named_are_dilations` |
| `prepared_is_false` | yes | yes | yes | none | `#print axioms prepared_is_false` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1033
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1033_gp_import_cptp_class.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1033_gp_import_cptp_class.md](../../../dag/derivations/08_l1_to_l2/tfq_1033_gp_import_cptp_class.md)
- sha256 (`lf-normalised`): `b8c80e5a9e52ca3b063800278b252122c5dffa295f08cb2d9538eab6eae8d644`
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
