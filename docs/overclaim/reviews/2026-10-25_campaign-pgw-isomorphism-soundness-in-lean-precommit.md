# Review of campaign PGW-ISOMORPHISM-SOUNDNESS-IN-LEAN

Scope: branch derive/PGW-ISOMORPHISM-SOUNDNESS-IN-LEAN against origin/main at 7fa69d621c27bed7045d0b7fe34bbb1d34b27248. Reviewed against the statements as they stand in this worktree. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the fragment summary, obligation, and fence for TFQ-0500; read lean4/CampaignPgwIsomorphismSoundnessInLean.lean through the axiom lines; read checks/independent/pgw-isomorphism-soundness-in-lean.py and dag/derivations/independent/pgw-isomorphism-soundness-in-lean.md. Scanner: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). The lake build of CampaignPgwIsomorphismSoundnessInLean exited 0 before this review. Cargo was not rebuilt. The independent check was run with `python -I -X utf8`.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. PGW-ISOMORPHISM-SOUNDNESS-IN-LEAN stays OPEN.

Corrections to the PR's own text:
- None. The standing statement is the two-data case. The implemented key is not proved.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-ISOMORPHISM-SOUNDNESS-IN-LEAN | `pgwIsoSwap` and `pgwIsoKey` (definitions, lean4/CampaignPgwIsomorphismSoundnessInLean.lean:10 and :16); `pgwIsoSwapInvolutive` (:27); `pgwIsoKeysOfFour` (:31); `pgwIsoKeySwap` (:38); `pgwIsoKeyIff` (:42); `pgwIsoConstants` (:48); `pgwIsoFour` (:54); `pgwIsoMixed` (:57) | NARROWED | The standing statement is this four-coloring case, and those declarations state it. Printed axioms are empty. The obligation's implemented key, the regimes past a brute-force limit, and the exported-orbit comparison are not proved. Status stays OPEN. |

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Statement keys | (0, 0), (0, 1), (0, 1), (1, 1) | `pgwIsoKeysOfFour` and the independent check's four key assertions | Match |
| Statement, universe | 4 colorings | `pgwIsoFour` states length 4; the check builds both bit pairs and compares them to the list | Match |
| Statement, shared key | 2 colorings have key (0, 1) | `pgwIsoMixed` states filter length 2; the check sums the same predicate | Match |
| Independent check | checked 34 conditions, 0 failures | 1 list equality + 1 length + 4 involutions + 4 key invariances + 4 key values + 1 shared-key count + 2 fixed points + 1 constant-key inequality + 16 pair comparisons = 34 | Match |
| README lean references | 2294 resolve | prior README row 2287 plus these 7 declarations | Match |
| README lake libraries / roots | 91 / 943 | prior 90 / 942 plus this one `lean_lib` and its one root | Match |
| README derivation papers | 1069 | prior 1068 plus this independent note | Match |
| README lean4 `.lean` files | 1000 | prior 999 plus this module; `git ls-files` count in this worktree is 1000 | Match |
| Fragment source quote | 482 | not recomputed; the digits stay in the pre-existing continuation.txt quote and are not in the standing statement | Unrecomputed |
| README rows other than the four deltas above | inventory figures written by `scripts/build_readme_facts.py --write` | `scripts/build_readme_facts.py --check` exited 0 on this worktree | Match to that script |

## Scanner output
HIGH 0. MEDIUM 0. LOW 3, none on this node: R10 TENSOR-ASSUMPTION-COUNTERMODELS (lean4/TensorCountermodelCones.lean in no replay receipt); R5 dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md (20261019); R5 dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md (1/2, 1/4). No baseline entry is proposed.

The evidence page grades this node E3. That grade counts files and a matching receipt. It is not a statement-match review, and it is not E4.
