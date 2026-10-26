Status: AI-drafted, awaiting human review.

# L1-U1-SELECTOR-OTHER-SEGMENT

Node status stays OPEN. The standing text is one circle over the integers modulo 7. Selection of a complex field or of a circle group, and every other modulus, stay outside this note.

## The product

Take pairs of residues modulo 7. Define

(a, b) * (c, d) = (a*c - b*d, a*d + b*c),

with both coordinates reduced modulo 7. The Lean definition adds the pad 252 = 7 * 36 before the subtraction so the first coordinate stays a natural number when both inputs have coordinates below 7. On those residues the pad is a multiple of 7, so the two formulas agree.

## Eight powers

Start at (1, 0) and multiply on the right by g = (2, 2), eight times:

1. (1, 0)
2. (2, 2)
3. (0, 1)
4. (5, 2)
5. (6, 0)
6. (5, 5)
7. (0, 6)
8. (2, 5)

The next product is (1, 0) again. Each of those seven pairs after the start differs from (1, 0). The eight pairs are pairwise distinct, so the first return is at step 8.

## The circle equation

Each of the eight pairs satisfies x*x + y*y = 1 modulo 7. A direct check of all 49 residue pairs finds no other solution. So the solution set is exactly this list of eight. The count 8 equals 7 + 1 and is not 4. The generator (2, 2) is not one of the four axis pairs (1, 0), (0, 1), (6, 0), (0, 6).

## What is proved

The eight powers, the return at the eighth step, the match with every solution of x*x + y*y = 1 modulo 7, and the two comparisons 8 = 7 + 1 and 8 ≠ 4.

## What is assumed

Arithmetic of the natural numbers and reduction modulo 7, together with the product written above. AuthorityEffect is None.

## What is open

Selection of C and of U(1), the unit Gaussian rationals, the four torsion phases inside those rationals, every modulus other than 7, cyclotomic extensions, completion and continuity. The pointer target in QM_028 / QM_062 stays unresolved.
