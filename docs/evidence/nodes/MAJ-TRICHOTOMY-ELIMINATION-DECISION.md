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

dag/derivations/28_majorana/majorana/the_majorana_problem.md record MAJ-C3 claims COMPUTATIONALLY_CHECKED; audited status PROVED_PROSE

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `dag/derivations/28_majorana/majorana/lean4/MajoranaCore.lean`

- file: [dag/derivations/28_majorana/majorana/lean4/MajoranaCore.lean](../../../dag/derivations/28_majorana/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1143
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains dag/derivations/28_majorana/majorana/lean4/MajoranaCore.lean`

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

### Python: `code/python/src/majorana/majorana_f2_trichotomy.py`

- file: [code/python/src/majorana/majorana_f2_trichotomy.py](../../../code/python/src/majorana/majorana_f2_trichotomy.py)
- sha256 (`bytes`): `d6ffe11ba0e9fd0ba5a4a467147b95cf560b3d4c860b845a025e3b0e5e283b7a`
- cited in: record TFQ-1143

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `GF2Matrix.solve` (python_symbol) | yes | yes | yes | - | - |
| `classify_residual` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/majorana/test_gf2_trichotomy.py`

- file: [code/python/src/majorana/test_gf2_trichotomy.py](../../../code/python/src/majorana/test_gf2_trichotomy.py)
- sha256 (`bytes`): `ef02fedf569c136afcde5946b0a5b597fa108fd48c981f60494aa3d9f517ec75`
- cited in: record TFQ-1143
- check: `python -m pytest code/python/src/majorana/test_gf2_trichotomy.py::test_gf2_matrix_rank_and_solve`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_gf2_matrix_rank_and_solve` (python_test) | yes | yes | yes | - | `python -m pytest code/python/src/majorana/test_gf2_trichotomy.py::test_gf2_matrix_rank_and_solve` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/majorana/claim_ledger.yaml`

- file: [dag/derivations/28_majorana/majorana/claim_ledger.yaml](../../../dag/derivations/28_majorana/majorana/claim_ledger.yaml)
- sha256 (`lf-normalised`): `1f37344a954f8aa15399391a21705a912b2891ae308997f85eee303f709418eb`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/majorana/the_majorana_problem.md`

- file: [dag/derivations/28_majorana/majorana/the_majorana_problem.md](../../../dag/derivations/28_majorana/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `2f55c0f24f87388cfa9d7a4a7d832f34c0fa30b857d344811f4336f634c1684b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/majorana/the_majorana_problem_claim_ledger.md`

- file: [dag/derivations/28_majorana/majorana/the_majorana_problem_claim_ledger.md](../../../dag/derivations/28_majorana/majorana/the_majorana_problem_claim_ledger.md)
- sha256 (`lf-normalised`): `c6a3554eb30108d6294ec0ab42952efacd3f5deff58b23b0bf69d061978ac914`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1143_maj_trichotomy_elimination_decision.md`

- file: [dag/derivations/28_majorana/tfq_1143_maj_trichotomy_elimination_decision.md](../../../dag/derivations/28_majorana/tfq_1143_maj_trichotomy_elimination_decision.md)
- sha256 (`lf-normalised`): `de9c1d5cb235ec1ec77b89313aaf497c042e370ca378e8192c0a15d62f8af8d7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1143
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-MAJ-TRICHOTOMY-ELIMINATION-DECISION` `DERIVED_PROSE`: [MAJ-TRICHOTOMY-EXHAUSTIVE](MAJ-TRICHOTOMY-EXHAUSTIVE.md) (PROVED_PROSE)

Outgoing (1):

- `APP-R-MAJ-TORUS-6X6-BENCHMARK` `COMPUTED`: [MAJ-TORUS-6X6-BENCHMARK](MAJ-TORUS-6X6-BENCHMARK.md) (COMPUTATIONALLY_CHECKED)
