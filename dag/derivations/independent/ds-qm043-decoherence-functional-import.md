Status: AI-drafted, awaiting human review.

# DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT

The imported formula is D_jk = Tr(C_j rho C_k dagger). This note records one integer Gram pattern and two cleared rational witnesses. It does not build a density operator, a class-operator family, or a bridge from finite transport.

## Gram square

For integers a, b, x and y, the number a*x + b*y has square (a*x + b*y) * (a*x + b*y). Every integer square is at least 0, so that value is at least 0. In particular each diagonal entry a*a and b*b is at least 0, and their sum a*a + b*b is at least 0.

The off-diagonal product a*b satisfies (a*b) * (a*b) = a*a * (b*b). The difference of those two products is 0. For the symmetric table with entries a*a, a*b, a*b, b*b, the determinant of that table is 0 and the trace of the table is a sum of two squares.

At a = b = x = y = 1 the square is 4, and the expanded count 1 + 2 + 1 is also 4.

## Two witnesses

Take the integer pair 1, 1 with denominator 2. The sum 1 + 1 equals 2 * 1, which is the cleared form of 1/2 + 1/2 = 1. The sum of squares is 2, while the square of the denominator is 4, and 2 differs from 4. That is the cleared form of (1/2)^2 + (1/2)^2 = 1/2, which differs from 1. The square of the sum is 4, which matches 4 * 1, the cleared form of a global weight 1.

Take the integer pair 3, 4 with denominator 5. The sum of squares is 9 + 16 = 25, and 5 * 5 = 25, so the cleared square-sum equals 1. The sum 3 + 4 equals 7, and 7 * 7 equals 49, which differs from 25. That is the cleared form of ((3/5) + (4/5))^2 = 49/25, which differs from 1.

The first witness has cleared class sum 1 and cleared square-sum different from 1. The second has cleared square-sum 1 and cleared square of the sum different from 1. The two controls are not the same integer condition.

## What is proved

Nonnegativity of an integer square, the Gram value (a*x + b*y)^2, nonnegativity of a*a and of a*a + b*b, the determinant identity, and the two numerical witnesses (1, 1) over 2 and (3, 4) over 5, including 2 ≠ 4 and 49 ≠ 25.

## What is assumed

Arithmetic of the integers, including that an integer square is at least 0. No density operator and no complex trace are assumed.

## What is open

The formula D_jk = Tr(C_j rho C_k dagger), a representation bridge from finite transport, a choice of class operators, and a physical history normalization. The two witnesses do not select that model.
