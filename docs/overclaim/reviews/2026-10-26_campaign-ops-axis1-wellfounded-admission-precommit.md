# Review of campaign OPS-AXIS1-WELLFOUNDED-ADMISSION

Scope: worktree branch `derive/OPS-AXIS1-WELLFOUNDED-ADMISSION` against `origin/main` at `4fea09ae176aae31115e38bb2b21819237055811`. Reviewed against the narrowed statement in `dag/fragments/foc035_observer_presheaf.json`. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound. Campaign outcome is Narrowed. The status stays IMPORTED_ASSUMPTION. No node was raised.

Method: `scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3, the three baseline findings only). Read the node statement, bottleneck, imported structure, route `OPS-R-AXIS1-WELLFOUNDED-ADMISSION`, and `lean4/CampaignOpsAxis1WellfoundedAdmission.lean` with its `#print axioms` lines. The campaign build of that module finished with exit 0 and module job 770 ms before this review. This review did not run a second build. The independent script was run with `python -I -X utf8`.

Result: 1 node FULL against the narrowed statement, 0 NARROWED, 0 OVERCLAIM. No node was raised.

Corrections to the PR's own text:

- None.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| OPS-AXIS1-WELLFOUNDED-ADMISSION | `pred0`–`pred2`, `adm0`–`adm2`, `none0`–`none2`, `zb0`–`zb2`, `zero0`–`zero2` in `lean4/CampaignOpsAxis1WellfoundedAdmission.lean:25-43` | FULL against the narrowed statement | Each mathematical sentence of the standing statement is the type of one of those declarations. Axioms are `propext` only. The Genesis theorem named in the statement is a non-claim: the status stays IMPORTED_ASSUMPTION, `lean` stays empty, and route `OPS-R-AXIS1-WELLFOUNDED-ADMISSION` stays `GAP_NO_DERIVATION`. |

Atomic claims:

- Candidate 0 has no predecessor → `pred0` (`lean4/CampaignOpsAxis1WellfoundedAdmission.lean:25`).
- Candidate 1 names candidate 0 → `pred1` (`:26`).
- Candidate 2 names candidate 1 → `pred2` (`:27`).
- For every base assignment, admission at 0 equals the base bit at 0 → `adm0` (`:29`), binder `b : Fin 3 → Bool`.
- Admission at 1 equals the base bit at 1 disjoined with admission at 0 → `adm1` (`:30`).
- Admission at 2 equals the base bit at 2 disjoined with admission at 1 → `adm2` (`:31`).
- The all-false base admits none of the three → `none0`, `none1`, `none2` (`:33-35`).
- The base that is true at 0 and false at 1 and at 2 admits all three → `zb0`, `zb1`, `zb2`, `zero0`, `zero1`, `zero2` (`:37-43`).
- The Genesis theorem `collapsed_of_no_insts` stays imported and is not re-run → not a Lean type. Recorded by status IMPORTED_ASSUMPTION and by the bottleneck.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Independent script stdout | `failures=0` | Script exit code 0; failure list length 0 | Match |
| Independent script stdout | `bases=8` | `range(8)` has 8 values; `2*2*2 = 8` boolean assignments on three candidates | Match |
| Independent script stdout and receipt anchors | `rows=15` | Fifteen `theorem` lines in `CampaignOpsAxis1WellfoundedAdmission.lean:25-43` | Match |
| README derivation papers | 1115 to 1116 | `scripts/build_readme_facts.py --check` after the new independent note | Match |
| README tracked `lean4` files | 1046 to 1047 | Same check; one new module | Match |
| README lake libraries / roots | 137 / 989 to 138 / 990 | Same check; one new `lean_lib` and one root | Match |
| README Lean references | 2545 | Unchanged in the README diff. The node `lean` list stays empty | Match |

Single digits 0, 1 and 2 in the statement are below the scanner's two-digit threshold. `WDP-CH14` and `L035` remain in the bottleneck and source status as source labels. The independent script comment echoes those labels and says they are not arithmetic.

## Scanner output

HIGH 0. MEDIUM 0. LOW 3, all baseline and outside this diff: R10 `TENSOR-ASSUMPTION-COUNTERMODELS`; R5 `tfq_1019_fq_gap_tensor_uniqueness.md` number `20261019`; R5 `tfq_0413_tensor_assumption_countermodels.md` fractions `1/2` and `1/4`. No baseline entry added.

The scanner does not judge that a definitional `rfl` chain is the whole content of a finite stand-in. The types above are that content. The original ledger sentence about the Genesis calculus is no longer the standing statement; it remains the imported structure and the open bottleneck.
