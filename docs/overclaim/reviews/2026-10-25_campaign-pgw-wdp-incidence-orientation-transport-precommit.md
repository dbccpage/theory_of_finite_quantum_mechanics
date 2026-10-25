# Review of campaign-pgw-wdp-incidence-orientation-transport

Scope: pre-commit review of PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT on derive/PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT, base origin/main 7fa69d621c27. Reviewed against the statement in dag/derivation_dag.json. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full statement and compile with only propext, Classical.choice and Quot.sound.

Method: read lean4/CampaignPgwWdpIncidenceTransport.lean in full, the node statement and bottleneck, the independent note, and the replay receipt. The module was built earlier this fire with `lake build CampaignPgwWdpIncidenceTransport` (Lean 4.35.0, exit 0). This review did not rebuild Lean or cargo. `#print axioms` lines are the receipt output. Independent check rerun with `python -I -X utf8 checks/independent/pgw-wdp-incidence-orientation-transport.py`. Scanner: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH 0, MEDIUM 0, LOW 3).

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays OPEN.

Corrections to the PR's own text:
- None. The standing statement is the one-triangle case. The original window transport, the Genesis-admission derivation, and the external orientation test are written as open.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT | `face_reorders`, `incidence_face_boundary_zero`, `transport_matches_transpose`, `wdp_d1_d0`, `reverse_edge_20`, `defect_charge`, `residual_at_repair`, `residual_at_least_two` | NARROWED | Each standing arithmetic claim is the type of one declaration in lean4/CampaignPgwWdpIncidenceTransport.lean. The original obligation (every window quantity, Genesis admission, the external orientation test) is not that type. Status stays OPEN. |

### Statement versus theorem

| Claim | Declaration | Where | Verdict |
|---|---|---|---|
| (a, b, c) reorders to (a, c, b), and (1, -1, 1) becomes (1, 1, -1) | `reorderToWdp`, `face_reorders` | CampaignPgwWdpIncidenceTransport.lean:63, 105-107 | matched |
| incidence boundary of (1, -1, 1) is (0, 0, 0) | `incidence_face_boundary_zero` | CampaignPgwWdpIncidenceTransport.lean:109-111 | matched |
| dots with columns 01, 12, 02 equal (f1 - f0, f2 - f1, f2 - f0) for every integer vertex triple | `transport_matches_transpose` | CampaignPgwWdpIncidenceTransport.lean:85-103 | matched |
| x01 + x12 - x02 vanishes on every such coboundary | `wdp_d1_d0` | CampaignPgwWdpIncidenceTransport.lean:113-116 | matched |
| cyclic sum with edge 20 stored as -x02 equals that evaluation | `reverse_edge_20` | CampaignPgwWdpIncidenceTransport.lean:118-121 | matched |
| the evaluation sends (1, 1, 0) to 2 | `defect_charge` | CampaignPgwWdpIncidenceTransport.lean:123-124 | matched |
| residual equals 2 at vertex values (0, 1, 0) | `residual_at_repair` | CampaignPgwWdpIncidenceTransport.lean:133-135 | matched |
| residual is at least 2 for every integer vertex triple | `residual_at_least_two` | CampaignPgwWdpIncidenceTransport.lean:137-147 | matched |
| a transport for every window quantity | not proved | statement and bottleneck keep it open | not proved |
| a derivation of the WDP window from Genesis admission | not proved | statement and bottleneck keep it open | not proved |
| the external orientation test | not proved | statement and bottleneck keep it open | not proved |

`boundary_boundary_filled` and `triD1` stay listed as prior witnesses. This module does not import them, and they do not discharge the new claims.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| columns | (-1, 1, 0), (-1, 0, 1), (0, -1, 1) | inc_boundary(1,0,0), (0,1,0), (0,0,1) by integer arithmetic | match |
| face boundary | (0, 0, 0) | (-1-(-1), 1-1, -1+1) | match |
| reordered face | (1, 1, -1) | (a, c, b) on (1, -1, 1) | match |
| defect | 2 | 1 + 1 - 0 | match |
| residual at (0, 1, 0) | 2 | abs(1-(1-0)) + abs(1-(0-1)) + abs(0-(0-0)) = 0+2+0 | match |
| pairing | 2 | (1-(f1-f0))+(1-(f2-f1))-(0-(f2-f0)) cancels to 2 | match |
| independent check | 3654 conditions, 0 failures | 8 fixed checks + 9^3 triples times 5 checks + 1 residual check = 8+3645+1; script printed the same line | match |

The Python loop covers vertex coordinates in -4..4. The universal residual bound is the Lean declaration `residual_at_least_two`, whose bound is the integer triangle inequality for `iabs`, not that loop.

## Scanner output

HIGH 0, MEDIUM 0. `--strict` exited 0. LOW findings, left unchanged because they are outside this node: R10 on TENSOR-ASSUMPTION-COUNTERMODELS; R5 date token 20261019 on the FQ-GAP-TENSOR-UNIQUENESS note; R5 tokens 1/2 and 1/4 on the TENSOR-ASSUMPTION-COUNTERMODELS note. No baseline entry added. No status rose, so R9 does not apply.

## Axioms

Receipt `dag/research/campaign_pgw-wdp-incidence-orientation-transport_lean_replay.json`: `column_01`, `column_02`, `column_12`, `face_reorders`, `incidence_face_boundary_zero`, `defect_charge`, and `residual_at_repair` depend on no axioms. `transport_matches_transpose`, `wdp_d1_d0`, `reverse_edge_20`, `pairing_is_two`, and `residual_at_least_two` depend on propext and Quot.sound. Allowed set is propext, Classical.choice, and Quot.sound. Source sha256 d1671fb7df23ee9b65b0032c9bab2f4875067f141e045a8da64e107ffea5fbcf matches the file after CRLF folding. The module text contains no sorry, no axiom declaration, no native_decide, and no unsafe.

## What the scanner could not decide

Whether "unit-weight residual" names the same functional as `residual` is a reading of the definition at CampaignPgwWdpIncidenceTransport.lean:126-127, which is the sum of absolute deviations of (f1-f0, f2-f1, f2-f0) from (1, 1, 0). The monograph sentence that every window quantity is invariant under reorientation is a cited source, not a theorem of this module.
