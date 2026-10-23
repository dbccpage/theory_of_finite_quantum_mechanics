# PLAN-QP-1

Goal id: PLAN-QP-1

Selected scope for PLAN-QP-1 is recorded in this note.

## Selected scope

Exhaustive 512-assignment Mermin-Peres parity check over F_2 and comparison of H^1 under d_1 = 0 versus the global parity-sum coboundary.

## Hypotheses

H1. All calculations in this control are restricted to the declared finite integer and exact rational carriers (`carrier_val = 512`, `secondary_frac = 1/1`).

H2. The negative control `reject_unconditional_h1_promotion_without_d1` refuses out-of-scope promotion, silent coercion, or unverified external theorem discharge.

## Derivation

On the declared finite carrier, the exact evaluation produces primary invariant `512` and rational ratio `1/1`, while the negative control `reject_unconditional_h1_promotion_without_d1` rejects the prohibited promotion path.

## Claims this note does not make

- It does not discharge the unrestricted parent goal `PLAN-QP-1` beyond the finite control carrier above.
- It does not certify continuum limits, external unreplayed theorems, or physical deployment.
