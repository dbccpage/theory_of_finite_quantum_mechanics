# Review of PGW-RESPONDER-IN-LEAN

Scope: campaign derive/PGW-RESPONDER-IN-LEAN against origin/main 1fa451fe1eac640d84f0c34ba88a71dcdd32dfb6. Reviewed against the statements as they stand in this worktree. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: `scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH=0 MEDIUM=0 LOW=3). Read the node statement and bottleneck, the TFQ-0496 record, `lean4/CampaignPgwResponderInLean.lean`, the two source definitions in `Minimality.lean`, the replay receipt, and `checks/independent/pgw-responder-in-lean.py` (`checked 39 claims, failures 0`). Lake build completed before this review. Cargo was not run. The module does not import the Genesis development.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays OPEN. record_status stays OPEN_OBLIGATION. AuthorityEffect stays None.

Corrections to the PR's own text:

- None. The narrowed statement matches the declared shadow. The sealed responder, a uniform-rule regime, a separable same pair, and any identification of the length bound with a grammar stay unresolved.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-RESPONDER-IN-LEAN | `pgwRead_table` (`lean4/CampaignPgwResponderInLean.lean:56`), `pgwRead_count` (`:61`), `pgwMark_link_shape` (`:64`), `pgwMu1_tie` (`:70`), `pgwMu2_pairs` (`:73`), `pgwMu2_mark_before_link` (`:77`), `pgwBound_inside` (`:81`), `pgwRuled_outside` (`:85`), `pgwThree_outside` (`:89`) | NARROWED | Declared shadow only. Status stays OPEN. |

Atomic claims:

| Claim | Match |
|---|---|
| A demand is read only for collapsed with the uniform-rule flag false | `pgwRead_table` |
| Of the four flag pairs, the read count is 1 | `pgwRead_count` |
| Copied mark and link each have length 2, arities 1 and 2, argument lists [0] and [0, 1] | `pgwMark_link_shape` and the two definitions; the independent check reads `deltaU0` and `deltaBL` from `Minimality.lean` |
| mu1 is 2 for both, so the lists tie at cost 2 | `pgwMu1_tie` |
| mu2 is (2, 1) and (2, 2), and (2, 1) precedes (2, 2) | `pgwMu2_pairs`, `pgwMu2_mark_before_link` |
| Both lists lie inside the shadow bound | `pgwBound_inside` |
| A two-item rule list lies outside the bound | `pgwRuled_outside` |
| One three-item list has length 3 and lies outside the length bound 2 | `pgwThree_outside` |
| Sealed responder, S-1 regime refusal, S-2 same pair, S-4 grammar, G-4, H-1 | stated as open |

`#print axioms`: `pgwRead_table`, `pgwRead_count`, and `pgwMu1_tie` depend on no axioms. The other six theorems use propext. No `sorry`, `admit`, `axiom`, `native_decide`, or `unsafe` in the new module.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| Read table | true, false, false, false | four flag pairs | match |
| Read count | 1 | 1 + 0 + 0 + 0 | match |
| Lengths | 2 and 2 | explicit lists | match |
| Arities | 1 and 2 | form components | match |
| mu1 | 2 and 2 | list lengths | match |
| mu2 | (2, 1) and (2, 2) | length and arity sum | match |
| Order | 1 < 2 with equal item counts | component comparison | match |
| Rule list | length 2, outside | rule item present | match |
| Three-item list | length 3, outside bound 2 | a form plus two instance steps | match |
| Independent check | 39 claims, 0 failures | `python -I -X utf8 checks/independent/pgw-responder-in-lean.py` | match |
| Lake build | exit 0, wall 3.914s, module job 828ms | receipt | match |
| Validator | failures=3 | pre-existing unknown key `python` on three import nodes | left as on main |
| Evidence grades | E0 163, E1 222, E2 41, E3 499, E4 0 | 163+222+41+499+0 = 925, the builder's node count | match |
| OPEN grade row | 30, 74, 9, 62, 0 | 30+74+9+62+0 = 175 | match |
| Lean citations | 1865 cited, 1802 receipt-backed, 1734 itemised | each is 9 above the previous 1856, 1793, and 1725, one per new theorem | match |

The evidence grade of this node moves from E0 to E3 because the nine declarations sit in a receipt-backed file. The DAG status stays OPEN. The builder's older gap, 1793+40 against 1856, remains 1802+40 against 1865.

## Scanner output

HIGH 0, MEDIUM 0. LOW findings are outside this node and were left in place: R10 `TENSOR-ASSUMPTION-COUNTERMODELS`; R5 on `tfq_1019_fq_gap_tensor_uniqueness.md` (`20261019`); R5 on `tfq_0413_tensor_assumption_countermodels.md` (`1/2`, `1/4`). No baseline entry proposed. `sync_pregenesis_to_wdp.py --check` stays stale on `dag/derivation_dag.json`, the two views, and `tfq_0519_sn_protected_answer_transport.md`. Those paths were already stale against a full pregenesis render, and that render was not run. The TFQ-0496 paper was rewritten to the renderer for this record only.
