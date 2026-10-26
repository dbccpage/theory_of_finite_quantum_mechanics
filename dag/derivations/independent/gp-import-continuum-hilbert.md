Status: AI-drafted, awaiting human review.

# GP-IMPORT-CONTINUUM-HILBERT

The imported claim is a passage from a finite presented carrier to a continuous infinite-dimensional Hilbert space. This note records one finite integer window and one finite geometric identity. It does not select a scalar field, an l2 uniformity, a topology, or a Cauchy completion.

## Window

Take the four positive integers 8, 4, 2 and 1. Each of the first three is the sum of two copies of the next:

- 8 = 4 + 4
- 4 = 2 + 2
- 2 = 1 + 1

Their squares are 64, 16, 4 and 1. The sum of the squares is 85. Three times 85, plus 1, equals 256. The same 256 is 4^4.

The successive differences of the squares are

- 64 - 16 = 48 = 3 * 16
- 16 - 4 = 12 = 3 * 4
- 4 - 1 = 3 = 3 * 1

No positive natural number z satisfies z + z = 1, so the last coordinate has no further positive integer half.

## Powers of four

Let 4^0 = 1 and 4^{k+1} = 4 * 4^k. Let S(n) be the sum of 4^0 through 4^{n-1}, with S(0) = 0.

The step S(n+1) = S(n) + 4^n is the definition of the partial sums, so S(n+1) - S(n) = 4^n.

The closed form 3 * S(n) + 1 = 4^n holds at n = 0, because both sides are 1. If it holds at n, then

3 * S(n+1) + 1 = 3 * (S(n) + 4^n) + 1 = (3 * S(n) + 1) + 3 * 4^n = 4^n + 3 * 4^n = 4^{n+1}.

Thus 4^n - 3 * S(n) = 1 for every natural number n. The missing scaled mass at every finite length is the positive integer 1.

For n = 4 the coordinates 8, 4, 2, 1 are 2^3, 2^2, 2^1, 2^0, and their squares are 4^3, 4^2, 4^1, 4^0. So the window sum 85 is S(4), and 3 * 85 + 1 = 4^4.

For n >= 1 the same identity is the integer form of the rational truncation. The sum of (1/4)^k from k = 0 through n - 1 equals (4^n - 1) / (3 * 4^{n-1}). Multiplying by the positive denominator 3 * 4^{n-1} clears it to 3 * S(n) = 4^n - 1, and the missing numerator is 1.

## What is proved

The length-4 window, its squares, the sum 85, the scaled value 256, the three successive differences, the identity 3 * S(n) + 1 = 4^n, the difference S(n+1) - S(n) = 4^n, and the absence of a positive natural solution of z + z = 1.

## What is assumed

Arithmetic of the natural numbers, including the usual rules used to move a concrete equality across a successor step. No Hilbert-space structure is assumed.

## What is open

Scalar-field selection, l2 uniformity, a verified topology, a Cauchy completion, and the lift of bounded exact operators to an infinite-dimensional carrier. QM_122 section 6 and the QM_020 demotion box still fence that transition. A finite window with a unit of missing scaled mass is not that carrier.
