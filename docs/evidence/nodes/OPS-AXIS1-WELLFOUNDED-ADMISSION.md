# OPS-AXIS1-WELLFOUNDED-ADMISSION

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Axis 1 of WDP-CH14-T01 under the hypothesis that admission is the Genesis calculus, in which every AdmitInst depends on a previously admitted base datum: with no base instance no rule instance is admitted (the Genesis theorem collapsed_of_no_insts), so the process has nothing to certify. It says nothing about other shapes of admission. Imported by name: the theorem is Genesis's.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 15
- distinct cited Lean declarations covered by a current replay receipt: 15
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Genesis theorem collapsed_of_no_insts: with no base instance no rule instance is admitted (assumption; cited by name, not re-run)

## Bottleneck

Cited by name, not re-run. WDP-CH14 has no node in this graph; the closest node is the admission gate PGW-GO-ADMISSION-GATE, and no source relates the two. The finite chain is a separate checked case and does not re-run collapsed_of_no_insts.

## Source status

Ledger row L035-C1, status cited. Only a pinned copy of the Genesis claim ledger is in the source repository, and the note did not re-run it. This repository has not re-run it either.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ObserverPresheafAxis1WellfoundedAdmission.lean`

- file: [lean4/ObserverPresheafAxis1WellfoundedAdmission.lean](../../../lean4/ObserverPresheafAxis1WellfoundedAdmission.lean)
- sha256 (`bytes`): `8fb9fa4432cc9e8b8255d3b6d5c7fb67ef18630b4fa9dc5c6626526a621e6056`
- cited in: node.source, receipt dag/research/campaign_ops-axis1-wellfounded-admission_lean_replay.json (ObserverPresheafAxis1WellfoundedAdmission), record TFQ-2524
- replay: `verified`
  - receipt [dag/research/campaign_ops-axis1-wellfounded-admission_lean_replay.json](../../../dag/research/campaign_ops-axis1-wellfounded-admission_lean_replay.json) (module `ObserverPresheafAxis1WellfoundedAdmission`): recorded sha256 `8fb9fa4432cc9e8b8255d3b6d5c7fb67ef18630b4fa9dc5c6626526a621e6056` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build ObserverPresheafAxis1WellfoundedAdmission`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ObserverPresheafAxis1WellfoundedAdmission.adm0` | yes | yes | yes | propext | `#print axioms ObserverPresheafAxis1WellfoundedAdmission.adm0` |
| `ObserverPresheafAxis1WellfoundedAdmission.adm1` | yes | yes | yes | propext | `#print axioms ObserverPresheafAxis1WellfoundedAdmission.adm1` |
| `ObserverPresheafAxis1WellfoundedAdmission.adm2` | yes | yes | yes | propext | `#print axioms ObserverPresheafAxis1WellfoundedAdmission.adm2` |
| `ObserverPresheafAxis1WellfoundedAdmission.none0` | yes | yes | yes | propext | `#print axioms ObserverPresheafAxis1WellfoundedAdmission.none0` |
| `ObserverPresheafAxis1WellfoundedAdmission.none1` | yes | yes | yes | propext | `#print axioms ObserverPresheafAxis1WellfoundedAdmission.none1` |
| `ObserverPresheafAxis1WellfoundedAdmission.none2` | yes | yes | yes | propext | `#print axioms ObserverPresheafAxis1WellfoundedAdmission.none2` |
| `ObserverPresheafAxis1WellfoundedAdmission.pred0` | yes | yes | yes | propext | `#print axioms ObserverPresheafAxis1WellfoundedAdmission.pred0` |
| `ObserverPresheafAxis1WellfoundedAdmission.pred1` | yes | yes | yes | propext | `#print axioms ObserverPresheafAxis1WellfoundedAdmission.pred1` |
| `ObserverPresheafAxis1WellfoundedAdmission.pred2` | yes | yes | yes | propext | `#print axioms ObserverPresheafAxis1WellfoundedAdmission.pred2` |
| `ObserverPresheafAxis1WellfoundedAdmission.zb0` | yes | yes | yes | propext | `#print axioms ObserverPresheafAxis1WellfoundedAdmission.zb0` |
| `ObserverPresheafAxis1WellfoundedAdmission.zb1` | yes | yes | yes | propext | `#print axioms ObserverPresheafAxis1WellfoundedAdmission.zb1` |
| `ObserverPresheafAxis1WellfoundedAdmission.zb2` | yes | yes | yes | propext | `#print axioms ObserverPresheafAxis1WellfoundedAdmission.zb2` |
| `ObserverPresheafAxis1WellfoundedAdmission.zero0` | yes | yes | yes | propext | `#print axioms ObserverPresheafAxis1WellfoundedAdmission.zero0` |
| `ObserverPresheafAxis1WellfoundedAdmission.zero1` | yes | yes | yes | propext | `#print axioms ObserverPresheafAxis1WellfoundedAdmission.zero1` |
| `ObserverPresheafAxis1WellfoundedAdmission.zero2` | yes | yes | yes | propext | `#print axioms ObserverPresheafAxis1WellfoundedAdmission.zero2` |

- counts toward the grade: yes

### Python: `checks/independent/ops-axis1-wellfounded-admission.py`

- file: [checks/independent/ops-axis1-wellfounded-admission.py](../../../checks/independent/ops-axis1-wellfounded-admission.py)
- sha256 (`bytes`): `54d781108232627123c6cb7612ce0a29e85d1e1427e77023a22a370066d214b7`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2524_ops_axis1_wellfounded_admission.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2524_ops_axis1_wellfounded_admission.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2524_ops_axis1_wellfounded_admission.md)
- sha256 (`lf-normalised`): `804ec8a0415a21ba89b81fb7801c1148e1d7d5ba497ecf157bf8412050c5982b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2524
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/ops-axis1-wellfounded-admission.md`

- file: [dag/derivations/independent/ops-axis1-wellfounded-admission.md](../../../dag/derivations/independent/ops-axis1-wellfounded-admission.md)
- sha256 (`lf-normalised`): `d69ed749cf9299c23fbb9f02ec9ba4b85bc5db864b9738c145b96aad71334edc`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ops-axis1-wellfounded-admission_lean_replay.json`

- file: [dag/research/campaign_ops-axis1-wellfounded-admission_lean_replay.json](../../../dag/research/campaign_ops-axis1-wellfounded-admission_lean_replay.json)
- sha256 (`lf-normalised`): `2a655c87b7b3d79eaa943fc852f403e217bb343fb28dac7c3fdcdf7c7be71618`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md`

- file: [sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md](../../../sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md)
- sha256 (`lf-normalised`): `da99779add73314574622d0db46ea4dfbc9b66c4938caf29ab98590033592ab4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md`

- file: [sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md](../../../sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md)
- sha256 (`lf-normalised`): `ae5564735bb6591e0f149868f83bd9f9793f297be0f8af3cc889c293ae4059cb`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `OPS-R-AXIS1-WELLFOUNDED-ADMISSION` `GAP_NO_DERIVATION`: [PGW-GO-ADMISSION-GATE](PGW-GO-ADMISSION-GATE.md) (DEFINITION)

Outgoing (0):

