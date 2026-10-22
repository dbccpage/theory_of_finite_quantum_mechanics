# DS-QM030-UNGRADED-OVERCOUNT

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Actual acyclic arrays give Z20=d+ab and (Z²)20=2d+3ab, with pure and mixed-length controls.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Grading is one sufficient bookkeeping choice. Do not claim that every possible ungraded formulation is not possible or that the old arithmetic identity was a path-count theorem. The broader source statement is kept in pfp_review.prior_statement.

## Source status

\[PROVEN — exact finite computation; MECHANIZED (Rust 3:1 over-count witness)\] (QM-030-C4)

## Review

- PFP review: [dag/results/DS-QM030-UNGRADED-OVERCOUNT/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/DS-QM030-UNGRADED-OVERCOUNT/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Actual acyclic arrays give Z20=d+ab and (Z²)20=2d+3ab, with pure and mixed-length controls.
  - does not support: Grading is one sufficient bookkeeping choice. Do not claim that every possible ungraded formulation is not possible or that the old arithmetic identity was a path-count theorem.
  - next test: Grading is one sufficient bookkeeping choice. Do not claim that every possible ungraded formulation is not possible or that the old arithmetic identity was a path-count theorem.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0240 (shared)
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_graded_pathsum_overcount_transfer_and_feynman_shadow` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_graded_pathsum_overcount_transfer_and_feynman_shadow` |
| `QuantumMechanics.DerivationDagQMClosure.qm030_ungraded_overcount_witness` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm030_ungraded_overcount_witness` |
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

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0240_ungraded_overcount_and_multiplicative_gauge_residual.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0240_ungraded_overcount_and_multiplicative_gauge_residual.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0240_ungraded_overcount_and_multiplicative_gauge_residual.md)
- sha256 (`lf-normalised`): `e3ab70fc1615368acff2f61b342743d9f071cca14d8e971cfb8fff95c5378416`
- generated view: listed, not counted
- cited in: record TFQ-0240 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/030_finite_weighted_transport_calculus/qm_030_finite_weighted_transport_calculus_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/030_finite_weighted_transport_calculus/qm_030_finite_weighted_transport_calculus_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0240 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/graded_path_sum.rs

## Routes

Incoming (2):

- `DS-R-OVERCOUNT-WITNESS` `COMPUTED`: [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) (CONDITIONAL)
- `DS-R-UNGRADED-COUNT` `COMPUTED`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION)

Outgoing (1):

- `DS-R-GRADED-PATHSUM-FROM-CARRIER` `COMPUTED`: [DS-QM030-GRADED-PATHSUM](DS-QM030-GRADED-PATHSUM.md) (COMPUTATIONALLY_CHECKED)
