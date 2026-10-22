# DS-QM070-PRODUCT-NONFACTORIZATION

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Actual marginals, normalized product reconstruction, signed residuals and Phi are checked; residual and zero-defect polynomials are general over Q in Lean.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- bipartite product structure A x B on a joint table (assumption)

## Bottleneck

Unmet after the PFP review: Formalize arbitrary finite table reconstruction and justify any tensor/basis/quantum coherence lift; a product defect of diagonals does not test entanglement. The broader source statement is kept in pfp_review.prior_statement.

## Source status

\[PROVEN\] mechanized Phi_zero_iff_factors, ENC-1123 (QM-070-C5, C6)

## Review

- PFP review: [dag/results/DS-QM070-PRODUCT-NONFACTORIZATION/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM070-PRODUCT-NONFACTORIZATION/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Actual marginals, normalized product reconstruction, signed residuals and Phi are checked; residual and zero-defect polynomials are general over Q in Lean.
  - does not support: Formalize arbitrary finite table reconstruction and justify any tensor/basis/quantum coherence lift; a product defect of diagonals does not test entanglement.
  - next test: Formalize arbitrary finite table reconstruction and justify any tensor/basis/quantum coherence lift; a product defect of diagonals does not test entanglement.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0256
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm070_071_product_nonfactorization_and_entanglement_witness` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm070_071_product_nonfactorization_and_entanglement_witness` |
- counts toward the grade: yes

### Lean: `lean4/H014TensorCompositionBoundary.lean`

- file: [lean4/H014TensorCompositionBoundary.lean](../../../lean4/H014TensorCompositionBoundary.lean)
- sha256 (`bytes`): `0754fd419711de9caf9e47d901c467db8f95dd38bfd570fefb305d0e9ad9386a`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build H014TensorCompositionBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `tensor_not_forced_open` | yes | yes | yes | - | `#print axioms tensor_not_forced_open` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/entanglement.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/entanglement.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0256_product_defect_on_a_bipartite_weight_table.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0256_product_defect_on_a_bipartite_weight_table.md](../../../dag/derivations/12_finite_qm_structure/tfq_0256_product_defect_on_a_bipartite_weight_table.md)
- sha256 (`lf-normalised`): `a8b8186f85a093a61bdcc4104959393ada8fa99ca487b667229e7f3d35694789`
- generated view: listed, not counted
- cited in: record TFQ-0256
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/070_product_non_factorization_as_a_bipartite_obstruction/qm_070_product_non_factorization_as_a_bipartite_obstruction_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/070_product_non_factorization_as_a_bipartite_obstruction/qm_070_product_non_factorization_as_a_bipartite_obstruction_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0256 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm
- TFQ-0256 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/entanglement.rs

## Routes

Incoming (2):

- `DS-R-PRODUCT-DEFECT` `DERIVED_LEAN`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION)
- `DS-R-PRODUCT-FROM-WEIGHTS` `DERIVED_LEAN`: [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) (CONDITIONAL)

Outgoing (2):

- `DS-R-PRODUCT-TO-ENTANGLEMENT` `DERIVED_LEAN`: [DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS](DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS.md) (PROVED_LEAN)
- `DS-R-QUBIT` `DERIVED_LEAN`: [DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED](DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED.md) (PROVED_LEAN)
