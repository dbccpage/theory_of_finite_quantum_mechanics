# Review of campaign TFQ-0319

Scope: branch derive/TFQ-0319 against origin/main at 7fa69d621c27. Reviewed against the statement as edited in this branch. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the TFQ-0319 statement, bottleneck, lean4/CampaignTfq0319UnjoinedReceipt.lean, checks/independent/tfq-0319.py, dag/derivations/independent/tfq-0319.md, and dag/research/campaign_tfq-0319_lean_replay.json. Scanner: python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict. Result of that run: HIGH 0, MEDIUM 0, LOW 3. Lean was built once in this worktree (lake build CampaignTfq0319UnjoinedReceipt, exit 0, about 1.1s). This review file does not rebuild it.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. TFQ-0319 stays OPEN.

Corrections to the PR's own text:
- None. The finite paragraph matches the declarations below. The atlas sentences in the same statement stay outside those declarations, and the bottleneck says so.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| TFQ-0319 | sealed_nibble_count (lean4/CampaignTfq0319UnjoinedReceipt.lean:58), sealed_nibbles_match (:61), all_self_coboundaries_zero (:67), edge_coboundaries (:74), images_are_the_four (:79), images_pairwise_distinct (:83), every_value_pair_is_listed (:88), pairing_keeps_sealed (:93), pairing_indices (:97), pairing_distinct (:101), green_receipt_two_edge_values (:107) | NARROWED | The finite paragraph is the Lean type of those declarations. The floor.yaml admission, the book README sentence, the proposed_gaps row, and a general reading of every Lake build stay open. Status stays OPEN. |

## Statement against declarations

| Claim | Declaration | Verdict |
|---|---|---|
| F000 floor.yaml admits finite sets, typed distinction steps, combinatorial coboundaries, and finite witness functionals | not proved | NOT PROVED |
| Shelf F000.S000 and the book pin sealed-derivation-v1 as a mechanical receipt | not proved | NOT PROVED |
| The seven stored nibbles are 3, 1, 0, 0, 12, 4, 14 and the green bit is true | sealed_nibbles_match, sealed_nibble_count | NARROWED |
| The base-16 reading of those nibbles is 3100c4e | checks/independent/tfq-0319.py positional accumulation; no Lean string theorem | NARROWED |
| The book README says this volume is not a completed Genesis-to-FOC derivation | not proved | NOT PROVED |
| Row S000-GAP-GENESIS-TO-PD still asks for a certified term map | not proved | NOT PROVED |
| A green Lake build is not correspondence, as a claim about Lake | not proved | NOT PROVED |
| Four functions Fin 2 to Fin 2 have value pairs (0, 0), (0, 1), (1, 0), (1, 1) | images_are_the_four | NARROWED |
| Every value pair on Fin 2 is one of those four | every_value_pair_is_listed | NARROWED |
| Each listed function has self-coboundary 0 at both marks | all_self_coboundaries_zero | NARROWED |
| Coboundaries on (0, 1) are 0, 1, 1, 0 | edge_coboundaries | NARROWED |
| Four pairings keep that one receipt, green stays true, and indices are 0, 1, 2, 3 | pairing_keeps_sealed, pairing_indices | NARROWED |
| The four pairings are pairwise distinct | pairing_distinct | NARROWED |
| Pairing 0 and pairing 1 share the receipt and carry edge coboundaries 0 and 1 | green_receipt_two_edge_values | NARROWED |
| A certified term map from sealed-derivation-v1 into PrimitiveDifference | not proved | NOT PROVED |

Each #print axioms line for the eleven declarations is [propext]. The receipt records those eleven lists. sha256 of the LF Lean bytes is 4f8200380d75a91f36babc8a768321f01acebc07e57f1f9de10563885f799953.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| statement and note | nibbles 3, 1, 0, 0, 12, 4, 14 | Lean sealed_nibbles_match; Python list of the same seven integers | match |
| statement | length of that nibble list is 7 | sealed_nibble_count; Python len | match |
| statement | edge coboundaries 0, 1, 1, 0 | edge_coboundaries; Python (f[v] - f[u]) mod 2 on the four pairs | match |
| statement | four pairings, pairwise distinct | pairing_distinct has six inequalities, one for each unordered pair of four indices; Python compares those pairs | match |
| statement | prefix 3100c4e | Python accumulates value = value * 16 + digit and compares with 0x3100C4E, then formats the value as hex | match |
| independent check stdout | checked 58 conditions, 0 failures | the script's own counter, run with python -I -X utf8, exit 0 | match |
| evidence map writer | grades E0 163, E1 222, E2 40, E3 500, E4 0 | stdout of dag/evidence/build_evidence.py --write | match as a file census, not a statement match |

## Scanner output

HIGH 0. MEDIUM 0. LOW 3, none on TFQ-0319: R10 on TENSOR-ASSUMPTION-COUNTERMODELS; R5 on dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md (20261019); R5 on dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md (1/2, 1/4). No baseline change.

The evidence page docs/evidence/nodes/TFQ-0319.md reports 22 cited symbols. The module declares 11 theorems. The node lean list and the record lean4 list are the same 11 paths, and the grade writer counts both. That page is generated. It is not a claim that 22 theorems were checked.
