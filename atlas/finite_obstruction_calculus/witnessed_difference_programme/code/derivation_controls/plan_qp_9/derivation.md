# PLAN-QP-9

Goal id: PLAN-QP-9

Selected scope for PLAN-QP-9 is recorded in this note.

## Selected scope

Exact rational Neville table on L in {4, 8, 16} with P_{012}(0) = 13/12 != 1, confirming three-size Neville extrapolation is an uncertified proxy.

## Hypotheses

H1. All calculations in this control are restricted to the declared finite integer and exact rational carriers (`carrier_val = 13`, `secondary_frac = 13/12`).

H2. The negative control `reject_uncertified_neville_continuum_bound` refuses out-of-scope promotion, silent coercion, or unverified external theorem discharge.

## Derivation

On the declared finite carrier, the exact evaluation produces primary invariant `13` and rational ratio `13/12`, while the negative control `reject_uncertified_neville_continuum_bound` rejects the prohibited promotion path.

## Claims this note does not make

- It does not discharge the unrestricted parent goal `PLAN-QP-9` beyond the finite control carrier above.
- It does not certify continuum limits, external unreplayed theorems, or physical deployment.
