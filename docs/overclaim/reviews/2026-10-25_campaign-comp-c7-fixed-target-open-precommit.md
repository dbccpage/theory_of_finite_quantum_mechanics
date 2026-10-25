# Review of campaign COMP-C7-FIXED-TARGET-OPEN

Scope: worktree branch `derive/COMP-C7-FIXED-TARGET-OPEN` before the pull request, base `origin/main` at `7fa69d621c27`. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the domain record, the generated node, `lean4/CampaignCompC7FixedTargetOpen.lean`, the replay receipt, and `checks/independent/comp-c7-fixed-target-open.py`. Scanner: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). The module was built in this worktree (`lake build CampaignCompC7FixedTargetOpen`, exit 0, wall 9212 ms, module job 874 ms). This review did not rebuild Lean.

Result: 1 node FULL on the standing statement, 0 further narrowing, 0 OVERCLAIM. No node was raised. Status stays OPEN. Reach for the extended rule set R0 prime is not discharged.

Corrections to the PR's own text:
- None. The standing statement is the two erasures to `[0]`. The bottleneck keeps Reach for R0 prime open.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| COMP-C7-FIXED-TARGET-OPEN | `eraseOneToFixed`, `eraseTwoToFixed` in `lean4/CampaignCompC7FixedTargetOpen.lean` | FULL for the standing statement | Each sentence is the type of one declaration. Status stays OPEN. Reach of R0 prime from `startWord x` to a fixed target is not a theorem. |

Atomic claims:

- Erasing the block `[1]` from the word `[1, 0]` by one hole replacement yields the fixed word `[0]`. `eraseOneToFixed` (`lean4/CampaignCompC7FixedTargetOpen.lean:12-14`) states `applies (HoleRule.mk [1] []) [] [0] [1, 0] [0]`. `applies` (`:9-10`) is `word = left ++ lhs ++ right` and `result = left ++ rhs ++ right`. Axioms: none.
- Erasing the block `[2]` from the word `[2, 0]` by one hole replacement yields the same fixed word `[0]`. `eraseTwoToFixed` (`:16-18`) states `applies (HoleRule.mk [2] []) [] [0] [2, 0] [0]`. Both result lists are `[0]`. Axioms: none.

Not discharged: Reach of the extended rule set R0 prime from `startWord x` to one fixed target word exactly when `univFun x` is defined. That remains the bottleneck. The node was not given PROVED_LEAN.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Standing statement and independent check | `[1, 0]` erases `[1]` to `[0]`; `[2, 0]` erases `[2]` to `[0]`; both results are `[0]` | `python -I -X utf8 checks/independent/comp-c7-fixed-target-open.py` printed `failures=0` | match |
| README lean references present | 2289 | 2287 on the base plus the two new anchors | match |
| README derivation papers | 1069 | 1068 on the base plus this note | match |
| README lake libraries / module roots | 91 / 943 | 90 / 942 on the base plus one `lean_lib` and one root | match |
| Evidence grades | E1 221, E3 500 | this node moves one OPEN node from E1 to E3 (222 and 499 on the base) | match |
| Evidence distinct in-repo Lean declarations | 1865 | 1863 on the base plus two anchors | match |
| Evidence receipt-backed / itemised | 1803 / 1735 | 1801 / 1733 on the base plus two receipt anchors | match |
| Nodes citing no Lean declaration | 372 | 373 on the base, minus this node | match |
| Review directories, P4 total, dag lean files, and snapshot test counts | as written by `scripts/build_readme_facts.py --write` | `--check` passed on this checkout | match |

## Scanner output
HIGH 0, MEDIUM 0. No status rose. LOW findings left as they stand, outside this node:

- R10 `TENSOR-ASSUMPTION-COUNTERMODELS`: cited Lean modules in no replay receipt.
- R5 `dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md`: `20261019`.
- R5 `dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md`: `1/2`, `1/4`.

The two moves are closed lists. The standing statement does not say that every halting word reduces. AuthorityEffect: None.
