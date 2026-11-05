# PLAN-QP-C3

Goal id: PLAN-QP-C3

Selected scope for PLAN-QP-C3 is recorded in this note.

## Selected scope

GAP-FQM-006 erratum verification refusing promotion of historical placeholder Zenodo IDs to published releases.

## Hypotheses

H1. All calculations in this control are restricted to the declared finite integer and exact rational carriers (`carrier_val = 6`, `secondary_frac = 0/1`).

H2. The negative control `reject_unpublished_zenodo_placeholder` refuses out-of-scope promotion, silent coercion, or unverified external theorem discharge.

## Derivation

On the declared finite carrier, the exact evaluation produces primary invariant `6` and rational ratio `0/1`, while the negative control `reject_unpublished_zenodo_placeholder` rejects the prohibited promotion path.

## Claims this note does not make

- It does not discharge the unrestricted parent goal `PLAN-QP-C3` beyond the finite control carrier above.
- It does not certify continuum limits, external unreplayed theorems, or physical deployment.
