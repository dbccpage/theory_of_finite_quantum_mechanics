# FQ-DISCRETE-DYNAMICS-DICHOTOMY

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: An all-natural-index integer numerator is nonzero in Lean; actual normalized retained powers have unit mass and never equal identity, unlike periodic controls.

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

- declared unitary step (assumption)
- generator branch selection for periodic sector (assumption)

## Bottleneck

Unmet after the PFP review: Prove the recurrence-to-normalized-matrix bridge for all powers, then formulate any closure/topology or generator selection claim. No full dynamics dichotomy is inferred. The broader source statement is kept in pfp_review.prior_statement.

## Source status

H061; Rust exact periodic/aperiodic classification

## Review

- PFP review: [dag/results/FQ-DISCRETE-DYNAMICS-DICHOTOMY/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/FQ-DISCRETE-DYNAMICS-DICHOTOMY/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: An all-natural-index integer numerator is nonzero in Lean; actual normalized retained powers have unit mass and never equal identity, unlike periodic controls.
  - does not support: Prove the recurrence-to-normalized-matrix bridge for all powers, then formulate any closure/topology or generator selection claim. No full dynamics dichotomy is inferred.
  - next test: Prove the recurrence-to-normalized-matrix bridge for all powers, then formulate any closure/topology or generator selection claim. No full dynamics dichotomy is inferred.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0245 (shared)
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition` |
- counts toward the grade: yes

### Lean: `lean4/H061DynamicsDichotomy.lean`

- file: [lean4/H061DynamicsDichotomy.lean](../../../lean4/H061DynamicsDichotomy.lean)
- sha256 (`bytes`): `6b4893a0aecdad09e886450c1533fdaf15dc292abfea80da96d2989fe9703c17`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build H061DynamicsDichotomy`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `periodic_sector_requires_declaration` | yes | yes | yes | - | `#print axioms periodic_sector_requires_declaration` |
| `pythagorean_rotation_order_infinite` | yes | yes | yes | - | `#print axioms pythagorean_rotation_order_infinite` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/dynamics_dichotomy.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/dynamics_dichotomy.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0245_unitary_finite_shadow_slot_still_reserved.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0245_unitary_finite_shadow_slot_still_reserved.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0245_unitary_finite_shadow_slot_still_reserved.md)
- sha256 (`lf-normalised`): `a70dea94189cb9ca6b93b538a6421895c099576905968fec92f698c6cbfcdbbb`
- generated view: listed, not counted
- cited in: record TFQ-0245 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/14_finite_gauge/tfq_0052_each_language_must_carry_on_a_declared_m_2_q_i_packet_d0_of_an.md`

- file: [dag/derivations/14_finite_gauge/tfq_0052_each_language_must_carry_on_a_declared_m_2_q_i_packet_d0_of_an.md](../../../dag/derivations/14_finite_gauge/tfq_0052_each_language_must_carry_on_a_declared_m_2_q_i_packet_d0_of_an.md)
- sha256 (`lf-normalised`): `24435b37027494cea1e6541393a74dfaa720915fdab89c57efcf22685a0d8568`
- generated view: listed, not counted
- cited in: record TFQ-0052 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0062_each_language_must_carry_a_truncated_intermediate_normalization_series_a.md`

- file: [dag/derivations/15_finite_qed/tfq_0062_each_language_must_carry_a_truncated_intermediate_normalization_series_a.md](../../../dag/derivations/15_finite_qed/tfq_0062_each_language_must_carry_a_truncated_intermediate_normalization_series_a.md)
- sha256 (`lf-normalised`): `d28b4c28546613fdb63a8abc8dd898dfc84f332f0afcf2944f8c6046ed79404b`
- generated view: listed, not counted
- cited in: record TFQ-0062
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: [sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml](../../../sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `16a418a93748cef695fad3c1fab0fd14dd95c6985b23ee8a814b171eca60a445`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `5e43f206b08726fd4b27888d6fed3f211aac8398d5f8bf3dce712c415d7d81cc`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0052 lean4: not located
- TFQ-0052 python: not located
- TFQ-0052 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/gauge_cochain_complex.rs
- TFQ-0062 lean4: not located
- TFQ-0062 python: not located
- TFQ-0062 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/perturbation_theory.rs

## Routes

Incoming (1):

- `FQ-R-DYN-DICHOTOMY` `DERIVED_LEAN`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION), [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `FQ-R-STONE-AMBIGUITY` `DERIVED_LEAN`: [FQ-DISCRETE-TIME-STONE-AMBIGUITY](FQ-DISCRETE-TIME-STONE-AMBIGUITY.md) (PROVED_LEAN)
