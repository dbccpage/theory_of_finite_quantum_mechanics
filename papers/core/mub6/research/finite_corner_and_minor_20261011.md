# Finite-corner audit and a quantitative minor bound

AuthorityEffect: None. Research checkpoint: 2026-10-11.
Parent checkpoint: `07882113ec818de04b10035fa223ede6d0dd89bf`.
The goal remains active. No quartet exclusion or exact quartet is supplied.

## 1. The external coverage theorem has passed replay

The external source is pinned to commit
`57b03025ecbe259e474281f49e201ea7cb474e34` of
[all_hadamard_matrices_in_dimension_six](https://github.com/mateocardeneswuttig/all_hadamard_matrices_in_dimension_six/tree/57b03025ecbe259e474281f49e201ea7cb474e34).
Its source ZIP has SHA-256
`90b202d4da34649d9a9f3b2c1f7c218b3febbf543e105c18e583e25243a31d5e`.
All 215 extracted source/archive files matched those ZIP bytes. The source
audit found no unfinished proofs or added axioms in the 136 project modules;
all were reachable from the project root. These source checks complement,
and do not replace, the kernel replay.

The public target `Hadamard6.PaperTheorem` completed with Lean
`4.33.0-rc2` and Mathlib `51e6992efd06126df61a496bebf8f49482a4e129`.
The final build reported 3,525 Lake jobs, including cached dependencies.
The separate public audit passed all nine required theorem reports. Those
reports and the additional Karlsson coverage report contain only `propext`,
`Classical.choice`, and `Quot.sound`. The earlier memory failure and its
successful single-worker retry remain in the execution history.

The actual definitions matter:

- The matrix index is `Fin 3 + Fin 3`. `IsHadamard H` requires unit-modulus
  entries and `H * H.conjTranspose = 6 I`.
- `Equivalent H K` is row and column permutation together with unit row
  and column phases. It is the equivalence that preserves raw quartet
  completion after simultaneous transport of the additional bases.
- `CornerData` supplies four unit complex phases in a dephased 3-by-3 block
  `E`. Horizontal candidates `B` have first row one and
  `E E* + B B* = 6 I`. Vertical candidates `C` have first column one and
  `E* E + C* C = 6 I`.
- `IsFiniteDilationCorner E` requires nonempty, finite sets of invertible
  horizontal and vertical candidates. The seed phases still range over a
  continuous domain.
- `Retained E B C` requires that finite-corner condition, invertible
  adjacent candidates, and unit entries in the forced block
  `D = -C E* (B^{-1})*`. The completion is the block matrix `[E B; C D]`.
- `paper_finite_corner_completeness` takes only `IsHadamard H` and produces
  equivalence to one such retained completion. Its soundness converse is
  also checked. It is not a five-family classification or a MUB exclusion.

The external `LEAN_ASSUMES_AND_PROVES.md` still leaves several manuscript
comparisons and geometric claims outside Lean, including the comparison
with Construction 3.1 and the generic product/ramification geometry. None
of those claims is used here.

## 2. The concrete quartet bridge has passed replay

`MubIndexTransport.lean` derives Gram and MU preservation under an actual
index equivalence. Its seven endpoints passed under the canonical pins.
`external_classification/MubFiniteCornerReduction.lean` then combines the
index equivalence with the existing normalization and simultaneous monomial
transport. It imports the external completeness theorem directly.

The integration script verified the external archive and all dependency
pins, then compiled the exact source bytes of 21 canonical local modules
and the new bridge under the external Lean pin. All five bridge endpoints
reported only standard axioms. No cross-version olean was imported.

The theorem `exists_quartet_iff_retained_completion` proves existence of
an actual normalized quartet on `Fin 6` if and only if some retained output
admits the two additional raw Hadamard matrices with all three raw MU
conditions. `no_quartet_iff_retained_nonextension` identifies its exact
universal negation. These endpoints have no supplied classification or
transport premise; the only open statement is the quantified nonextension
on the right. The canonical full `Mub6` root does not import this separate
external-pinned target.

## 3. Canonical quantitative bounds

`MubMinorChart.lean` enumerates the twenty increasing triples of columns.
Each triple defines an injective selection, as checked by ordinary kernel
reduction. For every complex 3-by-6 matrix `A`, an exact polynomial proof
establishes

\[
\sum_{|S|=3}|\det A_{[:,S]}|^2=\det(AA^*).
\]

Under `AA* = 6 I`, the sum is 216. The finite pigeonhole argument gives a
selected minor `B` with `|det B|^2 >= 54/5`, hence an invertible minor.
For a unit-entry matrix, every 2-by-2 cofactor is a difference of two unit
products and has squared modulus at most four. The adjugate formula yields

\[
|(B^{-1})_{ij}|^2\le 4/|\det B|^2\le 10/27.
\]

The endpoint `exists_bounded_inverse_minor` applies both bounds to the
first three rows of every unit-entry 6-by-6 matrix with row Gram matrix
`6 I`. All ten reported endpoints passed on canonical Lean `4.33.1` and
Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`, with only the three
standard axioms. A separate mutant changing the normalized sum from 216
to 215 failed at the mathematical equality; it is not an accepted source.

This theorem does not identify its chosen minor with the finite-fibre
minor supplied by the external classification. Intersecting the two
existence statements without a further argument would lose coverage.
No spectral lower bound, complementary-minor identity, or global chart
selection has been certified by this file.

The canonical targets can be replayed from
`lean4/research_programs/mub6` with its committed toolchain and manifest:

```powershell
$env:LEAN_NUM_THREADS = '1'
lake build +MubIndexTransport:olean +MubMinorChart:olean
```

The recorded execution used an isolated copy of the required local sources
and the same pins at `scratch/m6`. The external-pinned bridge uses the
separate replay script and preparation instructions in
`lean4/research_programs/mub6/external_classification/README.md`.

## 4. Strategic consequences and next obligations

The useful distinction is between exact coverage and exact exclusion.
Classification coverage can justify the domain on which exclusion must
be universal. It does not make the remaining continuum problem finite.
Likewise, an inverse bound controls denominators but supplies no sign or
infeasibility certificate for the MU equations.

The quantitative result suggests a separate elementary reconstruction
route. Its next obligations are explicit:

1. Extend each selected triple of columns to a complete permutation and
   place the bounded minor in the desired adjacent block.
2. Derive dephasing and simultaneous quartet transport while preserving
   determinant moduli and the inverse-entry bound.
3. Derive the forced-block formula from the actual Gram equations, and
   prove coverage and soundness for the resulting quantified block domain.
4. Encode all candidate-basis equations on that domain and establish an
   exact exclusion, or produce an exact quartet witness.

This route need not assume finite fibres, but its coverage theorem has
not been implemented. Even after coverage, the last step remains the
substantial open MUB6 problem. The existing unresolved interval boxes,
Laurent necessary-condition conjecture, and moment-variety emptiness
obligations are not discharged by the bounds above.

The corrected Subproblem 2 section and three-page master scaffold are
single-agent editorial consolidation. The two new level manifests record
zero executed merge agents and zero independent merge reviews. They do
not seal the five historical staged assignments. The six other master
sections retain explicit integration obligations.
