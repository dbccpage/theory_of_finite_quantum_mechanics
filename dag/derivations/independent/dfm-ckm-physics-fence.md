Status: AI-drafted, awaiting human review.

# DFM-CKM-PHYSICS-FENCE

AuthorityEffect: None.

The dossier writes three counting expressions for `N_g` generations: a cycle
expression `(N_g - 1)^2`, a constraint expression `N_g(N_g - 1)/2`, and a CP
expression `(N_g - 1)(N_g - 2)/2`. It also reads the CP expression as the
number of physical CP phases left after a unitarity-triangle reduction, and it
reads a CKM matrix as induced by dressed Yukawa couplings. This note keeps the
rational relation among the three expressions and separates that relation from
a quartet in `Q(i)`.

## Counting

For a rational `n`,

```
cycleCount(n) = (n - 1)^2
constraintCount(n) = n(n - 1)/2
cpCount(n) = (n - 1)(n - 2)/2
```

Clearing the common denominator `2` gives the identities

```
cycleCount(n) - constraintCount(n) = cpCount(n)
cpCount(n) + (n - 1) = constraintCount(n)
```

for every rational `n`. The four declared points are

```
n = 1: cycle 0, cp 0
n = 2: cycle 1, cp 0
n = 3: cycle 4, cp 1
n = 4: cycle 9, cp 3
```

The two expressions agree at `n = 1` and differ at `n = 2, 3, 4`. At `n = 3`
the constraint expression is `3`, and `4 - 3 = 1`.

## Quartets

Write a quartet in `Q(i)` as `a b conj(c) conj(d)`. The quartet of four ones
is `1`, with imaginary part `0`. Replacing the second factor by `i` yields
`i`, with imaginary part `1`. The CP expression at `n = 3` equals `1`, so it
matches the second imaginary part and misses the first. The same integer is
therefore not the imaginary part of every declared quartet.

## Classification of supplied nonzero labels

Take any commutative group G and a table M with a designated base row r and
column c. A supplied gauge acts by M[i,j] -> u[i] M[i,j] / v[j]. Define
N(M)[i,j] = M[i,j] M[r,c] / (M[i,c] M[r,j]). All divisions are in G.
The base row and column become one. Commutativity cancels the row and column
factors, so N is invariant and idempotent. The explicit gauge
u[i] = 1/M[i,c], v[j] = M[r,j]/M[r,c] sends M to N(M).
Consequently equal normal forms give a gauge from M to M' by composing the
first normalizing gauge with the inverse of the second. The converse follows
from invariance. This proves both directions, rather than assuming orbit
agreement.

With Option-indexed rows and columns, none is the base and the remaining
entries are free coordinates. Extending any free table with a boundary of
ones and restricting it back are inverse maps. Empty free row or column types
are included. Finite decidable equality gives a Boolean orbit decision with
soundness and completeness. For Fin n on both free axes there are n*n
coordinate positions; this counts positions, not physical phases.

The exact instance uses nonzero Gaussian rationals as Units. checkedLabel
returns none exactly at zero and preserves the underlying value on success.
Arbitrary nonzero rescalings are allowed; this action does not assert unit
modulus, unitarity, or that the entries describe a physical mixing matrix.

The independent checker exercises 2376 sign-gauge actions and 4388 pair
decisions across shapes 1x1, 1x2, 2x1, 2x2, 2x3. Their orbit counts are
1, 1, 1, 2, 4. A nonreal rational example checks the reconstructed witness;
a changed cross-ratio separates another pair. Eleven invalid inputs are
refused in normal and optimized Python. Four selected in-memory faults are
detected; this is scoped regression evidence, not exhaustive mutation coverage.

## What is proved

In `lean4/CampaignDfmCkmPhysicsFence.lean`:

- `cpCount_from_difference` and `constraintCount_sum` are the two rational
  identities for every `n`.
- `count_table` records the eight values at `n = 1, 2, 3, 4` and the pattern
  of agreement and disagreement.
- `three_generation_split` records `4`, `3`, and `1` at `n = 3`.
- `quartet_real_value`, `quartet_imag_value`, `quartets_differ`, and
  `count_misses_one_quartet` record the imaginary parts `0` and `1`.

The independent check recomputes the identities on nine rational samples, the
four-point table, and the two quartets.

The Rephasing namespace also proves the action laws, normalization laws,
constructive orbit classification, free-coordinate equivalence, Boolean
decision correctness and explicit zero refusal described above.

## What is assumed

The carrier of a quartet factor is `Q(i)` with the usual multiplication. The
three counting expressions are rational polynomials, not edge counts of a
graph. No Yukawa matrix, mass basis, unitary constraint, or measured angle is
an input.

## What is open

Derivation of a mixing matrix from Yukawa couplings, a unitarity
identification of these counts, any graph or tree of the flavour data, and
measured CP values stay open. The node status stays OPEN.
