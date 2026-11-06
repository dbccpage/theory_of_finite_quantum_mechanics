# Exact inspection and a smaller box for the quadratic lift

AuthorityEffect: None.

The checked 648-row table now has a native Rust loader and an exact interval
contractor. Its first full-box sweep returns `CONTRACTED_UNRESOLVED_BOX`:
coordinates 0–169 retain `[-1,1]`, while all 216 transition coordinates shrink
from `[-3,3]` to `[-10035/4096,10035/4096]`. Every final equation range still
contains zero. This does not show that the equations have a common zero.

The input remains the 4,920-monomial table with SHA-256
`a8b2dbcbc44d0618bbf0bf36fd2b252d7cc8a03a1168ebf98ecc28010dceed03`.
The loader requires these exact bytes, then validates the schema, complete
numbering, bounds, sorted degree-two monomials, reduced rational strings,
completion counts and all 2,592 recorded probe values. These probe comparisons
re-evaluate the coefficient rows; the separate direct matrix comparisons are
recorded in the earlier coefficient receipt.

## What the contractor does

One ordered sweep encloses each polynomial using exact rational arithmetic.
Repeated factors use a square enclosure: the image of `[-3,3]` under squaring
is `[0,9]`. If a variable occurs only in one linear or square monomial,
`c*x^k + R = 0` requires `x^k` to lie in `-range(R)/c`. Linear isolation
intersects this range with the current coordinate interval. Square isolation
uses twelve rational bisections to obtain an upper bound for the square root
of the nonnegative upper endpoint, and then takes a closed intersection.
Variables occurring elsewhere in the same polynomial are not isolated.

The 108 transition norm rows each give `re^2 + im^2 = 6`. They account for
all 216 strict contractions. The native result records the input and retained
boxes, every equation range, and every tightening with its row and coordinate.
The runtime output and general contractor are not kernel-reflected proofs.

## Independent formal bound

`MubQuadraticLiftNarrowBox.lean` checks the same rational bound directly from
the model. Its seven displayed endpoints passed a scoped Lean 4.33.1 build
using only `propext`, `Classical.choice` and `Quot.sound`.

`transitionRadius_bounds` checks that the new radius is nonnegative, below
three, and has square at least six. `components_of_norm_six` applies it to
both components of each complex transition entry. Numbering and box lemmas
then give `exists_quartet_iff_narrow_table`: actual quartet existence is
equivalent to a common zero of the literal table in this smaller box.
This formal theorem does not depend on trusting the native interval run.

## Replay and limits

From the repository root, with the shared Cargo target directory configured:

```powershell
cargo test -j 1 --manifest-path omega_engine/crates_rs/Cargo.toml `
  -p omega_mub --lib omega_native::mub6_quadratic_lift::tests
cargo run -j 1 --manifest-path omega_engine/crates_rs/Cargo.toml `
  -p omega_mub --bin mub_quadratic_lift -- `
  omega_engine_projects/mub6/artifacts/quadratic_lift_coefficients_20261011.jsonl `
  NEW_OUTPUT.json
```

The CLI refuses an existing output path. The three targeted Rust tests cover
the full table, exclusion of the zero singleton, invalid boxes, byte and
structural mutations, square enclosure, retained known roots, closed boundary
contact and refusal to isolate a variable that occurs in another monomial.
No full-crate or whole-workspace test result is claimed.

The run and source hashes are bound in
`artifacts/mub6_quadratic_native_20261011_receipt.json`; the native output is
`artifacts/quadratic_lift_full_box_20261011.json`.

Global quartet exclusion, a complete cover and an exact quartet witness remain
open. The smaller box is a retained search domain, not an exclusion certificate.
The next useful algebraic strengthening is to derive compatibility identities
among the three transition matrices before using them in an exclusion search.
