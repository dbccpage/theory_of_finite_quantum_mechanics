Status: AI-drafted, awaiting human review.

Node `FQ-PRIM-TO-QM-SELECTION-OPEN`. Status stays CONDITIONAL. This note records one integer witness on two amplitudes.

Take the amplitudes `1` and `2`. The quadratic numerators are `1 * 1 = 1` and `2 * 2 = 4`. Their sum is `5`. The quartic numerators are `1 * 1 = 1` and `4 * 4 = 16`. Their sum is `17`. Each numerator is positive, and each pair adds to its denominator, so both rules are positive and normalized: the quadratic weights are `1/5` and `4/5`, and the quartic weights are `1/17` and `16/17`.

The cross products are `1 * 17 = 17` and `1 * 5 = 5`. These are different, so `1/5` is not `1/17`. The same two amplitudes admit both rules.

For the equal amplitudes `1` and `1`, the quadratic numerators are `1` and `1` and sum to `2`, and the quartic numerators are `1` and `1` and sum to `2`. Both rules assign weight `1/2` to each label.

These integers are checked in `PrimToQmSelection` and again in `checks/independent/fq-prim-to-qm-selection-open.py`.

## What is proved

On amplitudes `1` and `2`, the quadratic numerators are `1` and `4` with sum `5`, and the quartic numerators are `1` and `16` with sum `17`. The normalized first weights `1/5` and `1/17` differ. On amplitudes `1` and `1`, both rules have numerators `1` and `1` with sum `2`.

## What is assumed

Arithmetic of closed natural numbers, and the reading of a numerator over the sum of the two numerators as a normalized weight. No primitive-difference value is an input to these identities.

## What is open

A selector from primitive difference to a declared quantum model or readout, packet-walk execution, the complexes, a Cayley parameter, cyclotomic weights, a detector, continuum matrix algebras, and Gleason for dimension at least `3`.
