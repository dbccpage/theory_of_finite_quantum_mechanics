Status: AI-drafted, awaiting human review.

# DFM-RELATIONAL-TIME-FENCE

AuthorityEffect: None.

The finite clock identity is a product of rational matrices. This note records
a reusable finite-clock construction and one step of order 4. The group,
links and action are supplied. It does not supply a continuous-time generator.

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

## Arbitrary supplied schedules

Let G be any group and u(t) its time-indexed links. Define F(0)=1 and
F(t+1)=u(t)F(t). A change of frame g gives d(t)=g(t+1)^{-1}u(t)g(t).
Induction with cancellation gives F_d(t)=g(t)^{-1}F(t)g(0).
Taking g=F cancels every interior edge. On a cycle of positive period n,
the last edge returns to frame F(0), not F(n), and its dressed value is F(n).
Thus a periodic frame cancelling every edge exists iff F(n)=1: necessity
follows by conjugating the displayed transport identity; sufficiency uses g=F.
This holds for noncommutative groups as well.

`Clock.validate` rejects zero period as `emptyPeriod` and a nonidentity
holonomy as `nontrivialHolonomy`. Success returns a `ClosedCycle` carrying
positivity and closure proofs. The success iff, returned period, both rejection
paths and roundtrip are proved. `cycleBlock_normal_form` identifies the interior
and closing blocks; `ClosedCycle.blocks` uses the checked closure certificate.
For a supplied group action, `historyEquiv` changes coordinates invertibly at
each time. `evolves_iff` proves covariance in both directions, and `stationary_iff`
identifies transported histories with stationary coordinates. This is a coordinate
change, not disappearance of physical evolution. Constant links specialize to
powers by `frame_constant`. `rotation_apply` connects the generic permutation
client to the original rational matrix; `rationalClock_blocks` instantiates it.

## What is proved

In `lean4/DressingFieldRelationalTimeFence.lean`:

- `step_square_and_order` records `U^2 = -I`, `U^4 = I`, and `U^T U = I`.
- `four_blocks` records the four products `(U^{t+1})^T U U^t = I`.
- `psi_recover` records the norm 1, the four transports back to `psi`, and
  the two inequalities of first components with `3/5`.

The independent check recomputes those matrices and vectors. It enumerates all
S3 schedules of lengths 1 through 4: 6+36+216+1296=1554 schedules, of which
1+6+36+216=259 close and 1295 do not. For each it tests 12 choices of frames
and 3 initial states, all block boundaries, and the periodic obstruction. It
checks 54 constant-step powers (6 steps and 9 exponents), zero-period rejection,
and four incorrect candidate expressions by explicit witnesses. Those witnesses
are not a source mutation campaign; no mutation coverage score is claimed. It also multiplies
the packaged 8 by 8 clock matrices for this same step. The Lean module does
not build that 8 by 8 matrix.

## What is assumed

The entries lie in `Q`. Multiplication and transpose are the usual matrix
operations. The step `U` and the vector `psi` are supplied. The generic API additionally
assumes a group, time-indexed links and (for histories) a group action. Closure
is checked or passed as a proof; invertibility comes from the supplied group.

## What is open

A continuous-time reading, a Stone generator, and a Wheeler-DeWitt constraint
stay open. No arbitrary graph or cohomology group is constructed. The generic
clock result is algebraic and does not derive those supplied structures from
primitive difference. The node status stays OPEN.
