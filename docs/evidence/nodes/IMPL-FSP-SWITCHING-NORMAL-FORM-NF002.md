# IMPL-FSP-SWITCHING-NORMAL-FORM-NF002

Stage: [IMPLEMENTATION](../stages/IMPLEMENTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> FSP switching normal form NF-002 on a fixed labelled finite graph with a supplied spanning forest: T1-T5, soundness and completeness of the normal form, and a duplicate-free enumeration are mechanized. normalForms_length gives length 2^numChord; normalForms_nodup and mem_normalForms_iff certify enumeration uniqueness and membership. Together with numChord_identity this records 2^(|E|-|V|+c) switching classes. It does not assert graph-isomorphism canonicalization or efficient fermionic sampling.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- distinct cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

All NF-002 theorems T1-T5 and the duplicate-free 2^numChord normal-form enumeration are mechanized in core Lean 4 without Classical.choice.

## Source status

Local compatibility port replayed with Lean 4.33.1; enumeration length, uniqueness, membership and chord-count identity depend only on propext and Quot.sound; replayed with Lean 4.35.0 on 2026-10-21.

## Review

- PFP review: [dag/results/IMPL-FSP-SWITCHING-NORMAL-FORM-NF002/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/IMPL-FSP-SWITCHING-NORMAL-FORM-NF002/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: All edge signings and vertex-switching orbits for the four declared graphs are exact; cycle XOR invariance and2^b Boolean-function cardinality are kernel checked.
  - does not support: Prove the general graph/forest refinement and freshly compile all source NF002 declarations before claiming its full core-only/no-Classical.choice theorem suite. This finite graph stage is not that suite.
  - next test: Prove the general graph/forest refinement and freshly compile all source NF002 declarations before claiming its full core-only/no-Classical.choice theorem suite. This finite graph stage is not that suite.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `dag/results/IMPL-FSP-SWITCHING-NORMAL-FORM-NF002/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_atlas/coda_atlas/proposals/008_fsp_switching_normal_form/SwitchingNormalForm.lean`

- file: [dag/results/IMPL-FSP-SWITCHING-NORMAL-FORM-NF002/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_atlas/coda_atlas/proposals/008_fsp_switching_normal_form/SwitchingNormalForm.lean](../../../dag/results/IMPL-FSP-SWITCHING-NORMAL-FORM-NF002/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_atlas/coda_atlas/proposals/008_fsp_switching_normal_form/SwitchingNormalForm.lean)
- sha256 (`bytes`): `dfb38dc1540c22c8bd805b5e00287b75125b8270ca3384a6251899bcb03e6931`
- cited in: node.source
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains dag/results/IMPL-FSP-SWITCHING-NORMAL-FORM-NF002/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_atlas/coda_atlas/proposals/008_fsp_switching_normal_form/SwitchingNormalForm.lean`
- counts toward the grade: yes

### Lean: `lean4/SwitchingNormalForm.lean`

- file: [lean4/SwitchingNormalForm.lean](../../../lean4/SwitchingNormalForm.lean)
- sha256 (`bytes`): `e83ec8c3651888fd3ae7c2abba9e2b5216c5b0c027dd02308280f9bcaec09d05`
- cited in: node.lean, node.source, record TFQ-1044
- replay: `verified`
  - receipt [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json) (module `SwitchingNormalForm`): recorded sha256 `e83ec8c3651888fd3ae7c2abba9e2b5216c5b0c027dd02308280f9bcaec09d05` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SwitchingNormalForm`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `SwitchingNormalForm.mem_normalForms_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms SwitchingNormalForm.mem_normalForms_iff` |
| `SwitchingNormalForm.normalForms_length` | yes | yes | yes | Quot.sound, propext | `#print axioms SwitchingNormalForm.normalForms_length` |
| `SwitchingNormalForm.normalForms_nodup` | yes | yes | yes | Quot.sound, propext | `#print axioms SwitchingNormalForm.normalForms_nodup` |
| `SwitchingNormalForm.normal_sound` | yes | yes | yes | none | `#print axioms SwitchingNormalForm.normal_sound` |
| `SwitchingNormalForm.numChord_identity` | yes | yes | yes | Quot.sound, propext | `#print axioms SwitchingNormalForm.numChord_identity` |
| `SwitchingNormalForm.same_class_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms SwitchingNormalForm.same_class_iff` |
| `mem_normalForms_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms mem_normalForms_iff` |
| `normalForms_length` | yes | yes | yes | Quot.sound, propext | `#print axioms normalForms_length` |
| `normalForms_nodup` | yes | yes | yes | Quot.sound, propext | `#print axioms normalForms_nodup` |
| `normal_sound` | yes | yes | yes | none | `#print axioms normal_sound` |
| `numChord_identity` | yes | yes | yes | Quot.sound, propext | `#print axioms numChord_identity` |
| `same_class_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms same_class_iff` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1044
- counts toward the grade: no

### Documents and data: `dag/derivations/21_implementation_core/tfq_1044_impl_fsp_switching_normal_form_nf002.md`

- file: [dag/derivations/21_implementation_core/tfq_1044_impl_fsp_switching_normal_form_nf002.md](../../../dag/derivations/21_implementation_core/tfq_1044_impl_fsp_switching_normal_form_nf002.md)
- sha256 (`lf-normalised`): `9e51b7b5094df982466715cefae6ea90325a9694971da3f07de90854afec603d`
- generated view: listed, not counted
- cited in: record TFQ-1044
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml`

- file: [sources/atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml](../../../sources/atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml)
- sha256 (`lf-normalised`): `2bfb4441352c4206cbd84f3e500e4c3ba817364aff49623a001087ecf12df5a6`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `IMPL-R-FSP-NF002` `DERIVED_LEAN`: [PG-WDP-QUOTIENT-EXACT-SEQUENCE](PG-WDP-QUOTIENT-EXACT-SEQUENCE.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-FSP-SWITCHING-NORMAL-FORM` `DERIVED_LEAN`: [FSP-SWITCHING-NORMAL-FORM](FSP-SWITCHING-NORMAL-FORM.md) (PROVED_LEAN)
