# L1-QM020-THM5-PHASE-AVERAGED-SHADOW

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Under a chosen Hilbert lift with independent Haar-uniform phases, E |\<u, psi(theta)\>|^2 = sum |u_gamma|^2 w_gamma. Worked replay w=(2,1,1) gives 37/16. Rust replaces Haar by a declared finite phase group (decided for n \<= 3). The paper says it must not be upgraded without full Hilbert and Haar discharge.

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

- Haar measure on phases: assumption
- independence of phases: assumption
- Hilbert inner product: assumption

## Bottleneck

Lean states the two-sector sign average ((a1+a2)^2 + (a1-a2)^2 + (-a1+a2)^2 + (-a1-a2)^2)/4 = a1^2 + a2^2 and the 2x2 diagonal pinching. Haar measure and independent continuous phases are not constructed; the worked value 37/16 is a native replay.

## Source status

Finite sign-group phase-averaging cross-term cancellation mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/L1-QM020-THM5-PHASE-AVERAGED-SHADOW/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM020-THM5-PHASE-AVERAGED-SHADOW/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Complete3-sector phase-conjugation mean, diagonal map and64 exact scalar readouts, with scalar cross cancellation in Lean.
  - does not support: Supply Haar measure, independence and Hilbert/source refinement. A finite polynomial-moment identity is not a continuum integration construction.
  - next test: Supply Haar measure, independence and Hilbert/source refinement. A finite polynomial-moment identity is not a continuum integration construction.

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
| `QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_phase_averaged_shadow_and_c10_pinching` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_phase_averaged_shadow_and_c10_pinching` |
| `QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_thm7_and_qm121_ladder_rungs_2_to_6_separation` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_thm7_and_qm121_ladder_rungs_2_to_6_separation` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/phase_averaged_shadow.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/phase_averaged_shadow.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0302_phase_averaged_shadow_under_declared_phases.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0302_phase_averaged_shadow_under_declared_phases.md](../../../dag/derivations/08_l1_to_l2/tfq_0302_phase_averaged_shadow_under_declared_phases.md)
- sha256 (`lf-normalised`): `4296a55d644277656be98d776d37082e584305634cc20c2f771e08c75b4288d2`
- generated view: listed, not counted
- cited in: record TFQ-0302
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0302 python: no local python twin located for sources/atlas/papers/quantum_foundations/_code/qm_020/code/qm_020_born_normalization_and_conditional_hilbert_lift_core.py
- TFQ-0302 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/phase_averaged_shadow.rs
- TFQ-0302 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs

## Routes

Incoming (1):

- `L1-R-THM5` `COMPUTED`: [L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY](L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY.md) (PROVED_PROSE), [L1-IMP-HILBERT-INNER-PRODUCT](L1-IMP-HILBERT-INNER-PRODUCT.md) (CONDITIONAL), [L1-IMP-HAAR-INDEPENDENT-PHASES](L1-IMP-HAAR-INDEPENDENT-PHASES.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

