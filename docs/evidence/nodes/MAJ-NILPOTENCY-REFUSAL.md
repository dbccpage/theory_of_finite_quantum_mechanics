# MAJ-NILPOTENCY-REFUSAL

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> If the declared matrices have d1 d0 nonzero mod 2 (or a residual of the wrong length is supplied), the evaluator emits RepresentationInvalid and assigns no residual class.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 2
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The refusal is a rule of the procedure; the Lean lemma only records that a violating vector falsifies the nilpotency predicate.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-C4 claims PROVED_LEAN; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1144
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `evaluate_complex_nilpotency` | yes | yes | yes | none | `#print axioms evaluate_complex_nilpotency` |
| `nilpotency_refusal_sound` | yes | yes | yes | none | `#print axioms nilpotency_refusal_sound` |

- counts toward the grade: yes

### Rust: `code/rust/src/majorana/classify.rs`

- file: [code/rust/src/majorana/classify.rs](../../../code/rust/src/majorana/classify.rs)
- sha256 (`bytes`): `93bf9e0d978e50493ba85a1031c488f6537ee5f1e833db44606995b97e398b6b`
- cited in: node.rust, record TFQ-1144
- check: `cd code/rust && cargo test -p tfqm_majorana representation_invalid_is_refused_not_classified`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `representation_invalid_is_refused_not_classified` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_majorana representation_invalid_is_refused_not_classified` |

- counts toward the grade: yes

### Python: `papers/core/majorana/code/majorana_evaluator.py`

- file: [papers/core/majorana/code/majorana_evaluator.py](../../../papers/core/majorana/code/majorana_evaluator.py)
- sha256 (`bytes`): `86798eabea510363b59e164c516625c6055df24b4e12086cfe2fde5db16835c3`
- cited in: record TFQ-1144

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `F2CochainComplex.is_nilpotent` (python_symbol) | yes | yes | yes | - | - |
| `classify_residual` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py`

- file: [papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py](../../../papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py)
- sha256 (`bytes`): `3389fbeaad7f67b996a8bc8aa2cef6d2ae1ae841d8b6cfa83564a3305190a60b`
- cited in: record TFQ-1144
- check: `python -m pytest papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py::test_cochain_nilpotency_and_refusal`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_cochain_nilpotency_and_refusal` (python_test) | yes | yes | yes | - | `python -m pytest papers/core/majorana/code/tests/unit/test_gf2_trichotomy.py::test_cochain_nilpotency_and_refusal` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1144_maj_nilpotency_refusal.md`

- file: [dag/derivations/28_majorana/tfq_1144_maj_nilpotency_refusal.md](../../../dag/derivations/28_majorana/tfq_1144_maj_nilpotency_refusal.md)
- sha256 (`lf-normalised`): `74948acdf00b67d21a448ef127bae638599707f1e49d0bc6263f0b71ee1499cf`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1144
- counts toward the grade: no

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

- `APP-R-MAJ-NILPOTENCY-REFUSAL` `DERIVED_PROSE`: [MAJ-F2-PARITY-SCHEDULE](MAJ-F2-PARITY-SCHEDULE.md) (DEFINITION)

Outgoing (0):

