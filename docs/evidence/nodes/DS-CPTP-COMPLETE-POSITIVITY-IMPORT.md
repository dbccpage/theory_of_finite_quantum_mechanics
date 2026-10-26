# DS-CPTP-COMPLETE-POSITIVITY-IMPORT

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For every integer n, the product n * n is at least 0, and (-n) * (-n) equals n * n. For every natural pair k and m, the product of the integer of k with the integer of m equals the integer of k * m. For every integer pair a and b, if a is at least 0 and b is at least 0, then a * b is at least 0. For every integer triple t, x and w, if t is at least 0, then t * ((x + w) * (x + w)) is at least 0. The sum 1 * (-1) + (-1) * 1 equals -2. For every integer t, t times that sum equals (-2) * t, and t * (-2) equals 2 * (-t). If t is greater than 0, then t * (-2) is less than 0 and -t is less than 0. The product 0 * (-2) equals 0. The sum of squares 0 * 0 + 1 * 1 + (-1) * (-1) + 0 * 0 equals 2.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 15
- distinct cited Lean declarations covered by a current replay receipt: 15
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- tensor product with identity (assumption)
- complete positivity (assumption)
- environment extension (assumption)

## Bottleneck

Complete positivity of a tensor extension, Kraus, Choi and Stinespring forms, and coherence transport above a classical kernel stay imported. The nonnegative product t * ((x + w) * (x + w)) for t at least 0, and the strict negative value t * (-2) for t greater than 0, are one finite scalar case. At t = 0 the product t * (-2) is 0.

## Source status

\[SCOPE FENCE\] CP / coherence transport is the non-forced lift (QM-082-C6); QM_083-C3 local positivity does not force CP

## Review

