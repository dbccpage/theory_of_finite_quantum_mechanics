# Review of FQ-GAP-C500-ORIGINAL-TARGETS

Scope: campaign derivation on `derive/FQ-GAP-C500-ORIGINAL-TARGETS` against `origin/main` `85cc76d0df01bcd7433a626ba75c38ccc19dd2d7`. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: `scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3). Read the node statement, bottleneck and `pfp_review`, `lean4/CampaignFqGapC500Blocks.lean`, the replay receipt, and `checks/independent/fq-gap-c500-original-targets.py`. The module was built in this worktree (`lake build CampaignFqGapC500Blocks`, compiler 0.920s, exit 0). The ten `#print axioms` lines were empty. This review did not rebuild.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays OPEN.

Corrections to the PR's own text:
- None. Lean states the transcribed clause lists and the three integer evaluations. The YAML binding is the independent check.

## Per-node table
| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| FQ-GAP-C500-ORIGINAL-TARGETS | `c500_block_count`, `c500_clause_sum`, `c500_block01_clauses`, `c500_block10_clauses`, `c500_block10_length`, `c500_target_product`, `c500_target_last`, `ising_poly_one`, `ising_poly_neg_one`, `ising_poly_on_square_five` | NARROWED | Length 10, clause-length sum 21, empty B01 list, B10 clauses M2 M5 M7 J1 J2, `25*10=250`, `301+250-1=550`, and the integer polynomial values. The file reading is the independent check. Original contracts and the spectrum text as a real-number claim stay open. |

## Numbers recomputed
| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Clause lengths | sum 21 | 0+2+4+2+4+1+1+1+1+5 | match |
| Targets | 25 per block, 250, last id 550 | 25*10=250 and 301+250-1=550 | match |
| Polynomial | value 0 at 1, at -1, and at the substitution 5 | integer arithmetic | match |
| Coefficients | `(x^2-5)(x^2-1) = x^4-6*x^2+5` | integer coefficient product `[1,0,-6,0,5]` | match |
| Independent check | 60 claims, failures 0 | the script's check counter | match |
| README Lean references | 2125 | 2115 on origin/main plus 10 new refs | match |
| README derivation papers | 1044 | 1043 plus this note | match |
| README tracked lean4 | 974 | 973 tracked plus this module | match |
| README Lake libraries / roots | 65 / 917 | 64 / 916 plus one library and one root | match |
| Ledger Lean count | 12 | 2 prior refs plus 10 new symbols | match |
| README combined_files | 8879 | tracked `.contract.score.yaml` count | match |

## Scanner output
No HIGH or MEDIUM findings. Three LOW findings are outside this node: R10 on `TENSOR-ASSUMPTION-COUNTERMODELS`, R5 `20261019` in the tensor-uniqueness note, and R5 `1/2`, `1/4` in the tensor-countermodel note. No baseline change.

The clause theorems are `rfl` or `decide` on a transcribed list. Lean does not parse `gap_register.yaml`.
