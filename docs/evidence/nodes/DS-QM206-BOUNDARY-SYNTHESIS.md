# DS-QM206-BOUNDARY-SYNTHESIS

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On a declared four-vertex toy map the image and kernel and all composition controls are exact, and additive homomorphism, collision and missed-arrow statements hold. The toy map is not the intended descent functor from the graph-transport category to finite-dimensional Hilbert spaces; functoriality, non-fullness and non-faithfulness are not established.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 1 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Define the intended GTOC/Hilb categories and actual descent functor, prove its properties and discharge the QM205 pointer-basis stub. The toy map is not that functor. The broader source statement is kept in pfp_review.prior_statement.

## Source status

QM206-C1 4-vertex plaquette cochain exactness d1(d0 f)=0, QM206-C3 coboundary holonomy invariance, and QM206-C7 Theorem 2.1 non-full/non-faithful diagonal descent F_Descent mechanized in DerivationDagQMClosure.lean and mirrored in 006_finite_qm

## Review

- PFP review: [dag/results/DS-QM206-BOUNDARY-SYNTHESIS/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/DS-QM206-BOUNDARY-SYNTHESIS/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: no; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Actual C4 image/kernel and all composition controls are exact; additive homomorphism, collision and missed-arrow statements are kernel checked.
  - does not support: Define the intended GTOC/Hilb categories and actual descent functor, prove its properties and discharge the QM205 pointer-basis stub. The toy map is not that functor.
  - next test: Define the intended GTOC/Hilb categories and actual descent functor, prove its properties and discharge the QM205 pointer-basis stub. The toy map is not that functor.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1041
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm206_207_211_non_full_non_faithful_descent_and_five_import_independence` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm206_207_211_non_full_non_faithful_descent_and_five_import_independence` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm206_four_tier_cochain_exactness_holonomy_invariance_and_nonfull_nonfaithful_descent` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm206_four_tier_cochain_exactness_holonomy_invariance_and_nonfull_nonfaithful_descent` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1041
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1041
- counts toward the grade: no

### Rust: `sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust, record TFQ-1041

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche19_ds_qm062_094_101_206_u1_selector_everett_threshold_and_boundary_synthesis_witness` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_1041_ds_qm206_boundary_synthesis.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_1041_ds_qm206_boundary_synthesis.md](../../../dag/derivations/12_finite_qm_structure/tfq_1041_ds_qm206_boundary_synthesis.md)
- sha256 (`lf-normalised`): `19e079060025f3c2c46394381021a9f8dc05f0fe21eb42cefdedafcc2bf119fa`
- generated view: listed, not counted
- cited in: record TFQ-1041
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/206_universal_boundary_synthesis_and_cochain_lift/qm_206_universal_boundary_synthesis_and_cochain_lift_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/206_universal_boundary_synthesis_and_cochain_lift/qm_206_universal_boundary_synthesis_and_cochain_lift_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `DS-R-MERMIN-PERES-TO-CONTEXTUALITY` `COMPUTED`: [DS-QM120-MERMIN-PERES-F2-OBSTRUCTION](DS-QM120-MERMIN-PERES-F2-OBSTRUCTION.md) (PROVED_LEAN)

Outgoing (0):

