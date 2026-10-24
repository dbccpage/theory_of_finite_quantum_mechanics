Status: AI-drafted, awaiting human review.

# L1-U1-SELECTOR-OTHER-SEGMENT

AuthorityEffect: None.

Outcome: Narrowed. The node stays OPEN. The module `CampaignL1U1SelectorFiniteField` records one finite-field table. It does not select `C` or `U(1)`.

## The product in Z/5Z

Pairs are residues modulo 5. The product used here is

`(a, b) * (c, d) = (a*c + 4*b*d, a*d + b*c)`.

The coefficient check is `4 + 1 = 0` in Z/5Z, so the coefficient 4 is the additive inverse of 1. The independent check, not the Lean module, enumerates all `5^4 = 625` residue inputs and finds that `a*c + 4*b*d` and `a*c - b*d` agree modulo 5.

## The circle x*x + y*y = 1

There are `5 * 5 = 25` residue pairs. Direct evaluation leaves four solutions:

`(0, 1), (0, 4), (1, 0), (4, 0)`.

The count is 4. The same count is `5 - 1`. The successor `5 + 1` is 6, and 4 differs from 6. This is the table for the single prime 5. It is not a formula for the order of the circle over every finite field.

## Powers of (0, 1)

`(0, 1) * (0, 1) = (4, 0)`.
`(4, 0)` differs from `(1, 0)`.
`(4, 0) * (0, 1) = (0, 4)`.
`(0, 4) * (0, 1) = (1, 0)`.

So the fourth power of `(0, 1)` is the identity pair `(1, 0)`, and the square is not that identity.

## Two further pairs

`(1, 1)` has norm `1 + 1 = 2`, which is not 1, so it lies off the circle.
`(2, 1)` differs from `(0, 0)`, and its norm is `4 + 1 = 0` in Z/5Z.

## What is proved

In Z/5Z, the norm-1 pairs are exactly the four listed above; there are 4 of them; `4 = 5 - 1`; `5 + 1 = 6` and `4 ≠ 6`; `4 + 1 = 0`; on all 625 residue inputs the coefficient-4 product agrees with subtraction modulo 5; the three products of `(0, 1)` above hold and the square is not `(1, 0)`; `(1, 1)` has norm 2 and `2 ≠ 1`; `(2, 1)` is a nonzero norm-zero pair. The enumeration covers all 25 residue pairs.

## What is assumed

Arithmetic of `Fin 5` and of the natural numbers in Lean 4 core, with no added import. The allowed kernel axioms used by the module are `propext` on the `decide` steps. The count and the two natural-number identities `4 = 5 - 1` and `5 + 1 = 6` use no axioms. No new axiom is declared.

## What is open

Selection of `C` and `U(1)` from finite carriers. The Gaussian-rational torsion statement cited as `U1SelectorSegment.circle_torsion_iff` is not re-discharged here. Other finite fields and rings, a general order formula, cyclotomic extensions, completion, continuity, and the QM_028 / QM_062 pointer stay unresolved. The node status stays OPEN.
