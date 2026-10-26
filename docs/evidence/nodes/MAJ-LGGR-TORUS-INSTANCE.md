# MAJ-LGGR-TORUS-INSTANCE

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the 2x2 torus the logical cycle torus_logical_x has d1 w = 0 on every plaquette yet classifies ClosedResidual (not Exact); on the triangle an exact residual and an open residual are not LGGR.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 2
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The general surface statement (every carrier with a non-contractible cycle with dim H1 \> 0 has such a residual) is only argued in prose.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-C11 claims PROVED_LEAN; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1146
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `local_green_not_global_red` | yes | yes | yes | none | `#print axioms local_green_not_global_red` |

- counts toward the grade: yes

### Rust: `code/rust/src/majorana/lggr.rs`

- file: [code/rust/src/majorana/lggr.rs](../../../code/rust/src/majorana/lggr.rs)
- sha256 (`bytes`): `ed5ed656e8d3a5a6b7641e2c4a1938435c7ae5d59a1d703e70ba60979937d025`
- cited in: node.rust, record TFQ-1146

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `detect_lggr` (rust_symbol) | yes | yes | yes | - | - |
| `exact_syndrome_is_not_lggr` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_majorana exact_syndrome_is_not_lggr` |
| `torus_logical_is_lggr` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_majorana torus_logical_is_lggr` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1146_maj_lggr_torus_instance.md`

- file: [dag/derivations/28_majorana/tfq_1146_maj_lggr_torus_instance.md](../../../dag/derivations/28_majorana/tfq_1146_maj_lggr_torus_instance.md)
- sha256 (`lf-normalised`): `967340b8be25536d386cbdae9f857f2d285bf5b3a160dfd7888fba1255d0d8a6`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1146
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

- `APP-R-MAJ-LGGR-TORUS-INSTANCE` `COMPUTED`: [MAJ-TORUS-2X2-WORKED-GRID](MAJ-TORUS-2X2-WORKED-GRID.md) (COMPUTATIONALLY_CHECKED), [DS-QM102-SYNDROME-CAPACITY-BOUND](DS-QM102-SYNDROME-CAPACITY-BOUND.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

