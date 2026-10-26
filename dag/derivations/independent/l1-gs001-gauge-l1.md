Status: AI-drafted, awaiting human review.

# L1-GS001-GAUGE-L1

Node status stays OPEN. This note records a shadow on two integer coordinates. It does not derive a maximal bounded-linear symmetry on a general gauge presentation.

## Signed permutations

A signed permutation of a pair `(x, y)` is a choice of three bits: whether to swap the coordinates, whether to change the sign of the first coordinate, and whether to change the sign of the second. Signs are applied before the swap. There are eight such maps.

Write `A(x, y) = |x| + |y|`.

Changing the sign of either coordinate leaves `A` unchanged, because `|-t| = |t|`. Swapping the coordinates leaves `A` unchanged, because addition of natural numbers is commutative. Therefore every signed permutation leaves `A` unchanged.

The two axis values add: `A(x, 0) + A(0, y) = |x| + |y| = A(x, y)`, since `|0| = 0`.

Scaling both coordinates by an integer `k` multiplies the aggregate by `|k|`: `|k x| + |k y| = |k| |x| + |k| |y| = |k| A(x, y)`.

## The eight images of (1, 2)

The eight maps send `(1, 2)` to

`(1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)`.

These eight pairs are distinct. Therefore two different bit choices cannot send `(1, 2)` to the same pair: the action on this one vector separates the eight maps.

## Weighted aggregates

For natural numbers `w1` and `w2`, write `W(x, y) = w1 |x| + w2 |y|`.

If `w1 = w2 = w`, then `W(x, y) = w A(x, y)`, and swapping coordinates leaves `W` unchanged.

If `W` is unchanged by a coordinate swap for every integer pair, evaluate `(1, 0)` and `(0, 1)`. Those two values are `w1` and `w2`, so `w1 = w2`.

Thus swap invariance for every integer pair holds exactly when the two weights are equal.

The unequal weights `1` and `2` give `W(1, 0) = 1` and `W(0, 1) = 2`.

## Equal squared length

`3 * 3 + 4 * 4 = 25` and `5 * 5 + 0 * 0 = 25`. The aggregates are `A(3, 4) = 7` and `A(5, 0) = 5`. Equal squared length does not force equal aggregate on this pair.

## What is proved

Sign invariance, swap invariance, and signed-permutation invariance of `A`. Edge additivity. Absolute homogeneity. The eight images of `(1, 2)` and their distinctness, hence separation of the eight maps by that vector. The swap criterion for two natural weights, the equal-weight scaling identity, the axis values `1` and `2`, and the squared-length split `25`, `7`, and `5`.

## What is assumed

Coordinates are integers. The absolute value is the usual one on the integers. Weights are natural numbers. A signed permutation is one of the eight bit choices above. AuthorityEffect is None. No package beyond the integer axioms used by the Lean kernel is imported.

## What is open

A faithful, edge-additive, maximal bounded-linear symmetry on a general gauge presentation stays open. Weighted `l1` as the outer aggregation of that symmetry stays open. Route `L1-R-GS001` from `L1-OBSERVER-AXIOMS-H1-H5` stays a gap. The conditional norming package in `gs001_maximal_symmetry_direction_independence_and_gauge_proportionality` stays a hypothesis package.
