# Review of campaign COMP-C6-TM0-OUTPUT-FORM-OPEN

Scope: worktree branch `derive/COMP-C6-TM0-OUTPUT-FORM-OPEN` before the pull request, base `origin/main` at `7fa69d621c27`. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read the domain record, the generated node, `lean4/CampaignCompC6Tm0OutputFormOpen.lean`, the replay receipt, and `checks/independent/comp-c6-tm0-output-form-open.py`. Scanner: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). The module was built in this worktree (`lake build CampaignCompC6Tm0OutputFormOpen`, exit 0, wall 3421 ms, module job 701 ms). This review did not rebuild Lean.

Result: 1 node FULL on the standing statement, 0 further narrowing, 0 OVERCLAIM. No node was raised. Status stays OPEN. The M0 tape obligation is not discharged.

Corrections to the PR's own text:
- None. The standing statement is the blank-cell writer and `evalConst`. The bottleneck keeps the Mathlib TM0 output form open.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| COMP-C6-TM0-OUTPUT-FORM-OPEN | `writeHaltFromBlank`, `evalConstReturns`, `constAgrees` in `lean4/CampaignCompC6Tm0OutputFormOpen.lean` | FULL for the standing statement | Each atomic sentence is the type of one of those declarations. Status stays OPEN. Membership of `v` in `Code.eval c n` tied to the tape of `M0` is not a theorem. |

Atomic claims:

- For every natural number `v`, writing `v` into the blank cell that is not halted and holds 0 equals the halted cell that holds `v`. `writeHaltFromBlank` (`lean4/CampaignCompC6Tm0OutputFormOpen.lean:15-17`) states `writeHalt v { halted := false, value := 0 } = { halted := true, value := v }`. Axioms: none.
- For every natural number `v` and every natural number `n`, `evalConst v n` equals `v`. `evalConstReturns` (`:19-20`) states `evalConst v n = v`. Axioms: none.
- The value written into that blank cell equals `evalConst v n`. `constAgrees` (`:22-24`) states `(writeHalt v { halted := false, value := 0 }).value = evalConst v n`. Axioms: none.

Not discharged: a natural number `v` lies in `Code.eval c n` exactly when `M0` halts from `initCfg0` with the encoded `v` on its output tape. That remains the bottleneck. The node was not given PROVED_LEAN.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Blank cell and independent check | blank value 0; for `v` in 0..4 the writer halts with value `v`; for `n` in 0..3, `evalConst(v, n)` equals that value | `python -I -X utf8 checks/independent/comp-c6-tm0-output-form-open.py` printed `failures=0` | match |
| README lean references present | 2290 | 2287 on the base plus the three new anchors | match |
| README derivation papers | 1069 | 1068 on the base plus this note | match |
| README lake libraries / module roots | 91 / 943 | 90 / 942 on the base plus one `lean_lib` and one root | match |
| Evidence grades | E1 221, E3 500 | this node moves one OPEN node from E1 to E3 (222 and 499 on the base) | match |
| Evidence distinct in-repo Lean declarations | 1866 | 1863 on the base plus three anchors | match |
| Evidence receipt-backed / itemised | 1804 / 1736 | 1801 / 1733 on the base plus three receipt anchors | match |
| Nodes citing no Lean declaration | 372 | 373 on the base, minus this node | match |
| `broken_reference` flags | 53 (was 70) | generator refresh; the dropped rows name tracked files. Not a new theorem. | match |
| Review directories 208, P4 total 47271, dag lean files 2428, snapshot tests py 4049 and rs 7995 | as written by `scripts/build_readme_facts.py --write` | `--check` passed on this checkout | match |

## Scanner output
HIGH 0, MEDIUM 0. No status rose. LOW findings left as they stand, outside this node:

- R10 `TENSOR-ASSUMPTION-COUNTERMODELS`: cited Lean modules in no replay receipt.
- R5 `dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md`: `20261019`.
- R5 `dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md`: `1/2`, `1/4`.

The quantifiers "every natural number" sit on declarations with binders `v` and `n`. The Python loop is a finite sample of those same equalities. AuthorityEffect: None.
