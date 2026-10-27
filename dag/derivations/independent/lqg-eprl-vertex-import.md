Status: AI-drafted, awaiting human review.

# LQG-EPRL-VERTEX-IMPORT

AuthorityEffect: None.

The formulas below are the rational label rules named by the imported
Euclidean and Lorentzian EPRL data. They are not a vertex amplitude.

## Euclidean labels

For a rational `gamma` and a rational `k`, write

```
j+ = |1 + gamma| * k / 2
j- = |1 - gamma| * k / 2
```

If `0 < gamma < 1`, then `|1 + gamma| = 1 + gamma` and `|1 - gamma| = 1 - gamma`, so

```
j+ = (1 + gamma) * k / 2
j- = (1 - gamma) * k / 2
j+ + j- = k
j+ - j- = gamma * k
```

If `gamma > 1`, then `|1 + gamma| = 1 + gamma` and `|1 - gamma| = gamma - 1`, so

```
j+ = (1 + gamma) * k / 2
j- = (gamma - 1) * k / 2
j+ - j- = k
j+ + j- = gamma * k
```

At `gamma = 1/2` and `k = 2`, the labels are `3/2` and `1/2`. Their sum is `2` and their difference is `1`, which is not `2`. At `gamma = 3` and `k = 2`, the labels are `4` and `2`. Their difference is `2` and their sum is `6`, which is not `2`. At `gamma = 1` and `k = 2`, the labels are `2` and `0`, and both the sum and the difference equal `2`. The two strict regimes are therefore not interchangeable, and the boundary `gamma = 1` makes both recoveries hold at once.

## Lorentzian labels

Write

```
n = 2 * k
rho = 2 * gamma * k
```

Then `n / 2 = k` and `rho = gamma * n = 2 * gamma * (n / 2)`. At `gamma = 1/2` and `k = 2`, the pair `(n, rho)` is `(4, 2)`. The index `j = n / 2` is `2`, and `gamma * j` is `1`. Thus `rho` equals `2 * gamma * j`, not `gamma * j`.

## Pair index

The number of unordered pairs among five indices is `5 * 4 / 2 = 10`. That is the count of labels `k_ab` in the imported indexing. It is not a spin-foam amplitude.

## What is proved

In `lean4/LqgEprlVertexImport.lean`:

- `euclidean_below` is the signed form, the sum `k`, and the difference `gamma * k` for every rational `k` when `0 < gamma < 1`.
- `euclidean_above` is the signed form, the difference `k`, and the sum `gamma * k` for every rational `k` when `gamma > 1`.
- `recorded_euclidean_points` records the three points above, including the two failures of the opposite recovery.
- `lorentzian_embedding` is the pair `(2k, 2 gamma k)` and the relations `rho = gamma * n = 2 * gamma * (n / 2)`.
- `lorentzian_half_two` records `(n, rho) = (4, 2)`, `j = 2`, and `gamma * j = 1`.
- `five_tetrahedron_pairs` records that five indices determine 10 unordered pairs.

The independent check recomputes the same points and the two regime identities on a finite list of positive rationals.

## What is assumed

`gamma` and `k` are rationals. The absolute value and the field operations are the rational ones. The three numerical points and the five-index count are supplied data. The identification of these formulas with equations (18)-(20) and (24) of arXiv:0711.0146 is the imported reading recorded by the node; this note does not re-audit the paper.

## What is open

A Spin(4) 15j symbol, a booster contraction, a continuum Lie-group representation, a spin-network boundary space, a sum over spins, a continuum limit, a semiclassical limit, and a cosmological constant stay open. The finite cyclotomic amplitudes named by TFQ-0198 are not identified with an EPRL-FK vertex. The node status stays IMPORTED_ASSUMPTION.
