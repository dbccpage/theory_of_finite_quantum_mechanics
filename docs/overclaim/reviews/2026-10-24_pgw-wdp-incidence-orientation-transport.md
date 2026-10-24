# Review of PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT

Scope: pre-commit derivation on `derive/PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT`, base `1fa451fe1eac640d84f0c34ba88a71dcdd32dfb6`. Reviewed against the statement as it stands in `dag/derivation_dag.json`. Rule applied: PROVED_LEAN only if Lean declarations in the repository state the node's full original claim and compile with only propext, Classical.choice and Quot.sound.

Method: `scripts/overclaim_scan.py --changed-since origin/main --strict` (HIGH=0 MEDIUM=0 LOW=3) and `scripts/auto/anti_pattern_lint.py --changed-since origin/main` (0 findings). Read the node statement, bottleneck, obligation, `lean4/CampaignPgwWdpIncidenceOrientationTransport.lean`, the `#print axioms` lines in `dag/research/campaign_pgw-wdp-incidence-orientation-transport_lean_replay.json`, `d2` in `lean4/Imported/OeWdp/GenesisIncidence.lean`, and `triD0` / `triD1` / `triD1Row` in `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`. Re-ran `python -I -X utf8 checks/independent/pgw-wdp-incidence-orientation-transport.py`. The lake build was not rerun for this review; the receipt records exit 0 and wall 6458 ms. Module sha256 `11af3b7cdcea7ff3ab3e9ad6b506163824fe4a4c590b0a0babb03e7725fed794` matches the file on disk.

Result: 0 nodes FULL, 1 NARROWED, 0 OVERCLAIM. No node was raised. Status stays OPEN. Record status stays OPEN_OBLIGATION. AuthorityEffect stays None.

The original obligation was a transport between the Genesis incidence edge order and the WDP window. That general transport is not a Lean theorem. The current statement is the one-triangle coordinate check below. Route `PGW-R-WDP-INCIDENCE-ORIENTATION-TRANSPORT` is unchanged and stays `GAP_NO_DERIVATION`.

Corrections to the PR's own text:
- None. The statement names the one triangle, the slot swap, the face row, the 02 sign change, the three boundary components, `triD1` of `triD0`, and the value 3. It does not say that a general window transport is done.

## Per-node table

| Node | Declarations that discharge it | Verdict | Reason |
|---|---|---|---|
| PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT | `pgwInc_swap_involutive`, `pgwInc_face_swapped`, `pgwInc_face_is_row`, `pgwInc_face_cyclic`, `pgwInc_transported_cycle`, `pgwInc_face_tri`, `pgwInc_d1_d0` | NARROWED | One triangle's slot swap, face row, 02 sign, boundary components, row value 3, and `triD1` of `triD0` match the declarations. A general window transport stays open. Status stays OPEN. |

Statement-vs-theorem, current statement only:

| Atomic claim | Declaration | Match |
|---|---|---|
| one triangle, vertices 0, 1, 2 | `d2` is the admitted 2-simplex 012 (`GenesisIncidence.lean:45-47`); `triD0` uses `(f0, f1, f2)` (`Obstruction.lean:303-307`); the campaign theorems are stated on `d2 1` and on every `(f0, f1, f2)` | the worked triangle, not a new complex |
| swapping slots (01, 02, 12) to (01, 12, 02) is an involution | `pgwInc_swap23` is `(a, c, b)` (`CampaignPgwWdpIncidenceOrientationTransport.lean:14-15`); `pgwInc_swap_involutive` (`:17-20`) | two swaps return `(a, b, c)` for every integer triple |
| admitted face column (1, -1, 1) becomes (1, 1, -1) | `pgwInc_face_swapped` (`:22-24`) | `pgwInc_swap23 (d2 1).x (d2 1).y (d2 1).z = (1, 1, -1)` |
| that triple matches triD1Row | `pgwInc_face_is_row` (`:30-35`) and `pgwInc_row` (`:26-28`) | `((d2 1).x, (d2 1).z, (d2 1).y) = (triD1Row .e01, triD1Row .e12, triD1Row .e02) = (1, 1, -1)` |
| negating the 02 component sends (1, 1, -1) to (1, 1, 1) | `pgwInc_face_cyclic` (`:40-44`) | `pgwInc_reverse02` of the swapped face is `(1, 1, 1)` |
| swapped column has vertex boundary 0 at each vertex | `pgwInc_transported_cycle` (`:46-49`) | `-a01 - a02 = 0`, `a01 - a12 = 0`, `a12 + a02 = 0` on the swapped face |
| triD1 of triD0 is 0 for every rational vertex triple | `pgwInc_d1_d0` (`:92-96`) | `triD1 (triD0 (f0, f1, f2)) = 0` for every `f0 f1 f2 : Rat` |
| triD1 of the swapped face row is 3 | `pgwInc_face_tri` (`:65-75`) | the `triD1` of the swapped `d2 1` coordinates equals 3 |
| a transport of every window quantity | none | open |
| d0 and d1 of the whole WDP window are the transposes of the Genesis boundary maps | none | open |
| monograph invariance under reorientation | none | open |

