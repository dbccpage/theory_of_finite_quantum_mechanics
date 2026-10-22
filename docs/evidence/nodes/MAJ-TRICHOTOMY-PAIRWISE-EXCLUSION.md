# MAJ-TRICHOTOMY-PAIRWISE-EXCLUSION

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every declared F2 cochain complex (with d1 d0 = 0 as a structure field) every Exact residual is a cocycle, and no residual satisfies two of Exact, ClosedResidual and OpenObstruction.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 9
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 2
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 5 Lean reference(s) cited, 5 in this checkout (replay: none 5). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Exhaustiveness (each residual has at least one label) is not stated in Lean; it is the prose record MAJ-THM-TRICHOTOMY-EXHAUSTIVE.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-C2 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1141
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `closed_residual_not_open` | yes | yes | yes | - | `#print axioms closed_residual_not_open` |
| `coboundary_is_cocycle` | yes | yes | yes | - | `#print axioms coboundary_is_cocycle` |
| `exact_not_closed_residual` | yes | yes | yes | - | `#print axioms exact_not_closed_residual` |
| `exact_not_open` | yes | yes | yes | - | `#print axioms exact_not_open` |
| `trichotomy_pairwise_disjoint` | yes | yes | yes | - | `#print axioms trichotomy_pairwise_disjoint` |
- counts toward the grade: yes

### Rust: `code/rust/src/majorana/classify.rs`

- file: [code/rust/src/majorana/classify.rs](../../../code/rust/src/majorana/classify.rs)
- sha256 (`bytes`): `93bf9e0d978e50493ba85a1031c488f6537ee5f1e833db44606995b97e398b6b`
- cited in: node.rust, record TFQ-1141
- check: `cd code/rust && cargo test -p tfqm_majorana torus_reaches_every_terminal`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `classify` (rust_symbol) | yes | yes | yes | - | - |
| `torus_reaches_every_terminal` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_majorana torus_reaches_every_terminal` |
- counts toward the grade: yes

### Python: `papers/core/majorana/code/majorana_evaluator.py`

- file: [papers/core/majorana/code/majorana_evaluator.py](../../../papers/core/majorana/code/majorana_evaluator.py)
- sha256 (`bytes`): `86798eabea510363b59e164c516625c6055df24b4e12086cfe2fde5db16835c3`
- cited in: record TFQ-1141

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `classify_residual` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py`

- file: [papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py](../../../papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py)
- sha256 (`bytes`): `3389fbeaad7f67b996a8bc8aa2cef6d2ae1ae841d8b6cfa83564a3305190a60b`
- cited in: record TFQ-1141
- check: `python -m pytest papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py::test_residual_trichotomy_classification`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_residual_trichotomy_classification` (python_test) | yes | yes | yes | - | `python -m pytest papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py::test_residual_trichotomy_classification` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1141_maj_trichotomy_pairwise_exclusion.md`

- file: [dag/derivations/28_majorana/tfq_1141_maj_trichotomy_pairwise_exclusion.md](../../../dag/derivations/28_majorana/tfq_1141_maj_trichotomy_pairwise_exclusion.md)
- sha256 (`lf-normalised`): `98954ef0e2e9a5eeef8e6ce5897d360cd44b975caffae197ef43b329eb4b3d2b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1141
- counts toward the grade: no

### Documents and data: `papers/core/majorana/claim_ledger.yaml`

- file: [papers/core/majorana/claim_ledger.yaml](../../../papers/core/majorana/claim_ledger.yaml)
- sha256 (`lf-normalised`): `3d5ac164f2ed90437e87eaea0c31fc883334a8f25a34eb4d6159cc428bc20f89`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/lean4/axiom_report.txt`

- file: [papers/core/majorana/lean4/axiom_report.txt](../../../papers/core/majorana/lean4/axiom_report.txt)
- sha256 (`lf-normalised`): `ec4465011fdd2b18f2c9df263004e9050f8c394dece1841835ff0bcd1e00df79`
- cited in: node.source
- counts toward the grade: yes

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

- `APP-R-MAJ-TRICHOTOMY-PAIRWISE-EXCLUSION` `DERIVED_LEAN`: [MAJ-TRICHOTOMY-LABELS](MAJ-TRICHOTOMY-LABELS.md) (DEFINITION)

Outgoing (2):

- `APP-R-MAJ-TRICHOTOMY-EXHAUSTIVE` `DERIVED_PROSE`: [MAJ-TRICHOTOMY-EXHAUSTIVE](MAJ-TRICHOTOMY-EXHAUSTIVE.md) (PROVED_PROSE)
- `APP-R-MAJ-TRIVIAL-H1-NO-CLOSED` `DERIVED_LEAN`: [MAJ-TRIVIAL-H1-NO-CLOSED](MAJ-TRIVIAL-H1-NO-CLOSED.md) (PROVED_LEAN)
