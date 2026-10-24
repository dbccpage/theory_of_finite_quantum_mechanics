Status: AI-drafted, awaiting human review.

# FQ-GAP-C500-ORIGINAL-TARGETS

AuthorityEffect: None.

Outcome: Narrowed. The node stays OPEN.

## What was counted

`sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml` has ten entries `GAP-C500-B01` through `GAP-C500-B10`, in that order. Each title is `C500 Block NN original target contract remains open`, with `NN` the two-digit index. Each `status` field is `RESOLVED_WITH_SCOPED_EVIDENCE` and each `resolution` field is `RESOLVED`.

Each entry lists 25 targets. Together the targets are `C500-T301` through `C500-T550`, which is 250 targets.

The `open_or_invalid_bet_clauses` lists are:

| Block | Clauses |
| --- | --- |
| B01 | (empty) |
| B02 | M2, M5 |
| B03 | M1, M3, M5, J2 |
| B04 | M3, M5 |
| B05 | M2, M5, M6, J2 |
| B06 | M5 |
| B07 | M6 |
| B08 | M6 |
| B09 | M6 |
| B10 | M2, M5, M7, J1, J2 |

The lengths are 0, 2, 4, 2, 4, 1, 1, 1, 1, and 5. Their sum is 21.

## One integer polynomial from the Block 09 description

The Block 09 description contains the text `x^4-6*x^2+5` and the text `{-sqrt(5),-1,1,sqrt(5)}`. For the integer polynomial `n^4 - 6*n^2 + 5`, the value at `1` is `0` and the value at `-1` is `0`. The substitution `5*5 - 6*5 + 5` is `0`. The coefficient product `(x^2 - 5)(x^2 - 1)` is `x^4 - 6*x^2 + 5`.

## What is proved

The Lean list has length 10, its clause lengths sum to 21, index 0 is the empty B01 list, and index 9 is B10 with clauses M2, M5, M7, J1, J2. Lean also records `25 * 10 = 250`, `301 + 250 - 1 = 550`, and the three integer evaluations of the polynomial. The independent check reads the gap register and matches the ten titles, statuses, resolutions, target lists, and clause lists, and it checks the coefficient identity.

## What is assumed

The clause lists and the polynomial numerals are a transcription of that gap register. Lean does not open the file. No added Lean import is used. A title that says the original contract remains open is a different sentence from a status field `RESOLVED_WITH_SCOPED_EVIDENCE`.

## What is open

Whether any original C500 target contract is discharged, the evidence files named by those entries, and any reading of the spectrum text as a real-number theorem. A clause list is not a derivation that a bet is invalid, and a receipt is not a derivation. The node status stays OPEN.
