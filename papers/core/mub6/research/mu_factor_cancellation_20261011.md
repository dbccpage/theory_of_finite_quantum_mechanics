# Positive determinant factor cancellation in 36 MU equations

AuthorityEffect: None.

The [complete bounded coefficient system](bounded_export_20261011.md) has
152 real coordinates, 396 equations and the inequality `q >= 54/5`, where
`q = |det B|^2`. This checkpoint replaces 36 of its equations by polynomials
of degree at most four. The other equations, box and determinant inequality
are retained. Global infeasibility and `N(6)=3` remain open.

The receipt is [`mub6_mu_factor_20261011_receipt.json`](../artifacts/mub6_mu_factor_20261011_receipt.json).

## Polynomial identity and domain

Write `d = conjugate(det B)` and let `S` be the scaled reconstruction
`[[d E, d B], [d C, N]]`. Its first three columns are `d` times the columns
of `L = [[E, 0], [C, 0]]`. For either additional basis `A = U,V`, and for
`i` in the first three column indices, conjugate transposition therefore gives

\[
(S^*A)_{ij}=\overline d\,(L^*A)_{ij},\qquad
|(S^*A)_{ij}|^2-6q=q\bigl(|(L^*A)_{ij}|^2-6\bigr).
\]

`MubBoundedMUFactor.left_factor` proves this identity in the actual rational
polynomial algebra. `equation_factor` binds the replacement expressions to
their original equation indices. `factorization` covers the whole indexed
system: its factor is `q` for these 36 equations and one for every other
equation. `replacement_count` checks that there are exactly 36 replacements.

Since `q >= 54/5 > 0`, `zero_iff` permits cancellation. The theorem
`exists_quartet_iff_reduced` preserves actual normalized quartet existence
on the full closed box. The replacement polynomials have degree at most
four; the entire remaining system still has degree at most eight.

The bound cannot be dropped from this cancellation argument. The checked
zero-coordinate example has `q=0`, original residual zero and replacement
residual `-5` for equation 108. `singular_real_probe` evaluates the residuals
over the reals, and `unconditional_cancellation_false` rejects a universal
cancellation equivalence without the bound. This example is not a solution
of the full quartet system.

## Coefficient replacement artifact

The 36 replacement rows are in
[`mub6_mu_factor_replacements_20261011.jsonl`](../artifacts/mub6_mu_factor_replacements_20261011.jsonl).
They replace only IDs `108..125` and `144..161` in the pinned
[`bounded_quartet_coefficients_20261011.jsonl.gz`](../artifacts/bounded_quartet_coefficients_20261011.jsonl.gz).
Retain every other row, all coordinate IDs, the determinant polynomial,
`q >= 54/5`, and the box `[-1,1]^152`. The receipt binds both artifacts and
the decompressed base hash; this is a base artifact plus a replacement table.

| Observed coefficient count | Before | After |
|---|---:|---:|
| The 36 selected equations | 371,520 | 3,096 |
| All equations and q | 3,760,338 | 3,391,914 |

The selected rows have 120 times fewer collected monomials. The replacement
table contains 70,331 bytes. These are exact counts of the serialized lists,
not complexity guarantees for a solver. The largest remaining rows are
unchanged, so cancellation does not remove the main degree-eight bottleneck.

All 36 rows passed four exact rational expression/coefficient comparisons
and four original/factored-expression comparisons, totaling 144 of each.
File validation checks all IDs, rational syntax, monomial ordering, coefficient
nonvanishing, coordinate ranges and degree bounds. It preserves the pinned
base bytes. The kernel theorems concern the defined polynomials; the native
serialized replacement table has not been kernel-reflected.

## Replay and remaining obligation

Eighteen displayed endpoints passed the pinned Lean replay with only
`propext`, `Classical.choice`, and `Quot.sound`. The exporter elaborated too.
A negative probe falsely requiring the singular replacement residual to be
zero is rejected after rewriting by its checked value `-5`.

From `lean4/research_programs/mub6`:

```powershell
$env:LEAN_NUM_THREADS = '1'
lake build +MubBoundedMUFactor:olean +MubBoundedExport:olean
lake env lean --run MubBoundedExport.lean mu-factors OUTPUT.jsonl
```

That command is the checkpoint command. The current wrapper is
`lean4/MubBoundedExport.lean mu-factors`.

The full-system coefficient export from the previous checkpoint remains an
unchanged historical artifact. No full new archive or whole-package build is
claimed here. The outstanding mathematical obligation is to exclude every
real solution of the complete reduced system, or produce an exact quartet.
