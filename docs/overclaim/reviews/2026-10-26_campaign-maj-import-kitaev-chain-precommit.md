# Review of campaign-maj-import-kitaev-chain-precommit

Scope: worktree `C:\gw\derive-maj-kitaev`, branch `derive/MAJ-IMPORT-KITAEV-CHAIN`, base `origin/main` `4fea09ae176aae31115e38bb2b21819237055811`. Reviewed against the standing statement before the pull request was opened. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). Read the standing statement and bottleneck in `dag/derivation_dag.json`, the corpus record `MAJ-C6` in `dag/fragments/unified_dag.json`, `lean4/CampaignMajImportKitaevChain.lean`, and `dag/research/campaign_maj-import-kitaev-chain_lean_replay.json`. Recomputed the integers with `python -I -X utf8 checks/independent/maj-import-kitaev-chain.py` (exit 0). Lean, lake and cargo were not rebuilt for this review; the receipt records the earlier lake build.

Result: 1 node FULL on the standing narrowed statement, 0 NARROWED, 0 OVERCLAIM. No node was raised. Campaign outcome is Narrowed. Status stays IMPORTED_ASSUMPTION.

Corrections to the PR's own text:
- None. The standing statement is the index split and two integer comparisons. The fermion Hamiltonian, the BdG spectrum, and a physical wire stay in the bottleneck.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| MAJ-IMPORT-KITAEV-CHAIN | `edgeAbsent` lean4/CampaignMajImportKitaevChain.lean:7; `edgeWitness` :11; `insidePoint` :16; `outsidePoint` :20 | FULL | Every atomic claim of the standing statement is the type of one of those declarations. Axioms in the receipt are only propext, Classical.choice and Quot.sound. Status stays IMPORTED_ASSUMPTION. |

Atomic claims:
- For every natural L with 2 <= L and every natural j with 1 <= j and j <= L - 1, 2 * j differs from 1 and from 2 * L, and 2 * j + 1 differs from 1 and from 2 * L. Matched by `edgeAbsent` (lean4/CampaignMajImportKitaevChain.lean:7).
- At L = 2 and j = 1, 2 * 1 = 2, 2 * 1 + 1 = 3, 2 * 2 = 4, and the four differences hold. Matched by `edgeWitness` (lean4/CampaignMajImportKitaevChain.lean:11).
- t = 1, mu = 1, delta = 1 satisfies mu * mu < (2 * t) * (2 * t) and delta differs from 0. Matched by `insidePoint` (lean4/CampaignMajImportKitaevChain.lean:16).
- t = 1, mu = 3, delta = 1 fails mu * mu < (2 * t) * (2 * t), and delta differs from 0. Matched by `outsidePoint` (lean4/CampaignMajImportKitaevChain.lean:20).

The older citations `KitaevSweetSpotChain`, `mzm_boundary_decoupling` and `disjoint_majorana_pair_commute` are not used as the discharge of this statement. `mzm_boundary_decoupling` returns fields assumed by the structure.

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| statement, edgeWitness | 2, 3, 4 | 2 * 1 = 2, 2 * 1 + 1 = 3, 2 * 2 = 4, independent check | match |
| statement, insidePoint | 1 < 4 | 1 * 1 = 1 and (2 * 1) * (2 * 1) = 4, independent check | match |
| statement, outsidePoint | 9 < 4 is false | 3 * 3 = 9 and (2 * 1) * (2 * 1) = 4, independent check | match |

## Scanner output
HIGH 0. MEDIUM 0. LOW 3, all outside this node's statement:
- R10 TENSOR-ASSUMPTION-COUNTERMODELS: cited modules absent from a replay receipt. Repin rebinds tensor receipt hashes. Not this node.
- R5 `dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md`: number 20261019.
- R5 `dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md`: numbers 1/2 and 1/4.

No baseline change. The hunter did not rebuild Lean, lake or cargo.
