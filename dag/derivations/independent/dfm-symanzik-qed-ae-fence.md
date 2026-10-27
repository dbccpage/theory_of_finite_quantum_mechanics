Status: AI-drafted, awaiting human review.

# DFM-SYMANZIK-QED-AE-FENCE

AuthorityEffect: None.

The five edges below are the replay's diamond edge order. The cotree sum is an
integer calculation on those edges. It is not an enclosure of a QED series.

## Edges and cotrees

Vertices are `{0, 1, 2, 3}`. Edges, in order, are

```
e0 = (0, 1), e1 = (0, 2), e2 = (1, 3), e3 = (2, 3), e4 = (1, 2).
```

A mask records which of these five edges are kept. Among the integers from 0
through 31, exactly ten have three bits set in positions 0 through 4:

```
7, 11, 13, 14, 19, 21, 22, 25, 26, 28.
```

Eight of them have one connected component:

```
7, 11, 13, 14, 21, 22, 25, 26.
```

The masks 19 and 28 have two components. For a kept-edge mask, the cotree
product is the product of the weights on the bits that are off. At weights
`2, 3, 5, 7, 11` the eight connected cotree products sum to 247. At weights
`1, 1, 1, 1, 1` the same sum is 8.

## What is proved

In `lean4/DressingFieldSymanzikQedAeFence.lean`:

- `component_counts` records one component on the eight masks and two
  components on 19 and 28.
- `three_bit_masks_are_listed` records that every three-bit mask below 32 is
  one of the ten listed masks.
- `cotree_sums` records the sums 247 and 8.

The independent check recomputes the same masks and sums.

## What is assumed

The five edges and the five weights are supplied. A component is the result of
the three-step parent-pointer calculation written in the Lean module.

## What is open

A rational interval around a 1-to-4-loop QED anomalous-moment series stays
open. Continuum Feynman-parameter integrals stay open. The node status stays
OPEN.
