# MAJ-TORUS-3X4-COSET-WEIGHTS

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the 3x4 tetron torus (12 sites, 24 channels, 12 islands) exhaustive Gray-code coset search gives Phi1 = 3 for the column class, 4 for the row class and 7 for their sum, all ClosedResidual, so the distance of that instance is 3.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 3
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Fixed instance only; additivity and d = min(rows, cols) for other sizes are MAJ-CLAIM-DISTANCE-FAMILY.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-C14 claims COMPUTATIONALLY_CHECKED; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1155
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `toric_distance_3x4` | yes | yes | yes | - | `#print axioms toric_distance_3x4` |
| `torus_3x4_additive_weight` | yes | yes | yes | - | `#print axioms torus_3x4_additive_weight` |
- counts toward the grade: yes

### Rust: `code/rust/src/majorana/tetron.rs`

- file: [code/rust/src/majorana/tetron.rs](../../../code/rust/src/majorana/tetron.rs)
- sha256 (`bytes`): `0004b6882118db4494c13ccb7683f858f611d702067e4bd3c62dee0a05b84bc0`
- cited in: node.rust, record TFQ-1155

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `logical_generators_are_closed` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_majorana logical_generators_are_closed` |
| `logical_generators_have_the_expected_weight` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_majorana logical_generators_have_the_expected_weight` |
- counts toward the grade: yes

### Python: `papers/core/majorana/code/majorana_evaluator.py`

- file: [papers/core/majorana/code/majorana_evaluator.py](../../../papers/core/majorana/code/majorana_evaluator.py)
- sha256 (`bytes`): `86798eabea510363b59e164c516625c6055df24b4e12086cfe2fde5db16835c3`
- cited in: record TFQ-1155

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `compute_coset_weight` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py`

- file: [papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py](../../../papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py)
- sha256 (`bytes`): `613eb90331749cead532af34aa06a1d61ff5c01a8cc6fd4bdce4bdb9923f7e32`
- cited in: record TFQ-1155
- check: `python -m pytest papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py::test_torus_per_class_minimum_weights`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_torus_per_class_minimum_weights` (python_test) | yes | yes | yes | - | `python -m pytest papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py::test_torus_per_class_minimum_weights` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1155_maj_torus_3x4_coset_weights.md`

- file: [dag/derivations/28_majorana/tfq_1155_maj_torus_3x4_coset_weights.md](../../../dag/derivations/28_majorana/tfq_1155_maj_torus_3x4_coset_weights.md)
- sha256 (`lf-normalised`): `16d564db784c3fd3faf53f0de313f82e37037d0c405cb336309b9cc927125e1c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1155
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

- `APP-R-MAJ-TORUS-3X4-COSET-WEIGHTS` `COMPUTED`: [MAJ-TETRON-BETTI-COMPUTED](MAJ-TETRON-BETTI-COMPUTED.md) (COMPUTATIONALLY_CHECKED), [MAJ-PHI1-HAMMING-COSET](MAJ-PHI1-HAMMING-COSET.md) (DEFINITION)

Outgoing (1):

- `APP-R-MAJ-OPEN-DISTANCE-FAMILY` `GAP_NO_DERIVATION`: [MAJ-OPEN-DISTANCE-FAMILY](MAJ-OPEN-DISTANCE-FAMILY.md) (OPEN)
