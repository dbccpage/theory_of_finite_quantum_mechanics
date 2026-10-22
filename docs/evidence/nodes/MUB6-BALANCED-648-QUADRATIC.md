# MUB6-BALANCED-648-QUADRATIC

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Quartet existence in C^6 is equivalent to a solution in the stated box of 648 rational polynomial equations of total degree at most two in 320 coordinates, obtained by affine completion of the balanced transition matrices.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Infeasibility is open; the literal table MubBalancedTable has no completed build and is not cited; the box \[-1,1\]^170 x \[-10035/4096, 10035/4096\]^150 holds on solutions only.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-C15 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MubBalancedCompletion.lean`

- file: [lean4/MubBalancedCompletion.lean](../../../lean4/MubBalancedCompletion.lean)
- sha256 (`bytes`): `75d38d52952c82337aff491dfc020829b0113e49831bdd7208df6c59ccc00b44`
- cited in: node.lean, record TFQ-1264
- replay: `none`
- check: `cd lean4 && lake build MubBalancedCompletion`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `complete_restrict` | yes | yes | yes | - | `#print axioms complete_restrict` |
| `restrict_complete` | yes | yes | yes | - | `#print axioms restrict_complete` |
- counts toward the grade: yes

### Lean: `lean4/MubBalancedQuadraticPolynomials.lean`

- file: [lean4/MubBalancedQuadraticPolynomials.lean](../../../lean4/MubBalancedQuadraticPolynomials.lean)
- sha256 (`bytes`): `e1e92915b1524e2eb349db5d85447739faac51bf790aea1a681b61999323c7a5`
- cited in: node.lean, record TFQ-1264
- replay: `none`
- check: `cd lean4 && lake build MubBalancedQuadraticPolynomials`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `equation_degree` | yes | yes | yes | - | `#print axioms equation_degree` |
| `exists_quartet_iff_balanced_polynomials` | yes | yes | yes | - | `#print axioms exists_quartet_iff_balanced_polynomials` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1264_mub6_balanced_648_quadratic.md`

- file: [dag/derivations/25_mub/tfq_1264_mub6_balanced_648_quadratic.md](../../../dag/derivations/25_mub/tfq_1264_mub6_balanced_648_quadratic.md)
- sha256 (`lf-normalised`): `6db73c6e6ac42450836d49919f7e6d06a56d1a26ebf22cf0cc864804aca7d8e9`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1264
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `edeb29b681854d6ff67bdf072e4d3163995e068973662ebb77220ba009345238`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/mub6_claim_ledger.md`

- file: [papers/core/mub6/mub6_claim_ledger.md](../../../papers/core/mub6/mub6_claim_ledger.md)
- sha256 (`lf-normalised`): `e21c9d2f20bd0e87979c8b003ab6e2c60422c19cfdd0117308db09ec10c47f7a`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-BALANCED-648-QUADRATIC` `DERIVED_LEAN`: [MUB6-QUADRATIC-LIFT-386](MUB6-QUADRATIC-LIFT-386.md) (PROVED_LEAN)

Outgoing (0):

