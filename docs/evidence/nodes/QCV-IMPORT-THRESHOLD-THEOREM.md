# QCV-IMPORT-THRESHOLD-THEOREM

Stage: [COMPUTATION](../stages/COMPUTATION.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The fault-tolerance threshold theorems (Shor 1996; Aharonov and Ben-Or 1997; Kitaev 1997; Knill, Laflamme and Zurek 1998; Aliferis, Gottesman and Preskill 2006) are cited under each theorem's own noise, locality and overhead hypotheses; they are not re-proved.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 19
- distinct cited Lean declarations covered by a current replay receipt: 9
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- threshold theorems for concatenated codes under their stated noise models

## Bottleneck

The fault-tolerance threshold theorems of Shor, Aharonov and Ben-Or, Kitaev, Knill, Laflamme and Zurek, and Aliferis, Gottesman and Preskill stay cited under each theorem's own noise, locality and overhead hypotheses. This integer orbit does not state those theorems, supplies no noise model, and identifies no code constant. The rational concatenation recurrence and its dichotomy stay on the concatenation-threshold record.

## Source status

dag/research/quantum_computation_self_obstruction.md record QCV-IMP-THRESHOLD claims IMPORTED_ASSUMPTION; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ThresholdTheoremImport.lean`

- file: [lean4/ThresholdTheoremImport.lean](../../../lean4/ThresholdTheoremImport.lean)
- sha256 (`bytes`): `b16952fa7f055afcb4f8ec5be0274cae786415c914beb9191640686be1567f0c`
- cited in: node.lean, receipt dag/research/campaign_qcv-import-threshold-theorem_lean_replay.json (ThresholdTheoremImport), record TFQ-1318
- replay: `verified`
  - receipt [dag/research/campaign_qcv-import-threshold-theorem_lean_replay.json](../../../dag/research/campaign_qcv-import-threshold-theorem_lean_replay.json) (module `ThresholdTheoremImport`): recorded sha256 `b16952fa7f055afcb4f8ec5be0274cae786415c914beb9191640686be1567f0c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build ThresholdTheoremImport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ThresholdTheoremImport.mul_eight` | yes | yes | yes | none | `#print axioms ThresholdTheoremImport.mul_eight` |
| `ThresholdTheoremImport.orbit_three` | yes | yes | yes | none | `#print axioms ThresholdTheoremImport.orbit_three` |
| `ThresholdTheoremImport.scale_one` | yes | yes | yes | none | `#print axioms ThresholdTheoremImport.scale_one` |
| `ThresholdTheoremImport.scale_zero` | yes | yes | yes | none | `#print axioms ThresholdTheoremImport.scale_zero` |
| `ThresholdTheoremImport.step_eight` | yes | yes | yes | none | `#print axioms ThresholdTheoremImport.step_eight` |
| `ThresholdTheoremImport.step_one` | yes | yes | yes | none | `#print axioms ThresholdTheoremImport.step_one` |
| `ThresholdTheoremImport.step_two` | yes | yes | yes | none | `#print axioms ThresholdTheoremImport.step_two` |
| `ThresholdTheoremImport.step_zero` | yes | yes | yes | none | `#print axioms ThresholdTheoremImport.step_zero` |
| `ThresholdTheoremImport.t_spec` | yes | yes | yes | none | `#print axioms ThresholdTheoremImport.t_spec` |
| `mul_eight` | yes | yes | yes | none | `#print axioms mul_eight` |
| `orbit_three` | yes | yes | yes | none | `#print axioms orbit_three` |
| `scale_one` | yes | yes | yes | none | `#print axioms scale_one` |
| `scale_zero` | yes | yes | yes | none | `#print axioms scale_zero` |
| `step_eight` | yes | yes | yes | none | `#print axioms step_eight` |
| `step_one` | yes | yes | yes | none | `#print axioms step_one` |
| `step_two` | yes | yes | yes | none | `#print axioms step_two` |
| `step_zero` | yes | yes | yes | none | `#print axioms step_zero` |
| `t_spec` | yes | yes | yes | none | `#print axioms t_spec` |

- counts toward the grade: yes

### Python: `checks/independent/qcv-import-threshold-theorem.py`

- file: [checks/independent/qcv-import-threshold-theorem.py](../../../checks/independent/qcv-import-threshold-theorem.py)
- sha256 (`bytes`): `8bf46e1641becc88f553aadef103df6d026dbf14a3f8010c8db7527ff7728204`
- cited in: record TFQ-1318

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `check` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/29_computation/tfq_1318_qcv_import_threshold_theorem.md`

- file: [dag/derivations/29_computation/tfq_1318_qcv_import_threshold_theorem.md](../../../dag/derivations/29_computation/tfq_1318_qcv_import_threshold_theorem.md)
- sha256 (`lf-normalised`): `b7bbbb4250baa2235a08164fd2a04c87e7f2dede5771adedad8ad79e550ced24`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1318
- counts toward the grade: no

### Documents and data: `dag/research/quantum_computation_self_obstruction.md`

- file: [dag/research/quantum_computation_self_obstruction.md](../../../dag/research/quantum_computation_self_obstruction.md)
- sha256 (`lf-normalised`): `8ae1b2ae291ee74f773da07740ebd0c1f98842bc01d7ec6a4d3c267e0077d178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-QCV-IMPORT-THRESHOLD-THEOREM` `CONDITIONAL_ON_IMPORT`: [DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE](DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE.md) (OPEN)

Outgoing (1):

- `APP-R-QCV-CONCATENATION-THRESHOLD-DICHOTOMY` `DERIVED_LEAN`: [QCV-CONCATENATION-THRESHOLD-DICHOTOMY](QCV-CONCATENATION-THRESHOLD-DICHOTOMY.md) (PROVED_LEAN)
