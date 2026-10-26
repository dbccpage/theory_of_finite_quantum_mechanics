# MUB6-QUHEX-TENSOR-CARRIER

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `DEFINITION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Fix the identification C^6 = C^2 tensor C^3 with product basis |j,k\> = |j\> tensor |k\> for j in {0,1} and k in {0,1,2}; this is a declared choice of tensor factorization of the six-dimensional carrier.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Hilbert tensor product C^2 tensor C^3 (GP-IMPORT-TENSOR-PRODUCT)

## Bottleneck

The source statement that every 6x6 operator decomposes into Pauli and Gell-Mann tensor products, and its SU(2)/SU(3) reading, are not checked here; the factorization selects no MUB structure.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-051 claims PROVED_LEAN; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/25_mub/tfq_1221_mub6_quhex_tensor_carrier.md`

- file: [dag/derivations/25_mub/tfq_1221_mub6_quhex_tensor_carrier.md](../../../dag/derivations/25_mub/tfq_1221_mub6_quhex_tensor_carrier.md)
- sha256 (`lf-normalised`): `b3eb2fb8b9d4f850c8ee7bc94e4864aea5acfe9135fea0d6e9ffc25c3e4cc52e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1221
- counts toward the grade: no

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.jsonl`

- file: [papers/core/mub6/theory_of_finite_mub6.jsonl](../../../papers/core/mub6/theory_of_finite_mub6.jsonl)
- sha256 (`lf-normalised`): `815b535641140895e823e99e201cf3314a9054db022f5a0c35be601a18663839`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.md`

- file: [papers/core/mub6/theory_of_finite_mub6.md](../../../papers/core/mub6/theory_of_finite_mub6.md)
- sha256 (`lf-normalised`): `b515bf981d6c3a339c2b0a7937d54d9deb05f3b53186c584b83f5fa3419dc902`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-QUHEX-TENSOR-CARRIER` `DERIVED_PROSE`: [MUB-EXACT-PROJECTORS](MUB-EXACT-PROJECTORS.md) (DEFINITION), [GP-IMPORT-TENSOR-PRODUCT](GP-IMPORT-TENSOR-PRODUCT.md) (IMPORTED_ASSUMPTION)

Outgoing (3):

- `APP-R-MUB6-NO-FIELD-OF-ORDER-SIX` `CONDITIONAL_ON_IMPORT`: [MUB6-NO-FIELD-OF-ORDER-SIX](MUB6-NO-FIELD-OF-ORDER-SIX.md) (IMPORTED_ASSUMPTION)
- `APP-R-MUB6-PRODUCT-TRIPLE-LOWER-BOUND` `COMPUTED`: [MUB6-PRODUCT-TRIPLE-LOWER-BOUND](MUB6-PRODUCT-TRIPLE-LOWER-BOUND.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-MUB6-WEYL-HEISENBERG-D6` `CONDITIONAL_ON_IMPORT`: [MUB6-WEYL-HEISENBERG-D6](MUB6-WEYL-HEISENBERG-D6.md) (IMPORTED_ASSUMPTION)
