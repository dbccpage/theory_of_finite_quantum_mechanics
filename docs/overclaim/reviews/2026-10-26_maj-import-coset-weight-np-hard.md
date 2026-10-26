# Overclaim review: MAJ-IMPORT-COSET-WEIGHT-NP-HARD

Scope: this branch versus origin/main `4fea09ae176a` for node MAJ-IMPORT-COSET-WEIGHT-NP-HARD. AuthorityEffect: None.

Method: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3, exit 0). Statement read from `dag/derivation_dag.json`. Theorems read from `lean4/CampaignMajImportCosetWeight.lean` after `lake build CampaignMajImportCosetWeight` (exit 0). Each `#print axioms` line reports no axioms. Numbers recomputed by `python -I -X utf8 checks/independent/maj-import-coset-weight-np-hard.py` (exit 0).

Result: 1 NARROWED (the finite statement is FULL against the theorems; status stays IMPORTED_ASSUMPTION). 0 OVERCLAIM.

## Statement versus theorems

Original statement was the Berlekamp–McEliece–van Tilborg 1978 NP-hardness claim. That claim is not proved. The node statement is the finite case below. Status was not raised.

| Claim | Declaration | Verdict |
|---|---|---|
| 16 labels, 0 through 15 | `length_sixteen` | FULL |
| Row (1, 1, 0, 0) matches `row1` on those labels | `row1_matches` | FULL |
| Row (0, 1, 1, 1) matches `row2` on those labels | `row2_matches` | FULL |
| Syndrome (1, 0) is labels 1, 6, 10, 13 | `coset_is` | FULL |
| Weights 1, 2, 2, 3 | `coset_weights` | FULL |
| Minimum weight 1 | `min_weight_one` | FULL |
| The weight-1 label in that list is 1 | `weight_one_labels` | FULL |
| Label 1 has coordinates (1, 0, 0, 0), least significant bit as coordinate 0 | `label_one_coordinates` together with `bit` | FULL |
| Syndrome (0, 0) is labels 0, 7, 11, 12 | `kernel_is` | FULL |
| NP-hardness for a general binary matrix | not proved | moved to the bottleneck |

Axioms: none of the nine theorems depend on an axiom. The allowed set is `propext`, `Classical.choice`, `Quot.sound`.

## Numbers recomputed

Independent check, integer arithmetic, labels 0 through 15: coset [1, 6, 10, 13], weights [1, 2, 2, 3], minimum 1, weight-1 labels [1], coordinates (1, 0, 0, 0), kernel [0, 7, 11, 12]. Match.

## Scanner notes that are not this node

LOW R10 on TENSOR-ASSUMPTION-COUNTERMODELS and LOW R5 on two derivation notes are on pages whose shared-file hashes moved (`dag/derivation_dag.json`, `dag/research/tensor_countermodel_validation.json`). Their statements were not edited.

## What is still open

The 1978 hardness claim stays in `imported_structure` and the bottleneck. This enumeration does not discharge it.
