# PLAN-QP-3

Goal id: PLAN-QP-3

Selected scope for PLAN-QP-3 is recorded in this note.

## Selected scope

Rationality of Hermitian Q(i) expectation values, 2-adic non-attainment of S^2 = 8 over Q, and DivisibleByEight predicate checks.

## Hypotheses

H1. All calculations in this control are restricted to the declared finite integer and exact rational carriers (`carrier_val = 8`, `secondary_frac = 196/25`).

H2. The negative control `reject_gaussian_rational_tsirelson_attainment` refuses out-of-scope promotion, silent coercion, or unverified external theorem discharge.

## Derivation

On the declared finite carrier, the exact evaluation produces primary invariant `8` and rational ratio `196/25`, while the negative control `reject_gaussian_rational_tsirelson_attainment` rejects the prohibited promotion path.

## Claims this note does not make

- It does not discharge the unrestricted parent goal `PLAN-QP-3` beyond the finite control carrier above.
- It does not certify continuum limits, external unreplayed theorems, or physical deployment.
