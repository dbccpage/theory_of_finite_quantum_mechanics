# BRIDGE-CLOSURE-RATIO-LOWER

Goal id: BRIDGE-CLOSURE-RATIO-LOWER

Selected scope for BRIDGE-CLOSURE-RATIO-LOWER is recorded in this note.

## Selected scope

F_2 support-norm closure ratio minimum 1/2 on H^1 = 0, paired with the geometric non-termination sequence h_n = 2^{-n} over Q and the d_1 = 0 nonzero-H^1 counterexample.

## Hypotheses

H1. All calculations in this control are restricted to the declared finite integer and exact rational carriers (`carrier_val = 1`, `secondary_frac = 1/2`).

H2. The negative control `reject_expansion_implies_unconditional_termination` refuses out-of-scope promotion, silent coercion, or unverified external theorem discharge.

## Derivation

On the declared finite carrier, the exact evaluation produces primary invariant `1` and rational ratio `1/2`, while the negative control `reject_expansion_implies_unconditional_termination` rejects the prohibited promotion path.

## Claims this note does not make

- It does not discharge the unrestricted parent goal `BRIDGE-CLOSURE-RATIO-LOWER` beyond the finite control carrier above.
- It does not certify continuum limits, external unreplayed theorems, or physical deployment.
