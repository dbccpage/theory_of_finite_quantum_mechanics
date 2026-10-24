# Review of PGW-WDP-BRIDGE-ONGOING-TO-WINDOW

Scope: pre-commit derivation on `derive/PGW-WDP-BRIDGE-ONGOING-TO-WINDOW`, base `1fa451fe1eac640d84f0c34ba88a71dcdd32dfb6`. Reviewed against the statement as it stands in `dag/derivation_dag.json`. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full original claim and compile with only propext, Classical.choice and Quot.sound.

Method: `scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH=0 MEDIUM=0 LOW=3) and `scripts/auto/anti_pattern_lint.py --changed-since origin/main` (0 findings). Read the node statement, bottleneck, obligation, and `lean4/CampaignPgwWdpBridgeOngoingToWindow.lean`, with the `#print axioms` lines in `dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json`. Re-ran `python -I -X utf8 checks/independent/pgw-wdp-bridge-ongoing-to-window.py`. The lake build was not rerun for this review; the receipt records exit 0, wall 6167 ms, and module job 1100 ms. Module sha256 `6942e82d06122f8ac06bce53e0eccc0562bef569ddfd1fa4c7c1d7a811e5ca1e` matches the file on disk.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays OPEN. Record status stays OPEN_OBLIGATION. AuthorityEffect stays None.

The original claim is the conditional bridge GEN-WDP-07, including a repair quotient, rational repair equality, and carrier-changing congruence. That bridge is not a Lean theorem. The current statement is the three-position integer check below. Route `PGW-R-WDP-BRIDGE-ONGOING-TO-WINDOW` is unchanged and stays `GAP_NO_DERIVATION`.

Corrections to the PR's own text:
- None. The statement names the three positions, the round sum, the shift invariance, the mark 3, the loop 4, and the two-way sum 8.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-WDP-BRIDGE-ONGOING-TO-WINDOW | `pgwBr_gradient_round`, `pgwBr_shift_preserves`, `pgwBr_unbalanced`, `pgwBr_loop_diag`, `pgwBr_loop_not_coboundary`, `pgwBr_loop_report`, `pgwBr_two_way` | NARROWED | Three positions, the round sum, the mark 3, the loop 4, and the two-way sum 8 match the declarations. A general marked family and the degree-1 window stay open. Status stays OPEN. |

Statement-vs-theorem, current statement only:

| Atomic claim | Declaration | Match |
|---|---|---|
| three positions labeled 0, 1, and 2 | `pgwBr_gradient_round` and `pgwBr_shift_preserves` (`CampaignPgwWdpBridgeOngoingToWindow.lean:9-17`) | integer slots `g0, g1, g2` and arcs `e01, e12, e20` |
| every integer triple has round sum 0 | `pgwBr_gradient_round` (`:9-11`) | `(g0 - g1) + (g1 - g2) + (g2 - g0) = 0` |
| adding those differences leaves e01 + e12 + e20 unchanged | `pgwBr_shift_preserves` (`:14-17`) | equality for every integer edge triple and every integer vertex triple |
| unbalanced mark 1 + 1 + 1 = 3, and it stays 3 after (2, 5, 11) | `pgwBr_unbalanced` (`:20-25`) | both equalities |
| for every integer g, the diagonal g - g is 0 | `pgwBr_loop_diag` (`:28-29`) | `g - g = 0` |
| the loop value 4 is not a diagonal coboundary | `pgwBr_loop_not_coboundary` (`:31-32`) | `g - g ≠ 4` for every integer g |
| oriented arcs 0, 0, 0 have diagnostic 0 | `pgwBr_loop_report` (`:35-37`) | `(0 : Int) + 0 + 0 = 0` and `4 ≠ 0` |
| forward arc 3 with the other oriented arcs 0 has diagnostic 3 | `pgwBr_two_way` (`:40-42`) | `(3 : Int) + 0 + 0 = 3` |
| two-way values 3 and 5 sum to 8 | `pgwBr_two_way` (`:40-42`) | `3 + 5 = 8` and `3 ≠ 8` |
| a repair quotient for a general marked family | none | open |
| a transport into the degree-1 window | none | open |
| rational repair equality | none | open |

Axiom lines recorded in the receipt, inside propext, Classical.choice, and Quot.sound. `pgwBr_gradient_round`, `pgwBr_shift_preserves`, `pgwBr_unbalanced`, `pgwBr_loop_diag`, and `pgwBr_loop_not_coboundary` list propext and Quot.sound. `pgwBr_loop_report` and `pgwBr_two_way` list propext, Classical.choice, and Quot.sound.

`normal_preserves_round_sums` remains a gauge-normalization fact for a whole table. It is not cited as this three-position transport.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| statement and note | round sum of (2, 5, 11) is 0 | `(2 - 5) + (5 - 11) + (11 - 2) = -3 + -6 + 9 = 0`; checker samples include this triple | match |
| statement and note | 1 + 1 + 1 = 3 | integer addition | match |
| statement and note | shift of (1, 1, 1) by (2, 5, 11) stays 3 | arcs become `1 + (2 - 5) = -2`, `1 + (5 - 11) = -5`, `1 + (11 - 2) = 10`; `-2 + -5 + 10 = 3`; checker prints `shifted (-2, -5, 10) diag 3` | match |
| statement and note | diagonal is 0 and 4 is not a diagonal | `g - g = 0` and `0 ≠ 4` | match |
| statement and note | oriented 0 + 0 + 0 = 0 | integer addition | match |
| statement and note | forward diagnostic 3 and two-way sum 8 | `3 + 0 + 0 = 3`, `3 + 5 = 8`, `3 ≠ 8` | match |
| receipt | wall 6167 ms, module job 1100 ms | lake timing already recorded; not an arithmetic identity | unrecomputed measurement |

Independent check on this review pass: `checked 70 claims, failures 0`.

## Scanner output

HIGH=0, MEDIUM=0, LOW=3. The three LOW rows are pre-existing and sit on nodes whose evidence pages changed only because receipt pins moved: R10 on TENSOR-ASSUMPTION-COUNTERMODELS (five cited Lean modules in no replay receipt, for example `lean4/TensorCountermodelCones.lean`), R5 on `tfq_1019_fq_gap_tensor_uniqueness.md` (number 20261019), and R5 on `tfq_0413_tensor_assumption_countermodels.md` (numbers 1/2 and 1/4). No baseline entry was added. Anti-pattern lint 0. The route diff does not contain a status change for `PGW-R-WDP-BRIDGE-ONGOING-TO-WINDOW`.

## What the scanner cannot decide

Whether the three-position cancellation is GEN-WDP-07 for a general marked family. It is not: the declarations quantify over integer triples and one ordered triple of arcs, and they do not construct the repair quotient or the degree-1 window.
