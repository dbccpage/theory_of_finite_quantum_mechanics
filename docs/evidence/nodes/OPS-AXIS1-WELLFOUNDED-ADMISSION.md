# OPS-AXIS1-WELLFOUNDED-ADMISSION

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Axis 1 of WDP-CH14-T01 under the hypothesis that admission is the Genesis calculus, in which every AdmitInst depends on a previously admitted base datum: with no base instance no rule instance is admitted (the Genesis theorem collapsed_of_no_insts), so the process has nothing to certify. It says nothing about other shapes of admission. Imported by name: the theorem is Genesis's.

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

- Genesis theorem collapsed_of_no_insts: with no base instance no rule instance is admitted (assumption; cited by name, not re-run)

## Bottleneck

Cited by name, not re-run. WDP-CH14 has no node in this graph; the closest node is the admission gate PGW-GO-ADMISSION-GATE, and no source relates the two.

## Source status

Ledger row L035-C1, status cited. Only a pinned copy of the Genesis claim ledger is in the source repository, and the note did not re-run it. This repository has not re-run it either.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2524_ops_axis1_wellfounded_admission.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2524_ops_axis1_wellfounded_admission.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2524_ops_axis1_wellfounded_admission.md)
- sha256 (`lf-normalised`): `63510859551560e5d0bb5f4c097c14876951e0adb1f146bb8be5f4bc6106cc3d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2524
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md)
- sha256 (`lf-normalised`): `da99779add73314574622d0db46ea4dfbc9b66c4938caf29ab98590033592ab4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md)
- sha256 (`lf-normalised`): `649532625cf9e8ec085a420fd1bad9227fcc4dae9f06ba02be1eb19f497e3ec7`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `OPS-R-AXIS1-WELLFOUNDED-ADMISSION` `GAP_NO_DERIVATION`: [PGW-GO-ADMISSION-GATE](PGW-GO-ADMISSION-GATE.md) (DEFINITION)

Outgoing (0):

