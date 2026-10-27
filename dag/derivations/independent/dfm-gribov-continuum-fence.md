Status: AI-drafted, awaiting human review.

# DFM-GRIBOV-CONTINUUM-FENCE

AuthorityEffect: None.

One quadratic form on a single generator does not fix the value on every
generator. This note keeps the matrix calculation and records both forms for
the same diagonal matrix.

## Matrices

Let `I = diag(1, 1, 1)` and `Ω1 = diag(1, -1, -1)`. Let `H23` be the matrix
with ones in positions `(2,3)` and `(3,2)` and zeros elsewhere, and let `H12`
be the matrix with ones in positions `(1,2)` and `(2,1)`. Indices here start
at 1. Then

```
H23^2 = diag(0, 1, 1)
H12^2 = diag(1, 1, 0)
```

Hence

```
Tr(I H23^2) = 2
Tr(Ω1 H23^2) = -2
Tr(Ω1 H12^2) = 0
```

The same matrix `Ω1` gives a negative value on `H23` and zero on `H12`.
Also `Ω1^2 = I`, the product of its diagonal entries is `1`, `Tr(I) = 3`,
and `Tr(Ω1) = -1`.

## What is proved

In `lean4/DressingFieldGribovContinuumFence.lean`:

- `h23_square` and `h12_square` are the two squares.
- `omega1_square_and_det` records `Ω1^2 = I`, the diagonal product `1`, and
  the traces `3` and `-1`.
- `trace_pair` records the three quadratic values `2`, `-2`, and `0`.
- `forms_differ` records that `-2` and `0` are unequal.

The independent check recomputes the same products and traces.

## What is assumed

The entries lie in `Q`. Multiplication is the usual matrix product, and the
trace is the sum of the diagonal entries. The two generators are the matrices
written above.

## What is open

The continuum Gribov-Singer obstruction, the spectrum of a Faddeev-Popov
operator, ghost-free quantization, and a Yang-Mills mass gap stay open. The
node status stays OPEN.
