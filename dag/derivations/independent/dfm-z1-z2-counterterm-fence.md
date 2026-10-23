Status: AI-drafted, awaiting human review.

# DFM-Z1-Z2-COUNTERTERM-FENCE

AuthorityEffect: None.

The cited replay returns the constant 1 for a counterterm ratio and does not
evaluate a Dirac contraction. This note records a finite matrix identity at
one rational momentum. It does not derive Z_1/Z_2 = 1.

## Matrices

Indices start at 0. The Dirac matrices in M_4(Q(i)) are the usual chiral
representation used by the dossier replay: g0 = diag(1, 1, -1, -1), g1 has
ones at (0,3) and (1,2) and minus ones at (2,1) and (3,0), g2 is the same
pattern with i and -i, and g3 has ones at (0,2) and (3,1) and minus ones at
(1,3) and (2,0). For an integer vector v,

```
slash(v) = v0 g0 - v1 g1 - v2 g2 - v3 g3.
```

The inverse propagator at mass m is slash(v) - m I. For every integer
momentum pair and every integer mass,

```
(slash(p+q) - m I) - (slash(p) - m I) = slash(q).
```

At p = (2, 0, 0, 0), q = (1, 0, 0, 1) and m = 1, the Minkowski squares give
denominators 3 and 7. The propagators are

```
S(p) = (slash(p) + I) / 3
S(p+q) = (slash(p+q) + I) / 7.
```

Both denominators are nonzero. The sandwiched identity

```
S(p+q) slash(q) S(p) = S(p) - S(p+q)
```

holds in M_4(Q(i)). The loop momentum in this check is 0, so these are the
integrand matrices at that point. Lowering the external index by
eta = diag(1, -1, -1, -1), the contraction q_mu I_Lambda^mu equals

```
I_Sigma(p) - I_Sigma(p+q),
```

where I_Sigma(v) = sum_nu g^nu S(v) (eta_nu g^nu). The common value has
nonzero entries 2/7 at (0,0), (1,1) and (2,0), -2/7 at (0,2), 2/7 at (1,3),
26/21 at (2,2) and (3,3), and -2/7 at (3,1). Every imaginary part on this
matrix is 0.

## What is proved

In `lean4/CampaignDfmZ1Z2CountertermFence.lean`:

- `inverse_difference` is the inverse-propagator identity for every integer
  momentum pair and every integer mass.
- `propagator_values` identifies S(p), S(p+q) and slash(q) with those
  formulas at the stated integers.
- `sandwich` is S(p+q) slash(q) S(p) = S(p) - S(p+q).
- `contraction` identifies the lowered vertex contraction with the Dirac
  adjoint difference of the two propagators.
- `contraction_entries` identifies that contraction with the witness matrix
  above.

The independent check recomputes the same products in Q(i).

## What is assumed

The Dirac matrices are the representation written above. Matrix
multiplication and the Minkowski lowering eta are the usual ones. The
numerator sum that builds a product keeps a shared denominator; the equality
proofs compare that operation with the propagator formulas and the witness.

## What is open

No loop integral is taken. No gauge-invariant subtraction scheme is fixed.
The equality Z_1/Z_2 = 1 is not proved, and the constant 1 returned by the
older replay is not this calculation. The node status stays OPEN.
