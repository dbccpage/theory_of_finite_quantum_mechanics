# MUB-PRIME-POWER-CONSTRUCTION

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Construct and verify a complete d+1 MUB family for the stated prime-power carrier, explicitly handling finite-field arithmetic, character sums and normalization.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Provide the construction and all pairwise trace identities for the admitted dimension; do not infer a dimension-six family from smaller dimensions.

## Source status

Source record or explicit branch obligation; status scoped to the statement.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/25_mub/tfq_0403_mub_prime_power_construction.md`

- file: [dag/derivations/25_mub/tfq_0403_mub_prime_power_construction.md](../../../dag/derivations/25_mub/tfq_0403_mub_prime_power_construction.md)
- sha256 (`lf-normalised`): `36a80e2b810e939e9276544b0b9bc012299d8c464296607aad02470495acefe8`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0403
- counts toward the grade: no

### Documents and data: `papers/core/mub6/README.md`

- file: [papers/core/mub6/README.md](../../../papers/core/mub6/README.md)
- sha256 (`lf-normalised`): `df09e721db359b5d96928ae66ee18f6f67d8e805182e6ae7dd76d156496198f9`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB-PRIME-POWER-CONSTRUCTION` `GAP_NO_DERIVATION`: [MUB-EXACT-PROJECTORS](MUB-EXACT-PROJECTORS.md) (DEFINITION)

Outgoing (1):

- `APP-R-MUB6-NO-FIELD-OF-ORDER-SIX` `CONDITIONAL_ON_IMPORT`: [MUB6-NO-FIELD-OF-ORDER-SIX](MUB6-NO-FIELD-OF-ORDER-SIX.md) (IMPORTED_ASSUMPTION)
