Status: AI-drafted, awaiting human review.

# CQFT-LOCAL-NET-AXIOMS-IMPORT

AuthorityEffect: None.

The continuum local net stays an import. The calculation below is one
four-point strict order and four integer matrices. It does not import
`CausalOrder.lean` and it does not construct a net on continuum regions or a
Minkowski light cone.

## Four-point order

The carrier is the set `{0, 1, 2, 3}`. The only strict relations are

```
0 < 2, 1 < 2, 1 < 3.
```

No element is related to itself. If `x < y` and `y < z`, then `x < z`: every
triple drawn from these four indices satisfies that implication, because the
three relations have no composable pair. Among the six unordered pairs, the
spacelike pairs (distinct, and unrelated in either direction) are

```
{0, 1}, {0, 3}, {2, 3}.
```

The pairs `{0, 2}`, `{1, 2}` and `{1, 3}` are not spacelike. Spacelike
separation on this order is symmetric: each of the three pairs is spacelike
when read in either order.

## Integer matrices

Write matrices as rows. Let

```
I = [[1, 0], [0, 1]],
X = [[0, 1], [1, 0]],
Z = [[1, 0], [0, -1]],
A = [[1, 2], [3, 4]],
B = [[5, 6], [7, 8]].
```

Left or right multiplication by `I` returns each of `A`, `B`, `X` and `Z`.
The products are

```
XZ = [[0, -1], [1, 0]],  ZX = [[0, 1], [-1, 0]],
```

so `XZ + ZX` is the zero matrix and `XZ` is not `ZX`. Transpose is an
involution on `A`, and `(AB)^T = B^T A^T`. The determinants are

```
det A = -2,  det B = -2,  det X = -1,  det Z = -1.
```

The Kronecker product `A ⊗ B` is the 4×4 integer matrix whose sixteen entries
sum to 260. Its corners are 5 and 32. Embedding `A` on the first factor and
`B` on the second,

```
(A ⊗ I)(I ⊗ B) = (I ⊗ B)(A ⊗ I) = A ⊗ B.
```

The same-site embeddings do not commute. The `(0, 2)` entry of `(X ⊗ I)(Z ⊗ I)`
is `-1`, and the `(0, 2)` entry of `(Z ⊗ I)(X ⊗ I)` is `1`.

## What is proved

In `lean4/CampaignCqftLocalNetAxiomsImport.lean`:

- `n_poset_pair_counts` records irreflexivity, the 64-triple scan, exactly
  three relations, exactly three spacelike unordered pairs, and the flags
  named above.
- `disjoint_site_products` records that the two disjoint-site products equal
  `A ⊗ B` and that the entry sum is 260.
- `same_site_and_star` records the zero anticommutator, the unequal same-site
  products and their `(0, 2)` entries, the unit laws on the four matrices,
  the transpose identity for `A` and `B`, and the four determinants.

The independent check recomputes the same counts and products.

## What is assumed

The four indices, the three relations, and the four matrices are supplied.
Spacelike means distinct and unrelated in either direction. Matrix product,
Kronecker product, transpose and determinant are the integer operations
written in the module. Nothing is taken from `CausalOrder.lean`.

## What is open

A spacetime with a causal order, and a family of unital star-algebras
indexed by continuum regions with isotony and spacelike commutation, stay
imported. A Minkowski light cone stays imported. The external light-cone
lift recorded at `DS-QM033-064-074-083-QHELD-CONTINUUM` is not discharged.
The relation of observer axiom H1 to Einstein causality is not established.
The node status stays `IMPORTED_ASSUMPTION`.
