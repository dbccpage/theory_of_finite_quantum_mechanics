# PLAN-QP-C4

Goal id: PLAN-QP-C4

Selected scope for PLAN-QP-C4 is recorded in this note.

## Selected scope

Decidable DivisibleByEight predicate check and claim-typing guard requiring CONDITIONAL_RESULT when depending on CITED_INPUT FQM-C1000-B06-001.

## Hypotheses

H1. All calculations in this control are restricted to the declared finite integer and exact rational carriers (`carrier_val = 8`, `secondary_frac = 1/0`).

H2. The negative control `reject_proved_theorem_on_cited_input` refuses out-of-scope promotion, silent coercion, or unverified external theorem discharge.

## Derivation

On the declared finite carrier, the exact evaluation produces primary invariant `8` and rational ratio `1/0`, while the negative control `reject_proved_theorem_on_cited_input` rejects the prohibited promotion path.

## Claims this note does not make

- It does not discharge the unrestricted parent goal `PLAN-QP-C4` beyond the finite control carrier above.
- It does not certify continuum limits, external unreplayed theorems, or physical deployment.
