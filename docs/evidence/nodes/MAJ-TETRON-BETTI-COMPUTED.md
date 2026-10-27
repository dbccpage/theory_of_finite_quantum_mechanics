# MAJ-TETRON-BETTI-COMPUTED

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For sizes 2x2, 2x3, 3x3, 3x4, 4x4, 5x5, 6x6, 6x8 and 8x8, F2 row reduction gives dim H1 = (E - rank d1) - rank d0 = 0 (disk), 1 (cylinder), 2 (torus), agreeing with (2 if closed else 1) minus the Euler characteristic, with d1 d0 = 0.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 4
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Fixed sizes only; a closed-form proof for all rows and cols is absent.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-COMP-TETRON-BETTI claims COMPUTATIONALLY_CHECKED; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `code/rust/src/majorana/tetron.rs`

- file: [code/rust/src/majorana/tetron.rs](../../../code/rust/src/majorana/tetron.rs)
- sha256 (`bytes`): `0004b6882118db4494c13ccb7683f858f611d702067e4bd3c62dee0a05b84bc0`
- cited in: node.rust, record TFQ-1152

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `benchmark_tetron_lattice_scaling` (rust_symbol) | yes | yes | yes | - | - |
| `dim_h1_agrees_with_the_euler_characteristic` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_majorana dim_h1_agrees_with_the_euler_characteristic` |
| `dim_h1_is_the_topologys_betti_number` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_majorana dim_h1_is_the_topologys_betti_number` |
| `tetron_lattice_scaling_benchmark_up_to_8x8` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_majorana tetron_lattice_scaling_benchmark_up_to_8x8` |

- counts toward the grade: yes

### Python: `code/python/src/majorana/test_tetron_surface_codes.py`

- file: [code/python/src/majorana/test_tetron_surface_codes.py](../../../code/python/src/majorana/test_tetron_surface_codes.py)
- sha256 (`bytes`): `6577a59d6a74b23a3f5a356b1ffaf308140451939f7541f472ac0de58bf6747e`
- cited in: record TFQ-1152
- check: `python -m pytest code/python/src/majorana/test_tetron_surface_codes.py::test_tetron_homology_dimensions`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_tetron_homology_dimensions` (python_test) | yes | yes | yes | - | `python -m pytest code/python/src/majorana/test_tetron_surface_codes.py::test_tetron_homology_dimensions` |

- counts toward the grade: yes

### Documents and data: `code/rust/src/majorana/fixtures/tetron_lattice_scaling.json`

- file: [code/rust/src/majorana/fixtures/tetron_lattice_scaling.json](../../../code/rust/src/majorana/fixtures/tetron_lattice_scaling.json)
- sha256 (`lf-normalised`): `7a565be0a73b25d8b1ba3b4d17e5f8fd9555594ee58fef4aa5bd9b6f05bf8581`
- cited in: node.rust, record TFQ-1152
- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1152_maj_tetron_betti_computed.md`

- file: [dag/derivations/28_majorana/tfq_1152_maj_tetron_betti_computed.md](../../../dag/derivations/28_majorana/tfq_1152_maj_tetron_betti_computed.md)
- sha256 (`lf-normalised`): `953f577e4c02a04eb9350308ca6157de06098a194b38105f3b188e5bfa0e1fd7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1152
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

- `APP-R-MAJ-TETRON-BETTI-COMPUTED` `COMPUTED`: [MAJ-TETRON-ARRAY-CARRIER](MAJ-TETRON-ARRAY-CARRIER.md) (DEFINITION)

Outgoing (2):

- `APP-R-MAJ-SYNDROME-READOUT-INADEQUATE` `COMPUTED`: [MAJ-SYNDROME-READOUT-INADEQUATE](MAJ-SYNDROME-READOUT-INADEQUATE.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-MAJ-TORUS-3X4-COSET-WEIGHTS` `COMPUTED`: [MAJ-TORUS-3X4-COSET-WEIGHTS](MAJ-TORUS-3X4-COSET-WEIGHTS.md) (COMPUTATIONALLY_CHECKED)
