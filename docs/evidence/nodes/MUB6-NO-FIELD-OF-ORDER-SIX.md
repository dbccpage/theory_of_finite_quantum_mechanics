# MUB6-NO-FIELD-OF-ORDER-SIX

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> No finite field has six elements, since finite fields have prime-power order; hence the finite-field Weyl-character construction of d+1 MUBs has no instance at d = 6.

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

- Finite fields have prime-power order (standard algebra; not instantiated at order 6 in this checkout)

## Bottleneck

This rules out one construction route only; it gives no upper bound on the number of MUBs in C^6 and does not exclude a complete family produced by another construction.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-052 claims PROVED_LEAN; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/25_mub/tfq_1222_mub6_no_field_of_order_six.md`

- file: [dag/derivations/25_mub/tfq_1222_mub6_no_field_of_order_six.md](../../../dag/derivations/25_mub/tfq_1222_mub6_no_field_of_order_six.md)
- sha256 (`lf-normalised`): `e14bb7a8f4a75cc7c02ca1c5f32984c48b92d7429ea52af1e472de5fd40bc6d0`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1222
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

- `APP-R-MUB6-NO-FIELD-OF-ORDER-SIX` `CONDITIONAL_ON_IMPORT`: [MUB-PRIME-POWER-CONSTRUCTION](MUB-PRIME-POWER-CONSTRUCTION.md) (OPEN), [MUB6-QUHEX-TENSOR-CARRIER](MUB6-QUHEX-TENSOR-CARRIER.md) (DEFINITION)

Outgoing (0):

