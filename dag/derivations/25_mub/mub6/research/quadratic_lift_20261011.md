# Full matrix and transition lift for the quartet problem

AuthorityEffect: None.

An actual quartet in dimension six exists if and only if the new system of
648 rational polynomial equalities has a real solution in its declared box.
There are 386 ambient real coordinates, and every polynomial has total degree
at most two. This is a checked reformulation; it does not establish either
infeasibility or an exact quartet witness. `N(6)=3` remains open.

The receipt is [`mub6_quadratic_lift_20261011_receipt.json`](../artifacts/mub6_quadratic_lift_20261011_receipt.json).
The subsequent [coefficient checkpoint](quadratic_coefficients_20261011.md)
adds the native table and its checked literal representation; the receipt
linked here continues to describe the preceding derivation checkpoint.

## Coordinates and equations

Retain the 152 coordinates of `MubBoundedCoordinates` for the gauge-fixed
blocks E, B, C and the two additional bases U, V. Add the nine complex entries
of D and all 108 complex entries of three transition matrices W. Thus

\[
152+2(9)+2(3\cdot36)=386,\qquad H=\begin{pmatrix}E&B\\C&D\end{pmatrix}.
\]

The additional transition matrices satisfy the graph equations

\[
W_0=H^*U,\qquad W_1=H^*V,\qquad W_2=U^*V.
\]

| Indexed equations | Count | Polynomial degree bound |
|---|---:|---:|
| Unit entry norms in H, U, V | 108 | 2 |
| Real and imaginary parts of the three Gram equations | 216 | 2 |
| Real and imaginary parts of the transition graph equations | 216 | 2 |
| Entry norms of W equal to six | 108 | 2 |
| Total | 648 | 2 |

All three Gram equations have the form `A* A = 6 I`. Redundant equations
and gauge constants are retained; these counts assert neither independence
nor the dimension of the solution set. The 170 matrix-entry coordinates lie
in `[-1,1]`, and the 216 transition coordinates lie in `[-3,3]`. The latter
bound follows from `re(z)^2 + im(z)^2 = 6`. Both boxes include their boundary.

## Coverage, soundness and degree

`MubQuadraticLift.exists_quartet_iff_lift` proves the matrix-level existence
equivalence. Forward coverage uses the checked bounded chart, restores its
actual D block and records its three actual transitions. Reverse soundness
checks H, U, V as full complex Hadamard matrices and obtains all three MU
conditions from the graph and norm equations. It then constructs an actual
quartet using the existing index and normalization transport.

`MubQuadraticLiftPolynomials` represents every equation in
`MvPolynomial Coord Q`. Complex arithmetic is the quadratic algebra with
generator squared equal to minus one. `solution_iff_system` checks the entire
indexed system against the matrix specification, and
`exists_quartet_iff_quadratic_solution` retains actual quartet existence on
the box. In particular, the overlap variables cannot be chosen independently
of the bases.

`MubQuadraticLiftDegree.equation_degree` bounds the total degree of those
actual polynomials by two. Matrix entries are affine; Gram products and
transitions are bilinear. The proof handles conjugation, finite sums, real
and imaginary components, and squared norms in the polynomial algebra.

The new model uses no inverse or determinant division in its defining
equations. Its soundness therefore does not require an invertible B block.
This does **not** remove the `q >= 54/5` condition from the earlier
152-coordinate reconstruction or its cancellation argument. Those older
models and their artifacts remain unchanged. No pointwise equivalence with
the older coordinates at a singular B is asserted.

## Validation and next obligation

The three new modules and their 28-module local import closure passed the
pinned Lean 4.33.1 replay. All 28 displayed endpoints use only `propext`,
`Classical.choice` and `Quot.sound`. This is a scoped build, not a replay of
the whole `Mub6` aggregate.

The overlap norm residual at the zero coordinate assignment is formally
evaluated as minus six, so the zero assignment is not a solution. A negative
probe falsely requiring that residual to be zero is rejected after rewriting
by the checked value. That check concerns this residual, not global exclusion.

From `lean4/research_programs/mub6`, replay with:

```powershell
$env:LEAN_NUM_THREADS = '1'
lake build +MubQuadraticLiftDegree:olean
```

No native coefficient table, solver run, finite cover, or infeasibility
certificate for this new formulation is supplied here. Existing coefficient
files describe the earlier formulation and cannot be substituted for this
one. A useful next step is a checked coefficient representation and exact
contraction or algebraic obstruction for these quadratics. Ultimately every
real solution must be excluded, or an exact quartet must be constructed.
