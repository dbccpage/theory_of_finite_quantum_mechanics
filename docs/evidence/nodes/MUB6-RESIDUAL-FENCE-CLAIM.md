# MUB6-RESIDUAL-FENCE-CLAIM

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claim: the residual norm satisfies ||f(x)|| \>= 0.043 along the Haagerup and Szollosi families via Lipschitz constants and certified balls around grid samples.

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

No Lipschitz certificate or grid receipt supports this; gap G3 is PARTIAL and the deltoid-cover margin 37249/90000 comes from a candidate box containing no unbiased basis (MUB6-C19).

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-079 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/25_mub/tfq_1245_mub6_residual_fence_claim.md`

- file: [dag/derivations/25_mub/tfq_1245_mub6_residual_fence_claim.md](../../../dag/derivations/25_mub/tfq_1245_mub6_residual_fence_claim.md)
- sha256 (`lf-normalised`): `9410972c10e1ac1987351afe7327d967f1d64a65eaaaf2f1e17f23ec167c3b5f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1245
- counts toward the grade: no

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

- `APP-R-MUB6-RESIDUAL-FENCE-CLAIM` `GAP_NO_DERIVATION`: [MUB6-SZOLLOSI-TWO-CIRCULANT](MUB6-SZOLLOSI-TWO-CIRCULANT.md) (PROVED_LEAN), [MUB6-GLOBAL-OBLIGATIONS](MUB6-GLOBAL-OBLIGATIONS.md) (OPEN)

Outgoing (0):

