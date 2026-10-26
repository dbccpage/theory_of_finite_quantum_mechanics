Status: AI-drafted, awaiting human review.

Let R be the set of integer pairs (a, b). Addition is coordinatewise. The product is (a, b)*(c, d) = (a*c - b*d, a*d + b*c + b*d). Write w for the pair (0, 1), and write 1 for (1, 0). The product rule gives w*w = (-1, 1), which is the same pair as w - 1. Iterating the product gives w*w*w = (-1, 0) and six factors of w equal to 1. The conjugate used below sends (a, b) to (a + b, -b). In particular the conjugate of w is (1, -1), and that pair times w is 1.

Index rows and columns by 0, 1, 2, 3, 4, 5. Let X be the 6 by 6 matrix over R with a 1 in each position (j + 1 mod 6, j) and zeros elsewhere. Let Z be diagonal, with diagonal entry w^j in column j, where w^j means the j-fold product of w and w^0 = 1. Matrix multiplication is the usual row-column rule, with the product of R in each summand.

The entry in row i and column j of Z X is w^i when i = j + 1 mod 6, and zero otherwise. The same positions of w X Z carry w * w^j = w^{j+1}. Those two descriptions agree, so Z X = w X Z. The opposite order does not obey the same factor: X Z and w Z X differ in 6 entries. One of them is row 1, column 0, where X Z has 1 and w Z X has w*w.

For p, q in 0..5, the product X^p Z^q has a single nonzero entry in each column. In column j that entry sits in row j + p mod 6 and equals w^{q j}. This is checked by comparing every entry of the matrix power with that formula. The conjugate-transpose therefore has, in row j and column j + p mod 6, the conjugate of w^{q j}.

Take two such products, for (p, q) and (r, s). In the product of the conjugate-transpose of the first by the second, the diagonal entry in position i is zero unless p = r, because the two nonzero patterns meet only then. When p = r the diagonal entry is the conjugate of w^{q i} times w^{s i}. Summing the six diagonal entries gives the trace. When (p, q) = (r, s) each of the six summands is 1, so the trace is (6, 0). When p = r and q differs from s, the same sum is the zero pair. When p differs from r the trace is the zero pair. There are 36 operators and 1296 ordered pairs.

MUB6-WEYL-HEISENBERG-D6 stays IMPORTED_ASSUMPTION.

What is proved

The integer-pair product and conjugate above, the three power identities for w, the stated positions of X and Z, the identity Z X = w X Z, the inequality of X Z with w Z X, and the trace values (6, 0) and (0, 0) for every p, q, r, s from 0 through 5.

What is assumed

Arithmetic of the integers, the definitions of this product, this conjugate, and 6 by 6 matrix multiplication over the pairs. AuthorityEffect: None.

What is open

No complex exponential is constructed, and the pair w is not identified with exp(2 pi i / 6). No count of mutually unbiased bases follows from the trace table. The source commutation written as X Z = w Z X belongs to the opposite clock convention.
