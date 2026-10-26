# Review of campaign L1-WDP-CH08-C01-REPLICA-L1

Scope: branch derive/L1-WDP-CH08-C01-REPLICA-L1 against origin/main f49b3c3b96fa. Reviewed against the statement as it stands in this worktree. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the node statement, bottleneck, and pfp_review in dag/derivation_dag.json; read lean4/CampaignL1ReplicaScale.lean in full, including the #print axioms lines from the lake build on 2026-10-26 (exit 0, wall 11.8s); ran scripts/overclaim_scan.py --changed-since origin/main --strict (HIGH 0, MEDIUM 0, LOW 2). Cargo was not run. The scan's LOW rows are on TENSOR-ASSUMPTION-COUNTERMODELS, whose evidence page changed only by the dag file sha.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. L1-WDP-CH08-C01-REPLICA-L1 stays OPEN.

Corrections to the PR's own text:
- None. The opening two sentences stay the open reading. The Nat identities are the checked slice.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| L1-WDP-CH08-C01-REPLICA-L1 | CampaignL1ReplicaScale.scaleSum, scaleSquares, sampleSum, sampleSquares, sampleFive, sampleSumSquare, sampleSquaresNeSumSquare, sampleScaledSum, sampleScaledSquares, sampleLinearScale, sampleScaledNeLinear | NARROWED | The two opening sentences are not the type of any new declaration. scaleSum and scaleSquares state the two Nat identities for every c, a, and b. The sample declarations state 7, 25, 49, 14, 100, and 50. scaleSquares depends on propext. The other printed axiom lists are empty. |

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| statement, a=3, b=4 | 7, 25, 25, 49, 25 differs from 49 | checks/independent/l1-wdp-ch08-c01-replica-l1.py | match |
| statement, c=2 | 14, 100, 50, 100 differs from 50 | same script | match |
| derivation note | (2 * 2) * (3 * 3 + 4 * 4) = 100 | same script, checks=22 failed=0 | match |

## Scanner output
HIGH 0. MEDIUM 0. LOW 2, both on TENSOR-ASSUMPTION-COUNTERMODELS (R10, five cited modules in no replay receipt; R5, 1/2 and 1/4 in an existing note). Those pages were sha-touched because dag/derivation_dag.json changed. They were not edited as claims and are not fixed here.

The evidence page for this node lists both qualified names and receipt anchors, so its symbol count is higher than the eleven public theorems. That count is the generator's inventory, not an extra theorem.
