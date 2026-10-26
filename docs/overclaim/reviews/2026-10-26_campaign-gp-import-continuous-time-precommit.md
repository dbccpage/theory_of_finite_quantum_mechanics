# Overclaim review: GP-IMPORT-CONTINUOUS-TIME

**AuthorityEffect:** None.

## Scope

Branch `derive/GP-IMPORT-CONTINUOUS-TIME` against `origin/main` at `4fea09ae176aae31115e38bb2b21819237055811`. One node, `GP-IMPORT-CONTINUOUS-TIME`. Status stays `IMPORTED_ASSUMPTION`.

## Method

`python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` reported HIGH=0, MEDIUM=0, LOW=3. The module was built with `lake build CampaignGpImportContinuousTime` (Lean 4.35.0, exit 0). Axioms were read from that build. Numbers were recomputed by `python -I -X utf8 checks/independent/gp-import-continuous-time.py`.

## Result

0 FULL, 1 NARROWED, 0 OVERCLAIM.

The narrowed statement is matched by the cited declarations. Continuous time, a topology, a one-parameter unitary group and Stone's theorem are not in that statement. They stay in the bottleneck, and the status is not raised.

## Corrections to the PR's own text

None in the statement. The generated audit row still quotes the 2026-10-19 review's narrowest claim. That cell is the old review digest, not the narrowed node statement.

## Per-node table

| Claim | Declaration | Verdict |
|---|---|---|
| toggle sends false to true and true to false | `toggle_images` | matched |
| no map on the two labels squares to toggle | `no_toggle_square_root` | matched |
| pair sum (a, b) + (c, d) = (a + c, b + d) | `gAdd_coords` | matched |
| pair product (a, b) * (c, d) = (a*c - b*d, a*d + b*c) | `gMul_coords` | matched |
| swap exchanges the two coordinates | `swap_exchanges` | matched |
| applying the interpolant twice returns the swap of the pair scaled by (4, 0) on each coordinate | `interp_twice_is_scaled_swap`, `scale4_swap` | matched |
| the coordinatewise negation has that same square | `interpNeg_twice_is_scaled_swap` | matched |
| at ((1, 0), (0, 0)) the interpolant returns ((1, 1), (1, -1)) | `witness_interp` | matched |
| the negation returns ((-1, -1), (-1, 1)) | `witness_neg` | matched |
| those two results differ | `interpolants_differ` | matched |
| continuous time, topology, a one-parameter unitary group, Stone's theorem | not in the statement | open, bottleneck |

Axioms: `interp_twice_is_scaled_swap` and `interpNeg_twice_is_scaled_swap` use `propext` and `Quot.sound`. The other cited declarations use none. `Classical.choice` does not appear.

## Numbers recomputed

| Number | Recomputation | Match |
|---|---|---|
| 4 | 2 × 2 maps on two labels; checker `maps=4` | match |
| 4 in (4, 0) | scale factor; `4 * 1 = 4` and `4 * 0 = 0` | match |
| 1, 0, -1 | witness coordinates in `witness_interp` and `witness_neg` | match |

Checker output: `checks=14 failures=0 maps=4 witness=(((1, 1), (1, -1)), ((-1, -1), (-1, 1))) scale=4`.

## What the scanner could not decide

The three LOW rows are outside this node. They sit on tensor notes whose receipt pin was rebound with the DAG hash. They are not claims of `GP-IMPORT-CONTINUOUS-TIME`.
