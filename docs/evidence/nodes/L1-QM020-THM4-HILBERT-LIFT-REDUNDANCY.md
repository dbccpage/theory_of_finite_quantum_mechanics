# L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Given a supplied lift c with |c_i|^2 = w_i (for example c_i = sqrt(w_i) e^{i theta_i}), |c_i|^2 / sum |c|^2 = w_i / sum w. So the Born-form probability of the lift equals the l1 normalization, and the lift is redundant for probability. Existence of the lift requires square roots (not available over Q in general) and a complex structure.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- square root field: lift
- complex scalars with modulus: lift
- unit phases: lift

## Bottleneck

No Lean theorem for |c|^2 normalization over C found; BornNormalization.lean treats discrete 2x2 density / POVM. Rust exact_amplitudes returns None unless every p_j is a rational square.

## Source status

Thm 4 \[PROVEN\]; finite_qm audit: a lift need not exist over the chosen rational coefficient field

## Review

- PFP review: [dag/results/L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact supplied-lift matching and Born/direct normalization arrays; generic equality under matching weights and an invalid-lift control in Lean.
  - does not support: Prove arbitrary source lift refinement and supply square-root/complex structure where required. Matching normalized probabilities alone is weaker than raw lift equality.
  - next test: Prove arbitrary source lift refinement and supply square-root/complex structure where required. Matching normalized probabilities alone is weaker than raw lift equality.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornNormalization.lean`

- file: [lean4/BornNormalization.lean](../../../lean4/BornNormalization.lean)
- sha256 (`bytes`): `83fdfac8a9b2d61cff987d7a8b8cd7acb809afd851d8d6d0369a3ae2b12004c8`
- cited in: node.lean, record TFQ-0295 (shared)
- replay: `none`
- check: `cd lean4 && lake build BornNormalization`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `born_normalization_redundancy` | yes | yes | yes | - | `#print axioms born_normalization_redundancy` |
- counts toward the grade: yes

### Lean: `lean4/BornRedundancy.lean`

- file: [lean4/BornRedundancy.lean](../../../lean4/BornRedundancy.lean)
- sha256 (`bytes`): `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b`
- cited in: record TFQ-0295 (shared)
- replay: `none`
- check: `cd lean4 && lake build BornRedundancy`
- counts toward the grade: no

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.qm020_thm4_hilbert_lift_redundancy` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm020_thm4_hilbert_lift_redundancy` |
- counts toward the grade: yes

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: record TFQ-0234 (shared)
- replay: `none`
- check: `cd lean4 && lake build FiniteQM`
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py`

- file: `code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py`
- resolution: `missing` (not found in this checkout)
- cited in: record TFQ-0318 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0355_stop_at_the_open_residual_to_weight_gap_and_do_not_import_a_hilbert.md`

- file: [dag/derivations/07_l1_emergence/tfq_0355_stop_at_the_open_residual_to_weight_gap_and_do_not_import_a_hilbert.md](../../../dag/derivations/07_l1_emergence/tfq_0355_stop_at_the_open_residual_to_weight_gap_and_do_not_import_a_hilbert.md)
- sha256 (`lf-normalised`): `afafc9b824245cd2b19b9f248fe02687da0b8782d2f01dd84904020ef321fe45`
- generated view: listed, not counted
- cited in: record TFQ-0355 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0295_born_readout_of_a_supplied_lift_is_redundant.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0295_born_readout_of_a_supplied_lift_is_redundant.md](../../../dag/derivations/08_l1_to_l2/tfq_0295_born_readout_of_a_supplied_lift_is_redundant.md)
- sha256 (`lf-normalised`): `53e71e6727e0d1b2ea74746ec90f8fb72d5052ada03be61eaf1fe5fc55076258`
- generated view: listed, not counted
- cited in: record TFQ-0295 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/09_finite_hilbert/tfq_0318_float_lift_helper_is_not_the_exact_embedding.md`

- file: [dag/derivations/09_finite_hilbert/tfq_0318_float_lift_helper_is_not_the_exact_embedding.md](../../../dag/derivations/09_finite_hilbert/tfq_0318_float_lift_helper_is_not_the_exact_embedding.md)
- sha256 (`lf-normalised`): `5e0938a0343faced0b1aa448278401e2cbfab27ae6f19cb21b03da344e69091a`
- generated view: listed, not counted
- cited in: record TFQ-0318 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_0234_supplied_hilbert_carrier_after_the_conditional_lift.md`

- file: [dag/derivations/10_finite_qm_core/tfq_0234_supplied_hilbert_carrier_after_the_conditional_lift.md](../../../dag/derivations/10_finite_qm_core/tfq_0234_supplied_hilbert_carrier_after_the_conditional_lift.md)
- sha256 (`lf-normalised`): `6d982adae0ff3da0e19f4cd971e50eb7d55233d37d62353f37b3e171d2ed5ea5`
- generated view: listed, not counted
- cited in: record TFQ-0234 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/claims/claim_ledger.yaml`

- file: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/claims/claim_ledger.yaml`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0234 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm
- TFQ-0295 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_020/code/qm_020_born_normalization_and_conditional_hilbert_lift_core.py
- TFQ-0295 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_020/tests/test_qm020_born_lift.py
- TFQ-0295 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs
- TFQ-0295 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_state.rs
- TFQ-0318 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_020/code/qm_020_born_normalization_and_conditional_hilbert_lift_core.py
- TFQ-0318 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_020/tests/test_qm020_born_lift.py
- TFQ-0318 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs
- TFQ-0318 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_state.rs

## Routes

Incoming (1):

- `L1-R-THM4` `DERIVED_LEAN`: [L1-QM020-THM1-DIRECT-NORMALIZATION](L1-QM020-THM1-DIRECT-NORMALIZATION.md) (PROVED_LEAN), [L1-IMP-SQRT-FIELD](L1-IMP-SQRT-FIELD.md) (IMPORTED_ASSUMPTION), [L1-IMP-COMPLEX-FIELD](L1-IMP-COMPLEX-FIELD.md) (CONDITIONAL), [L1-IMP-U1-PHASES](L1-IMP-U1-PHASES.md) (IMPORTED_ASSUMPTION)

Outgoing (6):

- `L1-R-C10-BRANCH-PINCHING` `DERIVED_LEAN`: [L1-QM020-C10-BRANCH-LOCALIZATION](L1-QM020-C10-BRANCH-LOCALIZATION.md) (PROVED_LEAN)
- `L1-R-LADDER` `DERIVED_LEAN`: [L1-QM121-LADDER-RUNGS-2-6](L1-QM121-LADDER-RUNGS-2-6.md) (PROVED_LEAN)
- `L1-R-PHASE-BLIND-INTERFERENCE` `DERIVED_LEAN`: [L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE](L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE.md) (PROVED_LEAN)
- `L1-R-THM5` `DERIVED_LEAN`: [L1-QM020-THM5-PHASE-AVERAGED-SHADOW](L1-QM020-THM5-PHASE-AVERAGED-SHADOW.md) (PROVED_LEAN)
- `L1-R-THM6-P2` `CONDITIONAL_ON_IMPORT`: [L1-QM020-THM6-P2-GLEASON](L1-QM020-THM6-P2-GLEASON.md) (IMPORTED_ASSUMPTION)
- `L1-R-THM7` `DERIVED_LEAN`: [L1-QM020-THM7-REPRESENTATION-CAPACITY](L1-QM020-THM7-REPRESENTATION-CAPACITY.md) (PROVED_LEAN)
