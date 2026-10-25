# MAJ-TETRON-ARRAY-CARRIER

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `DEFINITION`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A rows x cols tetron array takes MZM sites as vertices on a (rows or rows+1) x (cols or cols+1) grid, nearest-neighbour channels as edges and the rows x cols islands as 2-cells, with no wrap (disk), column wrap (cylinder) or both wraps (torus).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A tetron here is a 2-cell of a declared combinatorial carrier under an idealized corner-shared layout, not a superconducting island.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-DEF-TETRON-CARRIER claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `code/rust/src/majorana/tetron.rs`

- file: [code/rust/src/majorana/tetron.rs](../../../code/rust/src/majorana/tetron.rs)
- sha256 (`bytes`): `0004b6882118db4494c13ccb7683f858f611d702067e4bd3c62dee0a05b84bc0`
- cited in: node.rust, record TFQ-1151

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Topology` (rust_symbol) | yes | yes | yes | - | - |
| `build_tetron_array` (rust_symbol) | yes | yes | yes | - | - |
| `logical_class_representative` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `papers/core/majorana/code/majorana_evaluator.py`

- file: [papers/core/majorana/code/majorana_evaluator.py](../../../papers/core/majorana/code/majorana_evaluator.py)
- sha256 (`bytes`): `86798eabea510363b59e164c516625c6055df24b4e12086cfe2fde5db16835c3`
- cited in: record TFQ-1151

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `build_tetron_carrier` (python_symbol) | yes | yes | yes | - | - |
| `logical_representative` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1151_maj_tetron_array_carrier.md`

- file: [dag/derivations/28_majorana/tfq_1151_maj_tetron_array_carrier.md](../../../dag/derivations/28_majorana/tfq_1151_maj_tetron_array_carrier.md)
- sha256 (`lf-normalised`): `5f4627b460b242ba01946077d2f7ce694fb66c3543ceecb18c13609c4a619313`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1151
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-TETRON-ARRAY-CARRIER` `DERIVED_PROSE`: [MAJ-F2-PARITY-SCHEDULE](MAJ-F2-PARITY-SCHEDULE.md) (DEFINITION), [MAJ-SURFACE-SHADOW-FENCE](MAJ-SURFACE-SHADOW-FENCE.md) (DEFINITION)

Outgoing (2):

- `APP-R-MAJ-LEGACY-CARRIER-RETRACTION` `CONDITIONAL_ON_IMPORT`: [MAJ-LEGACY-CARRIER-RETRACTION](MAJ-LEGACY-CARRIER-RETRACTION.md) (CONDITIONAL)
- `APP-R-MAJ-TETRON-BETTI-COMPUTED` `COMPUTED`: [MAJ-TETRON-BETTI-COMPUTED](MAJ-TETRON-BETTI-COMPUTED.md) (COMPUTATIONALLY_CHECKED)