Axiom lines recorded in the receipt, inside propext, Classical.choice, and Quot.sound. `pgwInc_swap_involutive` has an empty axiom list. `pgwInc_face_swapped`, `pgwInc_face_cyclic`, and `pgwInc_transported_cycle` list propext. `pgwInc_row`, `pgwInc_face_is_row`, `pgwInc_dot_matches_order`, and `pgwInc_int_d1_d0` list propext and Quot.sound. `pgwInc_swapped_coord_is_tri`, `pgwInc_face_tri`, `pgwInc_rat_telescope`, and `pgwInc_d1_d0` list propext, Classical.choice, and Quot.sound.

The value 3 is `triD1` of the row `(1, 1, -1)`. It is not the vertex boundary, which is `(0, 0, 0)`. `boundary_boundary_filled` stays a chain-level fact in the incidence edge order and is not cited as this transport.

## Numbers recomputed

| Where | Claimed | Recomputed (method) | Match |
|---|---|---|---|
| statement and note | swap of (1, -1, 1) is (1, 1, -1) | checker prints `swapped (1, 1, -1)`; swap `(a, b, c) -> (a, c, b)` on `(1, -1, 1)` | match |
| statement and note | second swap returns (1, -1, 1) | `(1, -1, 1) -> (1, 1, -1) -> (1, -1, 1)` | match |
| statement and note | 02 sign change yields (1, 1, 1) | checker prints `cyclic (1, 1, 1)`; negate the last component of `(1, 1, -1)` | match |
| statement and note | vertex components 0, 0, 0 | `-1 - (-1) = 0`, `1 - 1 = 0`, `1 + (-1) = 0`; checker prints `boundary (0, 0, 0)` | match |
| statement and note | triD1 of the swapped row is 3 | `1 + 1 - (-1) = 3`; checker prints `row_tri 3` | match |
| statement | triD1 of triD0 is 0 on every rational triple | `(f1 - f0) + (f2 - f1) - (f2 - f0) = 0` by cancellation; `pgwInc_d1_d0` | match |
| receipt | wall 6458 ms | lake timing already recorded; not an arithmetic identity | unrecomputed measurement |
| independent check | 49 claims, 0 failures | re-ran the checker on this review pass | match |

Independent check on this review pass: `checked 49 claims, failures 0`.

## Scanner output

HIGH=0, MEDIUM=0, LOW=3. The three LOW rows are pre-existing and sit on nodes whose evidence pages changed only because receipt pins moved: R10 on TENSOR-ASSUMPTION-COUNTERMODELS (five cited Lean modules in no replay receipt, for example `lean4/TensorCountermodelCones.lean`), R5 on `tfq_1019_fq_gap_tensor_uniqueness.md` (number 20261019), and R5 on `tfq_0413_tensor_assumption_countermodels.md` (numbers 1/2 and 1/4). No baseline entry was added. Anti-pattern lint 0. The route diff does not contain a status change for `PGW-R-WDP-INCIDENCE-ORIENTATION-TRANSPORT`.

## What the scanner cannot decide

Whether the three boundary equations are a transport of every window quantity. They are not: they are the three integer equations on the swapped face column of `d2 1`, and `pgwInc_d1_d0` is the cancellation `triD1 (triD0 (f0, f1, f2)) = 0` on one rational triple of vertex values.
