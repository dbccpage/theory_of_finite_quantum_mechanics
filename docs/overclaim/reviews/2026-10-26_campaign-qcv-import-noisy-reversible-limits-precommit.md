# Overclaim review: QCV-IMPORT-NOISY-REVERSIBLE-LIMITS

AuthorityEffect: None.

## Scope

Branch `derive/QCV-IMPORT-NOISY-REVERSIBLE-LIMITS` against merge base `4fea09ae176a`. One node. Status was not raised.

## Method

`python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (no `--write`). Statement-vs-theorem reading of `dag/derivation_dag.json` and `lean4/CampaignQcvImportNoisyReversibleLimits.lean`, including the `#print axioms` lines. Exact integer recomputation by `python -I -X utf8 checks/independent/qcv-import-noisy-reversible-limits.py`. Lean was rebuilt in this worktree (`lake build CampaignQcvImportNoisyReversibleLimits`, module job 770 ms, exit 0).

## Result

1 FULL against the narrowed standing statement, 0 NARROWED, 0 OVERCLAIM. Campaign outcome: Narrowed. Status stays `IMPORTED_ASSUMPTION`.

## Corrections to the PR's own text

None. The standing statement is the integer recurrence. The literature limitation stays in the bottleneck.

## Per-node table

Node: `QCV-IMPORT-NOISY-REVERSIBLE-LIMITS`. Status: `IMPORTED_ASSUMPTION`.

| Claim in the standing statement | Declaration | Verdict |
| --- | --- | --- |
| u(0) = 1, v(0) = 1, w(0) = 1 | `u_zero`, `v_zero`, `w_zero` (lines 18, 20, 22) | FULL |
| u(t+1) = 3*u(t) for each natural t | `u_step` (line 24) | FULL |
| v(t+1) = 4*v(t) for each natural t | `v_step` (line 26) | FULL |
| w(t+1) = 3*w(t) + 0 for each natural t | `w_step` (line 28) | FULL |
| u(1) = 3, v(1) = 4 | `u1`, `v1` (lines 30, 32) | FULL |
| u(2) = 9, v(2) = 16 | `u2`, `v2` (lines 34, 36) | FULL |
| u(3) = 27, v(3) = 64 | `u3`, `v3` (lines 38, 40) | FULL |
| u is strictly below v at steps 1, 2 and 3 | `below1`, `below2`, `below3` (lines 42, 44, 46) | FULL |
| w equals u at steps 0, 1, 2 and 3 | `w0_u`, `w1`, `w2`, `w3` (lines 48, 50, 52, 54) | FULL |

The Aharonov, Ben-Or, Impagliazzo and Nisan limitation stays in the bottleneck. No declaration states that citation, a trace norm, a depolarizing channel, or an independent per-qubit noise model.

Axiom lines 56–74: each of the nineteen declarations does not depend on any axioms. The empty lists sit inside the allowed set `propext`, `Classical.choice`, `Quot.sound`.

## Numbers recomputed

Independent check output: `qcv-import-noisy-reversible-limits failures=0 steps=3 u3=27 v3=64 rows=4`.

| Number | Recomputation | Match |
| --- | --- | --- |
| 16 | 4*4 = 16, which is v(2) | match |
| 27 | 3*9 = 27, which is u(3) | match |
| 64 | 4*16 = 64, which is v(3) | match |
| 9 | 3*3 = 9, which is u(2) | match |
| 19 | Lean declarations cited on the node | match |

README census figures were rewritten by `scripts/build_readme_facts.py` and confirmed by `--check`. The deltas from this change are one derivation note (1115 to 1116), nineteen Lean references (2545 to 2564), one Lean file (1046 to 1047), one library (137 to 138), one module root (989 to 990), and one fewer node with an empty Lean list (350 to 349).

## What the scanner could not decide

Nothing further on this node. The scan reported HIGH=0, MEDIUM=0, LOW=3, the same three baseline items: R10 `TENSOR-ASSUMPTION-COUNTERMODELS`, R5 `tfq_1019_fq_gap_tensor_uniqueness.md` number 20261019, and R5 `tfq_0413_tensor_assumption_countermodels.md` fractions 1/2 and 1/4. No new finding.
