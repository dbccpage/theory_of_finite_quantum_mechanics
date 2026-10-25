# Overclaim review: TFQ-0003 pre-commit

AuthorityEffect: None.

## Scope

`derive/TFQ-0003` against `origin/main`. Node status stays OPEN. The statement was narrowed to the 3-cycle signature proved in `lean4/CampaignTfq0003FiniteObstruction.lean`.

## Method

`lake --dir lean4 build CampaignTfq0003FiniteObstruction` (Lean 4.35.0). `#print axioms` on the cited theorems. Independent script `checks/independent/tfq-0003.py` with integer arithmetic only. Scanner: `python -I -X utf8 scripts/overclaim_scan.py --changed-since origin/main --strict` from this worktree. Result: scope=changes since origin/main (merge base 1fa451fe1eac); HIGH=0 MEDIUM=0 LOW=3; exit 0.

## Result

1 NARROWED, 0 FULL, 0 OVERCLAIM. Status was not raised.

## Per-node table

| Claim | Declaration | Verdict |
| --- | --- | --- |
| hol(c - d0 h) = hol(c) for every integer 3-cycle cochain | `hol_gauge` | FULL |
| c is a coboundary iff hol c = 0 | `coboundary_iff_hol_zero` | FULL |
| same coboundary coset iff equal holonomy | `sameClass_iff_hol` | FULL |
| Phi1 = abs(hol) lower-bounds unweighted L1 on the class | `phi1_lower_bound` | FULL |
| (hol, 0, 0) attains Phi1 | `phi1_attained_edge0` | FULL |
| (0, hol, 0) attains Phi1 | `phi1_attained_edge1` | FULL |
| those residuals differ when hol is not 0 | `minimizers_differ` | FULL |
| Gamma2 means the holonomy and is gauge-invariant | `gamma2_gauge` | FULL |
| sample (1, -2, 4) has hol 3, Phi1 3, L1 7 | `sample_signature` | FULL |
| Python, Rust, and Lean state the same witness | not proved | NOT PROVED |
| F000 volume is not a completed Genesis pass | not proved | NOT PROVED |
| Weighted masses, other complexes, other Gamma2 | not proved | NOT PROVED |

The node status stays OPEN because the original three-language obligation is not the proved statement. The proved sentences are the whole new statement. The unproved sentences are only in the bottleneck.

## Numbers recomputed

| Number | Recomputation | Match |
| --- | --- | --- |
| 3 | `1 + (-2) + 4` | match |
| 3 | absolute value of that sum | match |
| 7 | `abs(1) + abs(-2) + abs(4)` | match |
| 238736 | count of integer checks in `checks/independent/tfq-0003.py`, 0 failures | match |

## Axioms

Cited theorems use only `propext` and `Quot.sound`, or no axioms. No `sorry`, `admit`, `axiom`, or `native_decide`.

## What the scanner could not decide

Whether the shelf book says the volume is not a completed pass. That sentence was removed from the statement and left in the bottleneck as not a theorem of this note.
