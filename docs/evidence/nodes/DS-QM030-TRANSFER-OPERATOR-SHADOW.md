# DS-QM030-TRANSFER-OPERATOR-SHADOW

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: All coefficients of AB, (AB)v, A(Bv), fA, f(Av), and (fA)v agree on exact retained inputs.

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

- ring structure (subtraction) (assumption)

## Bottleneck

Unmet after the PFP review: Formalize the full arbitrary finite action/dual sum transport; the state carrier, linearity and coefficients are supplied. The broader source statement is kept in pfp_review.prior_statement.

## Source status

\[PROVEN, CONDITIONAL-DERIVED + H2\] (QM-030-C6)

## Review

- PFP review: [dag/results/DS-QM030-TRANSFER-OPERATOR-SHADOW/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/DS-QM030-TRANSFER-OPERATOR-SHADOW/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: All coefficients of AB, (AB)v, A(Bv), fA, f(Av), and (fA)v agree on exact retained inputs.
  - does not support: Formalize the full arbitrary finite action/dual sum transport; the state carrier, linearity and coefficients are supplied.
  - next test: Formalize the full arbitrary finite action/dual sum transport; the state carrier, linearity and coefficients are supplied.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1039
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_graded_pathsum_overcount_transfer_and_feynman_shadow` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_graded_pathsum_overcount_transfer_and_feynman_shadow` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1039
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_1039_ds_qm030_transfer_operator_shadow.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_1039_ds_qm030_transfer_operator_shadow.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_1039_ds_qm030_transfer_operator_shadow.md)
- sha256 (`lf-normalised`): `ad543de27efa35afeb34fdcc55c3becebecb09949c5b8e19d75d868c196a4e94`
- generated view: listed, not counted
- cited in: record TFQ-1039
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/030_finite_weighted_transport_calculus/qm_030_finite_weighted_transport_calculus_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/030_finite_weighted_transport_calculus/qm_030_finite_weighted_transport_calculus_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `DS-R-PATHSUM` `COMPUTED`: [DS-QM030-GRADED-PATHSUM](DS-QM030-GRADED-PATHSUM.md) (COMPUTATIONALLY_CHECKED)

Outgoing (3):

- `DS-R-LGPT-GAUGE` `COMPUTED`: [DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS](DS-QM040-GAUSSINT-LAMBDA-COMMUTATOR-WITNESS.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-SCHRODINGER-CONDITIONAL` `COMPUTED`: [DS-QM033-SCHRODINGER-DISCRETE-COCHAIN](DS-QM033-SCHRODINGER-DISCRETE-COCHAIN.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-SCHRODINGER-FROM-PATHSUM` `COMPUTED`: [DS-QM033-SCHRODINGER-DISCRETE-COCHAIN](DS-QM033-SCHRODINGER-DISCRETE-COCHAIN.md) (COMPUTATIONALLY_CHECKED)
