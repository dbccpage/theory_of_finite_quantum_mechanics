# MAJ-SYNDROME-READOUT-INADEQUATE

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the 2x2 tetron torus the column and row logical representatives are distinct cochains with equal zero syndrome d1 w, so the readout M(w) = d1 w is DETECTOR_INADEQUATE for them.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Fixed instance; the adequacy of a syndrome-plus-class readout is asserted, not computed.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-COMP-SYNDROME-READOUT claims COMPUTATIONALLY_CHECKED; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/src/majorana/majorana_transfer_bounds.py`

- file: [code/python/src/majorana/majorana_transfer_bounds.py](../../../code/python/src/majorana/majorana_transfer_bounds.py)
- sha256 (`bytes`): `f14bf9dd639ec68e1e01d5d970cea8c5b36bcddfe066d2b3be00454a18f70737`
- cited in: record TFQ-1164

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `DetectorAdequacyAudit.audit_syndrome_readout` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/majorana/test_tetron_surface_codes.py`

- file: [code/python/src/majorana/test_tetron_surface_codes.py](../../../code/python/src/majorana/test_tetron_surface_codes.py)
- sha256 (`bytes`): `6577a59d6a74b23a3f5a356b1ffaf308140451939f7541f472ac0de58bf6747e`
- cited in: record TFQ-1164
- check: `python -m pytest code/python/src/majorana/test_tetron_surface_codes.py::test_detector_adequacy_syndrome_vs_homology`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_detector_adequacy_syndrome_vs_homology` (python_test) | yes | yes | yes | - | `python -m pytest code/python/src/majorana/test_tetron_surface_codes.py::test_detector_adequacy_syndrome_vs_homology` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1164_maj_syndrome_readout_inadequate.md`

- file: [dag/derivations/28_majorana/tfq_1164_maj_syndrome_readout_inadequate.md](../../../dag/derivations/28_majorana/tfq_1164_maj_syndrome_readout_inadequate.md)
- sha256 (`lf-normalised`): `2fc5eb849562df679f036915265481997727aab9f3fb1c2b69c55cf941af311d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1164
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `2f55c0f24f87388cfa9d7a4a7d832f34c0fa30b857d344811f4336f634c1684b`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-SYNDROME-READOUT-INADEQUATE` `COMPUTED`: [MAJ-DETECTOR-INADEQUATE](MAJ-DETECTOR-INADEQUATE.md) (DEFINITION), [MAJ-TETRON-BETTI-COMPUTED](MAJ-TETRON-BETTI-COMPUTED.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

