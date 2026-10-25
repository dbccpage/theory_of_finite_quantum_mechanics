# FQ-GAP-TENSOR-UNIQUENESS

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> General finite-dimensional quantum composition follows from supplied local complex QM, independent preparation and testing, local tomography, local unitaries, and a fully calibrated reversible controlled shift. The state and generated effect cones are PSD; full effect and POVM availability has explicit saturation assumptions. Primitive difference has not supplied these operational premises.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

- `receipt_not_current`: lean4/CoupledRelationalProjectors.lean: replay failed against 1 receipt(s). A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit.

## Imported structure

- local finite complex quantum state and effect spaces with trace probabilities
- independent preparation, testing and convex composition
- local tomography
- all local unitary operations
- fully coherently calibrated reversible controlled shift
- effect and finite-test saturation for full measurement availability

## Bottleneck

The state and measurement corollaries are verified under their stated operational hypotheses. Deriving local complex QM, tomography, calibrated reversible interactions and both saturation assumptions from primitive difference remains conditional.

## Source status

The 20261019 scope audit remains a determinant obstruction on a supplied rational host. TFQ-0410--TFQ-0412 verify general Lean tomography, Schmidt reachability and operational state-cone reconstruction. TFQ-0414--TFQ-0416 verify the generated effect cone, saturated binary interval and finite POVM corollaries. TFQ-0413 verifies assumption countermodels in Lean: full-cone duality, all-dimension cone separations, exact two-qubit calibration failures and hidden-coordinate tomography failure; external classification and primitive selection remain outside scope.

## Review

