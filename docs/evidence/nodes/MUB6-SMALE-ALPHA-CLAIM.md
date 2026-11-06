# MUB6-SMALE-ALPHA-CLAIM

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claim: Smale alpha-theory gives alpha(f,x) \> 1 at every candidate point, so no point lies in the quadratic convergence basin of a root of the MUB(6) system.

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

No alpha computation over a covering set is in the checkout; SmalePointCertificate and KrawczykContractor carry root and uniqueness as fields and krawczyk_inclusion_criterion projects them.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-078 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/25_mub/tfq_1244_mub6_smale_alpha_claim.md`

- file: [dag/derivations/25_mub/tfq_1244_mub6_smale_alpha_claim.md](../../../dag/derivations/25_mub/tfq_1244_mub6_smale_alpha_claim.md)
- sha256 (`lf-normalised`): `8694c2cb8639dfcfc87bb4706a543a9020d1b8e77b96090f49210b3bc35f9afb`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1244
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `31ddd89d2594bb5ad401aadb99a3a91edb6ea8e33158386031a40b1dc36f7223`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/mub6_claim_ledger.md`

- file: [papers/core/mub6/mub6_claim_ledger.md](../../../papers/core/mub6/mub6_claim_ledger.md)
- sha256 (`lf-normalised`): `b4860d325cad8aba746008e05faad7679f560d99e9967da0503ce80d2af36807`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.jsonl`

- file: [papers/core/mub6/theory_of_finite_mub6.jsonl](../../../papers/core/mub6/theory_of_finite_mub6.jsonl)
- sha256 (`lf-normalised`): `815b535641140895e823e99e201cf3314a9054db022f5a0c35be601a18663839`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.md`

- file: [papers/core/mub6/theory_of_finite_mub6.md](../../../papers/core/mub6/theory_of_finite_mub6.md)
- sha256 (`lf-normalised`): `0e5866c8c56eb624576b512e2f51f0378271797285bb11c764a9708a234085e1`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-SMALE-ALPHA-CLAIM` `GAP_NO_DERIVATION`: [MUB6-KRAWCZYK-GLOBAL-COVER-CLAIM](MUB6-KRAWCZYK-GLOBAL-COVER-CLAIM.md) (OPEN), [MUB6-GLOBAL-OBLIGATIONS](MUB6-GLOBAL-OBLIGATIONS.md) (OPEN)

Outgoing (0):

