# Bounded quartet coordinates and rational polynomial semantics

AuthorityEffect: None.

This checkpoint extends the
[bounded block equations](bounded_quartet_equations_20261011.md).
Its receipt is
[`mub6_bounded_polynomials_20261011_receipt.json`](../artifacts/mub6_bounded_polynomials_20261011_receipt.json).
It does not establish `N(6)=3` or supply a quartet.

## Exact coordinate domain

`MubBoundedCoordinates.lean` assigns two real coordinates to each unfixed
complex entry. The free entries are:

| Matrix | Free entries | Real coordinates |
|---|---:|---:|
| E, excluding its first row and column | 4 | 8 |
| B, excluding its first row | 6 | 12 |
| C, excluding its first column | 6 | 12 |
| U, excluding its first row | 30 | 60 |
| V, excluding its first row | 30 | 60 |
| Total | 76 | 152 |

`coordinate_count` checks the cardinality of the actual coordinate type.
`decodeE_encode` through `decodeV_encode` recover each matrix under precisely
its gauge hypotheses; `encode_decode` recovers every real coordinate vector.
`decode_gauges` establishes the substituted constants. `encode_system` retains
all fields of `QuartetEquations`, including all three MU relations.
`system_inBox` puts every solution in the closed box `[-1,1]^152`; the unit
circle equations remain imposed. This is an ambient coordinate count, not
the dimension of the solution set.

## Polynomial carrier and equations

`MubBoundedPolynomials.lean` uses
`Poly := MvPolynomial Coord ℚ` and
`CPoly := QuadraticAlgebra Poly (-1) 0`.
The latter has the complex multiplication law with formal generator squared
equal to minus one. Its `re` and `im` fields are rational polynomials.
`complexEval` is a ring homomorphism to the actual complex numbers, obtained
by evaluating each real polynomial at an arbitrary real coordinate vector.
The checked star and norm-square lemmas preserve conjugation and squared
modulus. Matrix multiplication, determinant and adjugate evaluation use the
actual ring-homomorphism laws.

The polynomial matrices `pE,pB,pC,pU,pV` evaluate to the five decoded matrices.
`pQ` evaluates to `q = |det B|^2`; `pD` evaluates to the conjugate of `det B`;
`pN` and `pS` evaluate to the previously checked numerator and scaled
completion. `equationPolynomial` indexes the following actual polynomials:

| Group | Indexed real equalities |
|---|---:|
| Unit entries of E, B, C | 27 |
| Numerator entry norm-square equals q | 9 |
| Unit entries of U, V | 72 |
| S-U, S-V, U-V squared overlaps | 108 |
| Top and bottom 3-by-3 Gram equations, real and imaginary parts | 36 |
| U and V 6-by-6 Gram equations, real and imaginary parts | 144 |
| Total | 396 |

`equation_count` checks this cardinality. Some indexed equations are
redundant or constant; independence is not asserted. `Solution` includes
every equation and the separate rational inequality `q >= 54/5`.
`solution_iff_polynomialSystem` checks the indexing; the matrix-level
semantic equivalence is `polynomialSystem_iff_coordinates`.

The final endpoints are:

```text
exists_quartet_iff_polynomials:
  (exists actual normalized quartet in C6)
    iff (exists r, Solution r and InBox r)

no_quartet_iff_no_polynomials:
  (no actual normalized quartet in C6)
    iff (every r in the box fails Solution)
```

Neither endpoint asserts the right side of the second equivalence. The
quantification is over all real coordinates, not a finite grid or a fixed
Hadamard family.

## Verification and limits

The canonical Lean 4.33.1 replay checks 13 coordinate and 26 polynomial
endpoints with only `propext`, `Classical.choice`, and `Quot.sound`.
The receipt binds the two source modules, their exact local import closure,
the pinned Mathlib and other dependencies, and the successful logs. This is
a targeted build, not a full `Mub6` build.

An isolated negative control changes only the indexed U-V MU target from
`6` to `6*q`, retaining the semantic bridge. Lean rejects the mismatch in
both directions of that bridge. This is one targeted mutation, not a
complete mutation audit.

Replay from `lean4/research_programs/mub6`:

```powershell
$env:LEAN_NUM_THREADS = '1'
lake build +MubBoundedCoordinates:olean +MubBoundedPolynomials:olean
```

The subsequent [expression and expansion checkpoint](bounded_expressions_20261011.md)
checks the expression semantics, upper degree bounds, and finite coefficient
representation. A complete serialized export with native parity and an exact
solver or certificate tied to these polynomials remain needed. The central
mathematical obligation remains global infeasibility of this bounded
semialgebraic system, or an exact solution producing a quartet. No native
complete export, successful contractor, finite-fibre assertion for this chart,
whole-domain cover, publication, deposit or authority promotion is claimed.
