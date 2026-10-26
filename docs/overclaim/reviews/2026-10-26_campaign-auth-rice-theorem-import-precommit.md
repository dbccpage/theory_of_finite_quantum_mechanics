# Overclaim review: AUTH-RICE-THEOREM-IMPORT

AuthorityEffect: None.

## Scope

Branch `derive/AUTH-RICE-THEOREM-IMPORT` against merge base `4fea09ae176a`. One node. Status was not raised.

## Method

`python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (no `--write`). Statement-vs-theorem reading of `dag/derivation_dag.json` and `lean4/CampaignAuthRiceTheoremImport.lean`, including the `#print axioms` lines. Exact recomputation by `python -I -X utf8 checks/independent/auth-rice-theorem-import.py`. Lean was rebuilt in this worktree (`lake build CampaignAuthRiceTheoremImport`, module job 780 ms, exit 0).

## Result

1 FULL against the narrowed standing statement, 0 NARROWED, 0 OVERCLAIM. Campaign outcome: Narrowed. Status stays `IMPORTED_ASSUMPTION`.

## Corrections to the PR's own text

None. The standing statement is the three-code table. Rice's theorem stays in the bottleneck.

## Per-node table

Node: `AUTH-RICE-THEOREM-IMPORT`. Status: `IMPORTED_ASSUMPTION`.

| Claim in the standing statement | Declaration | Verdict |
| --- | --- | --- |
| Code 0 sends 0 to 0 and 1 to 1 | `beh00`, `beh01` (lines 21, 23) | FULL |
| Code 1 sends 0 to 0 and 1 to 1 | `beh10`, `beh11` (lines 25, 27) | FULL |
| Code 2 sends 0 to 0 and 1 to 0 | `beh20`, `beh21` (lines 29, 31) | FULL |
| Identity-table bit true, true, false at codes 0, 1, 2 | `id0`, `id1`, `id2` (lines 33, 35, 37) | FULL |
| Code-zero bit true, false, false at codes 0, 1, 2 | `z0`, `z1`, `z2` (lines 39, 41, 43) | FULL |

Rice's theorem for a Turing-complete language, Mathlib `ComputablePred.rice` and `rice₂`, and any semantic property of `Nat.Partrec.Code` stay in the bottleneck. No declaration states them.

Axiom lines 45–56: `beh00` through `beh21` depend on `propext`. `id0`, `id1`, `id2`, `z0`, `z1` and `z2` depend on `propext`, `Classical.choice` and `Quot.sound`.

## Numbers recomputed

Independent check output: `auth-rice-theorem-import failures=0 codes=3 rows=12 id_true=2 code_zero_true=1`.

| Number | Recomputation | Match |
| --- | --- | --- |
| 12 | six behavior entries plus three identity bits plus three code-zero bits | match |
| 2 | identity-table bit true at codes 0 and 1 | match |
| 1 | code-zero bit true only at code 0, among the three codes | match |

README census figures were rewritten by `scripts/build_readme_facts.py` and confirmed by `--check`. The deltas from this change are one derivation note (1115 to 1116), twelve Lean references (2545 to 2557), one Lean file (1046 to 1047), one library (137 to 138), one module root (989 to 990), and one fewer node with an empty Lean list (350 to 349).

The strings 4.33.1 and 4.35.0 are version labels in the pre-existing external witness. They are not arithmetic results of this table.

## What the scanner could not decide

Nothing further on this node. The scan reported HIGH=0, MEDIUM=0, LOW=3, the same three baseline items: R10 `TENSOR-ASSUMPTION-COUNTERMODELS`, R5 `tfq_1019_fq_gap_tensor_uniqueness.md` number 20261019, and R5 `tfq_0413_tensor_assumption_countermodels.md` fractions 1/2 and 1/4. No new finding.
