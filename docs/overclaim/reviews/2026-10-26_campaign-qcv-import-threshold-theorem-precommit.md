# Overclaim review: QCV-IMPORT-THRESHOLD-THEOREM

AuthorityEffect: None.

## Scope

Branch `derive/QCV-IMPORT-THRESHOLD-THEOREM` against merge base `4fea09ae176a`. One node, `QCV-IMPORT-THRESHOLD-THEOREM`. Status was not raised.

## Method

`python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (no `--write`). Statement-vs-theorem reading of `dag/derivation_dag.json` and `lean4/CampaignQcvImportThresholdTheorem.lean`, including the `#print axioms` lines. Exact integer recomputation by `python -I -X utf8 checks/independent/qcv-import-threshold-theorem.py`. Lean was rebuilt in this worktree (`lake build CampaignQcvImportThresholdTheorem`, module job 788 ms, exit 0).

## Result

1 FULL against the narrowed standing statement, 0 NARROWED, 0 OVERCLAIM. Campaign outcome: Narrowed. Status stays `IMPORTED_ASSUMPTION`.

## Corrections to the PR's own text

None. The standing statement is the integer orbit. The literature threshold theorems stay in the bottleneck.

## Per-node table

Node: `QCV-IMPORT-THRESHOLD-THEOREM`. Status: `IMPORTED_ASSUMPTION` (`dag/derivation_dag.json` statement at the node object).

| Claim in the standing statement | Declaration | Verdict |
| --- | --- | --- |
| For each integer n, t(n) = 2*n*n | `t_spec` (`lean4/CampaignQcvImportThresholdTheorem.lean:8`) | FULL |
| t(0) = 0 | `step_zero` (line 10) | FULL |
| t(1) = 2 | `step_one` (line 12) | FULL |
| t(2) = 8 | `step_two` (line 14) | FULL |
| t(8) = 128 | `step_eight` (line 16) | FULL |
| Three applications of t starting at 1 yield 128 | `orbit_three` (line 18): `t (t (t 1)) = 128` | FULL |
| 2*0 = 0 | `scale_zero` (line 22) | FULL |
| 2*1 = 2 | `scale_one` (line 24) | FULL |

`mul_eight` (line 20) states 2*8*8 = 128. The standing statement does not use that product sentence; the derivation note does, and the declaration matches it.

The imported citation of the Shor, Aharonov and Ben-Or, Kitaev, Knill–Laflamme–Zurek, and Aliferis–Gottesman–Preskill threshold theorems is the bottleneck, not a clause of the standing statement. No declaration states those theorems.

Axiom lines 26–34: each of the nine declarations does not depend on any axioms. The empty lists sit inside the allowed set `propext`, `Classical.choice`, `Quot.sound`.

## Numbers recomputed

Independent check output: `qcv-import-threshold-theorem failures=0 orbit=128 scale0=0 scale1=2 rows=9`.

| Number | Recomputation | Match |
| --- | --- | --- |
| 128 | 2*8*8 = 2*64 = 128; also `t(8)` and `t(t(t(1)))` | match |
| 8 | 2*2*2 = 8, which is `t(2)` and `t(t(1))` | match |
| 2 | `t(1)` and `2*1` | match |
| 0 | `t(0)` and `2*0` | match |
| 9 | rows in the independent check, and Lean declarations on the node | match |

README census figures were rewritten by `scripts/build_readme_facts.py` and confirmed by `--check`. The deltas from this change are one derivation note (1115 to 1116), nine Lean references (2545 to 2554), one Lean file (1046 to 1047), one library (137 to 138), one module root (989 to 990), and one fewer node with an empty Lean list (350 to 349).

## What the scanner could not decide

Nothing further on this node. The scan reported HIGH=0, MEDIUM=0, LOW=3, the same three baseline items: R10 `TENSOR-ASSUMPTION-COUNTERMODELS`, R5 `tfq_1019_fq_gap_tensor_uniqueness.md` number 20261019, and R5 `tfq_0413_tensor_assumption_countermodels.md` fractions 1/2 and 1/4. No new finding.
