Status: AI-drafted, awaiting human review.

# FQ-GAP-U1-CIRCLE integer narrowing

The node stays CONDITIONAL. This note records one integer witness. It does not construct the circle group, and it does not treat continuity, power maps, or homomorphisms.

## The 3-4-5 identity

Direct arithmetic gives `3*3 + 4*4 = 9 + 16 = 25 = 5*5`.

## Squares modulo 5

The residues of a natural number modulo 5 are 0, 1, 2, 3, and 4. Their squares modulo 5 are 0, 1, 4, 4, and 1. So a square is congruent to 0, 1, or 4 modulo 5.

Multiply by 4: `4*0 = 0`, `4*1 = 4`, and `4*4 = 16 = 1` modulo 5. The product `4 * (b*b)` is divisible by 5 only when `b*b` itself is divisible by 5. A square divisible by 5 has base divisible by 5, because the other residues square to 1 or 4.

## Descent for `5*a*a = 4*b*b`

Assume `5*a*a = 4*b*b` for natural numbers `a` and `b`. The left side is divisible by 5, so `4*(b*b)` is divisible by 5, so `b` is divisible by 5. Write `b = 5*r`. Substitution gives

`5*a*a = 4*(5*r)*(5*r) = 100*(r*r)`,

so `a*a = 20*(r*r)`. The right side is divisible by 5, so `a` is divisible by 5. Write `a = 5*s`. Substitution gives

`25*(s*s) = 20*(r*r)`,

and cancelling a factor of 5 yields `5*s*s = 4*r*r`. Here `r < b` whenever `b > 0`, because `b = 5*r` and `r > 0`. Strong induction on `b` gives `b = 0`. The same identity on absolute values gives the integer form: `5*a*a = 4*d*d` forces `d = 0`.

## Cleared pair

Suppose integers `a`, `b`, and `d` satisfy both

`5*(a*a - b*b) = 3*(d*d)` and `a*a + b*b = d*d`.

From the second equation, `a*a - b*b = 2*a*a - d*d`. The first equation becomes `5*(2*a*a - d*d) = 3*(d*d)`, hence `10*a*a = 8*d*d`, hence `5*a*a = 4*d*d`. The previous paragraph forces `d = 0`. The norm equation collapses to `a*a + b*b = 0`. Each square is nonnegative, so each is zero, and `a = b = 0`.

The zero triple satisfies both equations. The triple `(3, 4, 5)` satisfies the norm and fails `5*(a*a - b*b) = 3*(d*d)`.

## What is proved

- `3*3 + 4*4 = 5*5`.
- For every natural number `a` and `b`, `5*a*a = 4*b*b` holds only when `b = 0`.
- For every integer `a`, `b`, and `d`, the two equations `5*(a*a - b*b) = 3*(d*d)` and `a*a + b*b = d*d` hold together only when `a = 0`, `b = 0`, and `d = 0`.

The Lean declarations are `pythagorean345`, `fiveFourSquareForcesZero`, `clearedDenominatorForcesFourFifths`, and `noNonzeroClearedSquareRoot` in `lean4/CampaignFqGapU1Circle.lean`.

## What is assumed

Arithmetic of natural numbers and integers in the Lean kernel, including divisibility, modulo 5, and nonnegativity of squares. No new axiom is declared. The node status stays CONDITIONAL.

## What is open

The circle group U(1) on the finite host is not constructed here. Continuity of a one-parameter phase group stays a hypothesis. Injectivity of `n` mapped to `u^n` for `u = (3+4i)/5`, and a homomorphism from `(Q, +)` into `U(1)(Q(i))` sending 1 to `u`, stay open. Compact continuous `R/Z` stays an external completion. The Python script scans `b` through 2000 and integers through a box of radius 12. That scan is not the descent.
