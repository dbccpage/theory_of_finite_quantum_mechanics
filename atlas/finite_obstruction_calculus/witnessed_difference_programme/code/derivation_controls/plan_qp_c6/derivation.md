# PLAN-QP-C6

Goal id: PLAN-QP-C6

Selected scope for PLAN-QP-C6 is recorded in this note.

## Selected scope

K_{2,3} primal-dual gap 9/2 < 6 and strict trace-distance contraction under CPTP dephasing.

## Hypotheses

H1. All calculations in this control are restricted to the declared finite integer and exact rational carriers (`carrier_val = 6`, `secondary_frac = 9/2`).

H2. The negative control `reject_inert_cptp_or_refuted_k23_dual` refuses out-of-scope promotion, silent coercion, or unverified external theorem discharge.

## Derivation

On the declared finite carrier, the exact evaluation produces primary invariant `6` and rational ratio `9/2`, while the negative control `reject_inert_cptp_or_refuted_k23_dual` rejects the prohibited promotion path.

## Claims this note does not make

- It does not discharge the unrestricted parent goal `PLAN-QP-C6` beyond the finite control carrier above.
- It does not certify continuum limits, external unreplayed theorems, or physical deployment.
