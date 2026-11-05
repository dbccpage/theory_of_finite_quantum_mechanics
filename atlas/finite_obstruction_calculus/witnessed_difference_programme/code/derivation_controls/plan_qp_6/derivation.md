# PLAN-QP-6

Goal id: PLAN-QP-6

Selected scope for PLAN-QP-6 is recorded in this note.

## Selected scope

Complete bipartite graph K_{2,3} qutrit witness comparing primal trace-norm sum 6 against unscaled dual 9/2.

## Hypotheses

H1. All calculations in this control are restricted to the declared finite integer and exact rational carriers (`carrier_val = 6`, `secondary_frac = 9/2`).

H2. The negative control `reject_refuted_k23_dual_equality` refuses out-of-scope promotion, silent coercion, or unverified external theorem discharge.

## Derivation

On the declared finite carrier, the exact evaluation produces primary invariant `6` and rational ratio `9/2`, while the negative control `reject_refuted_k23_dual_equality` rejects the prohibited promotion path.

## Claims this note does not make

- It does not discharge the unrestricted parent goal `PLAN-QP-6` beyond the finite control carrier above.
- It does not certify continuum limits, external unreplayed theorems, or physical deployment.
