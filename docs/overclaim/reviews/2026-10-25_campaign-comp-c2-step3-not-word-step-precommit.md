# Review of campaign COMP-C2-STEP3-NOT-WORD-STEP

Scope: worktree branch `derive/COMP-C2-STEP3-NOT-WORD-STEP` before the pull request, base `origin/main` at `7fa69d621c27`. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the domain record in `dag/fragments/unified_dag.json`, the generated node in `dag/derivation_dag.json`, `lean4/CampaignCompC2Step3NotWordStep.lean`, the replay receipt, and `checks/independent/comp-c2-step3-not-word-step.py`. Scanner: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). Lean was built earlier in this worktree (`lake build CampaignCompC2Step3NotWordStep`, exit 0, wall 3620 ms). This review did not rebuild Lean.

Result: 1 node FULL on the standing statement, 0 NARROWED further, 0 OVERCLAIM. No node was raised. Status stays OPEN. The original encoding obligation is not discharged.

Corrections to the PR's own text:
- None. The standing statement is the three list moves and `merge01`. The bottleneck keeps the Genesis Step3 encoding open.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| COMP-C2-STEP3-NOT-WORD-STEP | `addTermWordStep`, `addAssertionWordStep`, `identifyWordStep`, `merge01SendsBothToZero`, `merge01FixesOther` in `lean4/CampaignCompC2Step3NotWordStep.lean` | FULL for the standing statement | Each atomic sentence of the standing statement is the type of one of those declarations. Status stays OPEN. An encoding of every Genesis Step3 state is not a theorem. |

Atomic claims of the standing statement:

- Appending 1 takes `[0]` to `[0, 1]` by one hole replacement of an empty block. `addTermWordStep` (`lean4/CampaignCompC2Step3NotWordStep.lean:12-14`) states `applies (HoleRule.mk [] [1]) [0] [] [0] [0, 1]`. `applies` (`:9-10`) is `word = left ++ lhs ++ right` and `result = left ++ rhs ++ right`. Axioms: none.
- Appending the block `[0, 1]` takes `[0, 1]` to `[0, 1, 0, 1]` by one hole replacement of an empty block. `addAssertionWordStep` (`:16-18`). Axioms: none.
- Deleting a final 1 takes `[0, 1]` to `[0]` by one hole replacement of the block `[1]`. `identifyWordStep` (`:20-22`). Axioms: none.
- The map sending 1 to 0 and every other natural number to itself: `merge01` (`:24-25`) is `if t = 1 then 0 else t`, and `merge01FixesOther` (`:30-32`) states `(t : Nat) (h : t ≠ 1) : merge01 t = t`. Axioms: propext.
- That map sends both 0 and 1 to 0. `merge01SendsBothToZero` (`:27-28`) states `merge01 0 = 0 ∧ merge01 1 = 0 ∧ 0 ≠ 1`. Axioms: none.

Not discharged, and not in the standing statement: a word encoding of every Genesis Step3 state (finite term set, finite assertion set, two named terms) under which add-term, add-assertion and identify are word steps, and a demonstration that none exists. Those remain the bottleneck. The node was not given PROVED_LEAN.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Standing statement and independent check | `[0]` with empty block replaced by `[1]` yields `[0, 1]`; `[0, 1]` with empty block replaced by `[0, 1]` yields `[0, 1, 0, 1]`; `[0, 1]` with block `[1]` replaced by `[]` yields `[0]`; `merge01(0)=0`, `merge01(1)=0`, `0≠1`, `merge01(2)=2` | `python -I -X utf8 checks/independent/comp-c2-step3-not-word-step.py` printed `failures=0` | match |
| README lean references present | 2292 | count of node `lean` refs whose path is a file | match |
| README derivation papers | 1069 | `rglob('*.md')` under `dag/derivations` stage folders | match |
| README review directories / nodes | 208 / 177 | `dag/results/*/reviews/*` directories | match |
| README P4 mutations rejected | 47271 | max `rejected_P4_mutations` per review directory, summed | match |
| README lake libraries / module roots | 91 / 943 | `lean_lib` lines and names inside `roots := #[...]` | match |
| README dag/results test functions | py 4049, rs 7995 | `def test_` and `#[test]` under `dag/results` | match |
| Evidence grades | E1 221, E3 500 (was E1 222, E3 499) | this node moves E1 to E3; other grade totals unchanged by that move | match |
| Evidence distinct in-repo Lean declarations | 1868 (was 1863) | plus the five new anchors | match |
| Evidence receipt-backed / itemised | 1806 / 1738 (was 1801 / 1733) | plus the five receipt anchors | match |
| `broken_reference` flags | 53 (was 70) | the 17 dropped rows name tracked files that exist in this checkout | match |
| Nodes citing no Lean declaration | 372 (was 373) | this node now cites Lean | match |
| Contract row `all_passed = true` and the unchanged inventory rows | as written by `scripts/build_readme_facts.py --write` | `--check` passed; those rows were not re-added by hand | match |

## Scanner output
HIGH 0, MEDIUM 0. No status rose (R9 quiet). LOW findings, left as they stand because they are outside this node:

- R10 `TENSOR-ASSUMPTION-COUNTERMODELS`: cited Lean modules in no replay receipt.
- R5 `dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md`: `20261019`.
- R5 `dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md`: `1/2`, `1/4`.

`merge01FixesOther` has a binder, so the words "every other natural number" sit on a general declaration. The closed list moves do not use those words. AuthorityEffect: None.
