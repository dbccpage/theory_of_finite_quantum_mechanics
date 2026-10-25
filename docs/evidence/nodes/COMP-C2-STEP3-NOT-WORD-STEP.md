# COMP-C2-STEP3-NOT-WORD-STEP

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Appending 1 takes the list \[0\] to \[0, 1\] by one hole replacement of an empty block. Appending the block \[0, 1\] takes \[0, 1\] to \[0, 1, 0, 1\] by one hole replacement of an empty block. Deleting a final 1 takes \[0, 1\] to \[0\] by one hole replacement of the block \[1\]. The map sending 1 to 0 and every other natural number to itself sends both 0 and 1 to 0.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Still open: an encoding of every Genesis Step3 state, with a finite term set, a finite assertion set and two named terms, under which add-term, add-assertion and identify are word steps, or a demonstration that none exists.

## Source status

dag/research/genesis_to_universal_computation.md record COMP-C2e claims OPEN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `dag/results/PG-GEN-REWRITING-COMMUTATION/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Second/Rename.lean`

- file: [dag/results/PG-GEN-REWRITING-COMMUTATION/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Second/Rename.lean](../../../dag/results/PG-GEN-REWRITING-COMMUTATION/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Second/Rename.lean)
- sha256 (`bytes`): `7345c48641a53a32a4952f3cd3900d3c4ef7e98e3f353df489e32429fed9a0b3`
- cited in: node.source
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains dag/results/PG-GEN-REWRITING-COMMUTATION/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/lean4/Second/Rename.lean`
- counts toward the grade: yes

### Lean: `lean4/CampaignCompC2Step3NotWordStep.lean`

- file: [lean4/CampaignCompC2Step3NotWordStep.lean](../../../lean4/CampaignCompC2Step3NotWordStep.lean)
- sha256 (`bytes`): `78a438a504c33f16b0e5507aea5bf721cdc16f24ecb5ecadfabf61352d63976c`
- cited in: node.lean, receipt dag/research/campaign_comp-c2-step3-not-word-step_lean_replay.json (CampaignCompC2Step3NotWordStep), receipt dag/research/pr_367_review_replay.json (CampaignCompC2Step3NotWordStep), record TFQ-1290
- replay: `verified`
  - receipt [dag/research/campaign_comp-c2-step3-not-word-step_lean_replay.json](../../../dag/research/campaign_comp-c2-step3-not-word-step_lean_replay.json) (module `CampaignCompC2Step3NotWordStep`): recorded sha256 `78a438a504c33f16b0e5507aea5bf721cdc16f24ecb5ecadfabf61352d63976c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
  - receipt [dag/research/pr_367_review_replay.json](../../../dag/research/pr_367_review_replay.json) (module `CampaignCompC2Step3NotWordStep`): recorded sha256 `78a438a504c33f16b0e5507aea5bf721cdc16f24ecb5ecadfabf61352d63976c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignCompC2Step3NotWordStep`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `addAssertionWordStep` | yes | yes | yes | none | `#print axioms addAssertionWordStep` |
| `addTermWordStep` | yes | yes | yes | none | `#print axioms addTermWordStep` |
| `identifyWordStep` | yes | yes | yes | none | `#print axioms identifyWordStep` |
| `merge01FixesOther` | yes | yes | yes | propext | `#print axioms merge01FixesOther` |
| `merge01SendsBothToZero` | yes | yes | yes | none | `#print axioms merge01SendsBothToZero` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1290_comp_c2_step3_not_word_step.md`

- file: [dag/derivations/29_computation/tfq_1290_comp_c2_step3_not_word_step.md](../../../dag/derivations/29_computation/tfq_1290_comp_c2_step3_not_word_step.md)
- sha256 (`lf-normalised`): `d07e119d5d72bc23d0c32faa1ac110df1abd2479f412450510d7da27438067fd`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1290
- counts toward the grade: no

### Documents and data: `dag/research/genesis_to_universal_computation.md`

- file: [dag/research/genesis_to_universal_computation.md](../../../dag/research/genesis_to_universal_computation.md)
- sha256 (`lf-normalised`): `cd295356e167596371d5d343daac62cbf7b7b26a136e67799f2bbbb7d810c418`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-COMP-C2-STEP3-NOT-WORD-STEP` `GAP_NO_DERIVATION`: [COMP-C2-LETTER-RENAME-COMMUTES](COMP-C2-LETTER-RENAME-COMMUTES.md) (PROVED_LEAN), [PG-GEN-REWRITING-COMMUTATION](PG-GEN-REWRITING-COMMUTATION.md) (PROVED_LEAN)

Outgoing (0):

