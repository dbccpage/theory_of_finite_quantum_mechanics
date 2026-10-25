# Review of campaign TFQ-0385

Scope: branch derive/TFQ-0385 against origin/main at 7fa69d621c27. Reviewed against the statement as edited in this branch. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the TFQ-0385 statement, bottleneck, lean4/CampaignTfq0385RuleErasesSeparation.lean, checks/independent/tfq-0385.py, dag/derivations/independent/tfq-0385.md, and dag/research/campaign_tfq-0385_lean_replay.json. Scanner: python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict. Result of that run: HIGH 0, MEDIUM 0, LOW 3. Lean was built once in this worktree (lake build CampaignTfq0385RuleErasesSeparation, exit 0, about 1.0s). This review file does not rebuild it.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. TFQ-0385 stays OPEN.

Corrections to the PR's own text:
- None. The finite paragraph matches the declarations below. The ledger sentence, the unread atlas replay, the no-return count, and every later admission API stay outside those declarations.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| TFQ-0385 | two_data (lean4/CampaignTfq0385RuleErasesSeparation.lean:19), marked_separates (:23), rule_collapses (:31), uniform_rule_erases_separation (:39) | NARROWED | The finite paragraph is the Lean type of those declarations. The ledger row, the atlas replay, the no-return count, and any later admission API stay open. Status stays OPEN. |

## Statement against declarations

| Claim | Declaration | Verdict |
|---|---|---|
| Ledger row WDP-P000-017 records the counterexample | not in the module | NOT PROVED |
| The reproducing test was opened | not in the module | NOT PROVED |
| Two data, and every datum is 0 or 1 | two_data | NARROWED |
| Before the rule, profile bits are true and false, and the class count is 2 | marked_separates | NARROWED |
| After the uniform rule on form 0, both profile bits are true and the class count is 1 | rule_collapses | NARROWED |
| Datum 0 stays true and datum 1 changes, so the class count changes | uniform_rule_erases_separation | NARROWED |
| The no-return count | no declaration | NOT PROVED |
| Every later admission API | no declaration; the statement says this history is not that theorem | NOT PROVED |

Each #print axioms line is [propext]. The receipt records those four lists. sha256 of the LF Lean bytes is bb89512422e6d34ddfd19b01653c76325c46211bd98ced9b1898d59b6800eb12.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| statement | class count 2, then 1 | marked_separates, rule_collapses; Python class_count(False, True) and class_count(True, True) | match |
| statement | two data | two_data; Python data (0, 1) | match |
| independent check stdout | checked 15 conditions, 0 failures | the script's own counter, run with python -I -X utf8, exit 0 | match |
| evidence map writer | grades E0 163, E1 222, E2 40, E3 500, E4 0 | stdout of dag/evidence/build_evidence.py --write | match as a file census, not a statement match |

## Scanner output

HIGH 0. MEDIUM 0. LOW 3, none on TFQ-0385: R10 on TENSOR-ASSUMPTION-COUNTERMODELS; R5 on dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md (20261019); R5 on dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md (1/2, 1/4). No baseline change.

The evidence page docs/evidence/nodes/TFQ-0385.md reports 8 cited symbols. The module declares 4 theorems. The node lean list and the record lean4 list are the same 4 paths, and the grade writer counts both. That page is generated. It is not a claim that 8 theorems were checked. The page's grade E3 is a file census. It is not a statement match, and it is not E4.
