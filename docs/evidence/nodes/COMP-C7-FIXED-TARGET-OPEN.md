# COMP-C7-FIXED-TARGET-OPEN

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Adding erasing rules so that every halting word reduces to one fixed word should make Reach to that fixed word undecidable; this is not proved here.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Still open: Reach of the extended rule set R0 prime from startWord x to one fixed target word exactly when univFun x is defined.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C7d claims OPEN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignCompC7FixedTargetOpen.lean`

- file: [lean4/CampaignCompC7FixedTargetOpen.lean](../../../lean4/CampaignCompC7FixedTargetOpen.lean)
- sha256 (`bytes`): `fdf8c22aad238c9fc90ae8988290b8d214e29ceaf050e6246f5c8f49265a5347`
- cited in: node.lean, receipt dag/research/campaign_comp-c7-fixed-target-open_lean_replay.json (CampaignCompC7FixedTargetOpen), receipt dag/research/pr_369_review_replay.json (CampaignCompC7FixedTargetOpen), record TFQ-1311
- replay: `verified`
  - receipt [dag/research/campaign_comp-c7-fixed-target-open_lean_replay.json](../../../dag/research/campaign_comp-c7-fixed-target-open_lean_replay.json) (module `CampaignCompC7FixedTargetOpen`): recorded sha256 `fdf8c22aad238c9fc90ae8988290b8d214e29ceaf050e6246f5c8f49265a5347` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_369_review_replay.json](../../../dag/research/pr_369_review_replay.json) (module `CampaignCompC7FixedTargetOpen`): recorded sha256 `fdf8c22aad238c9fc90ae8988290b8d214e29ceaf050e6246f5c8f49265a5347` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignCompC7FixedTargetOpen`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `eraseOneToFixed` | yes | yes | yes | none | `#print axioms eraseOneToFixed` |
| `eraseTwoToFixed` | yes | yes | yes | none | `#print axioms eraseTwoToFixed` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1311_comp_c7_fixed_target_open.md`

- file: [dag/derivations/29_computation/tfq_1311_comp_c7_fixed_target_open.md](../../../dag/derivations/29_computation/tfq_1311_comp_c7_fixed_target_open.md)
- sha256 (`lf-normalised`): `877ac54aeb7b92ec57b919e55dde2099352e89f402fe0a473e4e02a302318c13`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1311
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C7-FIXED-TARGET-OPEN` `GAP_NO_DERIVATION`: [COMP-C7-NF-REACH-UNDECIDABLE](COMP-C7-NF-REACH-UNDECIDABLE.md) (PROVED_LEAN)

Outgoing (0):

