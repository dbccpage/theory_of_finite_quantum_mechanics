# MUB6-HAAGERUP-MATRIX-CHM

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The explicit 6x6 matrix haagerupMatrix with entries in {1, -1, i} has unit-modulus entries and H H* = 6I.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 1 Lean reference(s) cited, 1 in this checkout (replay: none 1). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

The source one-parameter family H6(q) without 2x2 or 3x3 Hadamard sub-blocks is not constructed; matching this matrix to the Haagerup source and to any exclusion theorem is an open step.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-058 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MasterClassification.lean`

- file: [lean4/MasterClassification.lean](../../../lean4/MasterClassification.lean)
- sha256 (`bytes`): `cbfd11e4e0038f1a3deb5c51c8079d1c28f7e5fad3d189b3296239b50507ccc3`
- cited in: node.lean, record TFQ-1227
- replay: `none`
- check: `cd lean4 && lake build MasterClassification`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `haagerupMatrix_isCH6` | yes | yes | yes | - | `#print axioms haagerupMatrix_isCH6` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1227_mub6_haagerup_matrix_chm.md`

- file: [dag/derivations/25_mub/tfq_1227_mub6_haagerup_matrix_chm.md](../../../dag/derivations/25_mub/tfq_1227_mub6_haagerup_matrix_chm.md)
- sha256 (`lf-normalised`): `ddeb32d44f6a62e96bb153f3a052348bd6d8967aaa4c4bc383035d055b47d8e3`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1227
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `edeb29b681854d6ff67bdf072e4d3163995e068973662ebb77220ba009345238`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.jsonl`

- file: [papers/core/mub6/theory_of_finite_mub6.jsonl](../../../papers/core/mub6/theory_of_finite_mub6.jsonl)
- sha256 (`lf-normalised`): `79a8e74d457a2c236999a6a1dcd1ff010f0f878b245c205f5f049add18ae2234`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.md`

- file: [papers/core/mub6/theory_of_finite_mub6.md](../../../papers/core/mub6/theory_of_finite_mub6.md)
- sha256 (`lf-normalised`): `4df95e7f697d7ab11bfa44f282353267197198f74bcfb535e5f10c18ffbeabf5`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-HAAGERUP-MATRIX-CHM` `DERIVED_LEAN`: [MUB6-QUARTET-RAW-HADAMARD-TRANSPORT](MUB6-QUARTET-RAW-HADAMARD-TRANSPORT.md) (PROVED_LEAN)

Outgoing (0):

