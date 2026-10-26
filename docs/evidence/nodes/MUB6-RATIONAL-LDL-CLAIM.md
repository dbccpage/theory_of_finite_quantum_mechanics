# MUB6-RATIONAL-LDL-CLAIM

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claim: an exact rational LDL^T factorization with positive pivots of the Gram matrix of the Positivstellensatz certificate gives a machine-checked refutation of fourth-basis candidates.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

There is no certificate Gram matrix to factor (MUB6-DERIV-073); the deposit rational LDL routines concern fixed candidate matrices only.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-074 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/25_mub/tfq_1242_mub6_rational_ldl_claim.md`

- file: [dag/derivations/25_mub/tfq_1242_mub6_rational_ldl_claim.md](../../../dag/derivations/25_mub/tfq_1242_mub6_rational_ldl_claim.md)
- sha256 (`lf-normalised`): `621b0c5f09950a6e2be12ec193e9f538ac3efe2578e3f086dee7d4fba0918f94`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1242
- counts toward the grade: no

### Documents and data: `papers/core/mub6/completion_supplement.md`

- file: [papers/core/mub6/completion_supplement.md](../../../papers/core/mub6/completion_supplement.md)
- sha256 (`lf-normalised`): `2436eaf1ff552dee22fa7539ba2e9b76d8999bcf3ee4f183db06a8d2563109e0`
- cited in: node.source
- counts toward the grade: yes

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

- `APP-R-MUB6-RATIONAL-LDL-CLAIM` `GAP_NO_DERIVATION`: [MUB6-POSITIVSTELLENSATZ-CLAIM](MUB6-POSITIVSTELLENSATZ-CLAIM.md) (OPEN), [MUB6-GLOBAL-OBLIGATIONS](MUB6-GLOBAL-OBLIGATIONS.md) (OPEN)

Outgoing (0):

