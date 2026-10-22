# L1-QM020-THM3-ROW-SPARSITY

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact phase-sign readouts, row sparsity, determinant, monomial and rank distinctions; general row interference and a singular sparse control in Lean.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- linear representation of sectors: assumption
- unit phase rotations: assumption

## Bottleneck

Unmet after the PFP review: Prove the full representation refinement and add injectivity/column conditions before claiming monomial invertibility. No scalar label licenses the stronger claim. The broader source statement is kept in pfp_review.prior_statement.

## Source status

General-n row-sparsity characterization mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/L1-QM020-THM3-ROW-SPARSITY/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM020-THM3-ROW-SPARSITY/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact phase-sign readouts, row sparsity, determinant, monomial and rank distinctions; general row interference and a singular sparse control in Lean.
  - does not support: Prove the full representation refinement and add injectivity/column conditions before claiming monomial invertibility. No scalar label licenses the stronger claim.
  - next test: Prove the full representation refinement and add injectivity/column conditions before claiming monomial invertibility. No scalar label licenses the stronger claim.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornRedundancy.lean`

- file: [lean4/BornRedundancy.lean](../../../lean4/BornRedundancy.lean)
- sha256 (`bytes`): `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b`
- cited in: node.lean, record TFQ-0300 (shared)
- replay: `none`
- check: `cd lean4 && lake build BornRedundancy`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `descent_compatible_iff_row_sparse` | yes | yes | yes | - | `#print axioms descent_compatible_iff_row_sparse` |
| `row_sparse_implies_descent_compatible` | yes | yes | yes | - | `#print axioms row_sparse_implies_descent_compatible` |
- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_phase_blind_descent_general_n_row_sparsity` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_phase_blind_descent_general_n_row_sparsity` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0300_descent_compatible_maps_stay_row_sparse.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0300_descent_compatible_maps_stay_row_sparse.md](../../../dag/derivations/08_l1_to_l2/tfq_0300_descent_compatible_maps_stay_row_sparse.md)
- sha256 (`lf-normalised`): `1711cef9f69d5cafbf72d2e3c1a12bb8ce47f6773b96bab5491aec0055e0ca38`
- generated view: listed, not counted
- cited in: record TFQ-0300 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0300 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs

## Routes

Incoming (1):

- `L1-R-THM3` `DERIVED_LEAN`: [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) (CONDITIONAL), [L1-IMP-COMPLEX-FIELD](L1-IMP-COMPLEX-FIELD.md) (CONDITIONAL), [L1-IMP-U1-PHASES](L1-IMP-U1-PHASES.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

