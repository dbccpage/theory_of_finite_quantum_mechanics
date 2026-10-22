# MAJ-CAPPED-COSET-SEARCH

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> When 2^rank(d0) exceeds the declared budget the Gray-code search stops, returns the lightest weight found with exact = False, and the Rust terminal drops from TypedHarmonic to ClosedResidual; checked on the 3x4 torus (budget 4, capped weight \>= exact weight) and the 4x4 torus (budget 16).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 2
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Fixed instances; the upper-bound property of any searched representative is immediate from the definition of the minimum.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-COMP-BUDGET-CAP claims COMPUTATIONALLY_CHECKED; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `code/rust/src/majorana/classify.rs`

- file: [code/rust/src/majorana/classify.rs](../../../code/rust/src/majorana/classify.rs)
- sha256 (`bytes`): `93bf9e0d978e50493ba85a1031c488f6537ee5f1e833db44606995b97e398b6b`
- cited in: node.rust, record TFQ-1159
- check: `cd code/rust && cargo test -p tfqm_majorana capped_search_falls_back_and_never_claims_exactness`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `capped_search_falls_back_and_never_claims_exactness` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_majorana capped_search_falls_back_and_never_claims_exactness` |
| `classify` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `papers/core/majorana/code/majorana_evaluator.py`

- file: [papers/core/majorana/code/majorana_evaluator.py](../../../papers/core/majorana/code/majorana_evaluator.py)
- sha256 (`bytes`): `86798eabea510363b59e164c516625c6055df24b4e12086cfe2fde5db16835c3`
- cited in: record TFQ-1159

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `compute_coset_weight` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py`

- file: [papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py](../../../papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py)
- sha256 (`bytes`): `613eb90331749cead532af34aa06a1d61ff5c01a8cc6fd4bdce4bdb9923f7e32`
- cited in: record TFQ-1159
- check: `python -m pytest papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py::test_coset_weight_budget_capping`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_coset_weight_budget_capping` (python_test) | yes | yes | yes | - | `python -m pytest papers/core/majorana/code/tests/integration/test_tetron_surface_codes.py::test_coset_weight_budget_capping` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1159_maj_capped_coset_search.md`

- file: [dag/derivations/28_majorana/tfq_1159_maj_capped_coset_search.md](../../../dag/derivations/28_majorana/tfq_1159_maj_capped_coset_search.md)
- sha256 (`lf-normalised`): `ae6a75984c85f01f737b65785a8698fa1a98bc78a05d7205f0c5fc269bb96b60`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1159
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem_change_log.md`

- file: [papers/core/majorana/the_majorana_problem_change_log.md](../../../papers/core/majorana/the_majorana_problem_change_log.md)
- sha256 (`lf-normalised`): `c37871232dd6ea91a271c77fa1e6f92d37b5b27e0b5f7517420cded3aee4bd38`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-CAPPED-COSET-SEARCH` `COMPUTED`: [MAJ-PHI1-SYNDROME-DECODING](MAJ-PHI1-SYNDROME-DECODING.md) (CONDITIONAL)

Outgoing (2):

- `APP-R-MAJ-OPEN-LP-DUAL-CERTIFIED-CEILING` `GAP_NO_DERIVATION`: [MAJ-OPEN-LP-DUAL-CERTIFIED-CEILING](MAJ-OPEN-LP-DUAL-CERTIFIED-CEILING.md) (OPEN)
- `APP-R-MAJ-TORUS-6X6-BENCHMARK` `COMPUTED`: [MAJ-TORUS-6X6-BENCHMARK](MAJ-TORUS-6X6-BENCHMARK.md) (COMPUTATIONALLY_CHECKED)
