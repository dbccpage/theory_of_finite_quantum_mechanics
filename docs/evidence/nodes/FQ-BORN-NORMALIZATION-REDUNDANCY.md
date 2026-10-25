# FQ-BORN-NORMALIZATION-REDUNDANCY

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Normalization of the Born readout is idempotent and ray quotients are classified (normalize_idempotent, ray_quotient_classification) over the stated finite/rational domain; the normalization step is redundant after ray quotienting.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Born/quadratic readout (assumption)

## Bottleneck

The cited declarations live in lean4/original_lean_20260809/qm_l010_01_born_redundancy.lean (2,215 lines, Mathlib.Tactic import); repo-level lean4/quantum_mechanics copy is Mathlib-free but this extraction did not run a build. Zenodo 20683775 needs the narrowing erratum.

## Source status

ledger: LEAN SOURCE (UNREPLAYED) for the 8 BornRedundancy rows (GAP-FQM-019)

## Review

- PFP review: [dag/results/FQ-BORN-NORMALIZATION-REDUNDANCY/reviews/20261019_next_ten_audit/review_result.json](../../../dag/results/FQ-BORN-NORMALIZATION-REDUNDANCY/reviews/20261019_next_ten_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: The quotient is by positive scaling of weight vectors, with a unique normalized representative; equal weights can still come from different amplitude rays.
  - does not support: Classification of complex amplitude rays, derivation or uniqueness of Born pairing, a formal probability-subtype operad, or publication/erratum completion.
  - next test: Batch review must check the literal weight/amplitude distinction and every retained proof/native receipt.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornNormalization.lean`

- file: [lean4/BornNormalization.lean](../../../lean4/BornNormalization.lean)
- sha256 (`bytes`): `83fdfac8a9b2d61cff987d7a8b8cd7acb809afd851d8d6d0369a3ae2b12004c8`
- cited in: record TFQ-0295 (shared), record TFQ-0317 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `BornNormalization`): recorded sha256 `83fdfac8a9b2d61cff987d7a8b8cd7acb809afd851d8d6d0369a3ae2b12004c8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornNormalization`
- counts toward the grade: no

### Lean: `lean4/BornRedundancy.lean`

- file: [lean4/BornRedundancy.lean](../../../lean4/BornRedundancy.lean)
- sha256 (`bytes`): `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b`
- cited in: node.lean, record TFQ-0290 (shared), record TFQ-0295 (shared), record TFQ-0317 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `BornRedundancy`): recorded sha256 `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornRedundancy`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `normalize_idempotent` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms normalize_idempotent` |
| `ray_quotient_classification` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ray_quotient_classification` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition` |

- counts toward the grade: yes

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: record TFQ-0317 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0290_direct_normalization_of_sector_weights.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0290_direct_normalization_of_sector_weights.md](../../../dag/derivations/08_l1_to_l2/tfq_0290_direct_normalization_of_sector_weights.md)
- sha256 (`lf-normalised`): `a491aa3ac2d7b76dd1c5f1dc490ab6b8ec60ef7691e2270986e80d918d5804d2`
- generated view: listed, not counted
- cited in: record TFQ-0290 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0295_born_readout_of_a_supplied_lift_is_redundant.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0295_born_readout_of_a_supplied_lift_is_redundant.md](../../../dag/derivations/08_l1_to_l2/tfq_0295_born_readout_of_a_supplied_lift_is_redundant.md)
- sha256 (`lf-normalised`): `53e71e6727e0d1b2ea74746ec90f8fb72d5052ada03be61eaf1fe5fc55076258`
- generated view: listed, not counted
- cited in: record TFQ-0295 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/09_finite_hilbert/tfq_0317_three_lean_files_stay_on_a_narrow_carrier.md`

- file: [dag/derivations/09_finite_hilbert/tfq_0317_three_lean_files_stay_on_a_narrow_carrier.md](../../../dag/derivations/09_finite_hilbert/tfq_0317_three_lean_files_stay_on_a_narrow_carrier.md)
- sha256 (`lf-normalised`): `2de99ce524cc77fb8301c243e2aaa5b51e99e575b888a3fa240dd3cd564a76da`
- generated view: listed, not counted
- cited in: record TFQ-0317 (shared)
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: [sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml](../../../sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `16a418a93748cef695fad3c1fab0fd14dd95c6985b23ee8a814b171eca60a445`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics_claim_ledger.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics_claim_ledger.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics_claim_ledger.md)
- sha256 (`lf-normalised`): `b9adbe593870ae277067c746b426f7b937a9cf98319cd4c8c0b712d9059dd5ac`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0290 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_020/code/qm_020_born_normalization_and_conditional_hilbert_lift_core.py
- TFQ-0290 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs
- TFQ-0295 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_020/code/qm_020_born_normalization_and_conditional_hilbert_lift_core.py
- TFQ-0295 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_020/tests/test_qm020_born_lift.py
- TFQ-0295 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs
- TFQ-0295 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_state.rs

## Routes

Incoming (2):

- `FQ-R-BORN-REDUNDANCY` `CONDITIONAL_ON_IMPORT`: [FQ-PHASE-FIBER-QUOTIENT](FQ-PHASE-FIBER-QUOTIENT.md) (PROVED_LEAN), [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)
- `X-R-BORN-REDUNDANCY-TO-FQ` `DERIVED_LEAN`: [L1-QM020-THM1-DIRECT-NORMALIZATION](L1-QM020-THM1-DIRECT-NORMALIZATION.md) (PROVED_LEAN)

Outgoing (1):

- `FQ-R-EVERETT` `DERIVED_LEAN`: [FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY](FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY.md) (PROVED_LEAN)
