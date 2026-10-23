# L1-IMP-SQRT-FIELD

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The lift c_i = sqrt(w_i) e^{i theta_i} needs a coefficient field with square roots of the weights. Over Q this fails in general; Rust exact_amplitudes returns None unless each normalized weight is a rational square.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- real closed field or algebraic closure of weights: assumption

## Bottleneck

Choice of coefficient field is not derived from carriers.

## Source status

Thm 4 audit: lift need not exist over the chosen rational coefficient field

## Review

- PFP review: [dag/results/L1-IMP-SQRT-FIELD/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-IMP-SQRT-FIELD/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Exact normalized-square classification on the retained rational packets, including zero/negative mass refusal and nonsquare controls.
  - does not support: Prove the rational-square decision refinement and construct any admitted algebraic/real square-root field. No blanket irrationality theorem is inferred from finite search.
  - next test: Prove the rational-square decision refinement and construct any admitted algebraic/real square-root field. No blanket irrationality theorem is inferred from finite search.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates` | yes | yes | yes | module-level | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates` |
| `QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` |
| `QuantumMechanics.DerivationDagQMClosure.l1_minkowski_sqrt_decoherence_and_scoped_custody_witness` | yes | yes | yes | module-level | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_minkowski_sqrt_decoherence_and_scoped_custody_witness` |
- counts toward the grade: yes

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

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0292_square_root_field_for_amplitude_coordinates.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0292_square_root_field_for_amplitude_coordinates.md](../../../dag/derivations/08_l1_to_l2/tfq_0292_square_root_field_for_amplitude_coordinates.md)
- sha256 (`lf-normalised`): `41eec6fe14c89d0f9dd72a2e6d7905abd44858198fb8c406ad6dea6c90fa02ae`
- generated view: listed, not counted
- cited in: record TFQ-0292
- counts toward the grade: no

### Documents and data: `dag/derivations/09_finite_hilbert/tfq_0318_float_lift_helper_is_not_the_exact_embedding.md`

- file: [dag/derivations/09_finite_hilbert/tfq_0318_float_lift_helper_is_not_the_exact_embedding.md](../../../dag/derivations/09_finite_hilbert/tfq_0318_float_lift_helper_is_not_the_exact_embedding.md)
- sha256 (`lf-normalised`): `5e0938a0343faced0b1aa448278401e2cbfab27ae6f19cb21b03da344e69091a`
- generated view: listed, not counted
- cited in: record TFQ-0318 (shared)
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/claims/claim_ledger.yaml`

- file: [sources/atlas/F004_papers/006_finite_qm/claims/claim_ledger.yaml](../../../sources/atlas/F004_papers/006_finite_qm/claims/claim_ledger.yaml)
- sha256 (`lf-normalised`): `9db8daae54ec82cab13d7f63cd24d21a793017302b9e8553255fe0c64881f4c7`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0292 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_020/code/qm_020_born_normalization_and_conditional_hilbert_lift_core.py
- TFQ-0292 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs
- TFQ-0318 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_020/code/qm_020_born_normalization_and_conditional_hilbert_lift_core.py
- TFQ-0318 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_020/tests/test_qm020_born_lift.py
- TFQ-0318 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs
- TFQ-0318 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_state.rs

## Routes

Incoming (1):

- `L1-R-SQRT-GAP` `GAP_NO_DERIVATION`: [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) (CONDITIONAL)

Outgoing (2):

- `L1-R-DENSITY-LIFT-PUB009` `DERIVED_LEAN`: [L1-DENSITY-LIFT-SIGNED-SQRT-PUB009](L1-DENSITY-LIFT-SIGNED-SQRT-PUB009.md) (PROVED_LEAN)
- `L1-R-THM4` `DERIVED_LEAN`: [L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY](L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY.md) (PROVED_LEAN)
