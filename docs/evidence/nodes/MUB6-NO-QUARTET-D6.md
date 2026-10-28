# MUB6-NO-QUARTET-D6

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Open problem: no four pairwise mutually unbiased bases exist in C^6.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
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

The corpus certifies exact reductions (quartet existence iff solutions of the 618-, 648- or 666-equation quadratic systems in stated boxes), conditional implications over supplied premises, and exclusion of the regions in MUB6-C28 and MUB6-PAPER-CLOSE-COLUMNS; it does not cover the full boxes, the six charts, the 56 family cells, the three cusp collars, or triples outside the Szollosi parameterization. N(6) \<= 5 is recorded separately as MUB6-OPENAI-FAMILY-LE-FIVE (external theorem of OpenAI, not built here); it does not decide whether a quartet exists. OpenAI N(6)=3 is recorded as external context only: a binary64 seed-cover, Stage A/B/C and clique-search pipeline whose code and run archive are unreleased (verification/ returns 404) and whose Lean tree does not formalize it; it is not imported.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-085 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/25_mub/tfq_1254_mub6_no_quartet_d6.md`

- file: [dag/derivations/25_mub/tfq_1254_mub6_no_quartet_d6.md](../../../dag/derivations/25_mub/tfq_1254_mub6_no_quartet_d6.md)
- sha256 (`lf-normalised`): `f826409db6e7ec0352b766c4e656965130632db9ea4a9115deda11c5d9548264`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1254
- counts toward the grade: no

### Documents and data: `papers/core/mub6/README.md`

- file: [papers/core/mub6/README.md](../../../papers/core/mub6/README.md)
- sha256 (`lf-normalised`): `b876520ea3960bef932e3723a1c47c60d05dace398dcb9a77518b724d8216f8e`
- cited in: node.source
- counts toward the grade: yes

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

- `APP-R-MUB6-NO-QUARTET-D6` `GAP_NO_DERIVATION`: [MUB6-GLOBAL-OBLIGATIONS](MUB6-GLOBAL-OBLIGATIONS.md) (OPEN), [MUB6-FIVE-BRANCH-ROUTING-CLAIM](MUB6-FIVE-BRANCH-ROUTING-CLAIM.md) (OPEN)

Outgoing (1):

- `APP-R-MUB6-MAX-MUB-SIX-EQUALS-THREE` `GAP_NO_DERIVATION`: [MUB6-MAX-MUB-SIX-EQUALS-THREE](MUB6-MAX-MUB-SIX-EQUALS-THREE.md) (OPEN)
