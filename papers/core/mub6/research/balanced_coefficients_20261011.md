# Exact coefficients for the 320-coordinate quartet model

AuthorityEffect: None.

The balanced model now has a complete exact coefficient export and checked
coefficient semantics. The generated literal Lean table still needs a completed
kernel build. Its smaller coordinate count
comes with denser equations. No global exclusion, quartet witness or solver
performance result follows from this export.

## Formal connection

`MubBalancedIndices.lean` numbers every reduced real coordinate exactly once
from 0 through 319. Coordinates 0–169 retain the previous matrix-entry
numbering; the three free transition cores occupy 50 coordinates each, with
real and imaginary components alternating in row-major order.

`MubBalancedCoefficients.lean` constructs the affine replacement lists and
substitutes them into every original coefficient row. Its
`equation_coefficients_polynomial` theorem identifies the resulting lists with
the renamed reduced polynomials. Sorting, collection and cancellation are
covered by the existing exact coefficient-algebra proofs. Lookup of an old
coordinate is checked by `oldCoordinate_code`; no coordinate is omitted from
the complete old enumeration.

`MubBalancedCodedSystem.lean` transports the bounded solution predicate to
`Fin 320`, with a checked `exists_quartet_iff_coded` equivalence. The generated
`MubBalancedTable.lean` contains proposed `decide +kernel` row checks and an
`exists_quartet_iff_table` theorem. Its full build was stopped while still
running to honor the instruction to commit, push, open a PR, then stop.
The literal-table theorem and literal bounds are therefore unverified in this
checkpoint. The proposed bounds are
`[-1,1]^170 × [-10035/4096,10035/4096]^150`.

The three completed proof modules display 18 verified endpoints using only
standard axioms. The six displayed literal-table endpoints remain unverified.
Source copies, completed scoped build, axiom reports, interrupted table build
and pinned dependencies are recorded in
`artifacts/mub6_balanced_coefficients_20261011_receipt.json`. JSON parsing and
the SHA-256 byte binding remain outside the Lean kernel.

## Export and density evidence

`MubBalancedExport.lean` computes the exact rational lists and compares each
of 648 rows at four rational assignments with direct rational complex matrix
arithmetic. The matrix check reconstructs transition entries from the free
cores without evaluating the coefficient lists. These 2,592 comparisons
are finite implementation checks; the general polynomial meaning comes from
the formal bridge above. Two full exports have identical bytes.

| Quantity | Previous model | Balanced model |
|---|---:|---:|
| Real coordinates | 386 | 320 |
| Indexed equations | 648 | 648 |
| Total sparse monomials | 4,920 | 8,313 |
| Largest row | 12 | 676 |
| Unit-entry terms | 255 | 255 |
| Matrix-Gram terms | 1,977 | 1,977 |
| Transition-graph terms | 2,364 | 2,748 |
| Transition-norm terms | 324 | 3,333 |
| Empty rows retained | 42 | 42 |
| JSONL bytes | 169,800 | 230,013 |

The first 324 exported rows, including their probe values, are identical.
The size comparison is in `artifacts/balanced_quadratic_density_20261011.json`.
The reduced JSONL has SHA-256
`cb552359467ede318508279b62b7203e65b3c510abf77b5492d3d3f4a49c217d`.

The completed corner has 25 free complex summands. Expanding its squared norm
creates the largest rows; all 66 eliminated real coordinates do not translate
into a smaller sparse-polynomial workload. A runtime or contraction-strength
comparison has not been performed.

## Falsification checks and search consequence

Replacing corner norm equation 575 by an empty list is rejected by the direct
matrix comparison at the all-zero assignment: the actual residual is
`(-24)^2 - 6 = 570`. A separate positive kernel check establishes that this
coefficient list is nonempty. Failed initial elaborations and inconclusive
reduction diagnostics are retained and are not counted as negative controls.

The existing native inspector still consumes the original 386-coordinate
table and has not changed. The coefficient-size evidence favors comparing a
factored affine-completion contractor with the existing representation before
using the expanded reduced table for search. Any comparison must preserve
solutions and account for the fact that an arbitrary reduced-box point can
expand outside the old box; reconstructed bounds require the equations.
Neither representation currently has a complete exclusion cover.

Reproduce the scoped checks from the canonical Lean package:

```powershell
$env:LEAN_NUM_THREADS = '1'
lake build +MubBalancedTable:olean +MubBalancedExport:olean
lake env lean --run MubBalancedExport.lean <fresh-output.jsonl>
```

That export command is the checkpoint command. Root `main` was later removed
from the exporter libraries, because Lean rejects `Mub6.lean` when two imported
modules both declare it. The current wrapper is
`lean4/MubBalancedExport.lean`. The 320 bound pairs are the same two runs,
written with `List.replicate`. `bounds_match` is still `decide +kernel` and
was not replayed.

Format the exported rows with `scripts/reflect_balanced_quadratic.py`, then
compile the generated table to check its equality. Merely formatting or
hashing it does not establish the equality. No whole-package Lean build or
new Rust execution is reported by this checkpoint. PR #779 subsequently merged the entrypoint separation. Full literal-table
verification remains incomplete.


## Closure at the user request

PR #779 merged the separation of all three exporter `main` functions into
standalone `cli/` wrappers. The final follow-up changes the generated row
checks to substitute into `MUB.QuadraticLiftTable.rows`, using
`QuadraticLiftTable.rows_match` as the semantic bridge. Literal coefficient
rows, compact bounds and coefficient JSONL bytes are preserved.

The full library build was stopped at the user's instruction to merge and
stop. It had progressed through inherited reflection modules, but the final
`Mub6` import, axiom-audit entrypoint and complete balanced-table replay were
not reached. The new proof route remains unverified. The source-preservation
checks, exact regeneration and targeted Python lint passed; these checks do
not replace Lean kernel verification. The interrupted run and source hashes
are recorded in `artifacts/mub6_entrypoints_20261011_receipt.json`.

Global quartet exclusion and `N(6)=3` remain open. MUB work is stopped at the
user's request.
