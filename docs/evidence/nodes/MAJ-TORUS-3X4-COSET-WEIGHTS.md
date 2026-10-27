# MAJ-TORUS-3X4-COSET-WEIGHTS

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the 3x4 tetron torus (12 sites, 24 channels, 12 islands) exhaustive Gray-code coset search gives Phi1 = 3 for the column class, 4 for the row class and 7 for their sum, all ClosedResidual, so the distance of that instance is 3.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 3
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

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
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `toric_distance_3x4` | yes | yes | yes | none | `#print axioms toric_distance_3x4` |
| `torus_3x4_additive_weight` | yes | yes | yes | none | `#print axioms torus_3x4_additive_weight` |

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

### Python: `code/python/src/majorana/majorana_f2_trichotomy.py`

- file: [code/python/src/majorana/majorana_f2_trichotomy.py](../../../code/python/src/majorana/majorana_f2_trichotomy.py)
- sha256 (`bytes`): `d6ffe11ba0e9fd0ba5a4a467147b95cf560b3d4c860b845a025e3b0e5e283b7a`
- cited in: record TFQ-1155

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `compute_coset_weight` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `code/python/src/majorana/test_tetron_surface_codes.py`

- file: [code/python/src/majorana/test_tetron_surface_codes.py](../../../code/python/src/majorana/test_tetron_surface_codes.py)
- sha256 (`bytes`): `6577a59d6a74b23a3f5a356b1ffaf308140451939f7541f472ac0de58bf6747e`
- cited in: record TFQ-1155
- check: `python -m pytest code/python/src/majorana/test_tetron_surface_codes.py::test_torus_per_class_minimum_weights`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_torus_per_class_minimum_weights` (python_test) | yes | yes | yes | - | `python -m pytest code/python/src/majorana/test_tetron_surface_codes.py::test_torus_per_class_minimum_weights` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1155_maj_torus_3x4_coset_weights.md`

- file: [dag/derivations/28_majorana/tfq_1155_maj_torus_3x4_coset_weights.md](../../../dag/derivations/28_majorana/tfq_1155_maj_torus_3x4_coset_weights.md)
- sha256 (`lf-normalised`): `7b99c8656c76408a3073bd26339846e777a257757ed5002ccef57cc7c69e0f3b`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1155
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

- `APP-R-MAJ-TORUS-3X4-COSET-WEIGHTS` `COMPUTED`: [MAJ-TETRON-BETTI-COMPUTED](MAJ-TETRON-BETTI-COMPUTED.md) (COMPUTATIONALLY_CHECKED), [MAJ-PHI1-HAMMING-COSET](MAJ-PHI1-HAMMING-COSET.md) (DEFINITION)

Outgoing (1):

- `APP-R-MAJ-OPEN-DISTANCE-FAMILY` `GAP_NO_DERIVATION`: [MAJ-OPEN-DISTANCE-FAMILY](MAJ-OPEN-DISTANCE-FAMILY.md) (OPEN)
