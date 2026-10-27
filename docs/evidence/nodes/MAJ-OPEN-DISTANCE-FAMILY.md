# MAJ-OPEN-DISTANCE-FAMILY

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `OPEN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For all sizes the torus distance is min(rows, cols), the cylinder distance is rows + 1, and the diagonal class weight is rows + cols.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Prove the distance formulas (e.g. by a cut argument on the dual grid); the source gives a one-sentence traversal argument for additivity only.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-CLAIM-DISTANCE-FAMILY claims PROVED_PROSE; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `code/python/src/majorana/majorana_f2_trichotomy.py`

- file: [code/python/src/majorana/majorana_f2_trichotomy.py](../../../code/python/src/majorana/majorana_f2_trichotomy.py)
- sha256 (`bytes`): `d6ffe11ba0e9fd0ba5a4a467147b95cf560b3d4c860b845a025e3b0e5e283b7a`
- cited in: record TFQ-1156

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `TetronCarrier` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1156_maj_open_distance_family.md`

- file: [dag/derivations/28_majorana/tfq_1156_maj_open_distance_family.md](../../../dag/derivations/28_majorana/tfq_1156_maj_open_distance_family.md)
- sha256 (`lf-normalised`): `a6786a9aed195888ec9449778bfa90d5d4bc6341163ccab03149943cb3566ffb`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1156
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `2f55c0f24f87388cfa9d7a4a7d832f34c0fa30b857d344811f4336f634c1684b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem_change_log.md`

- file: [papers/core/majorana/the_majorana_problem_change_log.md](../../../papers/core/majorana/the_majorana_problem_change_log.md)
- sha256 (`lf-normalised`): `4592b207071a2c05f46a6ffdd890a2332f957a7e6b805e9aa6c6988e451e9fa8`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-OPEN-DISTANCE-FAMILY` `GAP_NO_DERIVATION`: [MAJ-TORUS-3X4-COSET-WEIGHTS](MAJ-TORUS-3X4-COSET-WEIGHTS.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

