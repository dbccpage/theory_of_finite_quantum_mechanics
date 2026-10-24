# FQ-CARRIER-CONTRACT-V2

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Declared carrier: cyclotomic fields Q(zeta_n) with directed tower law (m | n gives Q(zeta_m) \<= Q(zeta_n)), declared target conductor LCM 120 (distinct conductors 1,2,3,4,5,8,12; 23 targets), Born weights |psi_j|^2 in the real subfield Q(zeta_n)^+. The colimit Q^ab is named but not constructed; Kronecker-Weber is DECLARED.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- complex/cyclotomic scalar field Q(zeta_n) (assumption)
- Kronecker-Weber theorem cited, not proved (assumption)
- target conductor 120 chosen, minimality not proved (assumption)

## Bottleneck

Q^ab colimit not constructed; no proof that 120 is minimal; amplitude embedding for all 23 targets not verified.

## Source status

REVIEWED_DECLARATIONS (carrier_contract.yaml); minimality_proved: false; all_target_amplitudes_embedding_verified: false

## Review

- PFP review: [dag/results/FQ-CARRIER-CONTRACT-V2/reviews/20261019_next_ten_audit/review_result.json](../../../dag/results/FQ-CARRIER-CONTRACT-V2/reviews/20261019_next_ten_audit/review_result.json); file present and sha256 matches the node's record: no; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `DEFINITION`; qualifies for E4: no.
  - narrowest claim: LCM120 on the actual inventory, literal conductor directedness and star-compatible RingHom theorem signatures, and seven independently checked quotient computations.
  - does not support: Constructed Q^ab colimit, proved Kronecker-Weber, field minimality, or verification of all amplitudes in all targets.
  - next test: Audit retained contract flags, complete coefficient arrays, actual Phi120 and optimized guard refusal.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1006
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation` |
| `QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure` |
- counts toward the grade: yes

### Lean: `lean4/H052CyclotomicTowerDirected.lean`

- file: [lean4/H052CyclotomicTowerDirected.lean](../../../lean4/H052CyclotomicTowerDirected.lean)
- sha256 (`bytes`): `c7e8d3e1e36a80bf4e60d9da3bae5cafef90a386f410fc244ea616e33a45fc43`
- cited in: node.lean, record TFQ-1006
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `H052CyclotomicTowerDirected`): recorded sha256 `c7e8d3e1e36a80bf4e60d9da3bae5cafef90a386f410fc244ea616e33a45fc43` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build H052CyclotomicTowerDirected`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `cyclotomic_tower_is_directed` | yes | yes | yes | none | `#print axioms cyclotomic_tower_is_directed` |
- counts toward the grade: yes

### Lean: `lean4/H057HigherDimConductorBounds.lean`

