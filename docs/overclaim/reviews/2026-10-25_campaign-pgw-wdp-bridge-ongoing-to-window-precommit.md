# Review of campaign-pgw-wdp-bridge-ongoing-to-window

Scope: pre-commit review of PGW-WDP-BRIDGE-ONGOING-TO-WINDOW on derive/PGW-WDP-BRIDGE-ONGOING-TO-WINDOW, base origin/main 7fa69d621c27. Reviewed against the statement in dag/derivation_dag.json. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read lean4/CampaignPgwWdpBridgeOngoing.lean in full, the node statement and bottleneck, the independent note, and the replay receipt. The module was built with `lake build CampaignPgwWdpBridgeOngoing` (Lean 4.35.0, exit 0, module job 786 ms). This review did not rebuild Lean or cargo. `#print axioms` lines are the receipt output. Independent check rerun with `python -I -X utf8 checks/independent/pgw-wdp-bridge-ongoing-to-window.py`. Scanner: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3).

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays OPEN.

Corrections to the PR's own text:
- None. The standing statement is the carrier {0, 1}. A general carrier, an arbitrary marked family, the degree-1 window, a continuous norm, and carrier-changing term operations stay open.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-WDP-BRIDGE-ONGOING-TO-WINDOW | `cob_slots`, `diag_on_coboundary`, `diag_after_repair`, `denominator_clears`, `compensated_loop_closed`, `compensated_loop_not_coboundary`, `silent_loop_closed`, `silent_loop_not_coboundary`, `one_arc_diagnostic`, `two_way_sum`, `two_way_difference` | NARROWED | Each standing arithmetic claim is the type of one declaration in lean4/CampaignPgwWdpBridgeOngoing.lean. The original GEN-WDP-07 register, for an arbitrary carrier and marked family, is not that type. Status stays OPEN. |

### Statement versus theorem

| Claim | Declaration | Where | Verdict |
|---|---|---|---|
| coboundary of (g0, g1) is (0, 0, g0 - g1, g1 - g0) | `cob_slots` | CampaignPgwWdpBridgeOngoing.lean:16-22 | matched |
| diagnostic of the mark (0, 1, 0) is 0 on every coboundary | `diag_on_coboundary` | CampaignPgwWdpBridgeOngoing.lean:24-27 | matched |
| adding a coboundary leaves the diagnostic unchanged | `diag_after_repair` | CampaignPgwWdpBridgeOngoing.lean:29-32 | matched |
| a nonzero integer scale onto a coboundary is already the integer coboundary of (0, -d01) | `denominator_clears` | CampaignPgwWdpBridgeOngoing.lean:34-59 | matched |
| table (1, 0, 0, -1) has diagnostic 0 and is not a coboundary | `compensated_loop_closed`, `compensated_loop_not_coboundary` | CampaignPgwWdpBridgeOngoing.lean:61-67 | matched |
| table (0, 1, 0, 0) has diagnostic 0 and is not a coboundary | `silent_loop_closed`, `silent_loop_not_coboundary` | CampaignPgwWdpBridgeOngoing.lean:69-75 | matched |
| one-arc table (0, 0, 1, 0) has diagnostic 1 | `one_arc_diagnostic` | CampaignPgwWdpBridgeOngoing.lean:78-79 | matched |
| two-way table (0, 0, 1, 1) has arc sum 2 and arc difference 0 | `two_way_sum`, `two_way_difference` | CampaignPgwWdpBridgeOngoing.lean:81-84 | matched |
| a general carrier and an arbitrary marked family | not proved | statement keeps them open | not proved |
| the degree-1 window of TFQ-0004 | not proved | statement keeps it open | not proved |
| a continuous norm | not proved | statement keeps it open | not proved |
| carrier-changing term operations | not proved | statement keeps them open | not proved |

`normal_preserves_round_sums` stays listed as a prior witness. This module does not import it, and it does not discharge the new claims.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| coboundary slots | (0, 0, g0 - g1, g1 - g0) | the four coordinates of `cob` | match |
| diagnostic on a coboundary | 0 | (g0 - g1) + (g1 - g0) + 0 | match |
| compensated loop | diagnostic 0 | 0 + (-1) + 1 | match |
| silent loop | diagnostic 0 | 0 + 0 + 0, and the unread loop is 1 | match |
| one arc | 1 | 1 + 0 + 0 | match |
| two-way arcs | sum 2, difference 0 | 1 + 1 and 1 - 1 | match |
| independent check | 10456 conditions, 0 failures | 6 fixed checks + 9×9×(3+125) repair checks + 82 denominator hits = 6+10368+82; the script printed the same line | match |

The Python loops cover vertex values in -4..4, table slots in -2..2, and denominators in -3..3 excluding 0. `denominator_clears` is the statement for every integer b ≠ 0. The loop only counts the pairs inside that box whose hypotheses hold.

## Scanner output

HIGH 0, MEDIUM 0. `--strict` exited 0. LOW findings, left unchanged because they are outside this node: R10 on TENSOR-ASSUMPTION-COUNTERMODELS; R5 date token 20261019 on the FQ-GAP-TENSOR-UNIQUENESS note; R5 tokens 1/2 and 1/4 on the TENSOR-ASSUMPTION-COUNTERMODELS note. No baseline entry added. No status rose, so R9 does not apply.

## Axioms

Receipt `dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json`: `cob_slots`, `compensated_loop_closed`, `silent_loop_closed`, `one_arc_diagnostic`, `two_way_sum`, and `two_way_difference` depend on no axioms. `diag_on_coboundary`, `diag_after_repair`, `denominator_clears`, `compensated_loop_not_coboundary`, and `silent_loop_not_coboundary` depend on propext and Quot.sound. Allowed set is propext, Classical.choice, and Quot.sound. Source sha256 70b6d1d23be815c94d992e1b1c3c50617997cdf2f139ef7c41ef9c3d6e68281a matches the file after CRLF folding. The module text contains no sorry, no axiom declaration, no native_decide, and no unsafe.

## What the scanner could not decide

Whether "not a coboundary" is the conjunction of a closed diagnostic and a loop slot unequal to every coboundary loop is a reading of `compensated_loop_not_coboundary` and `silent_loop_not_coboundary`. The two quotient groups are not constructed; the statement records two closed tables outside the coboundary image and one table outside the kernel. The monograph sentences about an arbitrary carrier remain cited sources, not theorems of this module.