- PFP review: [dag/results/DS-CPTP-COMPLETE-POSITIVITY-IMPORT/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/DS-CPTP-COMPLETE-POSITIVITY-IMPORT/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: A genuine Bell-input partial-transpose negative witness is computed entrywise and its positive-input and negative-output scalar forms are kernel checked.
  - does not support: Prove full transpose positivity, the native tensor-index transport and a full CP/Stinespring theorem. This counterexample does not derive the physical tensor product or channel law.
  - next test: Prove full transpose positivity, the native tensor-index transport and a full CP/Stinespring theorem. This counterexample does not derive the physical tensor product or channel law.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignDsCptpCompletePositivity.lean`

- file: [lean4/CampaignDsCptpCompletePositivity.lean](../../../lean4/CampaignDsCptpCompletePositivity.lean)
- sha256 (`bytes`): `27282c5c83c9655fc167d6e9273702adf87d9b6068ec41b4e94ec21a9a741722`
- cited in: node.lean, receipt dag/research/campaign_ds-cptp-complete-positivity-import_lean_replay.json (CampaignDsCptpCompletePositivity)
- replay: `verified`
  - receipt [dag/research/campaign_ds-cptp-complete-positivity-import_lean_replay.json](../../../dag/research/campaign_ds-cptp-complete-positivity-import_lean_replay.json) (module `CampaignDsCptpCompletePositivity`): recorded sha256 `27282c5c83c9655fc167d6e9273702adf87d9b6068ec41b4e94ec21a9a741722` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignDsCptpCompletePositivity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignDsCptpCompletePositivity.bellNonneg` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDsCptpCompletePositivity.bellNonneg` |
| `CampaignDsCptpCompletePositivity.mulNonneg` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDsCptpCompletePositivity.mulNonneg` |
| `CampaignDsCptpCompletePositivity.mulOfNat` | yes | yes | yes | propext | `#print axioms CampaignDsCptpCompletePositivity.mulOfNat` |
| `CampaignDsCptpCompletePositivity.negMulNeg` | yes | yes | yes | propext | `#print axioms CampaignDsCptpCompletePositivity.negMulNeg` |
| `CampaignDsCptpCompletePositivity.negOut` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDsCptpCompletePositivity.negOut` |
| `CampaignDsCptpCompletePositivity.negT` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDsCptpCompletePositivity.negT` |
| `CampaignDsCptpCompletePositivity.normSq` | yes | yes | yes | none | `#print axioms CampaignDsCptpCompletePositivity.normSq` |
| `CampaignDsCptpCompletePositivity.pairing` | yes | yes | yes | none | `#print axioms CampaignDsCptpCompletePositivity.pairing` |
| `CampaignDsCptpCompletePositivity.scaleTwice` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDsCptpCompletePositivity.scaleTwice` |
| `CampaignDsCptpCompletePositivity.scaled` | yes | yes | yes | propext | `#print axioms CampaignDsCptpCompletePositivity.scaled` |
| `CampaignDsCptpCompletePositivity.squareNonneg` | yes | yes | yes | propext | `#print axioms CampaignDsCptpCompletePositivity.squareNonneg` |
| `CampaignDsCptpCompletePositivity.zeroScale` | yes | yes | yes | none | `#print axioms CampaignDsCptpCompletePositivity.zeroScale` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0266
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall` |
| `QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels` | yes | yes | yes | propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels` |

- counts toward the grade: yes

### Lean: `lean4/H063CptpChannelsStinespring.lean`

- file: [lean4/H063CptpChannelsStinespring.lean](../../../lean4/H063CptpChannelsStinespring.lean)
- sha256 (`bytes`): `b10a105b3d5810e558e75b3f8504b61433032d6aaff821da3b832baf06e890a7`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `H063CptpChannelsStinespring`): recorded sha256 `b10a105b3d5810e558e75b3f8504b61433032d6aaff821da3b832baf06e890a7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build H063CptpChannelsStinespring`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `stinespring_requires_extension_verified` | yes | yes | yes | module-level | `#print axioms stinespring_requires_extension_verified` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0266_no_derivation_from_stochastic_kernels_to_complete_positivity.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0266_no_derivation_from_stochastic_kernels_to_complete_positivity.md](../../../dag/derivations/12_finite_qm_structure/tfq_0266_no_derivation_from_stochastic_kernels_to_complete_positivity.md)
- sha256 (`lf-normalised`): `9cf8a5abbb5a34752350de9da7053d33f0cc14e1cc947a284d5cb762fb1a1f5b`
- generated view: listed, not counted
- cited in: record TFQ-0266
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0267_completely_positive_import_annex.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0267_completely_positive_import_annex.md](../../../dag/derivations/12_finite_qm_structure/tfq_0267_completely_positive_import_annex.md)
- sha256 (`lf-normalised`): `d15381a243e254164c16e1eafedefccb868275f35a792b8564ec7f910f8138f5`
- generated view: listed, not counted
- cited in: record TFQ-0267 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/082_channels_as_stochastic_kernels_and_the_cptp_lift/qm_082_channels_as_stochastic_kernels_and_the_cptp_lift_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/082_channels_as_stochastic_kernels_and_the_cptp_lift/qm_082_channels_as_stochastic_kernels_and_the_cptp_lift_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/083_completely_positive_import_boundary/qm_083_completely_positive_import_boundary_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/083_completely_positive_import_boundary/qm_083_completely_positive_import_boundary_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0266 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/cptp_channels_stinespring.rs
- TFQ-0266 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/exact_channel.rs
- TFQ-0266 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_channel.rs

## Routes

Incoming (1):

- `DS-R-KERNEL-TO-CPTP` `GAP_NO_DERIVATION`: [DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL](DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL.md) (PROVED_LEAN)

Outgoing (2):

- `DS-R-MONOTONE-NONSELECTION` `DERIVED_LEAN`: [DS-QM081-CPTP-MONOTONE-NOT-SELECTING](DS-QM081-CPTP-MONOTONE-NOT-SELECTING.md) (PROVED_LEAN)
- `DS-R-TRACE-NORM-SELECTION` `DERIVED_LEAN`: [DS-QM080-081-TRACE-NORM-CONDITIONAL-SELECTION](DS-QM080-081-TRACE-NORM-CONDITIONAL-SELECTION.md) (PROVED_LEAN)
