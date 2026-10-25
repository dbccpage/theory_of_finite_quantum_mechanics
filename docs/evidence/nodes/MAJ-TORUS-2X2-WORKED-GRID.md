# MAJ-TORUS-2X2-WORKED-GRID

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the 2x2 periodic grid (V = 4, E = 8, F = 4) rank d0 = rank d1 = 3 and dim H1 = 2; the two declared logical cycles are ClosedResidual, a single edge is OpenObstruction, and a d0 column is Exact.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 2
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Fixed instance only; it does not establish the classification on other grids.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-EX-TORUS-2X2 claims PROVED_PROSE; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `code/rust/src/majorana/complexes.rs`

- file: [code/rust/src/majorana/complexes.rs](../../../code/rust/src/majorana/complexes.rs)
- sha256 (`bytes`): `185042ba131c005d8519b65159791a78f6a64df90e7976a54c0845f6de489646`
- cited in: node.rust, record TFQ-1145
- check: `cd code/rust && cargo test -p tfqm_majorana play_surface_torus_logical_closed_residual`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `play_surface_torus_logical_closed_residual` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_majorana play_surface_torus_logical_closed_residual` |
| `surface_grid_2x2_torus` (rust_symbol) | yes | yes | yes | - | - |
| `torus_logical_x_example` (rust_symbol) | yes | yes | yes | - | - |
| `torus_logical_z_example` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Rust: `code/rust/src/majorana/tetron.rs`

- file: [code/rust/src/majorana/tetron.rs](../../../code/rust/src/majorana/tetron.rs)
- sha256 (`bytes`): `0004b6882118db4494c13ccb7683f858f611d702067e4bd3c62dee0a05b84bc0`
- cited in: node.rust, record TFQ-1145
- check: `cd code/rust && cargo test -p tfqm_majorana tetron_lattice_scaling_benchmark_up_to_8x8`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `tetron_lattice_scaling_benchmark_up_to_8x8` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_majorana tetron_lattice_scaling_benchmark_up_to_8x8` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1145_maj_torus_2x2_worked_grid.md`

- file: [dag/derivations/28_majorana/tfq_1145_maj_torus_2x2_worked_grid.md](../../../dag/derivations/28_majorana/tfq_1145_maj_torus_2x2_worked_grid.md)
- sha256 (`lf-normalised`): `766d2ec6742dac11aebeecc918132539dcbc589b827ca5a564efd9f5e0ce30c7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1145
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-TORUS-2X2-WORKED-GRID` `COMPUTED`: [MAJ-TRICHOTOMY-EXHAUSTIVE](MAJ-TRICHOTOMY-EXHAUSTIVE.md) (PROVED_PROSE)

Outgoing (1):

- `APP-R-MAJ-LGGR-TORUS-INSTANCE` `COMPUTED`: [MAJ-LGGR-TORUS-INSTANCE](MAJ-LGGR-TORUS-INSTANCE.md) (COMPUTATIONALLY_CHECKED)
