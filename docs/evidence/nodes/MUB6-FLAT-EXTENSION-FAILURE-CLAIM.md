# MUB6-FLAT-EXTENSION-FAILURE-CLAIM

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claim: the flat-extension rank condition rank M_2 = rank M_1 fails for every admissible moment vector, so no measure supported on fourth-basis solutions exists.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
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

By fourth_basis_iff_positive_flat_moments (MUB6-C36) this is equivalent to absence of a fourth basis for the fixed triple, which is open.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-071 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/25_mub/tfq_1239_mub6_flat_extension_failure_claim.md`

- file: [dag/derivations/25_mub/tfq_1239_mub6_flat_extension_failure_claim.md](../../../dag/derivations/25_mub/tfq_1239_mub6_flat_extension_failure_claim.md)
- sha256 (`lf-normalised`): `b36c418b9fdc39c2f645261c02d7d3ce5624af2207540d101ac72fd9fd12b74c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1239
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `31ddd89d2594bb5ad401aadb99a3a91edb6ea8e33158386031a40b1dc36f7223`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/mub6_claim_ledger.md`

- file: [papers/core/mub6/mub6_claim_ledger.md](../../../papers/core/mub6/mub6_claim_ledger.md)
- sha256 (`lf-normalised`): `6708883b9f1ed33cc93d794d2c7c50484f0f8e075e4576c2eaa74fadf6fbf842`
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

- `APP-R-MUB6-FLAT-EXTENSION-FAILURE-CLAIM` `GAP_NO_DERIVATION`: [MUB6-MOMENT-EVALUATION-FLAT](MUB6-MOMENT-EVALUATION-FLAT.md) (PROVED_LEAN), [MUB6-GLOBAL-OBLIGATIONS](MUB6-GLOBAL-OBLIGATIONS.md) (OPEN)

Outgoing (2):

- `APP-R-MUB6-COMMUTATIVITY-DEFECT-CLAIM` `GAP_NO_DERIVATION`: [MUB6-COMMUTATIVITY-DEFECT-CLAIM](MUB6-COMMUTATIVITY-DEFECT-CLAIM.md) (OPEN)
- `APP-R-MUB6-INTERFACE-COUNTERMODEL` `DERIVED_LEAN`: [MUB6-INTERFACE-COUNTERMODEL](MUB6-INTERFACE-COUNTERMODEL.md) (PROVED_LEAN)
