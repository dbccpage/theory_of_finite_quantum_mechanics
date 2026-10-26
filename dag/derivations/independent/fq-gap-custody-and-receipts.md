Status: AI-drafted, awaiting human review.

# FQ-GAP-CUSTODY-AND-RECEIPTS

AuthorityEffect: None.

The standing custody sentence names two untyped-row numerals, 48 and 24, and two file-coverage numerals, 22 and 53. This note records only the arithmetic of those four numerals. It does not recount a ledger, open a library directory, rebuild Mathlib, read an axiom report, follow a provenance pointer, query Zenodo, or run a README check.

## Numeral arithmetic

Work in the natural numbers, where subtraction is truncated at zero. Both subtractions below stay inside the ordinary range, so truncation does not apply.

The untyped-row pair:

```
48 - 24 = 24
```

The coverage pair:

```
53 - 22 = 31
22 < 53
```

The second line follows from the first of that pair, since a positive remainder means the smaller numeral is strictly below the larger one. Both lines are recorded separately so each clause of the standing sentence has its own witness.

## What is proved

- `48 - 24 = 24`
- `53 - 22 = 31`
- `22 < 53`

## What is assumed

Nothing beyond the natural-number arithmetic of the four numerals named in the prior custody sentence. Those numerals are inputs to the identities. This note does not assume that a ledger contains 48 rows or that a report names 22 files.

## What is open

A recount of the ledger rows behind the numeral 48; a check that the GAP-FQM-002 text says 24; a search for the QM_208-211 libraries; the eight Mathlib claims of GAP-FQM-019; the Classical.choice dependency named H019.basisGen8_eval_pos; the GAP-FQM-022 provenance pointers; the Zenodo status of QM_020 and QM_080; and the README code-companion check. A stale receipt over H000..H018 coexists with Lean headers that say Candidate only. The three Nat identities do not discharge that inventory. Status stays OPEN.
