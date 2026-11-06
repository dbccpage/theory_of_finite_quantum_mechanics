# MUB6-OPENAI-FAMILY-LE-FIVE

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Every family of pairwise mutually unbiased orthonormal bases of C^6 has at most five members (N(6) \<= 5): OpenAI's Lean theorem OAI.MUB6.family_size_le_five (github.com/openai/math, commit 1581d4cbdd69a0faf34b2089614fe2a814316a6a, Apache-2.0), via the exact mixed-moment Gram certificate no_seven_mutually_unbiased_bases and Weiner's completion six_extend_to_seven.

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

- OpenAI, Lean OAI.MUB6.family_size_le_five and OAI.MUB6.fourier_and_family_bound, github.com/openai/math lean/OAI/Analysis/MutuallyUnbiased (commit 1581d4cbdd69a0faf34b2089614fe2a814316a6a, Apache-2.0); companion paper Exact Fourier certificates for complex Hadamard matrices of order six (2026-09-24)

## Bottleneck

External and not built here: the upstream proof (3381 Lean files, about 205 MB, Lean 4.34.1 and its own Mathlib commit) is neither vendored nor replayed. lean4/MubOpenAIBridge.lean states the repository-type consequence conditionally on OpenAIFamilyBound; it compiled on 2026-10-21 under Lean 4.35.0 and Mathlib v4.35.0 with exit code 0 and only propext, Classical.choice and Quot.sound (mub_openai_bridge_compile_receipt.md). The bound itself is not proved here. OpenAI N(6)=3 is recorded as external context only: a binary64 seed-cover, Stage A/B/C and clique-search pipeline whose code and run archive are unreleased (verification/ returns 404) and whose Lean tree does not formalize it; it is not imported. MUB6-NO-QUARTET-D6 and MUB6-MAX-MUB-SIX-EQUALS-THREE stay OPEN.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-IMPORT-OPENAI-LE5 claims IMPORTED_ASSUMPTION; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/25_mub/tfq_1365_mub6_openai_family_le_five.md`

- file: [dag/derivations/25_mub/tfq_1365_mub6_openai_family_le_five.md](../../../dag/derivations/25_mub/tfq_1365_mub6_openai_family_le_five.md)
- sha256 (`lf-normalised`): `d2a79fe2c336b509f08e3c94a1a7d06a01605070ef4208ba15595f91633a83e6`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1365
- counts toward the grade: no

### Documents and data: `papers/core/mub6/documentation/mub6_master_classification_and_openai_comparative_synthesis.md`

- file: [papers/core/mub6/documentation/mub6_master_classification_and_openai_comparative_synthesis.md](../../../papers/core/mub6/documentation/mub6_master_classification_and_openai_comparative_synthesis.md)
- sha256 (`lf-normalised`): `553804840511c2e6fcc48f0c9d1c7e418f1130fdccbc184e16faf2a0797b96b7`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/documentation/openai_mub6_le5_external_import.md`

- file: [papers/core/mub6/documentation/openai_mub6_le5_external_import.md](../../../papers/core/mub6/documentation/openai_mub6_le5_external_import.md)
- sha256 (`lf-normalised`): `09ebb4f28b5e74734d1be30202c6f83c482370d7c9c1e4e874813d135d297eeb`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-OPENAI-FAMILY-LE-FIVE` `CONDITIONAL_ON_IMPORT`: [MUB6-GLOBAL-OBLIGATIONS](MUB6-GLOBAL-OBLIGATIONS.md) (OPEN)

Outgoing (0):

