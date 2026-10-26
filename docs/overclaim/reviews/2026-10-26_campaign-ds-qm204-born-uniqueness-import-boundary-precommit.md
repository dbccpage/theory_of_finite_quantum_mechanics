# Review of campaign-ds-qm204-born-uniqueness-import-boundary-precommit

Scope: worktree `C:\gw\derive-ds-qm204`, branch `derive/DS-QM204-BORN-UNIQUENESS-IMPORT-BOUNDARY`, base `origin/main` `4fea09ae176aae31115e38bb2b21819237055811`. Reviewed against the standing statement before the pull request was opened. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). Read the standing statement, bottleneck and `pfp_review` in `dag/derivation_dag.json`, `lean4/CampaignDsQm204BornUniqueness.lean`, and `dag/research/campaign_ds-qm204-born-uniqueness-import-boundary_lean_replay.json`. Recomputed the integers with `python -I -X utf8 checks/independent/ds-qm204-born-uniqueness-import-boundary.py` (exit 0). Lean, lake and cargo were not rebuilt for this review; the receipt records the earlier lake build.

Result: 1 node FULL on the standing narrowed statement, 0 NARROWED, 0 OVERCLAIM. No node was raised. Campaign outcome is Narrowed. Status stays IMPORTED_ASSUMPTION.

Corrections to the PR's own text:
- None. The standing statement is the integer case. Gleason uniqueness and L^p measure pairings stay in the bottleneck.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| DS-QM204-BORN-UNIQUENESS-IMPORT-BOUNDARY | `pairNorm` lean4/CampaignDsQm204BornUniqueness.lean:53; `denom34` :56; `squares34` :58; `fourths34` :60; `quarticSeparates` :62; `linearSeparates` :65; `rot` :42; `rotWitness` :67 | FULL | Every atomic claim of the standing statement is the type of one of those declarations. Axioms in the receipt are only propext and Quot.sound. Status stays IMPORTED_ASSUMPTION. |

Atomic claims:
- For every integer pair A and B, A + B = (A + B) * 1. Matched by `pairNorm` (lean4/CampaignDsQm204BornUniqueness.lean:53).
- 3 + 4 = 7 and 7 differs from 0. Matched by `denom34` (lean4/CampaignDsQm204BornUniqueness.lean:56).
- 3 * 3 + 4 * 4 = 25 and 5 * 5 = 25. Matched by `squares34` (lean4/CampaignDsQm204BornUniqueness.lean:58).
- 3 * 3 * 3 * 3 + 4 * 4 * 4 * 4 = 337. Matched by `fourths34` (lean4/CampaignDsQm204BornUniqueness.lean:60).
- (3 * 3) * (3 * 3 * 3 * 3 + 4 * 4 * 4 * 4) differs from (3 * 3 * 3 * 3) * (5 * 5). Matched by `quarticSeparates` (lean4/CampaignDsQm204BornUniqueness.lean:62).
- 3 * (3 * 3 + 4 * 4) differs from (3 * 3) * (3 + 4). Matched by `linearSeparates` (lean4/CampaignDsQm204BornUniqueness.lean:65).
- For every integer quadruple a, b, r and s, the rotation identity. Matched by `rot` (lean4/CampaignDsQm204BornUniqueness.lean:42).
- At a = 3, b = 4, r = 3 and s = 4, both sides equal 625. Matched by `rotWitness` (lean4/CampaignDsQm204BornUniqueness.lean:67).

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| statement, squares34 | 25 | 3*3+4*4 = 9+16 = 25 and 5*5 = 25, independent check | match |
| statement, fourths34 | 337 | 81+256 = 337, independent check | match |
| statement, quarticSeparates | 3033 and 2025 | 9*337 = 3033 and 81*25 = 2025, independent check | match |
| statement, linearSeparates | 75 and 63 | 3*25 = 75 and 9*7 = 63, independent check | match |
| statement, rotWitness | 625 | (-7)*(-7)+24*24 = 49+576 = 625 and 25*25 = 625, independent check | match |
| derivation note | 9, 16, 81, 256, 49, 576, 24 | same products in the independent check | match |

## Scanner output
HIGH 0. MEDIUM 0. LOW 3, all outside this node's statement:
- R10 TENSOR-ASSUMPTION-COUNTERMODELS: cited modules absent from a replay receipt. Repin rebinds tensor receipt hashes. Not this node.
- R5 `dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md`: number 20261019.
- R5 `dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md`: numbers 1/2 and 1/4.

No baseline change. The hunter did not rebuild Lean, lake or cargo.
