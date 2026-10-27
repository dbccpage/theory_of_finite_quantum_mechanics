# MAJ-CAPPED-COSET-SEARCH

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> When 2^rank(d0) exceeds the declared budget the Gray-code search stops, returns the lightest weight found with exact = False, and the Rust terminal drops from TypedHarmonic to ClosedResidual; checked on the 3x4 torus (budget 4, capped weight \>= exact weight) and the 4x4 torus (budget 16).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 0
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

### Python: `code/python/src/majorana/majorana_f2_trichotomy.py`

- file: [code/python/src/majorana/majorana_f2_trichotomy.py](../../../code/python/src/majorana/majorana_f2_trichotomy.py)
- sha256 (`bytes`): `d6ffe11ba0e9fd0ba5a4a467147b95cf560b3d4c860b845a025e3b0e5e283b7a`
- cited in: record TFQ-1159

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `compute_coset_weight` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/majorana/test_tetron_surface_codes.py`

- file: [code/python/src/majorana/test_tetron_surface_codes.py](../../../code/python/src/majorana/test_tetron_surface_codes.py)
- sha256 (`bytes`): `6577a59d6a74b23a3f5a356b1ffaf308140451939f7541f472ac0de58bf6747e`
- cited in: record TFQ-1159
- check: `python -m pytest code/python/src/majorana/test_tetron_surface_codes.py::test_coset_weight_budget_capping`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_coset_weight_budget_capping` (python_test) | yes | yes | yes | - | `python -m pytest code/python/src/majorana/test_tetron_surface_codes.py::test_coset_weight_budget_capping` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1159_maj_capped_coset_search.md`

- file: [dag/derivations/28_majorana/tfq_1159_maj_capped_coset_search.md](../../../dag/derivations/28_majorana/tfq_1159_maj_capped_coset_search.md)
- sha256 (`lf-normalised`): `b7489a2c1eebc6fb298fc6f8cfbe9c82d49901cab6e782b97b0ba68ec47b7706`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1159
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

- `APP-R-MAJ-CAPPED-COSET-SEARCH` `COMPUTED`: [MAJ-PHI1-SYNDROME-DECODING](MAJ-PHI1-SYNDROME-DECODING.md) (CONDITIONAL)

Outgoing (2):

- `APP-R-MAJ-OPEN-LP-DUAL-CERTIFIED-CEILING` `GAP_NO_DERIVATION`: [MAJ-OPEN-LP-DUAL-CERTIFIED-CEILING](MAJ-OPEN-LP-DUAL-CERTIFIED-CEILING.md) (OPEN)
- `APP-R-MAJ-TORUS-6X6-BENCHMARK` `COMPUTED`: [MAJ-TORUS-6X6-BENCHMARK](MAJ-TORUS-6X6-BENCHMARK.md) (COMPUTATIONALLY_CHECKED)
