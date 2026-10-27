# DS-QM032-CONTINUUM-LIMIT-CONDITIONAL

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Affine restriction maps on declared singleton states compose and the states are compatible; retained ambient separations show that this bookkeeping alone supplies no convergence bound. If compatible refinements and a convergence certificate are supplied a limit object is defined; none is supplied here.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 1 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Specify compatible approximation spaces, a common embedding/topology, quantitative error and a real convergence proof before any continuum limit. This example does not refute a correctly hypothesized convergence theorem. The broader source statement is kept in pfp_review.prior_statement.

## Source status

QM-032-C4/C7/C10/C12 two-slice free-particle finite-shadow action enumeration, coarse-graining refinement compatibility vs RefinementTear, and CODA-A convergence terminalizer mechanized in DerivationDagQMClosure.lean and mirrored in finite_quantum_mechanics

## Review

- PFP review: [dag/results/DS-QM032-CONTINUUM-LIMIT-CONDITIONAL/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/DS-QM032-CONTINUUM-LIMIT-CONDITIONAL/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Affine restriction maps compose and the singleton states are compatible; retained ambient separations show that this bookkeeping alone supplies no convergence bound.
  - does not support: Specify compatible approximation spaces, a common embedding/topology, quantitative error and a real convergence proof before any continuum limit. This example does not refute a correctly hypothesized convergence theorem.
  - next test: Specify compatible approximation spaces, a common embedding/topology, quantitative error and a real convergence proof before any continuum limit. This example does not refute a correctly hypothesized convergence theorem.

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
| `QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm032_feynman_refinement_compatibility_terminalizer_and_two_slice_action` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm032_feynman_refinement_compatibility_terminalizer_and_two_slice_action` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm063_032_034_destructive_interference_and_cayley_vs_euler_norm` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm063_032_034_destructive_interference_and_cayley_vs_euler_norm` |

- counts toward the grade: yes

### Rust: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche20_ds_qm032_033_073_090_207_feynman_schrodinger_exchange_and_five_import_cascade_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0243_finite_feynman_history_shadow.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0243_finite_feynman_history_shadow.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0243_finite_feynman_history_shadow.md)
- sha256 (`lf-normalised`): `e34b782461355b6352c460ff4a7a8f9412d9a43cfbb723ade92cd5077cafaac7`
- generated view: listed, not counted
- cited in: record TFQ-0243 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0059_each_language_must_carry_even_leg_wick_pairings_through_20_legs_a_hard.md`

- file: [dag/derivations/15_finite_qed/tfq_0059_each_language_must_carry_even_leg_wick_pairings_through_20_legs_a_hard.md](../../../dag/derivations/15_finite_qed/tfq_0059_each_language_must_carry_even_leg_wick_pairings_through_20_legs_a_hard.md)
- sha256 (`lf-normalised`): `104c6f177a7c727786b14cbb395ab1f9d9fa6c04593ea8cf8c72d3b2eb7bdf47`
- generated view: listed, not counted
- cited in: record TFQ-0059 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0071_each_language_must_carry_hermitian_k_yields_a_unitary_cayley_s_on.md`

- file: [dag/derivations/15_finite_qed/tfq_0071_each_language_must_carry_hermitian_k_yields_a_unitary_cayley_s_on.md](../../../dag/derivations/15_finite_qed/tfq_0071_each_language_must_carry_hermitian_k_yields_a_unitary_cayley_s_on.md)
- sha256 (`lf-normalised`): `b4f76c09d7ffde16cc737b032458b0737899d4a6562182e7780d16f55f36b9e0`
- generated view: listed, not counted
- cited in: record TFQ-0071 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0072_each_language_must_carry_channel_amplitude_optical_defect_finite_born_partial_sum.md`

- file: [dag/derivations/15_finite_qed/tfq_0072_each_language_must_carry_channel_amplitude_optical_defect_finite_born_partial_sum.md](../../../dag/derivations/15_finite_qed/tfq_0072_each_language_must_carry_channel_amplitude_optical_defect_finite_born_partial_sum.md)
- sha256 (`lf-normalised`): `bc1017a8fe2b02814802bbec4dd55b40d95ca8f2d9ea8c744271e0077c3861b5`
- generated view: listed, not counted
- cited in: record TFQ-0072 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0083_each_language_must_carry_an_explicit_gap_record_the_finite_gauge_dirac.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0083_each_language_must_carry_an_explicit_gap_record_the_finite_gauge_dirac.md](../../../dag/derivations/16_finite_electroweak/tfq_0083_each_language_must_carry_an_explicit_gap_record_the_finite_gauge_dirac.md)
- sha256 (`lf-normalised`): `55926d07640196e84281a1e438d0cb9792d3df0d4781e8db3f75aa94df39ff8b`
- generated view: listed, not counted
- cited in: record TFQ-0083 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/20_continuum_interface/tfq_0113_gap_f000_f002_001_continuum_limit_is_not_discharged_by_the_s000_shelf_mark.md`

- file: [dag/derivations/20_continuum_interface/tfq_0113_gap_f000_f002_001_continuum_limit_is_not_discharged_by_the_s000_shelf_mark.md](../../../dag/derivations/20_continuum_interface/tfq_0113_gap_f000_f002_001_continuum_limit_is_not_discharged_by_the_s000_shelf_mark.md)
- sha256 (`lf-normalised`): `bcef3071bad375ab6f75a8a36d658b75a8a79695df74cb80a197e74fa3f40b50`
- generated view: listed, not counted
- cited in: record TFQ-0113
- counts toward the grade: no

### Documents and data: `dag/derivations/20_continuum_interface/tfq_0114_gap_f000_f002_001_no_limit_object_and_no_controlled_curvature_bound_are_constructed.md`

- file: [dag/derivations/20_continuum_interface/tfq_0114_gap_f000_f002_001_no_limit_object_and_no_controlled_curvature_bound_are_constructed.md](../../../dag/derivations/20_continuum_interface/tfq_0114_gap_f000_f002_001_no_limit_object_and_no_controlled_curvature_bound_are_constructed.md)
- sha256 (`lf-normalised`): `f47918263033db4533a20ab07842b70870dc37f53ec6b2fb77cbb40e0c5fcbf9`
- generated view: listed, not counted
- cited in: record TFQ-0114
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:187db3e0f25cc2fca3931f80f1ddde21a325df1192a4b8af98725a2fbe11cdbb#QM-032-C4`
- `external:sha256:187db3e0f25cc2fca3931f80f1ddde21a325df1192a4b8af98725a2fbe11cdbb#QM-032-C7`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche20_ds_qm032_033_073_090_207_feynman_schrodinger_exchange_and_five_import_cascade_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche9_bloch_gap_cayley_u1_hadamard_coherence_and_destructive_interference_witness`
- `external:sha256:b4a0392795f1e742a256ae815cdc26550b49a4f6e92e1b8c6beb0d28f159c92d::verify_tranche20_ds_qm032_033_073_090_207_feynman_schrodinger_exchange_and_five_import_cascade_witness`

## Absences recorded by the TFQ records

- TFQ-0059 lean4: not located
- TFQ-0059 python: not located
- TFQ-0059 rust: no local rust twin located for external:sha256:5750c8892fd61b580168841520e2dbb88c42dc9a2870654a5b5a13df5a7e3be1
- TFQ-0071 lean4: not located
- TFQ-0071 python: not located
- TFQ-0071 rust: no local rust twin located for external:sha256:2d9da71f2a615ba2de86c6896030b306594bc1169d72e912cd6e525b06887b66
- TFQ-0072 lean4: not located
- TFQ-0072 python: not located
- TFQ-0072 rust: no local rust twin located for external:sha256:a4ca67769f0cdeae91bce65233c44b0a2b18deb921c5d4e4fabd22880ee84034
- TFQ-0083 lean4: not located
- TFQ-0083 python: not located
- TFQ-0083 rust: no local rust twin located for external:sha256:2d9da71f2a615ba2de86c6896030b306594bc1169d72e912cd6e525b06887b66
- TFQ-0113 lean4: no local lean twin located for external:sha256:fa138464a47b0fe8c8163b9ac1f3c690215350943ffa16316bf0f63650f45efc
- TFQ-0113 python: no local python twin located for external:sha256:3aa4b5bfeec3b0c5d4cb3be6ec214de49e023c1f7e36b1617b0452100e39a8fb
- TFQ-0114 lean4: no local lean twin located for external:sha256:fa138464a47b0fe8c8163b9ac1f3c690215350943ffa16316bf0f63650f45efc
- TFQ-0114 python: no local python twin located for external:sha256:3aa4b5bfeec3b0c5d4cb3be6ec214de49e023c1f7e36b1617b0452100e39a8fb
- TFQ-0243 rust: no local rust twin located for external:sha256:4b48c2e282a2ea334c8e4d0c1fca71cdf5555a374d1aebd974794cd6dd92b489
- TFQ-0243 rust: no local rust twin located for external:sha256:f51cea05c639d8d39b42c50d466f3fdf2ef0bb52291a1196d9ff27bc5e4111a1

## Routes

Incoming (1):

- `DS-R-CONTINUUM-LIMIT` `COMPUTED`: [DS-QM032-FINITE-FEYNMAN-SHADOW](DS-QM032-FINITE-FEYNMAN-SHADOW.md) (COMPUTATIONALLY_CHECKED), [DS-CONTINUOUS-TIME-EXP-GENERATOR](DS-CONTINUOUS-TIME-EXP-GENERATOR.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

