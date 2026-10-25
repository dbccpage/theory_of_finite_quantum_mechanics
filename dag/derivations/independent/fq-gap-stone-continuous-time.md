Status: AI-drafted, awaiting human review.

# FQ-GAP-STONE-CONTINUOUS-TIME

Node status stays CONDITIONAL. The standing text is an integer equation. Continuous time, the Stone theorem, strong continuity, a one-parameter group, generator selection, and causal order stay outside this note.

## The 3-4-5 scale

The integers 3, 4 and 5 satisfy

3 * 3 + 4 * 4 = 5 * 5.

## The equation 5 * a * a = 4 * b * b

Let a and b be natural numbers, including 0, and suppose 5 * a * a = 4 * b * b.

Squares modulo 5 take only the values 0, 1 and 4. This is a check of the five residues 0, 1, 2, 3 and 4: their squares modulo 5 are 0, 1, 4, 4 and 1. A square is 0 modulo 5 only for residue 0, so a natural number whose square is divisible by 5 is itself divisible by 5. Likewise, 4 times a square is 0 modulo 5 only for residue 0.

The right-hand side 4 * b * b is divisible by 5, because it equals 5 * a * a. Therefore b is divisible by 5. Write b = 5 * r. Then r < b whenever b > 0, since 5 * r is strictly larger than r for r > 0.

Substituting gives 5 * a * a = 4 * (5 * r) * (5 * r) = 100 * r * r, so a * a = 20 * r * r. Thus a * a is divisible by 5, so a is divisible by 5. Write a = 5 * s. Then

5 * (5 * s) * (5 * s) = 4 * (5 * r) * (5 * r).

The integer scales 5 * (5 * s) * (5 * s) = 125 * s * s and 4 * (5 * r) * (5 * r) = 100 * r * r reduce that equation to 5 * s * s = 4 * r * r.

Repeat. Each positive b is replaced by b / 5, which is a strictly smaller natural number. The only natural number that survives is b = 0, and then 5 * a * a = 0, so a = 0.

The pair (0, 0) satisfies the equation. The same reduction returns (0, 0) on that pair.

## What is proved

The equality 3 * 3 + 4 * 4 = 5 * 5. For all natural numbers a and b, if 5 * a * a = 4 * b * b then a = 0 and b = 0.

## What is assumed

Natural-number arithmetic, including division by 5 when the remainder is 0, and the five-residue table for squares modulo 5. AuthorityEffect is None.

## What is open

Continuous time, the Stone theorem, strong continuity, a one-parameter group, generator selection, and a relation between spacetime events stay open. A rational matrix square root, a Q-parameter group, and a carrier extension by an extra square root stay open. The finite window a, b at most 30 in the independent script is an audit of the equation, not the general argument.
