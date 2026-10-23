# DS-QM063-HOLONOMY-COHERENT-INTENSITY

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Relative Gaussian holonomy and two-path intensity are invariant under the retained common unit phases; the rational unit-phase conditional is general in Lean.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 6 Lean reference(s) cited, 6 in this checkout (replay: none 6). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Prove the full graph connection/tree gauge-trivialization and matrix-valued holonomy transports; no SU(2) trace bound or higher-form result is claimed. The broader source statement is kept in pfp_review.prior_statement.

## Source status

QCS-C2 two-path coherent intensity identity, vertex gauge invariance, QCS-C4 3-edge spanning-tree gauge triviality, and QCS-C9 L1 non-factorization mechanized in DerivationDagQMClosure.lean and mirrored in 006_finite_qm

## Review

- PFP review: [dag/results/DS-QM063-HOLONOMY-COHERENT-INTENSITY/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM063-HOLONOMY-COHERENT-INTENSITY/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Relative Gaussian holonomy and two-path intensity are invariant under the retained common unit phases; the rational unit-phase conditional is general in Lean.
  - does not support: Prove the full graph connection/tree gauge-trivialization and matrix-valued holonomy transports; no SU(2) trace bound or higher-form result is claimed.
  - next test: Prove the full graph connection/tree gauge-trivialization and matrix-valued holonomy transports; no SU(2) trace bound or higher-form result is claimed.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CoboundaryHolonomy.lean`

- file: [lean4/CoboundaryHolonomy.lean](../../../lean4/CoboundaryHolonomy.lean)
- sha256 (`bytes`): `79c60e8ecd695f4e19de55b0502d2a0236c79d8b4d2ce6079a7516bc89e640fe`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build CoboundaryHolonomy`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `coboundary_closed_cycle_zero` | yes | yes | yes | - | `#print axioms coboundary_closed_cycle_zero` |
| `flux_obstructs_coboundary` | yes | yes | yes | - | `#print axioms flux_obstructs_coboundary` |
- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0254
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm063_032_034_destructive_interference_and_cayley_vs_euler_norm` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm063_032_034_destructive_interference_and_cayley_vs_euler_norm` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm063_holonomy_coherent_intensity_and_gauge_invariance` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm063_holonomy_coherent_intensity_and_gauge_invariance` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm063_tree_gauge_triviality_vertex_repair_and_l1_non_factorization` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm063_tree_gauge_triviality_vertex_repair_and_l1_non_factorization` |
- counts toward the grade: yes

### Lean: `sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`

- file: [sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean](../../../sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `a2ec0a203277c5c7b4bd71067351c574509c655c18bf0e08fe3c05a8005fc497`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm063_tree_gauge_triviality_vertex_repair_and_l1_non_factorization` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm063_tree_gauge_triviality_vertex_repair_and_l1_non_factorization` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/holonomy_interference.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/holonomy_interference.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche18_ds_qm063_072_073_090_holonomy_bit_shadow_chsh_and_o022_closure_witness` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0254_holonomy_structured_coherent_intensity.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0254_holonomy_structured_coherent_intensity.md](../../../dag/derivations/12_finite_qm_structure/tfq_0254_holonomy_structured_coherent_intensity.md)
- sha256 (`lf-normalised`): `de650e72bb0e5b52cd654778e381b6e0118ba16b275c3464603dc8ec910b00f9`
- generated view: listed, not counted
- cited in: record TFQ-0254
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0091_finite_loop_words_stay_on_the_declared_graph_continuum_connection_and_the.md`

- file: [dag/derivations/19_finite_qg/tfq_0091_finite_loop_words_stay_on_the_declared_graph_continuum_connection_and_the.md](../../../dag/derivations/19_finite_qg/tfq_0091_finite_loop_words_stay_on_the_declared_graph_continuum_connection_and_the.md)
- sha256 (`lf-normalised`): `d6cce5255667b1c4230d1ee056f267f4bd2b970fadb463b1f828358ae39de481`
- generated view: listed, not counted
- cited in: record TFQ-0091
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/063_holonomy_structured_superposition/qm_063_holonomy_structured_superposition_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/063_holonomy_structured_superposition/qm_063_holonomy_structured_superposition_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0091 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/holonomy_bridge_control.py
- TFQ-0091 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/holonomy_interference.rs
- TFQ-0254 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm

## Routes

Incoming (1):

- `DS-R-HOLONOMY-INTENSITY` `DERIVED_LEAN`: [DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE](DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE.md) (PROVED_LEAN)

Outgoing (5):

- `APP-R-FSP-U1-WILSON-ACTION` `CONDITIONAL_ON_IMPORT`: [FSP-U1-WILSON-ACTION](FSP-U1-WILSON-ACTION.md) (IMPORTED_ASSUMPTION)
- `DS-R-BUILDABILITY` `COMPUTED`: [DS-QM061-BUILDABILITY-SET-S](DS-QM061-BUILDABILITY-SET-S.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-DECOHERENCE-FUNCTIONAL` `DERIVED_LEAN`: [DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY](DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY.md) (PROVED_LEAN)
- `DS-R-GR-LQG` `DERIVED_LEAN`: [DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS](DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS.md) (PROVED_LEAN)
- `DS-R-REDIRECT` `DERIVED_LEAN`: [DS-QM064-074-083-ANNEX-REDIRECT-ROWS](DS-QM064-074-083-ANNEX-REDIRECT-ROWS.md) (PROVED_LEAN)
