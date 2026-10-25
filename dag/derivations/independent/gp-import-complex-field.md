Status: AI-drafted, awaiting human review.

Gaussian integers are pairs of ordinary integers, written a+bi. Multiplication is (a+bi)(c+di) = (ac-bd)+(ad+bc)i. The real unit is 1+0i.

Take the element 1+i. Its product with a+bi is (a-b)+(a+b)i. The two coordinates therefore sum to 2a. The coordinates of the real unit sum to 1. An even integer and an odd integer are distinct, so 1+i times a+bi is distinct from the real unit. The same coordinate formula with the factors swapped is the same pair, so a+bi times 1+i is distinct from the real unit as well.

Let M be the matrix whose rows are (0, 1) and (1, 1), with each entry a real Gaussian integer. Conjugation fixes 0 and 1. The two diagonal entries are fixed by conjugation, and each off-diagonal entry is the conjugate of the other, so M equals the conjugate transpose defined by those four equations. A column (x, y) is sent to (y, x+y), because the first row picks out y and the second row adds x and y.

Suppose (y, x+y) equals lam times (x, y) for a Gaussian integer lam, and suppose (x, y) is not the zero column. The first coordinate says y = lam x. If x were zero, y would be zero, so x is nonzero. Substituting gives x + lam x = lam (lam x), hence (lam lam - (1+lam)) x = 0. The norm a^2+b^2 is multiplicative and vanishes only at zero, so a product of Gaussian integers is zero only when one factor is zero. Thus lam lam = 1+lam.

Write lam = p+qi. The imaginary part of lam lam - lam - 1 is q(2p-1). A product of integers is zero only when one factor is zero, and 2p-1 is never zero for an integer p. So q = 0 and p^2 = p+1. Then (2p-1)^2 = 5. For an integer k with absolute value at least 3, k^2 is at least 9, and the five remaining squares are 4, 1, 0, 1 and 4. None of them is 5. This contradiction shows that no such lam and nonzero column exist together.

GP-IMPORT-COMPLEX-FIELD stays IMPORTED_ASSUMPTION.

What is proved

The coordinate formula for (1+i)(a+bi), both orders distinct from the real unit, the four conjugate-transpose equations for the matrix with row-major entries 0, 1, 1, 1, the column image (y, x+y), and the absence of a Gaussian-integer eigenpair on a nonzero column.

What is assumed

Integer arithmetic, including that a product of integers is zero only when a factor is zero, and the definition of Gaussian-integer multiplication, conjugation, and the 2 by 2 matrix action used above. AuthorityEffect: None.

What is open

The example rules out Gaussian-integer eigenpairs for this one matrix. A spectral theorem after extending scalars to a complete complex field, and a derivation or selection of that field from primitive difference, remain imported. This obstruction does not prove that completion or the complex numbers are uniquely necessary; the cyclotomic ring Z[zeta_n] remains a recorded discrete substitute. The cyclotomic ring Z[zeta_n] stays a recorded discrete substitute.

The independent audit also computes the residual M*(x,lambda*x)-lambda*(x,lambda*x) using a separate SymPy matrix representation, and checks that its second entry is -(lambda^2-lambda-1)*x. This does not establish that all complex eigenpairs are absent; the fixed matrix has eigenpairs over larger fields.
