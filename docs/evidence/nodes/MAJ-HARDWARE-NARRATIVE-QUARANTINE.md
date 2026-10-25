# MAJ-HARDWARE-NARRATIVE-QUARANTINE

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Device baths, continuum BdG spectra, fabrication narratives, conductance peaks 2e^2/h, gap protocols and capacitance shifts C_Q are external observer projections: they may motivate which complex to declare but do not populate F2 receipts or mint authority without a validated realization map.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declaration references covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A realization map that would lift this quarantine is not supplied.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-C10 claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1165
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `detector_inadequate_when_kernel_nontrivial` | yes | yes | yes | none | `#print axioms detector_inadequate_when_kernel_nontrivial` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1165_maj_hardware_narrative_quarantine.md`

- file: [dag/derivations/28_majorana/tfq_1165_maj_hardware_narrative_quarantine.md](../../../dag/derivations/28_majorana/tfq_1165_maj_hardware_narrative_quarantine.md)
- sha256 (`lf-normalised`): `528cc985d4f285dd314d4fcc33813e34018b516ce4ee3ff0b0a8774248e6816e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1165
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

- `APP-R-MAJ-HARDWARE-NARRATIVE-QUARANTINE` `DERIVED_PROSE`: [MAJ-REALIZATION-PACKET-GAP](MAJ-REALIZATION-PACKET-GAP.md) (DEFINITION)

Outgoing (5):

- `APP-R-MAJ-BINDING-NONCLAIMS` `DERIVED_PROSE`: [MAJ-BINDING-NONCLAIMS](MAJ-BINDING-NONCLAIMS.md) (DEFINITION)
- `APP-R-MAJ-IMPORT-ISING-ANYONS` `CONDITIONAL_ON_IMPORT`: [MAJ-IMPORT-ISING-ANYONS](MAJ-IMPORT-ISING-ANYONS.md) (IMPORTED_ASSUMPTION)
- `APP-R-MAJ-IMPORT-KITAEV-CHAIN` `CONDITIONAL_ON_IMPORT`: [MAJ-IMPORT-KITAEV-CHAIN](MAJ-IMPORT-KITAEV-CHAIN.md) (IMPORTED_ASSUMPTION)
- `APP-R-MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE` `GAP_NO_DERIVATION`: [MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE](MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE.md) (OPEN)
- `APP-R-MAJ-PARITY-OBSERVABLE-FENCE` `DERIVED_PROSE`: [MAJ-PARITY-OBSERVABLE-FENCE](MAJ-PARITY-OBSERVABLE-FENCE.md) (DEFINITION)
