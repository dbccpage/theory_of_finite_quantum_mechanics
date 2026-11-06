# Bounded quartet expression semantics, degree and coefficient expansion

AuthorityEffect: None.

This checkpoint follows the [152-coordinate polynomial reduction](bounded_polynomials_20261011.md).
The receipt is
[`mub6_bounded_expressions_20261011_receipt.json`](../artifacts/mub6_bounded_expressions_20261011_receipt.json).
Global quartet exclusion and `N(6)=3` remain open.

## Checked expression semantics

`MubBoundedExpressions.lean` constructs executable arithmetic expressions
using rational constants, the actual `Coord` variables, addition,
multiplication and negation. A pair of real expressions carries complex
arithmetic. The checked translation preserves multiplication and conjugation,
both finite matrix products, the explicit 3-by-3 determinant and all nine
adjugate entries. In particular, the cofactor signs and the conjugated
determinant denominator are retained.

The definitions `eE,eB,eC,eU,eV,eQ,eN,eS` translate to the polynomial objects
from the preceding checkpoint. `expression_polynomial` checks every indexed
equation without changing the 152-coordinate domain, 396 constraints or
positive determinant bound. `evalReal_polynomial` holds for every real
assignment; `eval_rational` relates exact rational execution to real evaluation.

`ExpressionSolution` includes all equation evaluations and `q >= 54/5`.
`exists_quartet_iff_expressions` identifies actual normalized quartet
existence with an expression solution in the closed box `[-1,1]^152`.
`no_quartet_iff_no_expressions` checks the corresponding universal negation.
Neither theorem establishes absence of solutions.

## Degree bounds

`Expr.degree` is an executable syntactic upper bound: constants have bound
zero, coordinates one, addition takes the maximum, multiplication adds,
and negation leaves the bound unchanged. Structural induction proves
`polynomial_degree` for every expression. Ordinary kernel-checked `decide`
checks the finite expression bounds; `native_decide` is not used.

The resulting theorems are:

| Polynomial family | Checked upper bound |
|---|---:|
| Every one of the 396 indexed equations | 8 |
| Determinant norm-square q | 4 |

These are upper bounds. Polynomial cancellation may lower a degree; sharpness
and constraint independence are not asserted.

## Finite coefficient representation

`MubBoundedCoefficientExpansion.lean` expands each expression into a finite
list of pairs `(rational coefficient, list of coordinate factors)`.
Multiplication concatenates factor lists and distributes over the term lists.
The representation permits duplicate monomials and zero coefficients.

`expansion_polynomial` identifies that list with the interpreted polynomial
for every expression. `equation_expansion` and `determinant_expansion`
specialize the identity to every bounded quartet equation and to `q`.
The factor-count theorems bound each term by eight factors for equations and
four for `q`. This is an exact coefficient representation, without a claim
that a complete external coefficient file has been produced or reflected.

## Verification and remaining obligation

The two canonical targets and their exact local import closure passed the
pinned Lean 4.33.1 replay. The 14 expression and six expansion endpoints
report only `propext`, `Classical.choice`, and `Quot.sound`. The receipt binds
source bytes, dependencies and logs. No whole-package build is claimed.

A cofactor-sign mutation in adjugate entry `(0,1)` is rejected at
`translate_adjugate`: the false residual would require a general product to
equal its negative. This is one targeted mutation, not a complete audit.

Four exact rational execution probes compare the interpreted expression
with its finite coefficient expansion. The final probe uses a tail-recursive
sum and discards terms whose rational coefficient is exactly zero:

| Probe | Expression degree | Raw terms | Nonzero terms before collection |
|---|---:|---:|---:|
| Determinant norm-square | 4 | 1,152 | 288 |
| Free unit-entry equation | 2 | 3 | 3 |
| Numerator norm equation | 6 | 58,274 | 6,560 |
| Scaled MU equation | 8 | 3,396,770 | 394,560 |

All four exact evaluation comparisons pass. An earlier probe evaluated the
full raw list with a right fold and exhausted Lean's interpreter stack on
the MU example; its exit-one log is retained. That failure concerns raw-list
execution, not the polynomial identities. The probes are not a complete
native export or a kernel-reflected coefficient file. The measured growth
supports collecting duplicate terms during export instead of retaining the
full raw expansion.

Replay from `lean4/research_programs/mub6`:

```powershell
$env:LEAN_NUM_THREADS = '1'
lake build +MubBoundedExpressions:olean +MubBoundedCoefficientExpansion:olean
```

Complete export requires explicit coordinate/equation coding and a complete
serialized artifact whose native interpretation is tied to these definitions.
Term collection should preserve the polynomial identity while avoiding the
cost of retaining zero terms and duplicate monomials. Exact contractor or
algebraic-certificate work must retain the determinant inequality and all
three MU relations. The central obligation remains infeasibility on the
whole bounded real domain, or an exact quartet witness. No numerical grid,
finite probe, unresolved box collection or degree bound discharges it.

## Subsequent numbered coefficient checkpoint

The [complete numbered coefficient system](bounded_export_20261011.md) adds
checked index coverage, polynomial-preserving term collection and the
`Fin 152` existence equivalence. Its receipt separately records the complete
native export. This earlier receipt remains unchanged; neither checkpoint
establishes global infeasibility or kernel reflection of serialized bytes.
