Status: AI-drafted, awaiting human review.

# DS-QM204 integer pair, rotation, and two splits

The imported Born-uniqueness claim asks for Gleason uniqueness and for L^p pairings in measure theory. This note records one integer case and leaves that import in place.

## Pair sum

For every integer pair A and B, multiplication by 1 is the identity, so A + B = (A + B) * 1. On the pair 3 and 4 the denominator of a two-term normalization is 3 + 4 = 7, and 7 differs from 0. This is the cleared form of adding the two shares of a nonzero sum. It does not select a quadratic pairing.

## Squares and fourth products

3 * 3 + 4 * 4 = 9 + 16 = 25, and 5 * 5 = 25.
3 * 3 * 3 * 3 + 4 * 4 * 4 * 4 = 81 + 256 = 337.

## Two splits of the pair (3, 4)

Quadratic mass against fourth-product mass, cleared of a common denominator:
(3 * 3) * (3 * 3 * 3 * 3 + 4 * 4 * 4 * 4) = 9 * 337 = 3033,
(3 * 3 * 3 * 3) * (5 * 5) = 81 * 25 = 2025,
and 3033 differs from 2025.

Linear mass against quadratic mass:
3 * (3 * 3 + 4 * 4) = 3 * 25 = 75,
(3 * 3) * (3 + 4) = 9 * 7 = 63,
and 75 differs from 63.

## Rotation identity

For every integer quadruple a, b, r and s,
(r * a - s * b) * (r * a - s * b) + (s * a + r * b) * (s * a + r * b)
= (r * r + s * s) * (a * a + b * b).

Expand the left-hand squares. The cross products (r * a) * (s * b), (s * b) * (r * a), (s * a) * (r * b) and (r * b) * (s * a) all rearrange, by commutativity and associativity, to (r * s) * (a * b), so they cancel. Each square (x * y) * (x * y) rearranges to (x * x) * (y * y). The remaining terms are the expansion of the right-hand side.

At a = 3, b = 4, r = 3 and s = 4 both sides equal 625:
(3 * 3 - 4 * 4) * (3 * 3 - 4 * 4) + (4 * 3 + 3 * 4) * (4 * 3 + 3 * 4)
= (-7) * (-7) + 24 * 24 = 49 + 576 = 625,
and (3 * 3 + 4 * 4) * (3 * 3 + 4 * 4) = 25 * 25 = 625.

## What is proved

The integer identities named above, including the rotation identity for every integer quadruple and the two inequalities for the pair (3, 4).

## What is assumed

Integer arithmetic in the Lean prelude, including the ring laws used in the rewrites and the linear arithmetic used after the products have been identified.

## What is open

Gleason uniqueness, frame-function, effect, continuity and dimension hypotheses, and L^p pairings in measure theory stay imported. Bare normalization does not select a quadratic pairing. The node stays IMPORTED_ASSUMPTION.
