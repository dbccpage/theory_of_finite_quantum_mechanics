Status: AI-drafted, awaiting human review.

The node stays OPEN. The two opening sentences stay the open reading: l1 appears when aggregation over independent replicas is required to be extensive, and WDP 8.5 states that l2 is not excluded by this argument. The checked slice is arithmetic on the natural numbers.

Take natural numbers c, a, and b. Multiplication distributes over addition on the left, so

c * a + c * b = c * (a + b).

The same distributivity, with associativity and left commutativity of multiplication, gives the scale of a sum of squares:

(c * a) * (c * a) + (c * b) * (c * b) = (c * c) * (a * a + b * b).

On a = 3 and b = 4 the sum is 7, the sum of squares is 25, and 5 * 5 = 25. The square of the sum is 49, and 25 differs from 49. On c = 2 the scaled sum is 14, the scaled sum of squares is 100, and c times the sum of squares is 50. 100 differs from 50. An independent integer script also recomputes (2 * 2) * (3 * 3 + 4 * 4) = 100, and the two scale identities on the six triples (0, 0, 0), (1, 3, 4), (2, 3, 4), (5, 7, 1), (8, 9, 2), and (4, 0, 6).

## What is proved

The two Nat scale identities for every c, a, and b, and the numerals 7, 25, 49, 14, 100, and 50 named above.

## What is assumed

Nat addition and multiplication from the Lean prelude. This module imports no Mathlib.

## What is open

A classification, a derivation that l1 appears from replica extensivity, and a reading that l2 is excluded. The older bundled citation records finite-sum additivity and the closed facts (2 * 3) * (2 * 3) + (2 * 4) * (2 * 4) = 100 and 3 * 3 + 4 * 4 = 5 * 5. That citation does not discharge the open reading. Status stays OPEN.
