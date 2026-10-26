Status: AI-drafted, awaiting human review.

# L1-IMP-ORTHOGONAL-ADDITIVITY

Node status stays CONDITIONAL. This note records one 2 by 2 integer coefficient matrix. The general sector-additive readout on a finite rational carrier is already in `lean4/SectorFormUniqueness.lean`. Arbitrary orthogonal frames stay outside this note.

## The matrix

Take the integer matrix with rows (1, 1) and (-1, 1). The two off-diagonal entries are 1 and -1. Their sum is 0. Neither entry is 0.

## The quadratic form

For integers a and b, the form is

1 * a * a + 1 * a * b + (-1) * b * a + 1 * b * b.

Integer multiplication commutes, so a * b and b * a are the same integer, and the cross terms cancel. The form equals a * a + b * b.

## The two axes

The form on (a, 0) is a * a. The form on (0, b) is b * b. Their sum equals the form on (a, b). The two axis vectors meet the disjoint-support pattern: one coordinate is zero in each.

## What is proved

The pair sum 0, the two nonzero off-diagonal entries, the diagonal square sum for every integer pair (a, b), and additivity of that form on the two axes.

## What is assumed

Integer addition and multiplication, including commutativity of multiplication. AuthorityEffect is None.

## What is open

Frame additivity on arbitrary orthogonal frames, projection measures, and Gleason-type uniqueness. Sector additivity as a law for a general carrier stays a hypothesis. A symmetric Gram matrix is still required before each off-diagonal entry, rather than only the pair sum, is zero.

The matrix is nonsymmetric, so it is not the Gram matrix of a real inner product. The checker uses a separate matrix-vector contraction and coefficient comparison, plus a changed-sign counterexample.
