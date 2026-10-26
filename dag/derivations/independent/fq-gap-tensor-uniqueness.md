Status: AI-drafted, awaiting human review.

# Integer outer products on a 2 by 2 coefficient matrix

AuthorityEffect: None.

Node FQ-GAP-TENSOR-UNIQUENESS stays CONDITIONAL. This note records one integer matrix identity. It does not select a tensor product.

## Setup

Take integers a0, a1, b0, b1. The outer product is the 2 by 2 matrix whose entries are a0*b0, a0*b1, a1*b0 and a1*b1. Its determinant is (a0*b0)*(a1*b1) - (a0*b1)*(a1*b0).

## Determinant

Multiplication of integers is associative and commutative, so the two products are the same integer:

(a0*b0)*(a1*b1) = a0*(b0*(a1*b1)) = a0*((b0*a1)*b1) = a0*((a1*b0)*b1) = a0*(a1*(b0*b1)) = a0*(a1*(b1*b0)) = (a0*b1)*(a1*b0).

Their difference is 0. Every such outer product therefore has determinant 0.

The matrix with entries 1, 0, 0 and 1 has determinant 1*1 - 0*0 = 1. A matrix whose determinant is 1 is not equal to a matrix whose determinant is 0, so this matrix is not an outer product of two integer vectors.

## What is proved

For every integer quadruple, the outer-product determinant is 0. The matrix with entries 1, 0, 0 and 1 has determinant 1 and is not such an outer product. The Lean declarations are `outerDet`, `identityDet` and `identityNotOuter`. Each printed axiom list is `propext`.

## What is assumed

Integer multiplication is the ring multiplication of `Int`. No local Hilbert space, no tomography axiom, and no controlled shift is used.

## What is open

Local complex quantum mechanics, independent preparation and testing, local tomography, local unitaries, a calibrated reversible controlled shift, and the saturation hypotheses for effects and finite tests stay supplied. The determinant split does not compare state cones with effect cones and does not choose a tensor product. Primitive difference has not supplied those operational premises.

The repaired independent checker compares determinant computations with separate exact rational row elimination, and rejects identity, wrong-sign and changed-entry controls. Counts are measured and failures raise explicit exceptions rather than returning an unbounded count as a process exit code. This finite census does not replace the universal Lean theorem.
