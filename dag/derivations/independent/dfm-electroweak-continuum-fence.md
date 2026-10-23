Status: AI-drafted, awaiting human review.

# DFM-ELECTROWEAK-CONTINUUM-FENCE

AuthorityEffect: None.

The dossier writes a residual hypercharge law for a normalized dressing
`u(Φ) = (1/v) U(Φ)`, with

```
U(Φ) = [[conj φ2, φ1], [-conj φ1, φ2]],
```

and claims `u(e^{iα/2} Φ) = u(Φ) diag(e^{-iα/2}, e^{iα/2})`. The phase
`e^{iα/2}` is not an element of `Q(i)` for a generic rational angle. This note
keeps the identity inside `Q(i)` and separates the shared denominator from
each doublet's own norm root.

## Algebra

Write `z = a + bi` and `w = c + di` in `Q(i)`. Multiplication

```
zw = (ac - bd) + (ad + bc)i
```

is commutative, and `conj(zw) = conj(z) conj(w)`. The squared modulus
`a^2 + b^2` is multiplicative. For the lower-left pattern
`negConj(w) = -conj(w)`,

```
negConj(zw) = negConj(w) conj(z).
```

Let `Φ = (φ1, φ2)`. Scaling the doublet by `z` replaces `(φ1, φ2)` with
`(z φ1, z φ2)`. The four entries of `U(zΦ)` are then

```
conj(z φ2) = conj(φ2) conj(z),
z φ1 = φ1 z,
negConj(z φ1) = negConj(φ1) conj(z),
z φ2 = φ2 z.
```

That is `U(zΦ) = U(Φ) diag(conj z, z)`, with no hypothesis on the modulus of `z`.
Dividing every entry by one and the same rational `s` preserves the equality,
because `(xy)/s = (x/s) y` in `Q`.

The squared norm of `zΦ` is `(a^2 + b^2)` times the squared norm of `Φ`.
If `a^2 + b^2 = 1` and a rational `s` satisfies `s * s` equal to the squared
norm of `Φ`, the same `s` is a square root of the squared norm of `zΦ`. The
normalized dressings, each divided by that `s`, obey the same diagonal law.

If the modulus is not 1, the two squared norms differ whenever the original
squared norm is nonzero. Using each doublet's own rational square root as the
denominator is a different normalization. On `Φ = (1, 0)` and `z = 2`, the
squared norms are `1` and `4`, the roots `1` and `2` satisfy `1*1 = 1` and
`2*2 = 4`. The `(1, 2)` entry of `U(2Phi)/2` is `1`, whereas that of
`(U(Phi)/1) diag(2,2)` is `2`. These are the two sides of the proposed
covariance law, not two separately normalized doublets. Dividing both
matrices by the shared denominator `1` still matches, so the failure is the
change of root, not the un-normalized multiplication.

The unit witness `z = 3/5 + (4/5)i` has squared modulus `9/25 + 16/25 = 1`.
On `Φ = (1, 0)` with `s = 1`, the normalized `(1, 2)` entry is `z` itself.

## Checked normalization and phase action

The repaired Normalization API validates a supplied rational scale before
constructing an Input. Its three typed failures distinguish zero doublet norm,
nonpositive scale and a mismatched square. Success is equivalent to the two
conditions 0 < s and s*s = v2(phi), and the successful value preserves the
original doublet and scale. It does not compute a rational square root.

Dividing the two components by s gives a UnitDoublet with proved squared norm
one. UnitPhase carries a Gaussian rational with squared modulus one. Its action
preserves unit doublets, its multiplication composes phases, and the action
composition law is proved. Acting on a checked Input preserves the same positive
scale. Normalizing then acting agrees with acting then normalizing; the matrix
covariance theorem is a client of these validated types.

The original low-level covariance equality still uses total rational division
and permits s=0. The new checked API refuses that normalization case. Neither
layer exports a determinant/unitarity theorem or continuum gauge fields.

The independent exact checker uses nine doublets obtained from three rational
examples at three positive scales. Eight rational unit phases give 72 covariance
and 576 composition cases. Ten invalid normalization/action inputs are refused,
including distinct failure classes and bool/float/text scales. Normal and
optimized runs, strict typing and four selected refusal-boundary mutations pass.
These are finite regression checks alongside the general Lean statements.

## What is proved

In `lean4/CampaignDfmElectroweakContinuumFence.lean`:

- `unnormalized_covariance` states `U(zΦ) = U(Φ) diag(conj z, z)` for every
  Gaussian rational `z` and every doublet `Φ`.
- `unit_normalized_covariance` states that when `norm2 z = 1` and `s * s`
  equals the squared norm of `Φ`, dividing by that `s` preserves the identity
  and `s * s` equals the squared norm of `zΦ`.
- `witness_three_fifths` states that `z = 3/5 + (4/5)i` has squared modulus
  `1`, `Φ = (1, 0)` has squared norm `1`, and the normalized `(1, 2)` entry
  at `s = 1` is `z`.
- `nonunit_normalized_entries_differ` states that `z = 2` on the same `Φ`
  has squared norms `1` and `4`, and the own-root `(1, 2)` entries are `1`
  and `2`, hence unequal.

The independent check recomputes one generic sample, the unit witness, the
own-root split, and the shared-denominator match at `z = 2`.

## What is assumed

The carrier is the field `Q(i)` with componentwise addition and the
multiplication above. A normalized dressing is division by a rational `s`
that is supplied in the statement; existence of such an `s` for an arbitrary
positive rational squared norm is not claimed. No continuum derivative, gauge
field, or phase outside `Q(i)` is used.

## What is open

Phases `e^{iα/2}` outside `Q(i)`, the dressed gauge field and its derivative
term, and any continuum electroweak reading, including an Elitzur or
symmetry-breaking reading, stay open. The node status stays OPEN.
