# COMP-C8-MINIMALITY-FENCE

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Mark A is the number 1, mark B is the number 2, and the blank is the number 0. The word mark A then mark B, followed by one blank cell, equals the list whose entries are 1, then 2, then 0. The blank differs from mark A, and the blank differs from mark B.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Simulation of a machine over a coded alphabet by a machine over the two marks and a blank stays open, and it is required before any minimality sentence. A sentence that composite machine M0 is not a smallest general-purpose machine stays open. Small-machine records stay literature only.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C8b claims OPEN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignCompC8MinimalityFence.lean`

- file: [lean4/CampaignCompC8MinimalityFence.lean](../../../lean4/CampaignCompC8MinimalityFence.lean)
- sha256 (`bytes`): `2fa4a9bed26ae6cb06d9f38f747e7e981f0266722c68c8e1d6ccb3fb37bf770d`
- cited in: node.lean, receipt dag/research/campaign_comp-c8-minimality-fence_lean_replay.json (CampaignCompC8MinimalityFence), receipt dag/research/pr_370_review_replay.json (CampaignCompC8MinimalityFence), record TFQ-1313
- replay: `verified`
  - receipt [dag/research/campaign_comp-c8-minimality-fence_lean_replay.json](../../../dag/research/campaign_comp-c8-minimality-fence_lean_replay.json) (module `CampaignCompC8MinimalityFence`): recorded sha256 `2fa4a9bed26ae6cb06d9f38f747e7e981f0266722c68c8e1d6ccb3fb37bf770d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_370_review_replay.json](../../../dag/research/pr_370_review_replay.json) (module `CampaignCompC8MinimalityFence`): recorded sha256 `2fa4a9bed26ae6cb06d9f38f747e7e981f0266722c68c8e1d6ccb3fb37bf770d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignCompC8MinimalityFence`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignCompC8MinimalityFence.blankDiffersFromMarks` | yes | yes | yes | none | `#print axioms CampaignCompC8MinimalityFence.blankDiffersFromMarks` |
| `CampaignCompC8MinimalityFence.oneWordThenBlank` | yes | yes | yes | none | `#print axioms CampaignCompC8MinimalityFence.oneWordThenBlank` |
| `blankDiffersFromMarks` | yes | yes | yes | none | `#print axioms blankDiffersFromMarks` |
| `oneWordThenBlank` | yes | yes | yes | none | `#print axioms oneWordThenBlank` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1313_comp_c8_minimality_fence.md`

- file: [dag/derivations/29_computation/tfq_1313_comp_c8_minimality_fence.md](../../../dag/derivations/29_computation/tfq_1313_comp_c8_minimality_fence.md)
- sha256 (`lf-normalised`): `a6d0ff20bccfdfffc0080748db3d390ae5f5238a7b2f46e1262429e1e996bbf4`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1313
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C8-MINIMALITY-FENCE` `GAP_NO_DERIVATION`: [COMP-C8-BINARY-CODING](COMP-C8-BINARY-CODING.md) (PROVED_LEAN), [COMP-C6-FINITE-MARKS](COMP-C6-FINITE-MARKS.md) (PROVED_LEAN)

Outgoing (0):

