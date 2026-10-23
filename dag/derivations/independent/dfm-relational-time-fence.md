Status: AI-drafted, awaiting human review.

# DFM-RELATIONAL-TIME-FENCE

AuthorityEffect: None.

The finite clock identity is a product of rational matrices. This note records
one step of order 4. It does not supply a continuous-time generator.

## One step

Let

```
U = [[0, -1], [1, 0]]
```

with entries in `Q`. Write `U^0 = I` and `U^{k+1} = U^k U`. Then `U^2 = -I`,
`U^4 = I`, and `U^T U = I`. For each `t` in `{0, 1, 2, 3}`,

```
(U^{t+1})^T U U^t = I.
```

Let `psi = (3/5, 4/5)`. Then `psi · psi = 1`, and
`(U^t)^T (U^t psi) = psi` for each such `t`. The first component of `U psi`
and of `U^2 psi` differs from `3/5`.

## What is proved

In `lean4/CampaignDfmRelationalTimeFence.lean`:

- `step_square_and_order` records `U^2 = -I`, `U^4 = I`, and `U^T U = I`.
- `four_blocks` records the four products `(U^{t+1})^T U U^t = I`.
- `psi_recover` records the norm 1, the four transports back to `psi`, and
  the two inequalities of first components with `3/5`.

The independent check recomputes those matrices and vectors. It also multiplies
the packaged 8 by 8 clock matrices for this same step. The Lean module does
not build that 8 by 8 matrix.

## What is assumed

The entries lie in `Q`. Multiplication and transpose are the usual matrix
operations. The step `U` and the vector `psi` are supplied.

## What is open

A continuous-time reading, a Stone generator, and a Wheeler-DeWitt constraint
stay open. The node status stays OPEN.
