# PLAN-QP-C7

Goal id: PLAN-QP-C7

Selected scope for PLAN-QP-C7 is recorded in this note.

## Selected scope

Source wording and 3-point Neville proxy check confirming absence of uncertified 'rigorously bounds' claims in 007_finite_to_continuum/README.md.

## Hypotheses

H1. All calculations in this control are restricted to the declared finite integer and exact rational carriers (`carrier_val = 3`, `secondary_frac = 13/12`).

H2. The negative control `reject_rigorous_bound_claim_for_neville_proxy` refuses out-of-scope promotion, silent coercion, or unverified external theorem discharge.

## Derivation

On the declared finite carrier, the exact evaluation produces primary invariant `3` and rational ratio `13/12`, while the negative control `reject_rigorous_bound_claim_for_neville_proxy` rejects the prohibited promotion path.

## Claims this note does not make

- It does not discharge the unrestricted parent goal `PLAN-QP-C7` beyond the finite control carrier above.
- It does not certify continuum limits, external unreplayed theorems, or physical deployment.
