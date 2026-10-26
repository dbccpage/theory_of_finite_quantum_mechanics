Status: AI-drafted, awaiting human review.

# One 2 by 4 coset over the two-element field

AuthorityEffect: None.

## Setup

Work in the two-element field. Coordinates of a length-4 vector are bits of an integer label `n` from 0 through 15, and coordinate `i` is the coefficient of `2^i` (the least significant bit is coordinate 0). There are 16 such labels.

The parity-check matrix has two rows:

- row 1: `(1, 1, 0, 0)`, so the first syndrome bit is `(bit0 + bit1) mod 2`;
- row 2: `(0, 1, 1, 1)`, so the second syndrome bit is `(bit1 + bit2 + bit3) mod 2`.

The Hamming weight of a label is the number of 1 bits among its four coordinates.

## Enumeration

Compute both syndrome bits for each label from 0 through 15.

Syndrome `(1, 0)` holds for labels 1, 6, 10 and 13, and for no other label in the range.

- label 1 has bits `(1, 0, 0, 0)` and weight 1;
- label 6 has bits `(0, 1, 1, 0)` and weight 2;
- label 10 has bits `(0, 1, 0, 1)` and weight 2;
- label 13 has bits `(1, 0, 1, 1)` and weight 3.

The weights are 1, 2, 2 and 3. The minimum is 1. The only label in this list with weight 1 is 1.

Syndrome `(0, 0)` holds for labels 0, 7, 11 and 12. That list has length 4. These are the vectors in the kernel of this one matrix, inside the same set of 16 labels.

## What is proved

For this one matrix and these two syndromes, the lists, weights, minimum, unique weight-1 label, and coordinates above.

## What is assumed

Arithmetic of nonnegative integers, including remainder modulo 2. No literature theorem is used in the count.

## What is open

Berlekamp, McEliece and van Tilborg 1978, that minimum-weight coset decoding of a general binary linear code given by its matrix is NP-hard, is still an imported literature claim. No reduction is formalized. The count above is one 2 by 4 matrix and does not discharge that claim. The node stays an imported assumption.
