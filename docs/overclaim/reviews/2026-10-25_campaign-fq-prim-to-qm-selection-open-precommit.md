# Review of FQ-PRIM-TO-QM-SELECTION-OPEN

Scope: branch `derive/FQ-PRIM-TO-QM-SELECTION-OPEN` before the pull request, base `7fa69d621c27`. Reviewed against the statement written by `dag/fragments/pfp_review_decisions.json` and applied by `dag/sync_pfp_results.py`. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read `.claude/skills/overclaim-hunter/SKILL.md` and `rubric.md`; ran `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3); read `lean4/CampaignFqPrimToQmSelection.lean` in full; rebuilt that module with Lean 4.35.0 (`lake build CampaignFqPrimToQmSelection`, read-only junction to the shared Mathlib cache). `#print axioms` reports no axioms for the four theorems. Recomputed the integers with `checks/independent/fq-prim-to-qm-selection-open.py` (`Fraction`, exit 0). Not rebuilt: the default Lean library, cargo, and the three older modules still cited on the node.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays CONDITIONAL.

Corrections to the PR's own text:
- The fraction words `1/5` and `1/17` are the reading of `quad0 / quadDen` and `quart0 / quartDen`. Lean states the integers and the cross-multiplication inequality `1 * 17 ≠ 1 * 5` (`normalized_first_weights_differ`, `lean4/CampaignFqPrimToQmSelection.lean:26`). It does not mention a rational type.
- The older citations `coupled_bipartite_and_tripartite_relational_master_certificate`, `fq_prim_to_qm_selection_finite_quotient_vs_continuum_gap` and `conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` do not state this sentence. They stay on the node and are outside the witness, as the bottleneck says.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| FQ-PRIM-TO-QM-SELECTION-OPEN | `quad_weights` (`lean4/CampaignFqPrimToQmSelection.lean:16`), `quart_weights` (`:21`), `normalized_first_weights_differ` (`:26`), `symmetric_agreement` (`:31`) | NARROWED | The statement's integer clauses match those four types. The prior selection sentence is in `pfp_review.prior_statement` and is not a theorem here. Status stays CONDITIONAL. |

Statement-vs-theorem rows:

| Claim | Declaration | Verdict |
|---|---|---|
| Amplitudes 1 and 2; quadratic numerators 1 and 4; sum 5; both positive | `quad_weights` | FULL |
| Quartic numerators 1 and 16; sum 17; both positive | `quart_weights` | FULL |
| Products 1*17 and 1*5 differ | `normalized_first_weights_differ` | FULL |
| Normalized weights 1/5 and 1/17 differ | integer cross-multiplication plus `checks/independent/fq-prim-to-qm-selection-open.py` | NARROWED |
| Equal amplitudes 1 and 1; both rules have numerators 1 and 1 with sum 2 | `symmetric_agreement` | FULL |
| Primitive difference selects no quantum model | not proved | NOT PROVED |

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| statement, quadratic | 1, 4, sum 5 | `1*1`, `2*2`, sum, in the independent script | match |
| statement, quartic | 1, 16, sum 17 | `1*1`, `4*4`, sum | match |
| statement, products | 17 and 5 | `1*17`, `1*5` | match |
| statement, fractions | 1/5, 4/5, 1/17, 16/17 | `Fraction` in the independent script | match |
| statement, equal amplitudes | 1, 1, sum 2 | `1*1` and `1+1` | match |
| README lean references | 2291 | prior table 2287 plus the four new citations | match |
| README lake libraries | 91 / 943 | prior 90 / 942 plus one `lean_lib` and one root | match |
| Lean axioms | none | `#print axioms` on the four theorems | match |

The README inventory rows for review directories, rejected mutations, `dag` `.lean` snapshots, and contract `all_passed` were rewritten by `scripts/build_readme_facts.py --write`. A direct `git ls-files` count of `.lean` paths gave dag 2428 and lean4 1000, matching that table. Those rows are inventory, not theorems of this node.

## Scanner output

HIGH 0, MEDIUM 0. LOW 3, not introduced as new claims of this node: R10 on `TENSOR-ASSUMPTION-COUNTERMODELS` (five Lean modules in no replay receipt); R5 on `tfq_1019_fq_gap_tensor_uniqueness.md` (the token `20261019`); R5 on `tfq_0413_tensor_assumption_countermodels.md` (`1/2`, `1/4`). No baseline change.
