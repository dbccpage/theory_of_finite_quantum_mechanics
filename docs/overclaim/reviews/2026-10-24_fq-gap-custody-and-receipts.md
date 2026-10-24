# Review of FQ-GAP-CUSTODY-AND-RECEIPTS

Scope: campaign derivation on `derive/FQ-GAP-CUSTODY-AND-RECEIPTS` against `origin/main` `85cc76d0df01bcd7433a626ba75c38ccc19dd2d7`. Reviewed against the statements as they stand in the worktree before the campaign commit. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: `scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). Read the node statement, bottleneck and `pfp_review` in `dag/derivation_dag.json`, `lean4/CampaignFqGapCustodyReceipts.lean`, the replay receipt, and `checks/independent/fq-gap-custody-and-receipts.py`. Lean was built earlier in this worktree (`lake build CampaignFqGapCustodyReceipts`, 0.859s, exit 0); this review did not rebuild it. The six `#print axioms` lines in that build were empty.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status of `FQ-GAP-CUSTODY-AND-RECEIPTS` stays OPEN.

Corrections to the PR's own text:
- None. The statement is the census below. The YAML binding is the independent check. Lean states the transcribed list and the two inequalities.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| FQ-GAP-CUSTODY-AND-RECEIPTS | `census_length`, `census_sum_eq`, `untyped_row`, `one_untyped_label`, `ledger_untyped_ne_gap_text`, `ledger_rows_ne_gap_text` in `lean4/CampaignFqGapCustodyReceipts.lean`; file binding in `checks/independent/fq-gap-custody-and-receipts.py` | NARROWED | The module transcribes 14 pairs and proves length 14, sum 834, index 6 = ("UNTYPED", 48), one UNTYPED label, 48 ≠ 24 and 834 ≠ 189, with empty axiom lists. It does not read the YAML. The check reads the `claims` list, stopping before `application_claims`. GAP-FQM-017, GAP-FQM-019, GAP-FQM-020, GAP-FQM-022, Zenodo publication and the README code-companion check stay open. |

Statement-vs-theorem:

| Claim | Declaration | Verdict |
|---|---|---|
| Transcribed census has length 14 | `census_length` (`CampaignFqGapCustodyReceipts.lean:26`) | FULL |
| Those counts sum to 834 | `census_sum_eq` (`CampaignFqGapCustodyReceipts.lean:28`) | FULL |
| Index 6 is ("UNTYPED", 48) | `untyped_row` (`CampaignFqGapCustodyReceipts.lean:30`) | FULL |
| The label UNTYPED occurs once | `one_untyped_label` (`CampaignFqGapCustodyReceipts.lean:33`) | FULL |
| 48 ≠ 24 | `ledger_untyped_ne_gap_text` (`CampaignFqGapCustodyReceipts.lean:37`) | FULL |
| 834 ≠ 189 | `ledger_rows_ne_gap_text` (`CampaignFqGapCustodyReceipts.lean:40`) | FULL |
| The `claims` list in `claim_ledger.yaml`, stopping before `application_claims`, is those 834 records and those 14 pairs | independent check, not Lean | NARROWED |
| GAP-FQM-002 title is `24 claim rows carry no parseable type` and its description contains `24 of 189` | independent check, not Lean | NARROWED |
| GAP-FQM-017, GAP-FQM-019, GAP-FQM-020, GAP-FQM-022, Zenodo, README code-companion check | not proved | NOT PROVED |

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Census pairs | sum 834 | 160+156+115+104+80+57+48+36+31+17+12+10+7+1 = 834, integer addition | match |
| Index 6 | UNTYPED 48 | pair position 6 in that descending list | match |
| Inequalities | 48 ≠ 24, 834 ≠ 189 | integer comparison | match |
| Independent check | 27 claims, failures 0 | 5 list checks + 14 label checks + 8 gap and inequality checks | match |
| README Lean references | 2121 | 2115 on origin/main plus 6 new refs | match |
| README derivation papers | 1044 | 1043 plus this derivation note | match |
| README tracked lean4 | 974 | 973 tracked plus this module (`git ls-files --cached --others`) | match |
| README Lake libraries / roots | 65 / 917 | 64 / 916 plus one `lean_lib` and one root | match |
| README scope_effect | consistent 68, statement_narrowed 66 | one node moved consistent to statement_narrowed; 68+18+66+25 = 177 | match |
| Ledger Lean count for TFQ-1023 | 8 | 2 prior refs plus 6 new symbols | match |
| README combined_files | 8879 | `git ls-files` of `.contract.score.yaml` is 8879; `contract_scores.py check` reports that count | match |

## Scanner output
No HIGH or MEDIUM findings. Three LOW findings are outside this node and were not edited here: R10 on `TENSOR-ASSUMPTION-COUNTERMODELS` (cited Lean modules absent from a replay receipt), R5 `20261019` in the tensor-uniqueness note, and R5 `1/2`, `1/4` in the tensor-countermodel note. No baseline change.

The census theorems are `rfl` or `decide` on a transcribed list. That is a check of the list, not a parse of `claim_ledger.yaml`. The independent check is the file reading. A type-label count is not a derivation that a row is unsupported.
