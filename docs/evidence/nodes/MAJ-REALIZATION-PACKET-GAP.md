# MAJ-REALIZATION-PACKET-GAP

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The Majorana problem is the gap between continuum open-system device narratives (nanowires, zero-bias peaks, interferometric parity readout) and declared finite algebraic schedules (F2 cochain homology, Ising matrices): neither discharges the verification conditions of the other without an explicit realization map.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
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

A validated realization map from a device to a declared complex is not supplied by this source.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-C1 claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1162
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `detector_inadequate_when_kernel_nontrivial` | yes | yes | yes | none | `#print axioms detector_inadequate_when_kernel_nontrivial` |
| `transfer_gap_strictly_positive` | yes | yes | yes | none | `#print axioms transfer_gap_strictly_positive` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1162_maj_realization_packet_gap.md`

- file: [dag/derivations/28_majorana/tfq_1162_maj_realization_packet_gap.md](../../../dag/derivations/28_majorana/tfq_1162_maj_realization_packet_gap.md)
- sha256 (`lf-normalised`): `4342910be4fe72422ba42c5500eb288f08542f4576b2629b55b36161fd73c2c2`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1162
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem_claim_ledger.md`

- file: [papers/core/majorana/the_majorana_problem_claim_ledger.md](../../../papers/core/majorana/the_majorana_problem_claim_ledger.md)
- sha256 (`lf-normalised`): `2d2b91881568780f56d7cdb53c97eec42bbfa09c21b2f1c6302665a79aad7565`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-REALIZATION-PACKET-GAP` `DERIVED_PROSE`: [DS-QM212-MAJORANA-PROBLEM](DS-QM212-MAJORANA-PROBLEM.md) (PROVED_LEAN), [MAJ-F2-PARITY-SCHEDULE](MAJ-F2-PARITY-SCHEDULE.md) (DEFINITION)

Outgoing (4):

- `APP-R-MAJ-BINDING-NONCLAIMS` `DERIVED_PROSE`: [MAJ-BINDING-NONCLAIMS](MAJ-BINDING-NONCLAIMS.md) (DEFINITION)
- `APP-R-MAJ-DETECTOR-INADEQUATE` `DERIVED_PROSE`: [MAJ-DETECTOR-INADEQUATE](MAJ-DETECTOR-INADEQUATE.md) (DEFINITION)
- `APP-R-MAJ-HARDWARE-NARRATIVE-QUARANTINE` `DERIVED_PROSE`: [MAJ-HARDWARE-NARRATIVE-QUARANTINE](MAJ-HARDWARE-NARRATIVE-QUARANTINE.md) (DEFINITION)
- `APP-R-MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE` `GAP_NO_DERIVATION`: [MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE](MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE.md) (OPEN)
