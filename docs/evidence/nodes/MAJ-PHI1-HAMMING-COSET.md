# MAJ-PHI1-HAMMING-COSET

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> H1 = ker d1 / im d0 over F2, and the quotient residual mass of a class is Phi1(\[r\]) = min over a in C0 of wt(r + d0 a), the Hamming weight of a lightest coset representative.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

This is the unit-weight binary specialization of the trunk Phi1 quotient seminorm; the coefficient change from weighted l1 to F2 Hamming weight is declared, not derived.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-DEF-PHI1-F2 claims DEFINITION; audited status DEFINITION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1140
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `F2Vec.weight` | yes | yes | yes | none | `#print axioms F2Vec.weight` |
| `coset_weight_upper_bound` | yes | yes | yes | none | `#print axioms coset_weight_upper_bound` |

- counts toward the grade: yes

### Python: `papers/core/majorana/code/majorana_evaluator.py`

- file: [papers/core/majorana/code/majorana_evaluator.py](../../../papers/core/majorana/code/majorana_evaluator.py)
- sha256 (`bytes`): `86798eabea510363b59e164c516625c6055df24b4e12086cfe2fde5db16835c3`
- cited in: record TFQ-1140

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `compute_coset_weight` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1140_maj_phi1_hamming_coset.md`

- file: [dag/derivations/28_majorana/tfq_1140_maj_phi1_hamming_coset.md](../../../dag/derivations/28_majorana/tfq_1140_maj_phi1_hamming_coset.md)
- sha256 (`lf-normalised`): `21c3393482b9046063b1c59c895d6b5e97a8c712f8ce78c6b93d140ed0dae1ad`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1140
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `2f55c0f24f87388cfa9d7a4a7d832f34c0fa30b857d344811f4336f634c1684b`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-PHI1-HAMMING-COSET` `DERIVED_PROSE`: [MAJ-F2-PARITY-SCHEDULE](MAJ-F2-PARITY-SCHEDULE.md) (DEFINITION), [L1-WDP-WINDOW-PHI1-GAMMA2](L1-WDP-WINDOW-PHI1-GAMMA2.md) (DEFINITION)

Outgoing (5):

- `APP-R-MAJ-IMPORT-COSET-WEIGHT-NP-HARD` `CONDITIONAL_ON_IMPORT`: [MAJ-IMPORT-COSET-WEIGHT-NP-HARD](MAJ-IMPORT-COSET-WEIGHT-NP-HARD.md) (IMPORTED_ASSUMPTION)
- `APP-R-MAJ-LP-INVARIANCE-BINARY` `DERIVED_PROSE`: [MAJ-LP-INVARIANCE-BINARY](MAJ-LP-INVARIANCE-BINARY.md) (PROVED_PROSE)
- `APP-R-MAJ-PHI1-SYNDROME-DECODING` `CONDITIONAL_ON_IMPORT`: [MAJ-PHI1-SYNDROME-DECODING](MAJ-PHI1-SYNDROME-DECODING.md) (CONDITIONAL)
- `APP-R-MAJ-SYNDROME-RECOVERY-CRITERION` `DERIVED_PROSE`: [MAJ-SYNDROME-RECOVERY-CRITERION](MAJ-SYNDROME-RECOVERY-CRITERION.md) (PROVED_PROSE)
- `APP-R-MAJ-TORUS-3X4-COSET-WEIGHTS` `COMPUTED`: [MAJ-TORUS-3X4-COSET-WEIGHTS](MAJ-TORUS-3X4-COSET-WEIGHTS.md) (COMPUTATIONALLY_CHECKED)
