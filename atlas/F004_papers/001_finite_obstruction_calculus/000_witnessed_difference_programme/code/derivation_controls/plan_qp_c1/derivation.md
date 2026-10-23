# PLAN-QP-C1

Goal id: PLAN-QP-C1

Selected scope for PLAN-QP-C1 is recorded in this note.

## Selected scope

3-slit Sorkin inclusion-exclusion sum I_3(A,B,C) = 0 on both additive degree-1 and quadratic degree-2 valuations, aligning finite_qm §5.2 with WDP CH19-N01.

## Hypotheses

H1. All calculations in this control are restricted to the declared finite integer and exact rational carriers (`carrier_val = 0`, `secondary_frac = 3/1`).

H2. The negative control `reject_i3_zero_implies_unique_born` refuses out-of-scope promotion, silent coercion, or unverified external theorem discharge.

## Derivation

On the declared finite carrier, the exact evaluation produces primary invariant `0` and rational ratio `3/1`, while the negative control `reject_i3_zero_implies_unique_born` rejects the prohibited promotion path.

## Claims this note does not make

- It does not discharge the unrestricted parent goal `PLAN-QP-C1` beyond the finite control carrier above.
- It does not certify continuum limits, external unreplayed theorems, or physical deployment.
