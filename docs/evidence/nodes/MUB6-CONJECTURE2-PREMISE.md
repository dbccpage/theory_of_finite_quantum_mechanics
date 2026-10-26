# MUB6-CONJECTURE2-PREMISE

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Matolcsi et al. Conjecture 2 (balanced Laurent vanishing on actual MUB triples) together with Conjecture 3 (no quartet contains a Szollosi family member) implies at most three MUBs in C^6 (Proposition 4.2); both conjectures are open.

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

- Matolcsi, Matszangosz, Varga, Weiner, Triplets of mutually unbiased bases, Proposition 4.2, doi:10.1007/s10801-026-01506-x

## Bottleneck

Locally only the count of 20 balanced sign masks among 64 and a declared row-count table are checked; AnalyticCubeSliceCertificate takes its row bound and table compatibility as fields. External: the alpha-vanishing part of Conjecture 2 for every order-6 complex Hadamard matrix not equivalent to the Tao matrix is a theorem of the OpenAI companion paper (Lean: OAI.MUB6.fourier_vanishing; external, not built here, see MUB6-OPENAI-FAMILY-LE-FIVE). Still open: the condition coupling the characters at 3a, Tao-class transitions inside triplets, Conjecture 3 and Proposition 4.2.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-075 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/25_mub/tfq_1252_mub6_conjecture2_premise.md`

- file: [dag/derivations/25_mub/tfq_1252_mub6_conjecture2_premise.md](../../../dag/derivations/25_mub/tfq_1252_mub6_conjecture2_premise.md)
- sha256 (`lf-normalised`): `bcbac129ee27a54d04221f9345baa31f0f02c6a5df1574e4f4538ad67bbb84c1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1252
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `31ddd89d2594bb5ad401aadb99a3a91edb6ea8e33158386031a40b1dc36f7223`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/mub6_claim_ledger.md`

- file: [papers/core/mub6/mub6_claim_ledger.md](../../../papers/core/mub6/mub6_claim_ledger.md)
- sha256 (`lf-normalised`): `e21c9d2f20bd0e87979c8b003ab6e2c60422c19cfdd0117308db09ec10c47f7a`
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

- `APP-R-MUB6-CONJECTURE2-PREMISE` `GAP_NO_DERIVATION`: [MUB6-TAO-MATRIX-CHM](MUB6-TAO-MATRIX-CHM.md) (PROVED_LEAN), [MUB6-GLOBAL-OBLIGATIONS](MUB6-GLOBAL-OBLIGATIONS.md) (OPEN)

Outgoing (1):

- `APP-R-MUB6-TAO-LAURENT-NORM-NINE` `DERIVED_LEAN`: [MUB6-TAO-LAURENT-NORM-NINE](MUB6-TAO-LAURENT-NORM-NINE.md) (PROVED_LEAN)
