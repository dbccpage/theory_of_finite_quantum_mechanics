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

dag/derivations/25_mub/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-074 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/25_mub/mub6/completion_supplement.md`

- file: [dag/derivations/25_mub/mub6/completion_supplement.md](../../../dag/derivations/25_mub/mub6/completion_supplement.md)
- sha256 (`lf-normalised`): `6991957c4eb15b9550b00904333eef6560530f4f26e769722b54b5c4ca6ff03e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/mub6/theory_of_finite_mub6.jsonl`

- file: [dag/derivations/25_mub/mub6/theory_of_finite_mub6.jsonl](../../../dag/derivations/25_mub/mub6/theory_of_finite_mub6.jsonl)
- sha256 (`lf-normalised`): `815b535641140895e823e99e201cf3314a9054db022f5a0c35be601a18663839`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/mub6/theory_of_finite_mub6.md`

- file: [dag/derivations/25_mub/mub6/theory_of_finite_mub6.md](../../../dag/derivations/25_mub/mub6/theory_of_finite_mub6.md)
- sha256 (`lf-normalised`): `0e5866c8c56eb624576b512e2f51f0378271797285bb11c764a9708a234085e1`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1242_mub6_rational_ldl_claim.md`

- file: [dag/derivations/25_mub/tfq_1242_mub6_rational_ldl_claim.md](../../../dag/derivations/25_mub/tfq_1242_mub6_rational_ldl_claim.md)
- sha256 (`lf-normalised`): `c6b833bf424c920e90bdcd17737d037c31ba7f514529397c0af2b139ab59fd37`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1242
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-MUB6-RATIONAL-LDL-CLAIM` `GAP_NO_DERIVATION`: [MUB6-POSITIVSTELLENSATZ-CLAIM](MUB6-POSITIVSTELLENSATZ-CLAIM.md) (OPEN), [MUB6-GLOBAL-OBLIGATIONS](MUB6-GLOBAL-OBLIGATIONS.md) (OPEN)

Outgoing (0):

