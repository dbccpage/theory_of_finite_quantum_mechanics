# PLAN-QP-8

Goal id: PLAN-QP-8

Selected scope for PLAN-QP-8 is recorded in this note.

## Selected scope

Unit-weight two-element Boolean meron orbit sum 0, zero-meron sector sum 2, and non-invariant observable doublet sum 1 != 0.

## Hypotheses

H1. All calculations in this control are restricted to the declared finite integer and exact rational carriers (`carrier_val = 2`, `secondary_frac = 1/1`).

H2. The negative control `reject_noninvariant_observable_orbit_cancellation` refuses out-of-scope promotion, silent coercion, or unverified external theorem discharge.

## Derivation

On the declared finite carrier, the exact evaluation produces primary invariant `2` and rational ratio `1/1`, while the negative control `reject_noninvariant_observable_orbit_cancellation` rejects the prohibited promotion path.

## Claims this note does not make

- It does not discharge the unrestricted parent goal `PLAN-QP-8` beyond the finite control carrier above.
- It does not certify continuum limits, external unreplayed theorems, or physical deployment.