- file: [lean4/H057HigherDimConductorBounds.lean](../../../lean4/H057HigherDimConductorBounds.lean)
- sha256 (`bytes`): `490d743d8b1395d21bed1914a4a7050117ea25b9cde576a42e1293c472a47253`
- cited in: node.lean, record TFQ-1006
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `H057HigherDimConductorBounds`): recorded sha256 `490d743d8b1395d21bed1914a4a7050117ea25b9cde576a42e1293c472a47253` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build H057HigherDimConductorBounds`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `css_horodecki_conductor_1_div_120` | yes | yes | yes | propext | `#print axioms css_horodecki_conductor_1_div_120` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/tower.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/tower.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1006
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1006
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1006_fq_carrier_contract_v2.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1006_fq_carrier_contract_v2.md](../../../dag/derivations/10_finite_qm_core/tfq_1006_fq_carrier_contract_v2.md)
- sha256 (`lf-normalised`): `9ebce71f008a50f9578bbded6858d4687aeb144c520deaf8530f51e45f57cc31`
- generated view: listed, not counted
- cited in: record TFQ-1006
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/claims/carrier_contract.yaml`

- file: [sources/atlas/F004_papers/006_finite_qm/claims/carrier_contract.yaml](../../../sources/atlas/F004_papers/006_finite_qm/claims/carrier_contract.yaml)
- sha256 (`lf-normalised`): `a1c709630c5a79fef6a8638e8fd9ee2d081643405a1ef49796e99c3b83ab8cb8`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `5e43f206b08726fd4b27888d6fed3f211aac8398d5f8bf3dce712c415d7d81cc`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (0):


Outgoing (18):

- `APP-R-DFM-GROUP-CONNECTION` `CONDITIONAL_ON_IMPORT`: [DFM-GROUP-CONNECTION](DFM-GROUP-CONNECTION.md) (DEFINITION)
- `DS-R-GRADED-PATHSUM-FROM-CARRIER` `COMPUTED`: [DS-QM030-GRADED-PATHSUM](DS-QM030-GRADED-PATHSUM.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-PRODUCT-DEFECT` `DERIVED_LEAN`: [DS-QM070-PRODUCT-NONFACTORIZATION](DS-QM070-PRODUCT-NONFACTORIZATION.md) (PROVED_LEAN)
- `DS-R-STOCHASTIC-KERNEL` `DERIVED_LEAN`: [DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL](DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL.md) (PROVED_LEAN)
- `DS-R-TRACE-NORM-CORE-FROM-CARRIER` `DERIVED_LEAN`: [DS-QM080-IMPORT-FREE-TRACE-NORM-CORE](DS-QM080-IMPORT-FREE-TRACE-NORM-CORE.md) (PROVED_LEAN)
- `DS-R-UNGRADED-COUNT` `COMPUTED`: [DS-QM030-UNGRADED-OVERCOUNT](DS-QM030-UNGRADED-OVERCOUNT.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-CARRIER-TO-INTERFACE` `CONDITIONAL_ON_IMPORT`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)
- `FQ-R-CONTINUUM-HILBERT-LIFT-CONSTRUCTION` `CONDITIONAL_ON_IMPORT`: [FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION](FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION.md) (PROVED_LEAN)
- `FQ-R-DYN-DICHOTOMY` `DERIVED_LEAN`: [FQ-DISCRETE-DYNAMICS-DICHOTOMY](FQ-DISCRETE-DYNAMICS-DICHOTOMY.md) (PROVED_LEAN)
- `FQ-R-EMBEDDING` `COMPUTED`: [FQ-GAP-REAL-EMBEDDING-CHOICE](FQ-GAP-REAL-EMBEDDING-CHOICE.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-ENTROPY` `DERIVED_LEAN`: [FQ-ENTROPY-DICHOTOMY-BAKER](FQ-ENTROPY-DICHOTOMY-BAKER.md) (PROVED_LEAN)
- `FQ-R-EVERETT` `DERIVED_LEAN`: [FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY](FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY.md) (PROVED_LEAN)
- `FQ-R-GAP-CONTINUUM` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-CONTINUUM-HILBERT-LIFT](FQ-GAP-CONTINUUM-HILBERT-LIFT.md) (CONDITIONAL)
- `FQ-R-QM207-231` `DERIVED_LEAN`: [FQ-QM207-231-FINITE-MAP-CONTROLS](FQ-QM207-231-FINITE-MAP-CONTROLS.md) (PROVED_LEAN)
- `FQ-R-SORKIN-CLASS` `DERIVED_LEAN`: [FQ-SORKIN-READOUT-CLASS-QM208](FQ-SORKIN-READOUT-CLASS-QM208.md) (PROVED_LEAN)
- `FQ-R-TSIRELSON` `CONDITIONAL_ON_IMPORT`: [FQ-TSIRELSON-SOS-Q-SQRT2](FQ-TSIRELSON-SOS-Q-SQRT2.md) (PROVED_LEAN)
- `FQ-R-U1` `DERIVED_LEAN`: [FQ-U1-TRANSPORT-N-TORSION](FQ-U1-TRANSPORT-N-TORSION.md) (PROVED_LEAN)
- `FQ-R-WEYL` `DERIVED_LEAN`: [FQ-WEYL-FINITE-SCHRODINGER-IRREDUCIBILITY](FQ-WEYL-FINITE-SCHRODINGER-IRREDUCIBILITY.md) (PROVED_LEAN)

No incoming route.
