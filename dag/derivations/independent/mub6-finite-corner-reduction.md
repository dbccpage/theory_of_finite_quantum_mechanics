Status: AI-drafted, awaiting human review.

Let B be the 3 by 3 integer matrix with rows (1, 1, 0), (0, 1, 1) and (0, 0, 1). Let E be the 3 by 3 identity, and let C have rows (0, 1, 0), (0, 0, 1) and (1, 0, 0). Write A^T for the transpose of A. Matrix product is the ordinary row-column product of integers.

The matrix R with rows (1, -1, 1), (0, 1, -1) and (0, 0, 1) satisfies B R = I and R B = I, where I is the identity. Both products are the identity, so R is a two-sided inverse of B.

Form -C E^T R^T. That product is the matrix D with rows (1, -1, 0), (-1, 1, -1) and (-1, 0, 0). The sum C E^T + D B^T is the zero matrix. The same sum with the zero matrix in place of D is not the zero matrix. That sum has 3 nonzero entries.

MUB6-FINITE-CORNER-REDUCTION stays IMPORTED_ASSUMPTION.

What is proved

The two-sided inverse identity for this B, the equality of D with -C E^T R^T, the vanishing of C E^T + D B^T, and the failure of that vanishing when D is replaced by zero.

What is assumed

Arithmetic of the integers and the definition of 3 by 3 matrix product and transpose. AuthorityEffect: None.

What is open

No complex Hadamard classification is constructed. No list of retained finite corners is given. Quartet existence in the complex matrices of order six is not identified with completion of an external reconstruction. The complex adjoint is not identified with this integer transpose.
