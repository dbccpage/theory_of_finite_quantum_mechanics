Status: AI-drafted, awaiting human review.

# MUB-PRIME-POWER-CONSTRUCTION

Node status stays OPEN. This note records dimension 2.

## Carrier

The Gaussian integers form the ring used for exact coordinates of vectors in C^2; they are not a field. A number a + bi is the pair (a, b). Multiplication is (a, b)(c, d) = (ac - bd, ad + bc). The squared modulus is a squared plus b squared. The square of i, the pair (0, 1), is (-1, 0).

These three orthogonal vector pairs represent bases of C^2 after normalization:

- Z0 = (1, 0) and Z1 = (0, 1).
- X0 = (1, 1) and X1 = (1, -1).
- Y0 = (1, i) and Y1 = (1, -i).

The squared norm of a vector is the sum of the squared moduli of its two components. Those six squared norms are 1, 1, 2, 2, 2 and 2. The inner product of a vector with itself is that squared norm, as a real Gaussian integer.

## Unbiasedness

Distinct vectors in the same basis have inner product 0.

Take a vector u from one basis and a vector v from a different basis. Twice the squared modulus of their inner product equals the product of their squared norms. For the computational basis against either of the other bases, the inner-product squared modulus is 1 and the norm product is 2. For the X basis against the Y basis, the inner-product squared modulus is 2 and the norm product is 4. In every such pair the two sides agree, so the normalized overlap has squared modulus 1/2.

## The two-element field

The additive character of the field with two elements sends 0 to 1 and 1 to -1. Addition in that field is exclusive or, so 1 + 1 = 0 and the character of 1 + 1 is 1. No factor of 1/2 is used.

## What is proved

For these six vectors: the square of i, the six squared norms, the six self-inner-products, the three orthogonalities inside a basis, and the twelve cross-basis norm identities. For the two-element field: the two character values and the character of a doubled element.

## What is assumed

Gaussian-integer arithmetic and the two-element exclusive-or. The listed pairs represent bases over C; no basis of the Z[i]-module Z[i]^2 is claimed. AuthorityEffect is None.

## What is open

A complete family for any prime power other than 2, odd characteristic, a general character sum, normalization in a larger cyclotomic field, and every reading at dimension 6. This dimension-2 family does not supply those constructions.
