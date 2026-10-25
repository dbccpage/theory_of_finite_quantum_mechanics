# DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Measurement as finite descent is derived structure (C15), but the projection postulate (E^2=E with spectral structure) and the observer pairing and normalization behind probability-like outputs are imported; O024 audits seven pairings and does not select a unique Born rule.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declaration references covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- projection postulate / spectral structure (assumption)
- probability pairing and normalization (assumption)

## Bottleneck

Overlaps L1_TO_L2 Born nodes (QM_020, other fragment).

## Source status

\[SCOPE FENCE — projection postulate IMPORTED\] (QM-030-C16); C12 \[PROVEN, CONDITIONAL — pairing + normalization IMPORTED\]; C13 \[REFUSED unique Born\]

## Review

- PFP review: [dag/results/DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Scalar idempotence holds exactly at 0 and 1 in Lean; retained diagonal effect controls and two different normalized pairings are exact.
  - does not support: Derive or explicitly admit the spectral/projector structure and the physical observer pairing. The bare finite carrier does not select the Born rule or an actual event.
  - next test: Derive or explicitly admit the spectral/projector structure and the physical observer pairing. The bare finite carrier does not select the Born rule or an actual event.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0236 (shared), record TFQ-0241
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels` | yes | yes | yes | propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels` |

- counts toward the grade: yes

### Lean: `lean4/GleasonTheorem.lean`

- file: [lean4/GleasonTheorem.lean](../../../lean4/GleasonTheorem.lean)
- sha256 (`bytes`): `881e01ee20e9af8f1d0f184edb5062447928fc98916c7a18f546d700fc839343`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `GleasonTheorem`): recorded sha256 `881e01ee20e9af8f1d0f184edb5062447928fc98916c7a18f546d700fc839343` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GleasonTheorem`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `d2_binary_non_bornian_obstruction` | yes | yes | yes | Quot.sound, propext | `#print axioms d2_binary_non_bornian_obstruction` |

- counts toward the grade: yes

### Lean: `lean4/H013BornPairingBoundary.lean`

- file: [lean4/H013BornPairingBoundary.lean](../../../lean4/H013BornPairingBoundary.lean)
- sha256 (`bytes`): `debafe0eefb016e289a18fb9a308224f73464282e15c17eef143e5ea5342b642`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `H013BornPairingBoundary`): recorded sha256 `debafe0eefb016e289a18fb9a308224f73464282e15c17eef143e5ea5342b642` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build H013BornPairingBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `born_pairing_boundary` | yes | yes | yes | module-level | `#print axioms born_pairing_boundary` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0236_declared_instruments_and_conditional_record_updates.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0236_declared_instruments_and_conditional_record_updates.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0236_declared_instruments_and_conditional_record_updates.md)
- sha256 (`lf-normalised`): `b94ca33803e9d3135a2fd1a06c1f4278652ce36635784e4a71b7aa5024b7073f`
- generated view: listed, not counted
- cited in: record TFQ-0236 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0241_projection_postulate_and_born_pairing_remain_imported.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0241_projection_postulate_and_born_pairing_remain_imported.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0241_projection_postulate_and_born_pairing_remain_imported.md)
- sha256 (`lf-normalised`): `54203a711dff1214150b94e6a2fc09dea829e2a93d44393046229b375364d8f8`
- generated view: listed, not counted
- cited in: record TFQ-0241
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/030_finite_weighted_transport_calculus/qm_030_finite_weighted_transport_calculus_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/030_finite_weighted_transport_calculus/qm_030_finite_weighted_transport_calculus_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0236 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm
- TFQ-0236 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/exact_instrument.rs
- TFQ-0236 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/instruments.rs
- TFQ-0236 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/measurement.rs

## Routes

Incoming (2):

- `DS-R-BORN-IMPORT` `DERIVED_LEAN`: [DS-QM204-BORN-UNIQUENESS-IMPORT-BOUNDARY](DS-QM204-BORN-UNIQUENESS-IMPORT-BOUNDARY.md) (IMPORTED_ASSUMPTION)
- `DS-R-MEASUREMENT-UPDATE` `GAP_NO_DERIVATION`: [DS-QM021-IDEMPOTENT-CONDITIONING](DS-QM021-IDEMPOTENT-CONDITIONING.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

