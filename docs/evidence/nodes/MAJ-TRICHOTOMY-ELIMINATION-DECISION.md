# MAJ-TRICHOTOMY-ELIMINATION-DECISION

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `PROVED_PROSE`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Given d0, d1 and w over F2, compute s = d1 w (OpenObstruction if s is nonzero), otherwise solve d0 a = w by Gaussian elimination (Exact if solvable, ClosedResidual if not); this uses polynomially many bit operations, O(E (V + F)^2) by the body's count.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

No Lean statement of the algorithm or its operation count exists; gaussian_elimination_cubic_bound is a reflexivity and must not be cited for this theorem.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-C3 claims COMPUTATIONALLY_CHECKED; audited status PROVED_PROSE

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1143
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `gaussian_elimination_cubic_bound` | yes | yes | yes | none | `#print axioms gaussian_elimination_cubic_bound` |
| `gaussian_elimination_ops` | yes | yes | yes | module-level | `#print axioms gaussian_elimination_ops` |

- counts toward the grade: yes

### Rust: `code/rust/src/majorana/classify.rs`

- file: [code/rust/src/majorana/classify.rs](../../../code/rust/src/majorana/classify.rs)
- sha256 (`bytes`): `93bf9e0d978e50493ba85a1031c488f6537ee5f1e833db44606995b97e398b6b`
- cited in: node.rust, record TFQ-1143

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `classify_default` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `papers/core/majorana/code/majorana_evaluator.py`

- file: [papers/core/majorana/code/majorana_evaluator.py](../../../papers/core/majorana/code/majorana_evaluator.py)
- sha256 (`bytes`): `86798eabea510363b59e164c516625c6055df24b4e12086cfe2fde5db16835c3`
- cited in: record TFQ-1143

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `GF2Matrix.solve` (python_symbol) | yes | yes | yes | - | - |
| `classify_residual` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py`

- file: [papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py](../../../papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py)
- sha256 (`bytes`): `3389fbeaad7f67b996a8bc8aa2cef6d2ae1ae841d8b6cfa83564a3305190a60b`
- cited in: record TFQ-1143
- check: `python -m pytest papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py::test_gf2_matrix_rank_and_solve`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_gf2_matrix_rank_and_solve` (python_test) | yes | yes | yes | - | `python -m pytest papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py::test_gf2_matrix_rank_and_solve` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1143_maj_trichotomy_elimination_decision.md`

- file: [dag/derivations/28_majorana/tfq_1143_maj_trichotomy_elimination_decision.md](../../../dag/derivations/28_majorana/tfq_1143_maj_trichotomy_elimination_decision.md)
- sha256 (`lf-normalised`): `fcc89a86bec2f522f418c3daa7a0654e10c89e4b83865990a436b280cc5fc1df`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1143
- counts toward the grade: no

### Documents and data: `papers/core/majorana/claim_ledger.yaml`

- file: [papers/core/majorana/claim_ledger.yaml](../../../papers/core/majorana/claim_ledger.yaml)
- sha256 (`lf-normalised`): `3d5ac164f2ed90437e87eaea0c31fc883334a8f25a34eb4d6159cc428bc20f89`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `2f55c0f24f87388cfa9d7a4a7d832f34c0fa30b857d344811f4336f634c1684b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem_claim_ledger.md`

- file: [papers/core/majorana/the_majorana_problem_claim_ledger.md](../../../papers/core/majorana/the_majorana_problem_claim_ledger.md)
- sha256 (`lf-normalised`): `37cc191a881cbb0f8fb52e30c2b865f9e9e70e235b4530df7bdd7d1b5728cb86`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-TRICHOTOMY-ELIMINATION-DECISION` `DERIVED_PROSE`: [MAJ-TRICHOTOMY-EXHAUSTIVE](MAJ-TRICHOTOMY-EXHAUSTIVE.md) (PROVED_PROSE)

Outgoing (1):

- `APP-R-MAJ-TORUS-6X6-BENCHMARK` `COMPUTED`: [MAJ-TORUS-6X6-BENCHMARK](MAJ-TORUS-6X6-BENCHMARK.md) (COMPUTATIONALLY_CHECKED)
