# FSP-SWITCHING-NORMAL-FORM

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a fixed labelled finite graph and supplied spanning forest, vertex sign switching has a canonical tree-zero representative determined by chord signs. NF-002 records a duplicate-free enumeration of length 2^numChord and numChord=|E|-|V|+c.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- cited Lean declaration references covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Retain fixed labels and vertex-switching equivalence; this canonicalizer is not a normal form under arbitrary many-body basis transformations.

## Source status

Local compatibility port replayed with Lean 4.33.1; enumeration length, uniqueness, membership and chord-count identity depend only on propext and Quot.sound; replayed with Lean 4.35.0 on 2026-10-21.

## Review

No recorded statement-match review.

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
- cited in: node.lean, node.source, record TFQ-0406
- replay: `verified`
  - receipt [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json) (module `SwitchingNormalForm`): recorded sha256 `e83ec8c3651888fd3ae7c2abba9e2b5216c5b0c027dd02308280f9bcaec09d05` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SwitchingNormalForm`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `mem_normalForms_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms mem_normalForms_iff` |
| `normalForms_length` | yes | yes | yes | Quot.sound, propext | `#print axioms normalForms_length` |
| `normalForms_nodup` | yes | yes | yes | Quot.sound, propext | `#print axioms normalForms_nodup` |
| `normal_sound` | yes | yes | yes | none | `#print axioms normal_sound` |
| `numChord_identity` | yes | yes | yes | Quot.sound, propext | `#print axioms numChord_identity` |
| `same_class_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms same_class_iff` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_0406_fsp_switching_normal_form.md`

- file: [dag/derivations/26_fsp/tfq_0406_fsp_switching_normal_form.md](../../../dag/derivations/26_fsp/tfq_0406_fsp_switching_normal_form.md)
- sha256 (`lf-normalised`): `0abc7f61a6a66f537f1c7472a42b480f2869ae6f2cd4d7cb5d5d10d9f68ce145`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0406
- counts toward the grade: no

## Routes

Incoming (1):

- `APP-R-FSP-SWITCHING-NORMAL-FORM` `DERIVED_LEAN`: [IMPL-FSP-SWITCHING-NORMAL-FORM-NF002](IMPL-FSP-SWITCHING-NORMAL-FORM-NF002.md) (PROVED_LEAN)

Outgoing (3):

- `APP-R-FSP-HUBBARD-PROTECTED-REPRESENTATIONS` `CONDITIONAL_ON_IMPORT`: [FSP-HUBBARD-PROTECTED-REPRESENTATIONS](FSP-HUBBARD-PROTECTED-REPRESENTATIONS.md) (CONDITIONAL)
- `APP-R-FSP-MERON-CHARACTER-CANCELLATION` `DERIVED_LEAN`: [FSP-MERON-CHARACTER-CANCELLATION](FSP-MERON-CHARACTER-CANCELLATION.md) (PROVED_LEAN)
- `APP-R-FSP-RATIONAL-QUOTIENT-NORMAL-FORM` `DERIVED_PROSE`: [FSP-RATIONAL-QUOTIENT-NORMAL-FORM](FSP-RATIONAL-QUOTIENT-NORMAL-FORM.md) (PROVED_PROSE)
