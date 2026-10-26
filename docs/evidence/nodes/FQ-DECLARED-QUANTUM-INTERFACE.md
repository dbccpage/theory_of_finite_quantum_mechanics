# FQ-DECLARED-QUANTUM-INTERFACE

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Bundle of inputs every finite-QM result in this fragment consumes: scalar field (Q(i) or Q(zeta_n)), Hilbert/inner-product carrier, positive cone and effects, trace/Born pairing, tensor composition, declared channels, and (where used) a unitary step or time. Declared, not derived.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- complex scalar field (assumption)
- Hilbert/inner-product carrier (assumption)
- positivity and Born/trace pairing (assumption)
- tensor composition (assumption)
- time / unitary step (assumption)
- observer/record availability (assumption)

## Bottleneck

See FQ-PRIM-TO-QM-SELECTION-OPEN.

## Source status

paper s7 / s13.1: complex structure, Hilbert space, tensor factorization, Born rule, continuous time "enter the source papers as a declared import"

## Review

- PFP review: [dag/results/FQ-DECLARED-QUANTUM-INTERFACE/reviews/20261019_next_ten_audit/review_result.json](../../../dag/results/FQ-DECLARED-QUANTUM-INTERFACE/reviews/20261019_next_ten_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Three exact rational-real examples on an admitted finite quantum carrier with explicit source and import boundaries.
  - does not support: Derivation, necessity or independence of the quantum interface from primitive difference, or a derived time/dynamics.
  - next test: Audit declarations and actual matrices; do not promote API refusal or component counts to theorems.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1009
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm062_u1_selector_layers_and_ring_iso` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm062_u1_selector_layers_and_ring_iso` |
| `QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates` | yes | yes | yes | module-level | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/hilbert_space.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/hilbert_space.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1009
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/operational_axiom_selection.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/operational_axiom_selection.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1009
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1009
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1009_fq_declared_quantum_interface.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1009_fq_declared_quantum_interface.md](../../../dag/derivations/10_finite_qm_core/tfq_1009_fq_declared_quantum_interface.md)
- sha256 (`lf-normalised`): `43eaed4d74b23a29e01c4b4d7b87102f2cde5f0d480bd90c3af9074bdb630f40`
- generated view: listed, not counted
- cited in: record TFQ-1009
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

## Routes

Incoming (3):

- `FQ-R-CARRIER-TO-INTERFACE` `CONDITIONAL_ON_IMPORT`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION)
- `FQ-R-GAP-PRIM-TO-INTERFACE` `GAP_NO_DERIVATION`: [FQ-PRIMDIFF-QUOTIENT-KERNEL](FQ-PRIMDIFF-QUOTIENT-KERNEL.md) (PROVED_LEAN), [FQ-POSITIVE-WEIGHTS-ADMITTED](FQ-POSITIVE-WEIGHTS-ADMITTED.md) (IMPORTED_ASSUMPTION)
- `X-R-IMPORTS-TO-DECLARED-INTERFACE` `CONDITIONAL_ON_IMPORT`: [L1-IMP-COMPLEX-FIELD](L1-IMP-COMPLEX-FIELD.md) (CONDITIONAL), [L1-IMP-U1-PHASES](L1-IMP-U1-PHASES.md) (IMPORTED_ASSUMPTION), [L1-IMP-HILBERT-INNER-PRODUCT](L1-IMP-HILBERT-INNER-PRODUCT.md) (CONDITIONAL), [GP-IMPORT-TENSOR-PRODUCT](GP-IMPORT-TENSOR-PRODUCT.md) (IMPORTED_ASSUMPTION), [GP-IMPORT-CPTP-CLASS](GP-IMPORT-CPTP-CLASS.md) (IMPORTED_ASSUMPTION), [GP-IMPORT-CONTINUOUS-TIME](GP-IMPORT-CONTINUOUS-TIME.md) (IMPORTED_ASSUMPTION)

Outgoing (16):

- `APP-R-TENSOR-TOMOGRAPHIC-COORDINATES` `DERIVED_LEAN`: [TENSOR-TOMOGRAPHIC-COORDINATES](TENSOR-TOMOGRAPHIC-COORDINATES.md) (PROVED_LEAN)
- `FQ-R-BELL-VIOLATION` `COMPUTED`: [FQ-BELL-RATIONAL-VIOLATION-14-5](FQ-BELL-RATIONAL-VIOLATION-14-5.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-BORN-REDUNDANCY` `CONDITIONAL_ON_IMPORT`: [FQ-BORN-NORMALIZATION-REDUNDANCY](FQ-BORN-NORMALIZATION-REDUNDANCY.md) (PROVED_LEAN)
- `FQ-R-BUSCH` `COMPUTED`: [FQ-BUSCH-EFFECT-FRAME](FQ-BUSCH-EFFECT-FRAME.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-CABELLO` `DERIVED_LEAN`: [FQ-CABELLO-NO-INTEGER-FRAME](FQ-CABELLO-NO-INTEGER-FRAME.md) (PROVED_LEAN)
- `FQ-R-CPTP` `CONDITIONAL_ON_IMPORT`: [FQ-CPTP-CLASS-DEFINITION](FQ-CPTP-CLASS-DEFINITION.md) (DEFINITION)
- `FQ-R-DYN-DICHOTOMY` `COMPUTED`: [FQ-DISCRETE-DYNAMICS-DICHOTOMY](FQ-DISCRETE-DYNAMICS-DICHOTOMY.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-GLEASON-D2` `DERIVED_LEAN`: [FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION](FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION.md) (PROVED_LEAN)
- `FQ-R-OPERATIONAL-LOCAL-TOMOGRAPHY` `CONDITIONAL_ON_IMPORT`: [FQ-OPERATIONAL-LOCAL-TOMOGRAPHY](FQ-OPERATIONAL-LOCAL-TOMOGRAPHY.md) (IMPORTED_ASSUMPTION)
- `FQ-R-PAIRING-AUDIT` `COMPUTED`: [FQ-IMPL-PAIRING-AUDIT](FQ-IMPL-PAIRING-AUDIT.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-PHASE-FIBER` `CONDITIONAL_ON_IMPORT`: [FQ-PHASE-FIBER-QUOTIENT](FQ-PHASE-FIBER-QUOTIENT.md) (PROVED_LEAN)
- `FQ-R-POWER-RULE` `COMPUTED`: [FQ-POWER-RULE-P2-SELECTION](FQ-POWER-RULE-P2-SELECTION.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-QM207-231` `COMPUTED`: [FQ-QM207-231-FINITE-MAP-CONTROLS](FQ-QM207-231-FINITE-MAP-CONTROLS.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-TENSOR-RIVAL` `DERIVED_LEAN`: [FQ-TENSOR-LU-RIVAL-EXCLUSION](FQ-TENSOR-LU-RIVAL-EXCLUSION.md) (PROVED_LEAN)
- `FRO-R-CT-QUBIT-NO-CLONING-FINITE-TARGET` `DERIVED_LEAN`: [CT-QUBIT-NO-CLONING-FINITE-TARGET](CT-QUBIT-NO-CLONING-FINITE-TARGET.md) (PROVED_LEAN)
- `X-R-INTERFACE-TO-FIVE-IMPORT-PROXIES` `DERIVED_LEAN`: [FQ-FIVE-IMPORT-PROXY-SEPARATION](FQ-FIVE-IMPORT-PROXY-SEPARATION.md) (PROVED_LEAN)
