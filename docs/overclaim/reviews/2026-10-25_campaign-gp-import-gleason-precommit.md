# Review of campaign GP-IMPORT-GLEASON

Scope: worktree branch derive/GP-IMPORT-GLEASON against origin/main 4fea09ae176aae31115e38bb2b21819237055811. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the standing statement, bottleneck, and pfp_review; read the six cited declarations and the printed axiom lines from the lake build. Scanner: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). Lean was built before this review; this review step did not rebuild.

Result: 1 node NARROWED, 0 FULL, 0 OVERCLAIM. No node was raised. Status stays IMPORTED_ASSUMPTION.

Corrections to the PR's own text:
- The prior sentence that Born uniqueness needs Gleason hypotheses is no longer the standing statement. It remains prior_statement, and the bottleneck keeps that uniqueness imported.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| GP-IMPORT-GLEASON | `twoLabelsBelowThree` (lean4/CampaignGpImportGleason.lean:36), `dimensionExtraFails` (line 38), `noThreeDistinctLabels` (line 40), `squaredWeights` (line 43), `unitPairingsAgree` (line 46), `falseIndicatorDisagrees` (line 49) | NARROWED | Standing text matches those declarations. Uniqueness at dimension at least 3 is not a declaration. |

## Statement versus theorem
| Claim in the standing statement | Declaration | Verdict |
|---|---|---|
| 2 < 3 | twoLabelsBelowThree | FULL |
| 3 ≤ 2 fails | dimensionExtraFails | FULL |
| no three pairwise distinct labels exist | noThreeDistinctLabels | FULL |
| amplitudes 2 and 1 have squared weights 4 and 1 | squaredWeights | FULL |
| the unit effect pairs both readout orders with 5 | unitPairingsAgree | FULL |
| the false-indicator pairs as 4 directly and as 1 after swapping | falseIndicatorDisagrees | FULL |
| Born uniqueness at dimension at least 3 | not proved | NOT PROVED |
| noncontextuality, sigma-additivity, continuity | not proved | NOT PROVED |

Axiom lines from the build: twoLabelsBelowThree, dimensionExtraFails, noThreeDistinctLabels, squaredWeights, unitPairingsAgree, and falseIndicatorDisagrees depend on no axioms.

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| statement and independent check | 2 < 3 and not (3 ≤ 2) | integer comparison | match |
| statement and independent check | weights 4 and 1 | 2*2 and 1*1 | match |
| statement and independent check | unit pairings 5 and 5 | 4*1 + 1*1 | match |
| statement and independent check | false-indicator 4 and swapped 1 | 4*1 + 1*0 and 4*0 + 1*1 | match |

## Scanner output

HIGH 0, MEDIUM 0, LOW 3. No new HIGH finding. The LOW findings are outside the standing statement of this node.
