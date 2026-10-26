# MUB6-PSI-GLUING-CLAIM

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `OPEN`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claim: a basis-gluing map Psi on dephased 6x6 complex Hadamard matrices is a strict contraction whose fixed point has an overlap deficiency, so gluing any candidate fourth basis violates unbiasedness.

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

Residual R4 is FORMALIZED_CONDITIONAL only: Gluing.lean links a supplied vector curvature wall to non-extension under BasisVectorMUContract over the opaque type Basis; no contraction estimate exists.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-DERIV-081 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/25_mub/tfq_1247_mub6_psi_gluing_claim.md`

- file: [dag/derivations/25_mub/tfq_1247_mub6_psi_gluing_claim.md](../../../dag/derivations/25_mub/tfq_1247_mub6_psi_gluing_claim.md)
- sha256 (`lf-normalised`): `533cc110cc6c383470f271fb4db5ebae4b09152222c76d93221624de39adfef2`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1247
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `31ddd89d2594bb5ad401aadb99a3a91edb6ea8e33158386031a40b1dc36f7223`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.jsonl`

- file: [papers/core/mub6/theory_of_finite_mub6.jsonl](../../../papers/core/mub6/theory_of_finite_mub6.jsonl)
- sha256 (`lf-normalised`): `79a8e74d457a2c236999a6a1dcd1ff010f0f878b245c205f5f049add18ae2234`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/theory_of_finite_mub6.md`

- file: [papers/core/mub6/theory_of_finite_mub6.md](../../../papers/core/mub6/theory_of_finite_mub6.md)
- sha256 (`lf-normalised`): `4df95e7f697d7ab11bfa44f282353267197198f74bcfb535e5f10c18ffbeabf5`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-PSI-GLUING-CLAIM` `GAP_NO_DERIVATION`: [MUB6-GLUING-G3-OPAQUE](MUB6-GLUING-G3-OPAQUE.md) (PROVED_LEAN), [MUB6-GLOBAL-OBLIGATIONS](MUB6-GLOBAL-OBLIGATIONS.md) (OPEN)

Outgoing (1):

- `APP-R-MUB6-PHI1-CIRCULATION-CLAIM` `GAP_NO_DERIVATION`: [MUB6-PHI1-CIRCULATION-CLAIM](MUB6-PHI1-CIRCULATION-CLAIM.md) (OPEN)
