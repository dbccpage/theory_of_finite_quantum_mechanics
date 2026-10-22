# MAJ-TORUS-6X6-BENCHMARK

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the 6x6 tetron torus (V = 36, E = 72, dim H1 = 2, rank d0 = 35) a weight-one residual classifies OpenObstruction within a 100 ms test bound in Rust and Python, and the full coset 2^35 exceeds the 2^20 search budget.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 2
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The body's 17 ms figure is not recorded in this checkout; the timed residual exits at the syndrome step, so the elimination step is not timed; timing is machine-dependent.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-C16 claims COMPUTATIONALLY_CHECKED; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1160
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `gaussian_elimination_cubic_bound` | yes | yes | yes | - | `#print axioms gaussian_elimination_cubic_bound` |
- counts toward the grade: yes

### Rust: `code/rust/src/majorana/classify.rs`

- file: [code/rust/src/majorana/classify.rs](../../../code/rust/src/majorana/classify.rs)
- sha256 (`bytes`): `93bf9e0d978e50493ba85a1031c488f6537ee5f1e833db44606995b97e398b6b`
- cited in: node.rust, record TFQ-1160
- check: `cd code/rust && cargo test -p tfqm_majorana six_by_six_torus_weight_one_is_open_within_a_tenth_of_a_second`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `six_by_six_torus_weight_one_is_open_within_a_tenth_of_a_second` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_majorana six_by_six_torus_weight_one_is_open_within_a_tenth_of_a_second` |
- counts toward the grade: yes

### Python: `papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py`

- file: [papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py](../../../papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py)
- sha256 (`bytes`): `3389fbeaad7f67b996a8bc8aa2cef6d2ae1ae841d8b6cfa83564a3305190a60b`
- cited in: record TFQ-1160
- check: `python -m pytest papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py::test_trichotomy_benchmark_6x6_torus`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_trichotomy_benchmark_6x6_torus` (python_test) | yes | yes | yes | - | `python -m pytest papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py::test_trichotomy_benchmark_6x6_torus` |
- counts toward the grade: yes

### Documents and data: `code/rust/src/majorana/fixtures/tetron_lattice_scaling.json`

- file: [code/rust/src/majorana/fixtures/tetron_lattice_scaling.json](../../../code/rust/src/majorana/fixtures/tetron_lattice_scaling.json)
- sha256 (`lf-normalised`): `7a565be0a73b25d8b1ba3b4d17e5f8fd9555594ee58fef4aa5bd9b6f05bf8581`
- cited in: node.rust, record TFQ-1160
- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1160_maj_torus_6x6_benchmark.md`

- file: [dag/derivations/28_majorana/tfq_1160_maj_torus_6x6_benchmark.md](../../../dag/derivations/28_majorana/tfq_1160_maj_torus_6x6_benchmark.md)
- sha256 (`lf-normalised`): `aef932f77a78acccd711d2ae33f959ecd87c6fee28c84c0414b2beaf571d5348`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1160
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

- `APP-R-MAJ-TORUS-6X6-BENCHMARK` `COMPUTED`: [MAJ-TRICHOTOMY-ELIMINATION-DECISION](MAJ-TRICHOTOMY-ELIMINATION-DECISION.md) (PROVED_PROSE), [MAJ-CAPPED-COSET-SEARCH](MAJ-CAPPED-COSET-SEARCH.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

