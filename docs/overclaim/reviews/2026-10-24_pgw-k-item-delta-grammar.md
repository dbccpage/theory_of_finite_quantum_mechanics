# Review of PGW-K-ITEM-DELTA-GRAMMAR

Scope: campaign derive/PGW-K-ITEM-DELTA-GRAMMAR against origin/main 1fa451fe1eac640d84f0c34ba88a71dcdd32dfb6. Reviewed against the statements as they stand in this worktree. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: `scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH=0 MEDIUM=0 LOW=3). Read the node statement and bottleneck, the TFQ-0490 record, `lean4/CampaignPgwKItemDeltaGrammar.lean`, the four source definitions in `Minimality.lean`, the replay receipt, and `checks/independent/pgw-k-item-delta-grammar.py` (`checked 32 claims, failures 0`). Lake build completed before this review. Cargo was not run. The module does not import the Genesis development.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays OPEN. record_status stays OPEN_OBLIGATION. AuthorityEffect stays None.

Corrections to the PR's own text:

- None. The narrowed statement matches the four copied lists. A k-item grammar for k at least 3, an exhaustive cost-two enumeration, and a response-size bound stay unresolved.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-K-ITEM-DELTA-GRAMMAR | `pgwKItem_lengths` (`lean4/CampaignPgwKItemDeltaGrammar.lean:30`), `pgwKItem_arities` (`:35`), `pgwKItem_arity_sum` (`:40`), `pgwKItem_pairwise` (`:43`), `pgwKItem_three_length` (`:49`), `pgwKItem_three_above_two` (`:53`) | NARROWED | Four named lists. Status stays OPEN. |

Atomic claims:

| Claim | Match |
|---|---|
| Each of deltaU0, deltaU1, deltaBL, deltaBD has length 2 | `pgwKItem_lengths` |
| New-form arities are 1, 1, 2, and 2 | `pgwKItem_arities` |
| Arity sum is 6 | `pgwKItem_arity_sum` |
| Argument lists are [0], [1], [0, 1], and [0, 0] | the four definitions; the independent check reads the same shapes from `Minimality.lean` |
| Six pairwise differences | `pgwKItem_pairwise` |
| One three-item list has length 3, and 3 > 2 | `pgwKItem_three_length`, `pgwKItem_three_above_two` |
| Exhaustive cost-two enumeration, k at least 3, response-size bound | stated as open |

`#print axioms`: `pgwKItem_arities` and `pgwKItem_arity_sum` use propext. The other four theorems depend on no axioms. No `sorry`, `admit`, `axiom`, `native_decide`, or `unsafe` in the new module.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Lengths | 2, 2, 2, 2 | explicit lists | match |
| Arities | 1, 1, 2, 2 | first form component | match |
| Arity sum | 6 | 1+1+2+2 | match |
| Pairwise comparisons | 6 | C(4, 2) | match |
| Three-item length | 3, and 3 > 2 | a form plus two instance steps | match |
| Independent check | 32 claims, 0 failures | `python -I -X utf8 checks/independent/pgw-k-item-delta-grammar.py` | match |
| Lake build | exit 0, wall 22.489s, module job 1.2s | receipt | match |
| README facts | nodes 925, routes 934, records 977, failures 3; lean refs 2286; lean4 files 999; Lake 90 / 942 | `build_readme_facts.py --check` current | match |
| Validator | failures=3 | pre-existing unknown key `python` on three import nodes | left as on main |

## Scanner output

HIGH 0, MEDIUM 0. LOW findings are outside this node and were left in place: R10 `TENSOR-ASSUMPTION-COUNTERMODELS`; R5 on `tfq_1019_fq_gap_tensor_uniqueness.md` (`20261019`); R5 on `tfq_0413_tensor_assumption_countermodels.md` (`1/2`, `1/4`). No baseline entry proposed. `sync_pregenesis_to_wdp.py --check` stays stale, including the four TFQ-0519 paths. That phrase was not rewritten. The hand-edited TFQ-0490 paper is also stale against a full pregenesis render, and that render was not run.
