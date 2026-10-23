# FQ-BELL-RATIONAL-VIOLATION-14-5

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Five literal kernel anchors for the fixed admitted quantum matrices and arbitrary Nat-weighted assignment obstruction, plus three independently checked exact native cases and actual mutation rejections.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- tensor composition, entangled preparation, trace/Born pairing (assumption)

## Bottleneck

Unmet after the PFP review: Deriving Born/tensor structure, physical locality/setting independence, a complete formal arbitrary-rational-table transport theorem, or general probability-subtype operad coherence. The broader source statement is kept in pfp_review.prior_statement.

## Source status

Pythagorean (3,4,5) CHSH violation 14/5 \> 2 and impossibility of non-negative joint extension mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/FQ-BELL-RATIONAL-VIOLATION-14-5/reviews/20261019_next_ten_audit/review_result.json](../../../dag/results/FQ-BELL-RATIONAL-VIOLATION-14-5/reviews/20261019_next_ten_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Five literal kernel anchors for the fixed admitted quantum matrices and arbitrary Nat-weighted assignment obstruction, plus three independently checked exact native cases and actual mutation rejections.
  - does not support: Deriving Born/tensor structure, physical locality/setting independence, a complete formal arbitrary-rational-table transport theorem, or general probability-subtype operad coherence.
  - next test: Deriving Born/tensor structure, physical locality/setting independence, a complete formal arbitrary-rational-table transport theorem, or general probability-subtype operad coherence.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0259 (shared), record TFQ-0260 (shared)
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_bell_rational_violation_14_5_no_joint_law` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_bell_rational_violation_14_5_no_joint_law` |
- counts toward the grade: yes

### Lean: `lean4/H053EverettForkingTree.lean`

- file: [lean4/H053EverettForkingTree.lean](../../../lean4/H053EverettForkingTree.lean)
- sha256 (`bytes`): `8730f0cdd32665b8aa902d31fe2bc2b99a5dcde35cf3ccb8f99019c952698b59`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build H053EverettForkingTree`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `chsh_pythagorean_quantum_value` | yes | yes | yes | - | `#print axioms chsh_pythagorean_quantum_value` |
- counts toward the grade: yes

### Lean: `lean4/QuantumCorrelation.lean`

- file: [lean4/QuantumCorrelation.lean](../../../lean4/QuantumCorrelation.lean)
- sha256 (`bytes`): `1efde024ea6004e14e564be78cc1e9c5238919f28f2ddc1a1fbf6b58f6fa00bd`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build QuantumCorrelation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `q1_violates_classical_bound` | yes | yes | yes | - | `#print axioms q1_violates_classical_bound` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/finite_bell_extension.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/finite_bell_extension.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/finite_chsh_correlations.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/finite_chsh_correlations.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0259_finite_chsh_ceiling_on_one_global_joint_table.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0259_finite_chsh_ceiling_on_one_global_joint_table.md](../../../dag/derivations/12_finite_qm_structure/tfq_0259_finite_chsh_ceiling_on_one_global_joint_table.md)
- sha256 (`lf-normalised`): `b2177f05c11715d1dec037d5488c6c1e891d6c536e6fb4c875616087051c4c65`
- generated view: listed, not counted
- cited in: record TFQ-0259 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0260_bell_theorem_not_derived_from_the_finite_tables.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0260_bell_theorem_not_derived_from_the_finite_tables.md](../../../dag/derivations/12_finite_qm_structure/tfq_0260_bell_theorem_not_derived_from_the_finite_tables.md)
- sha256 (`lf-normalised`): `8e74bdeb1880d57c749bbd6b57d2a038c234d7f96f014f15ccd1d5d5ea06c7a7`
- generated view: listed, not counted
- cited in: record TFQ-0260 (shared)
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `5e43f206b08726fd4b27888d6fed3f211aac8398d5f8bf3dce712c415d7d81cc`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0259 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm
- TFQ-0259 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/finite_chsh_correlations.rs
- TFQ-0260 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/finite_chsh_correlations.rs

## Routes

Incoming (1):

- `FQ-R-BELL-VIOLATION` `DERIVED_LEAN`: [FQ-BELL-CLASSICAL-JOINT-EXTENSION](FQ-BELL-CLASSICAL-JOINT-EXTENSION.md) (PROVED_LEAN), [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION), [FQ-TENSOR-LU-RIVAL-EXCLUSION](FQ-TENSOR-LU-RIVAL-EXCLUSION.md) (PROVED_LEAN)

Outgoing (1):

- `FQ-R-TSIRELSON` `CONDITIONAL_ON_IMPORT`: [FQ-TSIRELSON-SOS-Q-SQRT2](FQ-TSIRELSON-SOS-Q-SQRT2.md) (PROVED_LEAN)
