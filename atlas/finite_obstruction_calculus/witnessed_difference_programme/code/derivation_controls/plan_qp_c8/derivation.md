# PLAN-QP-C8

Goal id: PLAN-QP-C8

Selected scope for PLAN-QP-C8 is recorded in this note.

## Selected scope

5-record MUB6 gap registry alignment check (G1, G2, G4, G5, R6) retaining R6 = NOT_A_CERTIFICATE.

## Hypotheses

H1. All calculations in this control are restricted to the declared finite integer and exact rational carriers (`carrier_val = 5`, `secondary_frac = 9/1`).

H2. The negative control `reject_mub6_subgap_global_promotion` refuses out-of-scope promotion, silent coercion, or unverified external theorem discharge.

## Derivation

On the declared finite carrier, the exact evaluation produces primary invariant `5` and rational ratio `9/1`, while the negative control `reject_mub6_subgap_global_promotion` rejects the prohibited promotion path.

## Claims this note does not make

- It does not discharge the unrestricted parent goal `PLAN-QP-C8` beyond the finite control carrier above.
- It does not certify continuum limits, external unreplayed theorems, or physical deployment.
