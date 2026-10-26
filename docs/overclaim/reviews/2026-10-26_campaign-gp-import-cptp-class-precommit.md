# Overclaim review: GP-IMPORT-CPTP-CLASS

**AuthorityEffect:** None.

## Scope

Branch `derive/GP-IMPORT-CPTP-CLASS` against `origin/main` at `4fea09ae176aae31115e38bb2b21819237055811`. One node, `GP-IMPORT-CPTP-CLASS`. Status stays `IMPORTED_ASSUMPTION`.

## Method

`python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` reported HIGH=0, MEDIUM=0, LOW=3. The Lean module was built with `lake build CampaignGpImportCptpClass` (Lean 4.35.0, exit 0). Axioms were read from that build. Numbers were recomputed by `python -I -X utf8 checks/independent/gp-import-cptp-class.py`.

## Result

0 FULL, 1 NARROWED, 0 OVERCLAIM.

The narrowed statement is matched by the cited declarations. The Hilbert-space channel class is not in that statement. It stays in the bottleneck, and the status is not raised.

## Corrections to the PR's own text

None in the statement. The generated audit row still quotes the 2026-10-19 review's narrowest claim. That cell is the old review digest, not the narrowed node statement.

## Per-node table

| Claim | Declaration | Verdict |
|---|---|---|
| collapse sends false to false and true to false | `collapse_both_false` | matched |
| those two labels have the same image | `collapse_labels_agree` | matched |
| no map inv is a two-sided inverse of collapse | `collapse_no_two_sided_inverse` | matched |
| mass image coordinates are wF + wT and 0 | `collapseMass_coords` | matched |
| those coordinates sum to wF + wT | `collapseMass_preserves_sum` | matched |
| nonnegative weights give nonnegative image coordinates | `collapseMass_nonneg` | matched |
| weights 2 and 3 have mass image (5, 0) | `collapseMass_two_three` | matched |
| the ancilla label is prepared at false | `prepared_is_false` | matched |
| the four swap-pair maps are pairwise distinct | `four_maps_pairwise_unequal` | matched |
| each of those four maps is the forward map of a reversible dilation | `four_named_are_dilations` | matched |
| every reversible dilation agrees with one of those four maps at every label pair | `every_dilation_agrees` | matched |
| Hilbert-space completely positive trace-preserving class | not in the statement | open, bottleneck |

Axioms: `collapseMass_nonneg` uses `propext`. `every_dilation_agrees` uses `propext`. The other cited declarations use none. `Classical.choice` does not appear.

## Numbers recomputed

| Number | Recomputation | Match |
|---|---|---|
| 2 and 3 | weights in `collapseMass_two_three` | match |
| 5 | 2 + 3 = 5 | match |
| 0 | second mass coordinate and both collapse images | match |
| four | 2 × 2 swap pairs; the checker found 4 dilations among 256 maps on 4 points | match |

Checker output: `checks=37 failures=0 maps=256 dilations=4 named=4 mass=(5, 0) collapse=(0, 0)`.

## What the scanner could not decide

Three LOW rows are outside this node. R10 on `TENSOR-ASSUMPTION-COUNTERMODELS` and two R5 rows on tensor notes were already about those notes. They are not claims of `GP-IMPORT-CPTP-CLASS`.
