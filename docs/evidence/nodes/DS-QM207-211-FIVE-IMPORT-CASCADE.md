# DS-QM207-211-FIVE-IMPORT-CASCADE

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Exact phase/readout and noncommutative matrix controls are retained, and the cross-term and quartic-gap polynomials are exact identities over the rationals. They do not derive the five imports (U(1) phase fiber, quadratic readout, operator algebra, Born uniqueness, continuous dynamics) or establish that those imports are independent.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Prove each correctly specified physical necessity claim and supply phase, quadratic pairing, operator algebra, Born uniqueness and continuous dynamics. These controls do not derive or establish independence of all five imports. The broader source statement is kept in pfp_review.prior_statement.

## Source status

QM207-C1 phase-blindness of L1 weights, QM208-C3 quadratic cross-term interference, QM209-C2 non-commutative operator algebra, QM210-C3 Lp power-rule separation, and QM211-C1..C3 five-import drop-one independence mechanized in DerivationDagQMClosure.lean and mirrored in 006_finite_qm

## Review

- PFP review: [dag/results/DS-QM207-211-FIVE-IMPORT-CASCADE/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/DS-QM207-211-FIVE-IMPORT-CASCADE/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact phase/readout and noncommutative matrix controls are retained; cross-term and quartic-gap polynomials are general rational kernel identities.
  - does not support: Prove each correctly specified physical necessity claim and supply phase, quadratic pairing, operator algebra, Born uniqueness and continuous dynamics. These controls do not derive or establish independence of all five imports.
  - next test: Prove each correctly specified physical necessity claim and supply phase, quadratic pairing, operator algebra, Born uniqueness and continuous dynamics. These controls do not derive or establish independence of all five imports.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1042
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_and_207_211_tier3_survival_rebit_tomography_and_five_import_cascade` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_and_207_211_tier3_survival_rebit_tomography_and_five_import_cascade` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm206_207_211_non_full_non_faithful_descent_and_five_import_independence` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm206_207_211_non_full_non_faithful_descent_and_five_import_independence` |
- counts toward the grade: yes

### Lean: `lean4/H012OperatorAlgebraShadow.lean`

- file: [lean4/H012OperatorAlgebraShadow.lean](../../../lean4/H012OperatorAlgebraShadow.lean)
- sha256 (`bytes`): `bee179ccd42c430d04f382bcf88c73976797d938a5162bda1e8c8a24bebba3a3`
- cited in: node.lean, record TFQ-1042
- replay: `none`
- check: `cd lean4 && lake build H012OperatorAlgebraShadow`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `operator_algebra_shadow` | yes | yes | yes | - | `#print axioms operator_algebra_shadow` |
- counts toward the grade: yes

### Lean: `lean4/H013BornPairingBoundary.lean`

- file: [lean4/H013BornPairingBoundary.lean](../../../lean4/H013BornPairingBoundary.lean)
- sha256 (`bytes`): `debafe0eefb016e289a18fb9a308224f73464282e15c17eef143e5ea5342b642`
- cited in: node.lean, record TFQ-1042
- replay: `none`
- check: `cd lean4 && lake build H013BornPairingBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `quartic_not_proportional` | yes | yes | yes | - | `#print axioms quartic_not_proportional` |
- counts toward the grade: yes

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, record TFQ-1042
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1042
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1042
- counts toward the grade: no

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1042
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_1042_ds_qm207_211_five_import_cascade.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_1042_ds_qm207_211_five_import_cascade.md](../../../dag/derivations/12_finite_qm_structure/tfq_1042_ds_qm207_211_five_import_cascade.md)
- sha256 (`lf-normalised`): `944b578460c71a8d7f0269f13f41f79b5485c9f7cea0a676e1f0006a38367918`
- generated view: listed, not counted
- cited in: record TFQ-1042
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/207_complex_phase_fiber_and_u1_transport_lift/qm_207_complex_phase_fiber_and_u1_transport_lift_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/207_complex_phase_fiber_and_u1_transport_lift/qm_207_complex_phase_fiber_and_u1_transport_lift_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/208_quadratic_l2_readout_and_interference_boundary/qm_208_quadratic_l2_readout_and_interference_boundary_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/208_quadratic_l2_readout_and_interference_boundary/qm_208_quadratic_l2_readout_and_interference_boundary_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/209_non_commutative_operator_algebra_and_contextuality/qm_209_non_commutative_operator_algebra_and_contextuality_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/209_non_commutative_operator_algebra_and_contextuality/qm_209_non_commutative_operator_algebra_and_contextuality_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/210_born_rule_postulate_and_state_effect_pairing/qm_210_born_rule_postulate_and_state_effect_pairing_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/210_born_rule_postulate_and_state_effect_pairing/qm_210_born_rule_postulate_and_state_effect_pairing_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/211_continuous_unitary_dynamics_and_l1_to_qm_synthesis/qm_211_continuous_unitary_dynamics_and_l1_to_qm_synthesis_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/211_continuous_unitary_dynamics_and_l1_to_qm_synthesis/qm_211_continuous_unitary_dynamics_and_l1_to_qm_synthesis_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (2):

- `DS-R-DYNAMICS-FROM-L1` `COMPUTED`: [DS-QM030-GRADED-PATHSUM](DS-QM030-GRADED-PATHSUM.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-FIVE-IMPORT` `COMPUTED`: [DS-QM062-U1-RESIDUES-IMPORT](DS-QM062-U1-RESIDUES-IMPORT.md) (IMPORTED_ASSUMPTION), [DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE](DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE.md) (PROVED_LEAN), [DS-QM204-BORN-UNIQUENESS-IMPORT-BOUNDARY](DS-QM204-BORN-UNIQUENESS-IMPORT-BOUNDARY.md) (IMPORTED_ASSUMPTION), [DS-CONTINUOUS-TIME-EXP-GENERATOR](DS-CONTINUOUS-TIME-EXP-GENERATOR.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

