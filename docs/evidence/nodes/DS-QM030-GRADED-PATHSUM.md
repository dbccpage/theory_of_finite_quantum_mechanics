# DS-QM030-GRADED-PATHSUM

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact two-state path enumeration, matrix powers and graded composition agree on retained lengths, including zero.

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

- grading / time-slicing of the category (assumption)
- commutative semiring of weights (assumption)
- finite fibers (assumption)

## Bottleneck

Unmet after the PFP review: Prove the full path-enumeration/matrix-power bridge and transport to a selected physical dynamics; a weighted graph and chosen grading are inputs. The broader source statement is kept in pfp_review.prior_statement.

## Source status

\[PROVEN, CONDITIONAL-DERIVED + H1\] (QM-030-C3); QM-031-C5 \[PROVEN, MECHANIZED ENC-1128\]

## Review

- PFP review: [dag/results/DS-QM030-GRADED-PATHSUM/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/DS-QM030-GRADED-PATHSUM/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact two-state path enumeration, matrix powers and graded composition agree on retained lengths, including zero.
  - does not support: Prove the full path-enumeration/matrix-power bridge and transport to a selected physical dynamics; a weighted graph and chosen grading are inputs.
  - next test: Prove the full path-enumeration/matrix-power bridge and transport to a selected physical dynamics; a weighted graph and chosen grading are inputs.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0239, record TFQ-0240 (shared), record TFQ-0242
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_graded_pathsum_overcount_transfer_and_feynman_shadow` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_graded_pathsum_overcount_transfer_and_feynman_shadow` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/graded_path_sum.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/graded_path_sum.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0239_finite_path_sum_on_a_unique_intermediate_cut.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0239_finite_path_sum_on_a_unique_intermediate_cut.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0239_finite_path_sum_on_a_unique_intermediate_cut.md)
- sha256 (`lf-normalised`): `72af62b8257c0b97b4c304a2d30904a588ab0458a052291b3da84c55e1aa05a4`
- generated view: listed, not counted
- cited in: record TFQ-0239
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0240_ungraded_overcount_and_multiplicative_gauge_residual.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0240_ungraded_overcount_and_multiplicative_gauge_residual.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0240_ungraded_overcount_and_multiplicative_gauge_residual.md)
- sha256 (`lf-normalised`): `e3ab70fc1615368acff2f61b342743d9f071cca14d8e971cfb8fff95c5378416`
- generated view: listed, not counted
- cited in: record TFQ-0240 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0242_graded_path_sum_as_finite_transport.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0242_graded_path_sum_as_finite_transport.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0242_graded_path_sum_as_finite_transport.md)
- sha256 (`lf-normalised`): `b561317e74f12b1ac4cfecb4d7687c043b759161c3217895df621250f1bb9a9e`
- generated view: listed, not counted
- cited in: record TFQ-0242
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/030_finite_weighted_transport_calculus/qm_030_finite_weighted_transport_calculus_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/030_finite_weighted_transport_calculus/qm_030_finite_weighted_transport_calculus_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/031_finite_path_sum_as_graded_transport/qm_031_finite_path_sum_as_graded_transport_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/031_finite_path_sum_as_graded_transport/qm_031_finite_path_sum_as_graded_transport_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0239 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm
- TFQ-0239 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/graded_path_sum.rs
- TFQ-0239 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/path_integral.rs
- TFQ-0240 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/graded_path_sum.rs
- TFQ-0242 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm
- TFQ-0242 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/graded_path_sum.rs
- TFQ-0242 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/path_integral.rs

## Routes

Incoming (1):

- `DS-R-GRADED-PATHSUM-FROM-CARRIER` `COMPUTED`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION), [DS-QM030-UNGRADED-OVERCOUNT](DS-QM030-UNGRADED-OVERCOUNT.md) (COMPUTATIONALLY_CHECKED)

Outgoing (3):

- `DS-R-DYNAMICS-FROM-L1` `COMPUTED`: [DS-QM207-211-FIVE-IMPORT-CASCADE](DS-QM207-211-FIVE-IMPORT-CASCADE.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-FEYNMAN-SHADOW` `COMPUTED`: [DS-QM032-FINITE-FEYNMAN-SHADOW](DS-QM032-FINITE-FEYNMAN-SHADOW.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-PATHSUM` `COMPUTED`: [DS-QM030-TRANSFER-OPERATOR-SHADOW](DS-QM030-TRANSFER-OPERATOR-SHADOW.md) (COMPUTATIONALLY_CHECKED)
