# GP-IMPORT-CPTP-CLASS

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The class of completely positive trace-preserving maps. Collapse non-reversibility and failure of a same-basis isometry are not CPTP obstructions; exactly four reversible dilations of collapse exist under the declared convention that the ancilla starts at false.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 24
- distinct cited Lean declarations covered by a current replay receipt: 12
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

- PFP review: [dag/results/GP-IMPORT-CPTP-CLASS/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/GP-IMPORT-CPTP-CLASS/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Four actual reversible dilation maps/inverses and exact reset-channel Choi/TP/action arrays, with generic inverse and reset trace identities in Lean.
  - does not support: Prove the native-array-to-channel/dilation refinement and classify arbitrary CPTP maps under admitted complex Hilbert structure. The ancilla convention is essential.
  - next test: Prove the native-array-to-channel/dilation refinement and classify arbitrary CPTP maps under admitted complex Hilbert structure. The ancilla convention is essential.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CollapseDilations.lean`

- file: [lean4/CollapseDilations.lean](../../../lean4/CollapseDilations.lean)
- sha256 (`bytes`): `5e215575a05df32a74179ff48601a40c0f1d186b2dfbe27898f65427da720bae`
- cited in: node.lean, record TFQ-1033
- replay: `none`
- check: `cd lean4 && lake build CollapseDilations`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `four_reversible_dilations_of_collapse` | yes | yes | yes | - | `#print axioms four_reversible_dilations_of_collapse` |

- counts toward the grade: yes

### Lean: `lean4/CptpClassImport.lean`

- file: [lean4/CptpClassImport.lean](../../../lean4/CptpClassImport.lean)
- sha256 (`bytes`): `41e95e8f13e33696903397f4e7c50947122e33119eb7aa0a56189f4273cba409`
- cited in: node.lean, receipt dag/research/campaign_gp-import-cptp-class_lean_replay.json (CptpClassImport), record TFQ-1033
- replay: `verified`
  - receipt [dag/research/campaign_gp-import-cptp-class_lean_replay.json](../../../dag/research/campaign_gp-import-cptp-class_lean_replay.json) (module `CptpClassImport`): recorded sha256 `41e95e8f13e33696903397f4e7c50947122e33119eb7aa0a56189f4273cba409` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build CptpClassImport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CptpClassImport.collapseMass_coords` | yes | yes | yes | none | `#print axioms CptpClassImport.collapseMass_coords` |
| `CptpClassImport.collapseMass_nonneg` | yes | yes | yes | propext | `#print axioms CptpClassImport.collapseMass_nonneg` |
| `CptpClassImport.collapseMass_preserves_sum` | yes | yes | yes | none | `#print axioms CptpClassImport.collapseMass_preserves_sum` |
| `CptpClassImport.collapseMass_two_three` | yes | yes | yes | none | `#print axioms CptpClassImport.collapseMass_two_three` |
| `CptpClassImport.collapse_both_false` | yes | yes | yes | none | `#print axioms CptpClassImport.collapse_both_false` |
| `CptpClassImport.collapse_labels_agree` | yes | yes | yes | none | `#print axioms CptpClassImport.collapse_labels_agree` |
| `CptpClassImport.collapse_no_two_sided_inverse` | yes | yes | yes | none | `#print axioms CptpClassImport.collapse_no_two_sided_inverse` |
| `CptpClassImport.every_dilation_agrees` | yes | yes | yes | propext | `#print axioms CptpClassImport.every_dilation_agrees` |
| `CptpClassImport.four_maps_pairwise_unequal` | yes | yes | yes | none | `#print axioms CptpClassImport.four_maps_pairwise_unequal` |
| `CptpClassImport.four_named_are_dilations` | yes | yes | yes | none | `#print axioms CptpClassImport.four_named_are_dilations` |
| `CptpClassImport.prepared_is_false` | yes | yes | yes | none | `#print axioms CptpClassImport.prepared_is_false` |
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

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1033
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1033_gp_import_cptp_class.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1033_gp_import_cptp_class.md](../../../dag/derivations/08_l1_to_l2/tfq_1033_gp_import_cptp_class.md)
- sha256 (`lf-normalised`): `c449d815d6c89506c7edd3e7963d80bde0b44ab792a06790dc23d281dadd577e`
- generated view: listed, not counted
- cited in: record TFQ-1033
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:49250fc3940b574236fe8aeb8acabb9673af35fe28f17474e9deb52ecd18a713#GAP-F001-S000-007`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`
- `external:sha256:f4ef85f405ba846ddf92fd6bbd8fc7aaa86d658c4678b4b841989f2cb97ee004:155`
- `external:sha256:f4ef85f405ba846ddf92fd6bbd8fc7aaa86d658c4678b4b841989f2cb97ee004:205`

## Routes

Incoming (0):


Outgoing (2):

- `X-R-DROP-ONE-CENSUS` `DERIVED_LEAN`: [GP-DROP-ONE-CENSUS](GP-DROP-ONE-CENSUS.md) (PROVED_LEAN)
- `X-R-IMPORTS-TO-DECLARED-INTERFACE` `CONDITIONAL_ON_IMPORT`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

No incoming route.
