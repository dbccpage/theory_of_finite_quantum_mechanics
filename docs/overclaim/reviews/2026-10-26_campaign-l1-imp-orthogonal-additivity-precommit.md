# Review of campaign L1-IMP-ORTHOGONAL-ADDITIVITY

Scope: branch `derive/L1-IMP-ORTHOGONAL-ADDITIVITY` against merge base `4ead062a413c848c68bab12ac20879c077320f9d`. Reviewed against the statement in `dag/derivation_dag.json` as it stands in this worktree. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: `scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 4). Read the node statement and bottleneck, `lean4/CampaignL1OrthogonalAdditivity.lean`, the three cited declarations in `lean4/SectorFormUniqueness.lean`, the replay receipt, and `checks/independent/l1-imp-orthogonal-additivity.py`. This review pass did not rebuild Lean. The receipt records the earlier `lake build CampaignL1OrthogonalAdditivity` (exit 0). The source sha256 `4cd851daef44f1583b0de85c2cf7729cb4c959c52568265be656c6ec62dd0421` matches the file on disk.

Result: 1 node NARROWED, 0 OVERCLAIM. No node was raised. Status stays CONDITIONAL.

Corrections to the PR's own text:
- None. The old sentence that every off-diagonal Gram entry vanishes is no longer the standing statement. The 2 by 2 witness keeps entries 1 and -1.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| L1-IMP-ORTHOGONAL-ADDITIVITY | `InnerProductFable.SectorForm.offdiag_pair_sum_eq_zero`, `qf_eq_sum_diag_sq_of_sectorAdditive`, `offdiag_eq_zero`; `CampaignL1OrthogonalAdditivity.pairSum`, `entriesNotZero`, `readout`, `axisSum` | NARROWED | The sector-form sentences match the existing finite-n theorems. The 2 by 2 sentences match the new module. Arbitrary orthogonal frames stay supplied, so the status stays CONDITIONAL. |

Atomic claims:
- Pair sum of off-diagonal entries is zero for a sector-additive rational Gram matrix: `offdiag_pair_sum_eq_zero` (`lean4/SectorFormUniqueness.lean:112`).
- The quadratic readout equals the sum of the diagonal squares: `qf_eq_sum_diag_sq_of_sectorAdditive` (`lean4/SectorFormUniqueness.lean:171`).
- Symmetry is a further hypothesis before each off-diagonal entry is zero: `offdiag_eq_zero` takes `Gᵀ = G` (`lean4/SectorFormUniqueness.lean:123`).
- On entries 1, 1, -1, 1, the off-diagonal pair sums to 0: `pairSum` (`lean4/CampaignL1OrthogonalAdditivity.lean:9`).
- Neither off-diagonal entry is 0: `entriesNotZero` (`lean4/CampaignL1OrthogonalAdditivity.lean:12`).
- For every integer pair a, b the form equals a*a + b*b: `readout` (`lean4/CampaignL1OrthogonalAdditivity.lean:21`).
- That value equals the sum of the forms on (a, 0) and (0, b): `axisSum` (`lean4/CampaignL1OrthogonalAdditivity.lean:29`).
- Probability additive on arbitrary orthogonal frames stays supplied: not a theorem. It is the bottleneck.

`pairSum` and `entriesNotZero` have empty axiom lists. `readout` and `axisSum` depend only on propext. AuthorityEffect stays None.

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Statement, `pairSum` | 1 + (-1) = 0 | `decide` and the independent script | match |
| Statement, `entriesNotZero` | 1 ≠ 0 and -1 ≠ 0 | `decide` and the independent script | match |
| Independent checker | 869 checks, 0 failures | 2 closed checks plus 17 by 17 assignments and 3 checks each; 17 = 8 − (−8) + 1; 17*17*3 + 2 = 869 | match |
| Receipt wall time 26.154 s and module job 2000 ms | build measurement | not a mathematical identity; left as recorded | not recomputed as arithmetic |

## Scanner output
No HIGH or MEDIUM findings. LOW R5 cites 310, 465 and 620 in `dag/derivations/08_l1_to_l2/tfq_0299_orthogonal_additivity_is_an_extra_frame_law.md`, a note this PR does not edit. Those three integers are unrecomputed here. LOW R10 and the other R5 hits sit on nodes outside this derivation. No baseline edit.
