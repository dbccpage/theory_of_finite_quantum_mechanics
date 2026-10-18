# Exact coefficients for the full quadratic lift

AuthorityEffect: None.

The [full quadratic lift](quadratic_lift_20261011.md) represents actual MUB
quartet existence with 648 equations on 386 real coordinates. Its complete
native coefficient table contains **4,920 collected monomials**, at most 12
per row, in 169,800 bytes. The coordinate box remains `[-1,1]` for indices
0 through 169 and `[-3,3]` for indices 170 through 385, with boundaries included.
Global infeasibility and `N(6)=3` remain open.

Artifacts:

- [Complete coefficient table](../artifacts/quadratic_lift_coefficients_20261011.jsonl).
- [Source and execution receipt](../artifacts/mub6_quadratic_coefficients_20261011_receipt.json).
- [Literal-table formatter](../scripts/reflect_quadratic_lift.py).

## Defined coefficients and numbering

`MubQuadraticLiftIndices` checks complete, unique numbering of every
coordinate and equation. The first 152 coordinate IDs preserve the preceding
bounded coordinate codec; IDs 152 through 169 are the D block, and IDs 170
through 385 are the three complex transition matrices. The radius theorem
checks the bounds attached to these IDs.

| Equation IDs | Condition | Count |
|---|---|---:|
| 0–107 | Unit entry norms in H, U, V | 108 |
| 108–323 | Real and imaginary Gram components | 216 |
| 324–539 | Real and imaginary transition graph components | 216 |
| 540–647 | Transition entry norms equal to six | 108 |

`MubQuadraticLiftCoefficients` reuses the proved rational term collector, with
structural insertion sorts so its small lists reduce in the kernel. The new
normalizer has its own polynomial-preservation proof. It constructs complex
arithmetic directly on collected lists and
proves that every resulting list represents the corresponding actual
quadratic polynomial after coordinate renaming. It does not rely on agreement
at test points. `MubQuadraticLiftCodedSystem.exists_quartet_iff_coded` retains
quartet existence on `Fin 386` and the same box.

Forty-two rows have empty coefficient lists and hence are identically zero.
They remain present in the complete table. Equation counts do not assert
independence or dimension. Comparing monomial counts across the older and
newer formulations does not establish solver performance: the ambient
variables and constraints differ.

## Native replay and literal table

`MubQuadraticLiftExport` writes every row and compares its coefficient-list
evaluation with separate direct rational matrix arithmetic at four points.
All 2,592 comparisons passed. A second export produced identical bytes:

`a8b2dbcbc44d0618bbf0bf36fd2b252d7cc8a03a1168ebf98ecc28010dceed03`

Replacing one transition norm row by the empty polynomial is rejected at
equation 540, probe zero. This is a negative control for the native checker,
not a proof of global exclusion.

The formatter validates numbering, dimensions, bounds, rational syntax,
coefficient nonvanishing, factor ordering, unique monomials and degree limits.
It then writes all rows and bounds as literals in `MubQuadraticLiftTable`.
The generated source is tied to the JSON hash, and regenerating it reproduces
the exact source bytes. JSON parsing and file hashing remain outside Lean.

`rows_match` checks the entire literal table against the defining coefficient
lists using kernel reduction. `bounds_match` checks every literal bound.
`exists_quartet_iff_table` connects common zeros of those literal rows to
actual quartet existence, using the checked coordinate box. The theorem is
about these literal lists; it does not assume that an arbitrary external file
with similar metadata is correct.

## Replay

The five new modules and their 37-module local import closure passed scoped
Lean 4.33.1 replay. All 30 displayed endpoints use only `propext`,
`Classical.choice` and `Quot.sound`. This does not report a whole-package build.

From `lean4/research_programs/mub6`:

```powershell
$env:LEAN_NUM_THREADS = '1'
lake build +MubQuadraticLiftExport:olean +MubQuadraticLiftTable:olean
lake env lean --run MubQuadraticLiftExport.lean OUTPUT.jsonl
```

That command is the checkpoint command. The current wrapper is
`cli/MubQuadraticLiftExport.lean`.

From the repository root, regenerate a separate Lean source file with:

```powershell
python omega_engine_projects/mub6/scripts/reflect_quadratic_lift.py `
  --coefficients OUTPUT.jsonl --output GENERATED.lean
```

The exact coefficient representation is now available for exclusion work.
No interval contractor, finite cover, or complete infeasibility certificate
for this new system is claimed. All earlier reconstruction and cancellation
artifacts retain their original determinant condition.