- PFP review: [dag/results/FQ-GAP-TENSOR-UNIQUENESS/reviews/20261019_scope_audit/review_result.json](../../../dag/results/FQ-GAP-TENSOR-UNIQUENESS/reviews/20261019_scope_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `CONDITIONAL`; qualifies for E4: yes.
  - narrowest claim: On the admitted 2x2 rational coefficient host every simple tensor has zero coefficient determinant; \[\[1,0\],\[0,1\]\] has determinant one and is not simple. Native norm multiplication is checked on retained inputs.
  - does not support: Formalize state/effect cones, covariance requirements, their min/max comparison and any uniqueness theorem; general tensor selection remains an import.
  - next test: Formalize state/effect cones, covariance requirements, their min/max comparison and any uniqueness theorem; general tensor selection remains an import.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CoupledRelationalProjectors.lean`

- file: [lean4/CoupledRelationalProjectors.lean](../../../lean4/CoupledRelationalProjectors.lean)
- sha256 (`bytes`): `22fcce9a754950721bc56674fef83ff3910b73d73f8919c6bd576f6e28500d60`
- cited in: node.lean, record TFQ-1019
- replay: `failed`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `CoupledRelationalProjectors`): recorded sha256 `22fcce9a754950721bc56674fef83ff3910b73d73f8919c6bd576f6e28500d60` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: no; axioms recorded: none (not itemised); only standard axioms: yes
- check: `cd lean4 && lake build CoupledRelationalProjectors`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.CoupledRelationalProjectors.coupled_bipartite_and_tripartite_relational_master_certificate` | yes | yes | yes | - | `#print axioms QuantumMechanics.CoupledRelationalProjectors.coupled_bipartite_and_tripartite_relational_master_certificate` |
- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1019
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm070_071_product_nonfactorization_and_entanglement_witness` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm070_071_product_nonfactorization_and_entanglement_witness` |
| `QuantumMechanics.DerivationDagQMClosure.fq_gap_tensor_uniqueness_min_vs_max_tensor_and_covariance` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gap_tensor_uniqueness_min_vs_max_tensor_and_covariance` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/coupled_relational_operad.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/coupled_relational_operad.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1019
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1019
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md](../../../dag/derivations/10_finite_qm_core/tfq_1019_fq_gap_tensor_uniqueness.md)
- sha256 (`lf-normalised`): `1fda0a5a407c3168c4c8bd936049059514e100157f2594c4f2d96c5bae7d5f78`
- generated view: listed, not counted
- cited in: record TFQ-1019
- counts toward the grade: no

### Documents and data: `dag/derivations/27_tensor_composition/tfq_0412_tensor_controlled_shift_reconstruction.md`

- file: [dag/derivations/27_tensor_composition/tfq_0412_tensor_controlled_shift_reconstruction.md](../../../dag/derivations/27_tensor_composition/tfq_0412_tensor_controlled_shift_reconstruction.md)
- sha256 (`lf-normalised`): `3dd28ec9850c6667c6b8ca677516507f3a56667b03d264c225f3b5056b7b2a34`
- generated view: listed, not counted
- cited in: node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md`

- file: [dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md](../../../dag/derivations/27_tensor_composition/tfq_0413_tensor_assumption_countermodels.md)
- sha256 (`lf-normalised`): `3d1f897722aad08811a52c863e8bc47cfda41d9d087929a00c3925f4782de12f`
- generated view: listed, not counted
- cited in: node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/27_tensor_composition/tfq_0414_tensor_generated_effect_cone.md`

- file: [dag/derivations/27_tensor_composition/tfq_0414_tensor_generated_effect_cone.md](../../../dag/derivations/27_tensor_composition/tfq_0414_tensor_generated_effect_cone.md)
- sha256 (`lf-normalised`): `126de574698271544d28d12fda6f87f088637b5f3b4cf0ddd0aa6a974362cc02`
- generated view: listed, not counted
- cited in: node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/27_tensor_composition/tfq_0415_tensor_binary_effect_interval.md`

- file: [dag/derivations/27_tensor_composition/tfq_0415_tensor_binary_effect_interval.md](../../../dag/derivations/27_tensor_composition/tfq_0415_tensor_binary_effect_interval.md)
- sha256 (`lf-normalised`): `2c5fb04175f367a1d58477d317882002336577f65d895226c9ab4bc01eb9377a`
- generated view: listed, not counted
- cited in: node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/27_tensor_composition/tfq_0416_tensor_finite_povm_availability.md`

- file: [dag/derivations/27_tensor_composition/tfq_0416_tensor_finite_povm_availability.md](../../../dag/derivations/27_tensor_composition/tfq_0416_tensor_finite_povm_availability.md)
- sha256 (`lf-normalised`): `db945ab62338d7c0037b8c012ad05d4c893694524faf0397ac79ffee4ddda4e9`
- generated view: listed, not counted
- cited in: node.source
- counts toward the grade: no

### Documents and data: `dag/research/tensor_composition_validation.json`

- file: [dag/research/tensor_composition_validation.json](../../../dag/research/tensor_composition_validation.json)
- sha256 (`lf-normalised`): `9f4014f2485a76aeaa79e6ea0a10f50ce6176aa3f66df26ccbbe86e6f0621c3a`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/tensor_countermodel_validation.json`

- file: [dag/research/tensor_countermodel_validation.json](../../../dag/research/tensor_countermodel_validation.json)
- sha256 (`lf-normalised`): `9a3e9275bb33b7685e3e4fee65915044fd36b0a65e14d2a079a645039d7494e2`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/tensor_formalization_validation.json`

- file: [dag/research/tensor_formalization_validation.json](../../../dag/research/tensor_formalization_validation.json)
- sha256 (`lf-normalised`): `ca55404cc4a6e1f125b85d21f9bd60a7bc9dfe0e65c85207110c788f0203c120`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/tensor_measurement_validation.json`

- file: [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json)
- sha256 (`lf-normalised`): `0ba5c6fbd2b445aaf6f372a6f0b46427b7440245e863408a41ef7d6f0a2c6e90`
- cited in: node.source
- counts toward the grade: yes

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

## Routes

Incoming (2):

- `FQ-R-GAP-TENSOR` `CONDITIONAL_ON_IMPORT`: [FQ-TENSOR-LU-RIVAL-EXCLUSION](FQ-TENSOR-LU-RIVAL-EXCLUSION.md) (PROVED_LEAN)
- `FRO-R-BACK-CT-INTEROP-TO-TENSOR` `GAP_NO_DERIVATION`: [CT-INFORMATION-MEDIA-INTEROPERABILITY](CT-INFORMATION-MEDIA-INTEROPERABILITY.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `APP-R-TENSOR-TOMOGRAPHIC-COORDINATES` `DERIVED_LEAN`: [TENSOR-TOMOGRAPHIC-COORDINATES](TENSOR-TOMOGRAPHIC-COORDINATES.md) (PROVED_LEAN)
