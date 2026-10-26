# DS-QM021-IDEMPOTENT-CONDITIONING

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact sector normalization, support collapse and repeated-conditioning idempotence are reproduced on retained finite tables.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- declared outcome partition (observer-relative) (assumption)

## Bottleneck

Unmet after the PFP review: Formalize the masked support/restriction bridge and justify any physical sector rule. Classical normalization is not a derived projection postulate or solution to measurement. The broader source statement is kept in pfp_review.prior_statement.

## Source status

\[PROVEN — prose\] secured ENC-1125; Lean TARGETED (QM-021-C5)

## Review

- PFP review: [dag/results/DS-QM021-IDEMPOTENT-CONDITIONING/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/DS-QM021-IDEMPOTENT-CONDITIONING/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact sector normalization, support collapse and repeated-conditioning idempotence are reproduced on retained finite tables.
  - does not support: Formalize the masked support/restriction bridge and justify any physical sector rule. Classical normalization is not a derived projection postulate or solution to measurement.
  - next test: Formalize the masked support/restriction bridge and justify any physical sector rule. Classical normalization is not a derived projection postulate or solution to measurement.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0235, record TFQ-0236 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning` |
| `QuantumMechanics.DerivationDagQMClosure.qm021_idempotent_conditioning_and_order_sensitivity` | yes | yes | yes | propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm021_idempotent_conditioning_and_order_sensitivity` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0235_selective_measurement_update_as_idempotent_conditioning.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0235_selective_measurement_update_as_idempotent_conditioning.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0235_selective_measurement_update_as_idempotent_conditioning.md)
- sha256 (`lf-normalised`): `0b3e0cdac66b55bd27be6ccca1f2acf555afa7eaf305cd18824130fa66935a35`
- generated view: listed, not counted
- cited in: record TFQ-0235
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0236_declared_instruments_and_conditional_record_updates.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0236_declared_instruments_and_conditional_record_updates.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0236_declared_instruments_and_conditional_record_updates.md)
- sha256 (`lf-normalised`): `b94ca33803e9d3135a2fd1a06c1f4278652ce36635784e4a71b7aa5024b7073f`
- generated view: listed, not counted
- cited in: record TFQ-0236 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/021_measurement_update_as_idempotent_conditioning/qm_021_measurement_update_as_idempotent_conditioning_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/021_measurement_update_as_idempotent_conditioning/qm_021_measurement_update_as_idempotent_conditioning_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0235 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm
- TFQ-0235 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/measurement.rs
- TFQ-0236 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm
- TFQ-0236 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/exact_instrument.rs
- TFQ-0236 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/instruments.rs
- TFQ-0236 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/measurement.rs

## Routes

Incoming (2):

- `DS-R-IDEMPOTENT-FROM-WEIGHTS` `COMPUTED`: [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) (CONDITIONAL)
- `DS-R-MEASUREMENT-CONDITIONING` `COMPUTED`: [L1-QM020-THM1-DIRECT-NORMALIZATION](L1-QM020-THM1-DIRECT-NORMALIZATION.md) (PROVED_LEAN)

Outgoing (2):

- `DS-R-MEASUREMENT-UPDATE` `GAP_NO_DERIVATION`: [DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT](DS-QM030-PROJECTION-POSTULATE-AND-BORN-PAIRING-IMPORT.md) (IMPORTED_ASSUMPTION)
- `UDG-R-TFQ-0237` `GAP_NO_DERIVATION`: [TFQ-0237](TFQ-0237.md) (OPEN)
