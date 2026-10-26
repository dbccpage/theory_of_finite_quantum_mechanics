# Review of campaign FSP-THETA-TERM-COMPLEX-WEIGHT

Scope: campaign checkout against origin/main 4fea09ae176aae31115e38bb2b21819237055811, before the pull request opened. The node is named in the table. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the standing statement and bottleneck in dag/fragments/unified_dag.json and the generated node in dag/derivation_dag.json; read lean4/CampaignFspThetaTermComplexWeight.lean through the declarations and the #print axioms lines; read checks/independent/fsp-theta-term-complex-weight.py and dag/derivations/independent/fsp-theta-term-complex-weight.md. Scanner: python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict (exit 0, HIGH 0, MEDIUM 0, LOW 3). Lean was built in this worktree; this note does not rebuild it again.

Result: 0 FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays IMPORTED_ASSUMPTION.

Corrections to the PR's own text:
- The standing sentence is the four-index Gaussian-integer table. An exponential, a real angle, a plaquette sum, and a Monte Carlo sampler stay in the bottleneck.
- The source sentence about S_theta = i theta Q_top and a positive-weight sampler is not the standing statement.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| FSP-THETA-TERM-COMPLEX-WEIGHT | quarter0, quarter1, quarter2, quarter3, quarter4, mulNegI_eq_gMul, phaseProduct, weight00, weight10, weight20, weight30, weight01, weight11, weight21, weight31, im01, im11, im21, im31, im11_ne, im31_ne, re21, notPositive21, positive01, charge1PositiveOnlyAtZero | NARROWED | Standing arithmetic matches the declarations. The prior exponential sentence is not the standing statement. |

Statement-vs-theorem:

| Atomic claim | Declaration | Where | Axioms |
|---|---|---|---|
| Quarter turns of (1, 0) at indices 0, 1, 2, 3, 4 are (1, 0), (0, -1), (-1, 0), (0, 1), (1, 0) | quarter0, quarter1, quarter2, quarter3, quarter4 | lean4/CampaignFspThetaTermComplexWeight.lean:20-24 | none |
| The turn (a, b) to (b, -a) equals multiplication by (0, -1) | mulNegI_eq_gMul, gMul | lean4/CampaignFspThetaTermComplexWeight.lean:10 and :26 | propext, Quot.sound |
| (1, 0) times (0, -1) is (0, -1) | phaseProduct | lean4/CampaignFspThetaTermComplexWeight.lean:30 | none |
| Charge 0 keeps (1, 0) at indices 0, 1, 2 and 3 | weight00, weight10, weight20, weight30 | lean4/CampaignFspThetaTermComplexWeight.lean:32-35 | none |
| Charge 1 uses the quarter-turn value | weight01, weight11, weight21, weight31 | lean4/CampaignFspThetaTermComplexWeight.lean:37-40 | none |
| Second coordinates at charge 1 are 0, -1, 0, 1 | im01, im11, im21, im31 | lean4/CampaignFspThetaTermComplexWeight.lean:42-45 | none |
| The second coordinate is nonzero at indices 1 and 3 | im11_ne, im31_ne | lean4/CampaignFspThetaTermComplexWeight.lean:47-48 | none |
| At index 2 with charge 1 the first coordinate is -1 and is not positive | re21, notPositive21 | lean4/CampaignFspThetaTermComplexWeight.lean:50 and :52 | none |
| Among the four charge-1 pairs, only index 0 is positive in the first coordinate with second coordinate 0 | positive01, charge1PositiveOnlyAtZero | lean4/CampaignFspThetaTermComplexWeight.lean:54 and :56 | none |

An exponential, a real angle, a plaquette sum, and a Monte Carlo sampler are not declarations in this module.

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| quarter turns | (1, 0), (0, -1), (-1, 0), (0, 1), (1, 0) | recurrence in checks/independent/fsp-theta-term-complex-weight.py, exit 0 | match |
| product (1, 0) * (0, -1) | (0, -1) | same script | match |
| charge 0 weights | four copies of (1, 0) | same script | match |
| charge 1 weights | the four quarter values | same script | match |
| index 2 first coordinate | -1, not greater than 0 | same script | match |
| lake build | exit 0, wall 8.926 s, module job 882 ms | lake log for CampaignFspThetaTermComplexWeight | match |
| axiom lines | 24 empty lists; mulNegI_eq_gMul uses propext and Quot.sound | #print axioms in that build | match |
| README census rows touched by this change | papers 1116, resolving Lean refs 2570, lean4 files 1047, libraries 138, roots 990 | scripts/build_readme_facts.py --check exit 0 | match |
| evidence grades | E0 153, E1 208, E2 35, E3 529 | dag/evidence/build_evidence.py --check exit 0 | match |
| receipt-backed declarations | 2085 of 2146, of which 2018 are itemised | same evidence page | match |

## Scanner output
HIGH findings: none. MEDIUM findings: none.

LOW findings, left as they stood (they name other nodes and were already present on the base):
- R10 TENSOR-ASSUMPTION-COUNTERMODELS: cited Lean modules in no replay receipt.
- R5 dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md: number 20261019.
- R5 dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md: fractions 1/2 and 1/4.

No baseline entry added. The receipt itemises all 25 declarations.
