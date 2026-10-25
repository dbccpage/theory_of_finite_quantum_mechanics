# Review of campaign TFQ-0374

Scope: branch derive/TFQ-0374 against origin/main at 7fa69d621c27. Reviewed against the statement as edited in this branch. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the TFQ-0374 statement, bottleneck, lean4/CampaignTfq0374ThreeRecoveryContracts.lean, checks/independent/tfq-0374.py, dag/derivations/independent/tfq-0374.md, and dag/research/campaign_tfq-0374_lean_replay.json. Scanner: python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict. Result of that run: HIGH 0, MEDIUM 0, LOW 3. Lean was built once in this worktree (lake build CampaignTfq0374ThreeRecoveryContracts, exit 0, about 1.5s). This review file does not rebuild it.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. TFQ-0374 stays OPEN.

Corrections to the PR's own text:
- None. The finite paragraph matches the declarations below. The ledger sentence, the unread atlas files, and free-monoid size stay outside those declarations.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| TFQ-0374 | letters_are_old_or_fresh (lean4/CampaignTfq0374ThreeRecoveryContracts.lean:33), fresh_is_not_old (:40), witness_uses_one_fresh (:43), old_word_agrees (:48), three_contracts_differ_on_a_new_letter (:54) | NARROWED | The finite paragraph is the Lean type of those declarations. The ledger row, preservation.py, WordRecovery.lean, and free-monoid size stay open. Status stays OPEN. |

## Statement against declarations

| Claim | Declaration | Verdict |
|---|---|---|
| Ledger row WDP-P001-009 says the three contracts have different types, with no Ext calculation | not in the module | NOT PROVED |
| preservation.py defines recover_word, erase_word, and decimal_decode | not in the module | NOT PROVED |
| One finite witness on one new letter is still required | letters_are_old_or_fresh, witness_uses_one_fresh, three_contracts_differ_on_a_new_letter | NARROWED |
| That witness stays distinct from free-monoid size | the module has no free-monoid theorem | NARROWED as a fence, not a theorem about free monoids |
| WordRecovery.lean stays unchecked | the file is absent from this checkout | NOT PROVED |
| Letters are a and fresh, and fresh is not a | letters_are_old_or_fresh, fresh_is_not_old | NARROWED |
| The witness is [a, fresh] and contains fresh once | witness_uses_one_fresh | NARROWED |
| Restriction of [[a, fresh], [a]] returns [[a]] | three_contracts_differ_on_a_new_letter | NARROWED |
| Recovery of the witness returns none | three_contracts_differ_on_a_new_letter | NARROWED |
| Erasure of the witness returns [a] | three_contracts_differ_on_a_new_letter | NARROWED |
| On [a], recovery and erasure return [a] | old_word_agrees | NARROWED |
| Recovery of the witness is not the erased word, and erasure is not the witness | three_contracts_differ_on_a_new_letter | NARROWED |
| The witness is absent from the restricted sample, and the old word is present | three_contracts_differ_on_a_new_letter | NARROWED |
| An Ext group is calculated | no declaration | NOT PROVED, and none is defined in this file |

letters_are_old_or_fresh, fresh_is_not_old, witness_uses_one_fresh, and old_word_agrees depend on no axioms. three_contracts_differ_on_a_new_letter depends on [propext]. The receipt records those lists. sha256 of the LF Lean bytes is 1558936ca62404215225ede5f79be94146902a1c460a2e55d4edf0391717b2ea.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| statement | the witness contains fresh once | witness_uses_one_fresh says the fresh-filter length is 1; Python counts fresh letters in (0, 1) | match |
| statement | two letters, a and fresh | letters_are_old_or_fresh; Python letters (0, 1) with length 2 | match |
| independent check stdout | checked 24 conditions, 0 failures | the script's own counter, run with python -I -X utf8, exit 0 | match |
| evidence map writer | grades E0 163, E1 222, E2 40, E3 500, E4 0 | stdout of dag/evidence/build_evidence.py --write | match as a file census, not a statement match |

## Scanner output

HIGH 0. MEDIUM 0. LOW 3, none on TFQ-0374: R10 on TENSOR-ASSUMPTION-COUNTERMODELS; R5 on dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md (20261019); R5 on dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md (1/2, 1/4). No baseline change.

The evidence page docs/evidence/nodes/TFQ-0374.md reports 10 cited symbols. The module declares 5 theorems. The node lean list and the record lean4 list are the same 5 paths, and the grade writer counts both. That page is generated. It is not a claim that 10 theorems were checked. The page's grade E3 is a file census. It is not a statement match, and it is not E4.
