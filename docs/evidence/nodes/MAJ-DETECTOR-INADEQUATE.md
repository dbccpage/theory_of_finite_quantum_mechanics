# MAJ-DETECTOR-INADEQUATE

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A measurement projection M is DETECTOR_INADEQUATE for a hypothesis pair when two distinct candidate states have the same readout (rho1 - rho2 in ker M), so the protocol cannot discriminate them.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Which laboratory maps M are adequate is the open program MAJ-OPEN-EVIDENCE-ADEQUACY.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-DEF-DETECTOR-INADEQUATE claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1163
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `MeasurementProjection` | yes | yes | yes | none | `#print axioms MeasurementProjection` |
| `detector_inadequate` | yes | yes | yes | none | `#print axioms detector_inadequate` |
| `detector_inadequate_when_kernel_nontrivial` | yes | yes | yes | none | `#print axioms detector_inadequate_when_kernel_nontrivial` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1163_maj_detector_inadequate.md`

- file: [dag/derivations/28_majorana/tfq_1163_maj_detector_inadequate.md](../../../dag/derivations/28_majorana/tfq_1163_maj_detector_inadequate.md)
- sha256 (`lf-normalised`): `2f237a1ce119deb6abe2b55cf9bb97ea412f39e58c4163794a5000a7d74af738`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1163
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-DETECTOR-INADEQUATE` `DERIVED_PROSE`: [MAJ-REALIZATION-PACKET-GAP](MAJ-REALIZATION-PACKET-GAP.md) (DEFINITION)

Outgoing (2):

- `APP-R-MAJ-OPEN-EVIDENCE-ADEQUACY` `GAP_NO_DERIVATION`: [MAJ-OPEN-EVIDENCE-ADEQUACY](MAJ-OPEN-EVIDENCE-ADEQUACY.md) (OPEN)
- `APP-R-MAJ-SYNDROME-READOUT-INADEQUATE` `COMPUTED`: [MAJ-SYNDROME-READOUT-INADEQUATE](MAJ-SYNDROME-READOUT-INADEQUATE.md) (COMPUTATIONALLY_CHECKED)
