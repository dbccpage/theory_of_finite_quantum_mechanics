# Transition compatibility and a regional exclusion

AuthorityEffect: None.

This checkpoint derives coupling equations among the three transition matrices
and uses one consequence to exclude a nondegenerate closed coordinate box.
The full quartet domain remains unresolved. The evidence is bound in
`artifacts/mub6_quadratic_compatibility_20261011_receipt.json`.

## Matrix and polynomial consequences

For the existing model, `W0 = H* U`, `W1 = H* V`, and `W2 = U* V`, where
the star denotes the conjugate transpose. `MubQuadraticLiftCompatibility.lean`
derives the following from `System r`:

- Each transition has both Gram matrices equal to `36 I`.
- `W0 W2 = 6 W1`, `W0* W1 = 6 W2`, and `W1 W2* = 6 W0`.
- Every row and every column of every transition sums to six. This uses
  the common first-row gauge in the decoded matrices.

`MubQuadraticCompatibilityPolynomials.lean` translates these consequences
into 504 real rational polynomial equations: 216 column-Gram components,
216 cycle components, and 72 row/column-sum components. The first two groups
have total degree at most two, and the last group at most one.
`solution_iff_strengthened` retains every original equation and adds these
consequences. `exists_quartet_iff_strengthened_table` preserves actual quartet
existence in the previously narrowed box. No independence claim is made.

These added polynomials are defined and checked in Lean. They have not yet
been exported as a new literal coefficient table. The native change below
implements the derived distance inequality, rather than claiming to evaluate
all 504 added equations.

## A quantitative exclusion criterion

For any columns `i,j`, `MubQuadraticTransitionSeparation.lean` checks

\[
\sum_{k=0}^{5}|(W_0)_{ki}-(W_1)_{kj}|^2
 =72-12\operatorname{Re}(W_2)_{ij}
 \ge \frac{43623}{1024}.
\]

The lower bound follows from the earlier proved component bound
`10035/4096`; it is not a numerical approximation to a square root.
`component_box_exclusion` therefore excludes any region whose rational
upper bound for the left-hand side is strictly below `43623/1024`.
Equality at the threshold is retained.

The example fixes no coordinate. In column zero of both `W0` and `W1`,
every real component lies in `[9/10,11/10]`. The imaginary components lie
in `[11/5,23/10]` on even numbered rows and `[-23/10,-11/5]` on odd rows.
Every other coordinate retains its original full-box interval. All 386
intervals have positive width. These two columns have squared distance at
most `3/10` even before contraction, below the necessary lower bound.

`close_columns_box_excluded` proves a family of such exclusions directly:
real components in `[9/10,11/10]`, and imaginary components within `1/20`
of any common row-dependent centers. The example takes alternating centers
`9/4` and `-9/4`. This formal theorem concerns the stated real-coordinate
conditions; it does not kernel-check JSON parsing or Rust execution.

## Native replay

The Rust inspector now accepts an optional exact box request bound to the
original coefficient hash. After its original sweep, it tests all 36 column
pairs between `W0` and `W1` using exact rational interval differences and
squares. A separation witness records the column indices, twelve component
upper bounds, their total and the proved lower bound. The output schema is
`mub6.quadratic_lift.interval_inspection.v2`.

The example returns `EXCLUDED_BOX`, with no excluding original equation.
All 648 original equation ranges still contain zero after their sweep.
The targeted regression checks that the previous sweep alone does not
exclude this box, whereas the new distance criterion does. The full box
continues to return `CONTRACTED_UNRESOLVED_BOX`.

From the repository root, with the shared Cargo target directory configured:

```powershell
cargo test -j 1 --manifest-path omega_engine/crates_rs/Cargo.toml `
  -p omega_mub --lib omega_native::mub6_quadratic_lift::tests
cargo run -j 1 --manifest-path omega_engine/crates_rs/Cargo.toml `
  -p omega_mub --bin mub_quadratic_lift -- `
  omega_engine_projects/mub6/artifacts/quadratic_lift_coefficients_20261011.jsonl `
  NEW_OUTPUT.json `
  omega_engine_projects/mub6/artifacts/quadratic_lift_close_columns_box_20261011.json
```

Five targeted Rust tests passed, including strict-threshold contact and
invalid-request rejection. The three new Lean modules have 37 displayed
endpoints; all passed scoped replay with only `propext`, `Classical.choice`
and `Quot.sound`. No whole-package Lean build or full Rust suite is claimed.

The example is one region, not a complete cover or an excluded fraction of
the search domain. `N(6)=3`, global quartet exclusion and an exact quartet
witness remain open. A useful next step is to combine these coupling
constraints with a coverage-preserving subdivision or another global bound;
repeating isolated example exclusions would not close that obligation.
