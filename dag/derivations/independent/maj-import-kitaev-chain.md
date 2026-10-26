Status: AI-drafted, awaiting human review.

# Sweet-spot index labels and two integer comparisons

The imported Kitaev-chain claim names a fermion Hamiltonian, a BdG spectrum, a phase region, and a sweet-spot Majorana form. This note records which bulk indices meet the edge indices, and two integer comparisons of the bound written as mu * mu against (2 * t) * (2 * t).

## Index split

For every natural number L with 2 ≤ L, and every natural number j with 1 ≤ j and j ≤ L - 1, set the bulk indices to 2 * j and 2 * j + 1, and the edge indices to 1 and 2 * L.

Since j ≥ 1, the index 2 * j is at least 2, so it differs from 1. The next index 2 * j + 1 is at least 3, so it differs from 1. Since j ≤ L - 1, the index 2 * j is at most 2 * L - 2, and 2 * j + 1 is at most 2 * L - 1. Both differ from 2 * L.

At L = 2 and j = 1 the bulk indices are 2 * 1 = 2 and 2 * 1 + 1 = 3. The upper edge index is 2 * 2 = 4. Then 2 differs from 1 and from 4, and 3 differs from 1 and from 4.

## Two integer points

For t = 1 and mu = 1, mu * mu = 1 and (2 * t) * (2 * t) = 4, so 1 < 4. The third integer delta = 1 differs from 0.

For t = 1 and mu = 3, mu * mu = 9 and (2 * t) * (2 * t) = 4, so 9 < 4 is false. The third integer delta = 1 still differs from 0.

## What is proved

The index separation for every such L and j, the L = 2 witness, and the two integer comparisons above.

## What is assumed

The ordering and arithmetic of the natural numbers and the integers used in those comparisons.

## What is open

The fermion Hamiltonian, the BdG spectrum, the phase region as a physical claim, and a wire without disorder or trivial subgap states stay imported. The index split does not select a topological phase. The node stays IMPORTED_ASSUMPTION.
