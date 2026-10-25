# MUB-EXACT-PROJECTORS

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On a supplied finite-dimensional Hilbert carrier, a MUB family consists of rank-one orthogonal projector resolutions with cross-basis trace pairing 1/d. Exact arithmetic must include the required scalar extension.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- supplied finite-dimensional Hilbert carrier
- sufficient exact scalar extension

## Bottleneck

Check the scalar field, adjoint, rank, resolutions and all cross-basis trace equalities before accepting a MUB witness.

## Source status

Source record or explicit branch obligation; status scoped to the statement.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/25_mub/tfq_0402_mub_exact_projectors.md`

- file: [dag/derivations/25_mub/tfq_0402_mub_exact_projectors.md](../../../dag/derivations/25_mub/tfq_0402_mub_exact_projectors.md)
- sha256 (`lf-normalised`): `bf9e6f921ff6c5e41d8aabf191026a18ffd1487987c8846b01d727aabebb2ddd`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0402
- counts toward the grade: no

### Documents and data: `papers/core/mub6/README.md`

- file: [papers/core/mub6/README.md](../../../papers/core/mub6/README.md)
- sha256 (`lf-normalised`): `df09e721db359b5d96928ae66ee18f6f67d8e805182e6ae7dd76d156496198f9`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB-EXACT-PROJECTORS` `CONDITIONAL_ON_IMPORT`: [GP-FIN-GAUSS-MATRIX-ALGEBRA](GP-FIN-GAUSS-MATRIX-ALGEBRA.md) (PROVED_LEAN), [GP-IMPORT-COMPLEX-FIELD](GP-IMPORT-COMPLEX-FIELD.md) (IMPORTED_ASSUMPTION)

Outgoing (8):

- `APP-R-MUB-PRIME-POWER-CONSTRUCTION` `GAP_NO_DERIVATION`: [MUB-PRIME-POWER-CONSTRUCTION](MUB-PRIME-POWER-CONSTRUCTION.md) (OPEN)
- `APP-R-MUB-TOMOGRAPHY-INVERSION` `DERIVED_PROSE`: [MUB-TOMOGRAPHY-INVERSION](MUB-TOMOGRAPHY-INVERSION.md) (PROVED_PROSE)
- `APP-R-MUB6-CONCRETE-PROJECTORS` `DERIVED_LEAN`: [MUB6-CONCRETE-PROJECTORS](MUB6-CONCRETE-PROJECTORS.md) (PROVED_LEAN)
- `APP-R-MUB6-FIXED-TRIPLE-VARIETY` `DERIVED_LEAN`: [MUB6-FIXED-TRIPLE-VARIETY](MUB6-FIXED-TRIPLE-VARIETY.md) (PROVED_LEAN)
- `APP-R-MUB6-GLOBAL-OBLIGATIONS` `GAP_NO_DERIVATION`: [MUB6-GLOBAL-OBLIGATIONS](MUB6-GLOBAL-OBLIGATIONS.md) (OPEN)
- `APP-R-MUB6-PRODUCT-TRIPLE-LOWER-BOUND` `COMPUTED`: [MUB6-PRODUCT-TRIPLE-LOWER-BOUND](MUB6-PRODUCT-TRIPLE-LOWER-BOUND.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-MUB6-QUARTET-RAW-HADAMARD-TRANSPORT` `DERIVED_LEAN`: [MUB6-QUARTET-RAW-HADAMARD-TRANSPORT](MUB6-QUARTET-RAW-HADAMARD-TRANSPORT.md) (PROVED_LEAN)
- `APP-R-MUB6-QUHEX-TENSOR-CARRIER` `DERIVED_PROSE`: [MUB6-QUHEX-TENSOR-CARRIER](MUB6-QUHEX-TENSOR-CARRIER.md) (DEFINITION)
