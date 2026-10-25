Status: AI-drafted, awaiting human review.

# GP-IMPORT-CIRCLE-U1

Node status stays IMPORTED_ASSUMPTION. The standing text is integer arithmetic on signs, one pair product, and one cycle. The circle group and continuity of a one-parameter phase group stay outside this note.

## Signs

A sign is an integer equal to 1 or equal to -1. For either value, the product of the integer with itself is 1.

## Two pairs

The integer pairs (1, 1) and (1, -1) are different. Each coordinate of either pair is 1 or -1, so each coordinate is a sign.

## One unit-norm pair

Write the product of integer pairs by

(a, b) * (c, d) = (a * c - b * d, a * d + b * c)

and the square norm by a * a + b * b. For the pair 0, 1 the square norm is 1. The product of that pair with itself is the pair -1, 0. That pair differs from the pair 1, 0.

## One three-step cycle

Let the map on natural numbers send 0 to 1, 1 to 2, and 2 to 0, and send every other natural number to itself. Starting at 0, one application yields 1, the second application yields 2, and the third application yields 0.

## What is proved

Each sign squares to 1. The pairs (1, 1) and (1, -1) differ, and each of their coordinates is a sign. The integer pair 0, 1 has square norm 1, and the product of that pair with itself is the pair -1, 0, which differs from the pair 1, 0. The map above returns 2 at the second step from 0 and returns 0 at the third step from 0.

## What is assumed

Integer arithmetic and the declared product, square norm, and cycle map. AuthorityEffect is None.

## What is open

The circle group U(1), continuity of a one-parameter phase group, and a selector for that circle.

The independent audit uses the matrix with rows (0,-1), (1,0) for multiplication by i and the permutation table (1,2,0) for the cycle. It checks all three starting points, while the Lean claim is restricted to the stated iterates from zero. No classification or construction of a continuous phase group is inferred.
