# DS-QM032-CONTINUUM-LIMIT-CONDITIONAL

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Affine restriction maps on declared singleton states compose and the states are compatible; retained ambient separations show that this bookkeeping alone supplies no convergence bound. If compatible refinements and a convergence certificate are supplied a limit object is defined; none is supplied here.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `computational_no_runnable_test`: 1 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Specify compatible approximation spaces, a common embedding/topology, quantitative error and a real convergence proof before any continuum limit. This example does not refute a correctly hypothesized convergence theorem. The broader source statement is kept in pfp_review.prior_statement.

## Source status

QM-032-C4/C7/C10/C12 two-slice free-particle finite-shadow action enumeration, coarse-graining refinement compatibility vs RefinementTear, and CODA-A convergence terminalizer mechanized in DerivationDagQMClosure.lean and mirrored in 006_finite_qm

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
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm032_feynman_refinement_compatibility_terminalizer_and_two_slice_action` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm032_feynman_refinement_compatibility_terminalizer_and_two_slice_action` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm063_032_034_destructive_interference_and_cayley_vs_euler_norm` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm063_032_034_destructive_interference_and_cayley_vs_euler_norm` |
- counts toward the grade: yes

### Lean: `sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`

- file: [sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean](../../../sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `a2ec0a203277c5c7b4bd71067351c574509c655c18bf0e08fe3c05a8005fc497`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains sources/atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm032_feynman_refinement_compatibility_terminalizer_and_two_slice_action` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm032_feynman_refinement_compatibility_terminalizer_and_two_slice_action` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs)
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

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/032_gtta_feynman_finite_shadow_histories/qm_032_gtta_feynman_finite_shadow_histories_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/032_gtta_feynman_finite_shadow_histories/qm_032_gtta_feynman_finite_shadow_histories_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0059 lean4: not located
- TFQ-0059 python: not located
- TFQ-0059 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/feynman_diagram.rs
- TFQ-0071 lean4: not located
- TFQ-0071 python: not located
- TFQ-0071 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/s_matrix.rs
- TFQ-0072 lean4: not located
- TFQ-0072 python: not located
- TFQ-0072 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/scattering_amplitude.rs
- TFQ-0083 lean4: not located
- TFQ-0083 python: not located
- TFQ-0083 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/s_matrix.rs
- TFQ-0113 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent/002_from_primitive_difference_to_mtheory/lean4/FromPrimitiveDifferenceToMTheory/ContinuumLimit.lean
- TFQ-0113 python: no local python twin located for omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent/002_from_primitive_difference_to_mtheory/python/src/mtheory_interfaces/cochain_limit.py
- TFQ-0114 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent/002_from_primitive_difference_to_mtheory/lean4/FromPrimitiveDifferenceToMTheory/ContinuumLimit.lean
- TFQ-0114 python: no local python twin located for omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent/002_from_primitive_difference_to_mtheory/python/src/mtheory_interfaces/cochain_limit.py
- TFQ-0243 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/graded_path_sum.rs
- TFQ-0243 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/path_integral.rs

## Routes

Incoming (1):

- `DS-R-CONTINUUM-LIMIT` `COMPUTED`: [DS-QM032-FINITE-FEYNMAN-SHADOW](DS-QM032-FINITE-FEYNMAN-SHADOW.md) (COMPUTATIONALLY_CHECKED), [DS-CONTINUOUS-TIME-EXP-GENERATOR](DS-CONTINUOUS-TIME-EXP-GENERATOR.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

