# L1-QM003-C17-COMPOSABLE-FACTORIZATION

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact stochastic composition/action equality and diagonal density presentation, plus scalar matrix multiplication identities and the Hadamard defect in Lean.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Prove source residual-density factorization on its full carrier and channel class. The source diagonal multiplication anchor alone does not prove it. The broader source statement is kept in pfp_review.prior_statement.

## Source status

QM_003 C17 diagonal composable factorization and off-diagonal coherence boundary mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/L1-QM003-C17-COMPOSABLE-FACTORIZATION/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM003-C17-COMPOSABLE-FACTORIZATION/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact stochastic composition/action equality and diagonal density presentation, plus scalar matrix multiplication identities and the Hadamard defect in Lean.
  - does not support: Prove source residual-density factorization on its full carrier and channel class. The source diagonal multiplication anchor alone does not prove it.
  - next test: Prove source residual-density factorization on its full carrier and channel class. The source diagonal multiplication anchor alone does not prove it.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1005
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.qm003_c17_diagonal_composable_factorization` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm003_c17_diagonal_composable_factorization` |
| `QuantumMechanics.DerivationDagQMClosure.qm003_c17_off_diagonal_obstruction_to_diagonal_factorization` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm003_c17_off_diagonal_obstruction_to_diagonal_factorization` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1005
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1005_l1_qm003_c17_composable_factorization.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1005_l1_qm003_c17_composable_factorization.md](../../../dag/derivations/08_l1_to_l2/tfq_1005_l1_qm003_c17_composable_factorization.md)
- sha256 (`lf-normalised`): `6a1f01c0e8d5555c308f6a47fa44b39e53633183b6d1e3e8788238e4a5c3a1f5`
- generated view: listed, not counted
- cited in: record TFQ-1005
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/003_residual_density_calculus_l1_l2_boundary/qm_003_residual_density_calculus_l1_l2_boundary_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/003_residual_density_calculus_l1_l2_boundary/qm_003_residual_density_calculus_l1_l2_boundary_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `L1-R-QM003-C17-FACTORIZATION` `DERIVED_LEAN`: [L1-DENSITY-LIFT-SIGNED-SQRT-PUB009](L1-DENSITY-LIFT-SIGNED-SQRT-PUB009.md) (PROVED_LEAN)

Outgoing (0):

