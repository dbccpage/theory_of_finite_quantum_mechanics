# DS-QM061-BUILDABILITY-SET-S

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In the declared finite device model UsefulQC is defined as the conjunction S (race, floor, reachability, advantage), so the stated iff is definitional; the declared rate inequality and all four Boolean conjunction controls are exact. This is a criterion about the model, not evidence that any device satisfies S.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- declared finite device model (assumption)
- imported generation rate lambda_gen (assumption)

## Bottleneck

Unmet after the PFP review: Provide measured or derived rate/floor/reachability/advantage evidence and a justified device-to-fields bridge before claiming a buildable useful quantum computer. The broader source statement is kept in pfp_review.prior_statement.

## Source status

\[PROVEN, MECHANIZED\] finite criterion (QM-061-C12..C14); C15 \[CONDITIONAL / SCOPE FENCE\]

## Review

- PFP review: [dag/results/DS-QM061-BUILDABILITY-SET-S/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM061-BUILDABILITY-SET-S/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: The declared rate inequality and all four Boolean conjunction controls are exact; the alias and Boolean characterization are kernel checked.
  - does not support: Provide measured or derived rate/floor/reachability/advantage evidence and a justified device-to-fields bridge before claiming a buildable useful quantum computer.
  - next test: Provide measured or derived rate/floor/reachability/advantage evidence and a justified device-to-fields bridge before claiming a buildable useful quantum computer.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BuildabilitySetS.lean`

- file: [lean4/BuildabilitySetS.lean](../../../lean4/BuildabilitySetS.lean)
- sha256 (`bytes`): `d9578faac630fc31ee86e257ee12ffe169c9e321d6f881f5d84a234b00fe54f6`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `BuildabilitySetS`): recorded sha256 `d9578faac630fc31ee86e257ee12ffe169c9e321d6f881f5d84a234b00fe54f6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build BuildabilitySetS`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `s1_necessary` | yes | yes | yes | none | `#print axioms s1_necessary` |
| `setS_satisfiable` | yes | yes | yes | none | `#print axioms setS_satisfiable` |
| `useful_qc_iff_set_S` | yes | yes | yes | none | `#print axioms useful_qc_iff_set_S` |
- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0252 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels` | yes | yes | yes | propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels` |
- counts toward the grade: yes

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: record TFQ-0252 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0252_interference_as_a_resource_outside_l1_bookkeeping.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0252_interference_as_a_resource_outside_l1_bookkeeping.md](../../../dag/derivations/12_finite_qm_structure/tfq_0252_interference_as_a_resource_outside_l1_bookkeeping.md)
- sha256 (`lf-normalised`): `97f3fbb9777b27f143ba1ce853c88170987c15d90a4a9e59f9a310a89ff96995`
- generated view: listed, not counted
- cited in: record TFQ-0252 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/061_interference_as_the_non_l1_resource/qm_061_interference_as_the_non_l1_resource_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/061_interference_as_the_non_l1_resource/qm_061_interference_as_the_non_l1_resource_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0252 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm

## Routes

Incoming (1):

- `DS-R-BUILDABILITY` `COMPUTED`: [DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE](DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE.md) (PROVED_LEAN), [DS-QM063-HOLONOMY-COHERENT-INTENSITY](DS-QM063-HOLONOMY-COHERENT-INTENSITY.md) (PROVED_LEAN)

Outgoing (2):

- `APP-R-QCV-QUESTION-SELF-LIMITING-REPAIR` `GAP_NO_DERIVATION`: [QCV-QUESTION-SELF-LIMITING-REPAIR](QCV-QUESTION-SELF-LIMITING-REPAIR.md) (OPEN)
- `APP-R-QCV-SELF-OBSTRUCTION-MODEL` `DERIVED_PROSE`: [QCV-SELF-OBSTRUCTION-MODEL](QCV-SELF-OBSTRUCTION-MODEL.md) (DEFINITION)
