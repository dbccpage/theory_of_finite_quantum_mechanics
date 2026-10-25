Status: AI-drafted, awaiting human review.

The node retains IMPORTED_ASSUMPTION for its original real-p Minkowski obligation. The standing slice is arithmetic on the natural numbers. It does not use a real exponent, a root, or a vector of arbitrary length.

Take natural numbers a and b. Expand the square by distributing:

(a + b) * (a + b) = a * (a + b) + b * (a + b) = a * a + a * b + b * a + b * b.

Commutativity of multiplication on Nat gives a * b = b * a, so the two cross terms are 2 * (a * b). That is the square expansion.

If a > 0 and b > 0, then a * b > 0, so the cross term 2 * (a * b) is positive. Substituting the expansion then gives

a * a + b * b < (a + b) * (a + b).

If the left input is 0, the cross term 2 * (0 * b) is 0, and (0 + b) * (0 + b) = b * b. If the right input is 0, the cross term 2 * (a * 0) is 0, and (a + 0) * (a + 0) = a * a. Those are equality cases, not strict cases.

The same ring arithmetic gives the cubic sum

(a + b) * (a + b) * (a + b) = a * a * a + b * b * b + 3 * a * b * (a + b).

On one disjoint coordinate pair, the squared coordinates add with no cross coordinate:

(x + 0) * (x + 0) + (0 + y) * (0 + y) = x * x + y * y.

A separate integer script checks every pair of coordinates from 0 through 12, and one witness pair a = 3, b = 5. For that witness the square is 64, the cross term is 30, the sum of squares is 34, and 34 < 64. The cube of 8 is 512, with parts 27, 125, and 3 * 3 * 5 * 8.

## What is proved

The Nat square expansion, the positive cross term and the strict square gap for two positive inputs, the two zero-input equality cases, the cubic sum, and the one disjoint Nat pair.

## What is assumed

Nat addition and multiplication, and the ordering of Nat. No real-analysis import is used in this slice.

## What is open

Real exponent p>1, a Minkowski comparison on real vectors, strict convexity, roots, and transport past this Nat square, cubic, and one disjoint pair.
