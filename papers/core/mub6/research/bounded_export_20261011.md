# Complete numbered coefficient system for the bounded quartet problem

AuthorityEffect: None.

This checkpoint follows the [expression and degree reduction](bounded_expressions_20261011.md).
Its receipt is [`mub6_bounded_export_20261011_receipt.json`](../artifacts/mub6_bounded_export_20261011_receipt.json).
The global quartet exclusion and `N(6)=3` remain open.

## Checked coverage and polynomial semantics

`MubBoundedExportIndices.lean` assigns every real coordinate a unique code
in `0..151` and every equation a unique code in `0..395`. The two enumerated
code lists equal the corresponding complete ranges by ordinary kernel
reduction. Separate membership proofs cover every source index, and
`variableFin_bijective` identifies the actual coordinate type with `Fin 152`.

The complex-entry slot order is as follows; real and imaginary parts have
codes `2*slot` and `2*slot+1`. Matrix indices in this table start at zero.
The six-dimensional indices use `blockIndex` from the bounded chart.

| Slots | Entries |
|---|---|
| 0–3 | E rows 1–2, columns 1–2 |
| 4–9 | B rows 1–2, columns 0–2 |
| 10–15 | C rows 0–2, columns 1–2 |
| 16–45 | U rows 1–5, columns 0–5 |
| 46–75 | V rows 1–5, columns 0–5 |

The complete equation order is:

| Equation IDs | Constraints |
|---|---|
| 0–26 | Unit entries of E, B, C |
| 27–35 | Numerator entry norm squares equal q |
| 36–107 | Unit entries of U, V |
| 108–215 | Scaled H–U, scaled H–V, and U–V MU relations |
| 216–251 | Real and imaginary components of the two block Gram equations |
| 252–395 | Real and imaginary components of the U and V Gram equations |

`MubBoundedTermCollection.lean` checks that sorting factors, sorting terms,
adding coefficients of adjacent equal monomials, and removing exact zeros
preserve the polynomial. Collection at each expression node avoids retaining
the complete raw distributive expansion. `coefficients_polynomial` applies
to every expression; the equation and determinant specializations retain
their original rational polynomials under the checked coordinate renaming.
These identities do not require a sorted-input hypothesis. Canonical order
and absence of duplicate monomials in the exported lists are runtime checks.

`MubBoundedCodedSystem.exists_quartet_iff_coded` identifies actual quartet
existence with a solution of these numbered coefficient lists on
`[-1,1]^152`. The predicate includes every enumerated equation and
`q >= 54/5`. It retains the containing box boundary and all three MU
relations. This equivalence does not establish that the solution set is empty.

The nine index, twelve collection and seven coded-system endpoints passed
targeted replay with only `propext`, `Classical.choice`, and `Quot.sound`.
The IO exporter also passed elaboration. No whole-package build is claimed.

## Native artifact and its boundary

The compressed artifact is
[`bounded_quartet_coefficients_20261011.jsonl.gz`](../artifacts/bounded_quartet_coefficients_20261011.jsonl.gz).
Its decompressed JSON-lines stream contains a domain header, the determinant
norm-square polynomial, all 396 equations in order, and a completion record.
Coefficients are normalized rational strings; each monomial is a sorted
list of coordinate IDs. Equations that collect to zero retain their IDs.

| Observed export quantity | Value |
|---|---:|
| Polynomial rows, including q | 397 |
| Collected monomials across all rows | 3,760,338 |
| Maximum monomials in one row | 90,280 |
| Exact expression/list evaluation comparisons | 1,588 |
| Decompressed bytes | 120,920,846 |
| Compressed bytes | 12,576,354 |

Both complete executions produced the same decompressed SHA-256:
`5839c552d2252ca44e09c121bebecf7c359f883589a9a834c40c66f55cc6736a`.
The final execution used the frozen 31-module source closure. The archive
decompresses to those exact bytes. These are native artifact observations.

`MubBoundedExport.lean` compares every collected polynomial with its original
expression at four exact rational assignments, checks factor ranges and
degree bounds, and rejects zero coefficients or duplicate/unsorted monomials.
The receipt records completion, sizes, term counts, runtime probes, byte
replay and archive roundtrip. The packaging check validates file structure
and rational syntax; it is not a solver or a separate polynomial proof.

The kernel theorems concern the defined coefficient lists. They do not
reflect the serialized file bytes. Exact execution probes and deterministic
byte replay do not replace such a reflection theorem or an infeasibility
certificate. No contractor, exhaustive exclusion, quartet witness,
publication or authority promotion follows from this checkpoint.

Two targeted negative controls are rejected: shifting B's slot offset
breaks the complete coordinate range, and replacing coefficient addition
with subtraction breaks the collection identity. They are not a complete
mutation audit.

From `lean4/research_programs/mub6`, with the pinned dependencies:

```powershell
$env:LEAN_NUM_THREADS = '1'
lake build +MubBoundedCodedSystem:olean +MubBoundedExport:olean
lake env lean --run MubBoundedExport.lean OUTPUT.jsonl
```

That command is the checkpoint command. The current wrapper is
`lean4/MubBoundedExport.lean`, because the library module no longer declares
root `main`.

The output directory must already exist. An interrupted file lacks its final
completion record and must not be accepted as a complete export. The remaining
mathematical obligation is infeasibility on the whole bounded real domain,
or an exact quartet witness, with the determinant inequality retained.

## Subsequent positive-factor cancellation

The [MU factor cancellation checkpoint](mu_factor_cancellation_20261011.md)
checks 36 lower-degree replacements and exports their coefficient rows.
The base archive and this checkpoint receipt remain unchanged. The replacement
table must retain the positive determinant inequality and all other equations.
