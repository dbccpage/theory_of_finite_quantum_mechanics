# MAJ-IMPORT-COSET-WEIGHT-NP-HARD

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Minimum-weight coset decoding of a binary linear code given by its matrix is NP-hard (Berlekamp, McEliece and van Tilborg 1978).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 19
- distinct cited Lean declarations covered by a current replay receipt: 9
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Berlekamp-McEliece-van Tilborg 1978 hardness of coset weights

## Bottleneck

Berlekamp, McEliece and van Tilborg 1978 remains an imported literature claim. No reduction is formalized. The 2 by 4 enumeration is one matrix and one syndrome and does not discharge hardness for a general binary matrix.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-IMPORT-BMVT claims IMPORTED_ASSUMPTION; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignMajImportCosetWeight.lean`

- file: [lean4/CampaignMajImportCosetWeight.lean](../../../lean4/CampaignMajImportCosetWeight.lean)
- sha256 (`bytes`): `29b2497864b3b9c7e9b9500c6c90cbb902df4b81029253c70acc2923d1971008`
- cited in: node.lean, receipt dag/research/campaign_maj-import-coset-weight-np-hard_lean_replay.json (CampaignMajImportCosetWeight), record TFQ-1157
- replay: `verified`
  - receipt [dag/research/campaign_maj-import-coset-weight-np-hard_lean_replay.json](../../../dag/research/campaign_maj-import-coset-weight-np-hard_lean_replay.json) (module `CampaignMajImportCosetWeight`): recorded sha256 `29b2497864b3b9c7e9b9500c6c90cbb902df4b81029253c70acc2923d1971008` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignMajImportCosetWeight`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignMajImportCosetWeight.coset_is` | yes | yes | yes | none | `#print axioms CampaignMajImportCosetWeight.coset_is` |
| `CampaignMajImportCosetWeight.coset_weights` | yes | yes | yes | none | `#print axioms CampaignMajImportCosetWeight.coset_weights` |
| `CampaignMajImportCosetWeight.kernel_is` | yes | yes | yes | none | `#print axioms CampaignMajImportCosetWeight.kernel_is` |
| `CampaignMajImportCosetWeight.label_one_coordinates` | yes | yes | yes | none | `#print axioms CampaignMajImportCosetWeight.label_one_coordinates` |
| `CampaignMajImportCosetWeight.length_sixteen` | yes | yes | yes | none | `#print axioms CampaignMajImportCosetWeight.length_sixteen` |
| `CampaignMajImportCosetWeight.min_weight_one` | yes | yes | yes | none | `#print axioms CampaignMajImportCosetWeight.min_weight_one` |
| `CampaignMajImportCosetWeight.row1_matches` | yes | yes | yes | none | `#print axioms CampaignMajImportCosetWeight.row1_matches` |
| `CampaignMajImportCosetWeight.row2_matches` | yes | yes | yes | none | `#print axioms CampaignMajImportCosetWeight.row2_matches` |
| `CampaignMajImportCosetWeight.weight_one_labels` | yes | yes | yes | none | `#print axioms CampaignMajImportCosetWeight.weight_one_labels` |
| `coset_is` | yes | yes | yes | none | `#print axioms coset_is` |
| `coset_weights` | yes | yes | yes | none | `#print axioms coset_weights` |
| `kernel_is` | yes | yes | yes | none | `#print axioms kernel_is` |
| `label_one_coordinates` | yes | yes | yes | none | `#print axioms label_one_coordinates` |
| `length_sixteen` | yes | yes | yes | none | `#print axioms length_sixteen` |
| `min_weight_one` | yes | yes | yes | none | `#print axioms min_weight_one` |
| `row1_matches` | yes | yes | yes | none | `#print axioms row1_matches` |
| `row2_matches` | yes | yes | yes | none | `#print axioms row2_matches` |
| `weight_one_labels` | yes | yes | yes | none | `#print axioms weight_one_labels` |

- counts toward the grade: yes

### Python: `checks/independent/maj-import-coset-weight-np-hard.py`

- file: [checks/independent/maj-import-coset-weight-np-hard.py](../../../checks/independent/maj-import-coset-weight-np-hard.py)
- sha256 (`bytes`): `d58ac1f34053f116695c5f485b0fdb13ab8dcfa4e8fa2e1194ed594d0cbce398`
- cited in: record TFQ-1157

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1157_maj_import_coset_weight_np_hard.md`

- file: [dag/derivations/28_majorana/tfq_1157_maj_import_coset_weight_np_hard.md](../../../dag/derivations/28_majorana/tfq_1157_maj_import_coset_weight_np_hard.md)
- sha256 (`lf-normalised`): `176c50469ad99b8712bfde39890c6f141f7d4f42ab337c65d6c361132ba52218`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1157
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `2f55c0f24f87388cfa9d7a4a7d832f34c0fa30b857d344811f4336f634c1684b`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-IMPORT-COSET-WEIGHT-NP-HARD` `CONDITIONAL_ON_IMPORT`: [MAJ-PHI1-HAMMING-COSET](MAJ-PHI1-HAMMING-COSET.md) (DEFINITION)

Outgoing (1):

- `APP-R-MAJ-PHI1-SYNDROME-DECODING` `CONDITIONAL_ON_IMPORT`: [MAJ-PHI1-SYNDROME-DECODING](MAJ-PHI1-SYNDROME-DECODING.md) (CONDITIONAL)
