# Review of campaign L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED

Scope: branch `derive/L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED` against origin/main `7fa69d621c27bed7045d0b7fe34bbb1d34b27248`. Reviewed against the statement in `dag/fragments/pfp_review_decisions.json` before the pull request. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read `lean4/CampaignL1ResidualSectorWeights.lean` (no import) and the node statement, bottleneck and source list. The campaign `lake build CampaignL1ResidualSectorWeights` exited 0 (module job 768 ms, wall 15568 ms). This review does not rebuild. Mathlib is unused; the package junction was present and not written. Independent check: `python -I -X utf8 checks/independent/l1-residual-sector-weights-declared.py` printed `checked 8 conditions, 0 failures`. Scanner: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` reported HIGH 0, MEDIUM 0, LOW 5.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays CONDITIONAL.

Corrections to the PR's own text:
- None. The standing statement is the two pairs and the two length-4 holonomy checks.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED | `same_phi1`, `weights_differ`, `holonomy_two_not_divisible`, `holonomy_four_divisible` in `lean4/CampaignL1ResidualSectorWeights.lean` | NARROWED | The standing statement is one closed witness. The general n-cycle, the weighted L1 form, and the sum-of-squares reading of Gamma2 stay in the bottleneck. |

Statement-vs-theorem:

| Claim | Declaration | Verdict |
|---|---|---|
| Pairs (2, 0) and (0, 2) both have coordinate sum 2 | `same_phi1` (`CampaignL1ResidualSectorWeights.lean:10`) | NARROWED |
| Those pairs differ | `weights_differ` (`CampaignL1ResidualSectorWeights.lean:13`) | NARROWED |
| No natural number k satisfies 4 * k = 2 | `holonomy_two_not_divisible` (`CampaignL1ResidualSectorWeights.lean:16`) | NARROWED |
| 4 * 1 = 4 | `holonomy_four_divisible` (`CampaignL1ResidualSectorWeights.lean:20`) | NARROWED |
| General n-cycle, weighted masses, or a sum-of-squares Gamma2 | not proved | NOT PROVED |

Axioms: `same_phi1`, `weights_differ` and `holonomy_four_divisible` depend on no axioms. `holonomy_two_not_divisible` depends on propext and Quot.sound. That list is inside propext, Classical.choice and Quot.sound.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Statement, coordinate sums | 2 + 0 = 2 and 0 + 2 = 2 | `same_phi1` by `decide`; independent check adds the coordinates | match |
| Statement, inequality of pairs | (2, 0) differs from (0, 2) | `weights_differ`; independent check compares the tuples | match |
| Statement, holonomy 2 | no k with 4 * k = 2 | `holonomy_two_not_divisible` by `omega`; independent check has 4 * 0 ≠ 2, 4 * 1 ≠ 2, and 4 * 2 = 8 > 2 | match |
| Statement, holonomy 4 | 4 * 1 = 4 | `holonomy_four_divisible` by `decide`; independent check multiplies 4 * 1 | match |

## Scanner output

HIGH 0. MEDIUM 0. LOW 5 left unchanged: R10 on TENSOR-ASSUMPTION-COUNTERMODELS; R5 on tfq_1019 number 20261019; R5 on tfq_0413 numbers 1/2 and 1/4; R5 on tfq_0354 numbers 8.2, 790, 1185, 1580, 348, 188; R5 on tfq_0167 number 180. The last two notes already named this node and were not edited. No baseline entry is proposed.
