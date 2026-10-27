Status: AI-drafted, awaiting human review.

Node `L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED`, record TFQ-0005. Status stays CONDITIONAL. This note records one integer witness.

Two sector-weight pairs are `(2, 0)` and `(0, 2)`. Each coordinate sum is `2 + 0 = 2` and `0 + 2 = 2`. The pairs differ. A common coordinate sum therefore does not fix the pair.

Length `4` and holonomy `2`: the products `4 * 0` and `4 * 1` are not `2`, and `4 * 2 = 8`, which is greater than `2`. Every larger multiple is at least `8`. So no natural number `k` satisfies `4 * k = 2`.

Length `4` and holonomy `4`: `4 * 1 = 4`.

These integers are checked in `L1ResidualSectorWeights` and again in `checks/independent/l1-residual-sector-weights-declared.py`.

## What is proved

The pairs `(2, 0)` and `(0, 2)` have coordinate sum `2` and differ. No natural number `k` satisfies `4 * k = 2`. The product `4 * 1` equals `4`.

## What is assumed

Arithmetic of closed natural numbers, and the two pairs as labels for sector weights. The general identification of `Phi1` with a holonomy, and of `Gamma2` with that holonomy, is not a hypothesis of these identities.

## What is open

The general n-cycle, the weighted L1 form with declared masses, the sum-of-squares reading of Gamma2, and any selector other than these two length-4 holonomy checks.
