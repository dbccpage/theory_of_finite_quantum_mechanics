# FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On rational 2-vectors there is a binary-valued, scale-invariant frame function (additive on orthogonal frames) with no quadratic representation (no_quadratic_representation); in dimension 2 the Gleason dimension condition fails.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- rational plane Q^2 with orthogonality (assumption)

## Bottleneck

Says nothing for d \>= 3.

## Source status

repository module GleasonRationalPlane.lean (gap register S000-004/010); older GleasonTheorem.lean supplies arithmetic witnesses

## Review

- PFP review: [dag/results/FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION/reviews/20261019_scope_audit/review_result.json](../../../dag/results/FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION/reviews/20261019_scope_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: The source rational-plane binary frame function is generally scale-invariant, additive on nonzero orthogonal frames, and has no quadratic representation; the concrete fitting residual is reproduced exactly.
  - does not support: No extension to dimension at least three, arbitrary real frames or a general Gleason reconstruction is supplied. A complete refined-carrier operad remains open.
  - next test: No extension to dimension at least three, arbitrary real frames or a general Gleason reconstruction is supplied. A complete refined-carrier operad remains open.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GleasonRationalPlane.lean`

- file: [lean4/GleasonRationalPlane.lean](../../../lean4/GleasonRationalPlane.lean)
- sha256 (`bytes`): `91a4852b4de9cca52e348a22b6cb01a13bb27545c7be8cfef3793c337e2f46fb`
- cited in: node.lean, record TFQ-1014
- replay: `none`
- check: `cd lean4 && lake build GleasonRationalPlane`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `binary_values` | yes | yes | yes | - | `#print axioms binary_values` |
| `no_quadratic_representation` | yes | yes | yes | - | `#print axioms no_quadratic_representation` |
- counts toward the grade: yes

### Lean: `lean4/GleasonTheorem.lean`

- file: [lean4/GleasonTheorem.lean](../../../lean4/GleasonTheorem.lean)
- sha256 (`bytes`): `881e01ee20e9af8f1d0f184edb5062447928fc98916c7a18f546d700fc839343`
- cited in: node.lean, record TFQ-1014
- replay: `none`
- check: `cd lean4 && lake build GleasonTheorem`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `d2_binary_non_bornian_obstruction` | yes | yes | yes | - | `#print axioms d2_binary_non_bornian_obstruction` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/frame_function_polytope.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/frame_function_polytope.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1014
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1014
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1014_fq_gleason_d2_rational_plane_obstruction.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1014_fq_gleason_d2_rational_plane_obstruction.md](../../../dag/derivations/10_finite_qm_core/tfq_1014_fq_gleason_d2_rational_plane_obstruction.md)
- sha256 (`lf-normalised`): `d64f0a18f6c0305485afcb08a20aba5d1f3bb77cfc70eb8e97087329e172da94`
- generated view: listed, not counted
- cited in: record TFQ-1014
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: [sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml](../../../sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `16a418a93748cef695fad3c1fab0fd14dd95c6985b23ee8a814b171eca60a445`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQ-R-GLEASON-D2` `DERIVED_LEAN`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `FQ-R-GAP-BORN-UNIQUENESS` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-BORN-UNIQUENESS-GLEASON](FQ-GAP-BORN-UNIQUENESS-GLEASON.md) (CONDITIONAL)
