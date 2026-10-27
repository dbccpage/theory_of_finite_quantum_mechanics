# DS-QM032-FINITE-FEYNMAN-SHADOW

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Two-path interference has residual 2pq, including cancellation and rational controls.

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

- declared discrete Lagrangian and weights (assumption)
- time slicing (assumption)

## Bottleneck

Unmet after the PFP review: Supply action weights, refinement, measure and convergence before invoking a Feynman continuum formula. The broader source statement is kept in pfp_review.prior_statement.

## Source status

\[PROVEN — finite, elementary; MECHANIZED ENC-1072\] (QM-032-C3)

## Review

- PFP review: [dag/results/DS-QM032-FINITE-FEYNMAN-SHADOW/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/DS-QM032-FINITE-FEYNMAN-SHADOW/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Two-path interference has residual 2pq, including cancellation and rational controls.
  - does not support: Supply action weights, refinement, measure and convergence before invoking a Feynman continuum formula.
  - next test: Supply action weights, refinement, measure and convergence before invoking a Feynman continuum formula.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0243 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_graded_pathsum_overcount_transfer_and_feynman_shadow` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_graded_pathsum_overcount_transfer_and_feynman_shadow` |
| `QuantumMechanics.DerivationDagQMClosure.qm032_finite_feynman_interference_vs_stochastic` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm032_finite_feynman_interference_vs_stochastic` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0243_finite_feynman_history_shadow.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0243_finite_feynman_history_shadow.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0243_finite_feynman_history_shadow.md)
- sha256 (`lf-normalised`): `fc6206f2656909284f4da934c84e1fe3948118378c3060bdd42df7884fed28e8`
- generated view: listed, not counted
- cited in: record TFQ-0243 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0059_each_language_must_carry_even_leg_wick_pairings_through_20_legs_a_hard.md`

- file: [dag/derivations/15_finite_qed/tfq_0059_each_language_must_carry_even_leg_wick_pairings_through_20_legs_a_hard.md](../../../dag/derivations/15_finite_qed/tfq_0059_each_language_must_carry_even_leg_wick_pairings_through_20_legs_a_hard.md)
- sha256 (`lf-normalised`): `1f4fecca4a038e98182773480da8ba35c0a8da69739610d670e863a76c0273c8`
- generated view: listed, not counted
- cited in: record TFQ-0059 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0061_each_language_must_carry_2_forest_f0_equals_the_schur_complement_on_the.md`

- file: [dag/derivations/15_finite_qed/tfq_0061_each_language_must_carry_2_forest_f0_equals_the_schur_complement_on_the.md](../../../dag/derivations/15_finite_qed/tfq_0061_each_language_must_carry_2_forest_f0_equals_the_schur_complement_on_the.md)
- sha256 (`lf-normalised`): `ba4ac1f7ed211c27bbf5a76fb60538ce5001d2f0922cb5caf9e40a4cc32ba046`
- generated view: listed, not counted
- cited in: record TFQ-0061 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0072_each_language_must_carry_channel_amplitude_optical_defect_finite_born_partial_sum.md`

- file: [dag/derivations/15_finite_qed/tfq_0072_each_language_must_carry_channel_amplitude_optical_defect_finite_born_partial_sum.md](../../../dag/derivations/15_finite_qed/tfq_0072_each_language_must_carry_channel_amplitude_optical_defect_finite_born_partial_sum.md)
- sha256 (`lf-normalised`): `9bd4114f4897192f1238074c4153429f980c0d2c31045abde0b72be43f8e5ded`
- generated view: listed, not counted
- cited in: record TFQ-0072 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:187db3e0f25cc2fca3931f80f1ddde21a325df1192a4b8af98725a2fbe11cdbb#QM-032-C10`
- `external:sha256:187db3e0f25cc2fca3931f80f1ddde21a325df1192a4b8af98725a2fbe11cdbb#QM-032-C3`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_ds_qm_dynamics_structure_and_majorana_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`

## Absences recorded by the TFQ records

- TFQ-0059 lean4: not located
- TFQ-0059 python: not located
- TFQ-0059 rust: no local rust twin located for external:sha256:5750c8892fd61b580168841520e2dbb88c42dc9a2870654a5b5a13df5a7e3be1
- TFQ-0061 lean4: not located
- TFQ-0061 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/symanzik_two_forest_bphz_control.py
- TFQ-0061 rust: no local rust twin located for external:sha256:376085dc410bbb86117c8efb40f2280ed15cb5734a22d050f6e1718aef3be579
- TFQ-0072 lean4: not located
- TFQ-0072 python: not located
- TFQ-0072 rust: no local rust twin located for external:sha256:a4ca67769f0cdeae91bce65233c44b0a2b18deb921c5d4e4fabd22880ee84034
- TFQ-0243 rust: no local rust twin located for external:sha256:4b48c2e282a2ea334c8e4d0c1fca71cdf5555a374d1aebd974794cd6dd92b489
- TFQ-0243 rust: no local rust twin located for external:sha256:f51cea05c639d8d39b42c50d466f3fdf2ef0bb52291a1196d9ff27bc5e4111a1

## Routes

Incoming (1):

- `DS-R-FEYNMAN-SHADOW` `COMPUTED`: [DS-QM030-GRADED-PATHSUM](DS-QM030-GRADED-PATHSUM.md) (COMPUTATIONALLY_CHECKED)

Outgoing (1):

- `DS-R-CONTINUUM-LIMIT` `COMPUTED`: [DS-QM032-CONTINUUM-LIMIT-CONDITIONAL](DS-QM032-CONTINUUM-LIMIT-CONDITIONAL.md) (COMPUTATIONALLY_CHECKED)
