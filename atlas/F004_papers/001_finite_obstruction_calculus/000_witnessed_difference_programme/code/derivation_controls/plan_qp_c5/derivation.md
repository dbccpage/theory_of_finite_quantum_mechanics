# PLAN-QP-C5

Goal id: PLAN-QP-C5

Selected scope for PLAN-QP-C5 is recorded in this note.

## Selected scope

3-cycle cochain complex C^0 -> C^1 -> C^2 with explicit cycle-sum d_1 satisfying rank(d_0) = nullity(d_1) = 2.

## Hypotheses

H1. All calculations in this control are restricted to the declared finite integer and exact rational carriers (`carrier_val = 3`, `secondary_frac = 2/2`).

H2. The negative control `reject_undeclared_d1_or_phantom_artifacts` refuses out-of-scope promotion, silent coercion, or unverified external theorem discharge.

## Derivation

On the declared finite carrier, the exact evaluation produces primary invariant `3` and rational ratio `2/2`, while the negative control `reject_undeclared_d1_or_phantom_artifacts` rejects the prohibited promotion path.

## Claims this note does not make

- It does not discharge the unrestricted parent goal `PLAN-QP-C5` beyond the finite control carrier above.
- It does not certify continuum limits, external unreplayed theorems, or physical deployment.
