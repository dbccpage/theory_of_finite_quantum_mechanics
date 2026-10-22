# GP-IMPORT-TENSOR-PRODUCT

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Hilbert tensor product as the unique way to combine systems. On Bool x Bool a bilinear integer-homogeneous Kronecker-normalized map equals the pointwise product; a weaker same-host combining interface has a rival (dump-the-right-report map).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- tensor product combining rule: assumption

## Bottleneck

Combining-systems uniqueness not derived; needs a second presented carrier (QM_122 7.1 item 1).

## Source status

imported; unique only on the named bilinear Kronecker interface

## Review

- PFP review: [dag/results/GP-IMPORT-TENSOR-PRODUCT/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/GP-IMPORT-TENSOR-PRODUCT/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Exact tensor/dumpRight and norm-multiplicativity arrays, with generic bilinearity and a basis-collision control in Lean.
  - does not support: Refine the complete CombiningEmbed/Kronecker uniqueness theorem and justify the physical composition rule; weak tag interfaces do not select a Hilbert tensor product.
  - next test: Refine the complete CombiningEmbed/Kronecker uniqueness theorem and justify the physical composition rule; weak tag interfaces do not select a Hilbert tensor product.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1032
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` |
- counts toward the grade: yes

### Lean: `lean4/H014BilinearProduct.lean`

- file: [lean4/H014BilinearProduct.lean](../../../lean4/H014BilinearProduct.lean)
- sha256 (`bytes`): `fabd54a913240848de949fb629a744d82f0485b3a40aeba32fc1c39e55353cde`
- cited in: node.lean, record TFQ-1032
- replay: `none`
- check: `cd lean4 && lake build H014BilinearProduct`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `embed_eq_tensor` | yes | yes | yes | - | `#print axioms embed_eq_tensor` |
- counts toward the grade: yes

### Lean: `lean4/H014Interface.lean`

- file: [lean4/H014Interface.lean](../../../lean4/H014Interface.lean)
- sha256 (`bytes`): `320a143feb167f7665d81508f191954b270d47bfc9a14fab1d51fe6428e0fba0`
- cited in: node.lean, record TFQ-1032
- replay: `none`
- check: `cd lean4 && lake build H014Interface`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `two_combinings_share_interface_and_disagree` | yes | yes | yes | - | `#print axioms two_combinings_share_interface_and_disagree` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1032
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1032_gp_import_tensor_product.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1032_gp_import_tensor_product.md](../../../dag/derivations/08_l1_to_l2/tfq_1032_gp_import_tensor_product.md)
- sha256 (`lf-normalised`): `e0410012d2769f4e87332efe846e375d8d5e8fbb43a441ab691a41c8df4b3e63`
- generated view: listed, not counted
- cited in: record TFQ-1032
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/claims/continuum_price_ledger.yaml`

- file: `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/claims/continuum_price_ledger.yaml`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/claims/gap_register.yaml`

- file: `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/claims/gap_register.yaml`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/finite_hilbert_boundary_from_primitive_difference.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/finite_hilbert_boundary_from_primitive_difference.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (0):


Outgoing (3):

- `APP-R-MUB6-QUHEX-TENSOR-CARRIER` `DERIVED_PROSE`: [MUB6-QUHEX-TENSOR-CARRIER](MUB6-QUHEX-TENSOR-CARRIER.md) (DEFINITION)
- `X-R-DROP-ONE-CENSUS` `DERIVED_LEAN`: [GP-DROP-ONE-CENSUS](GP-DROP-ONE-CENSUS.md) (PROVED_LEAN)
- `X-R-IMPORTS-TO-DECLARED-INTERFACE` `CONDITIONAL_ON_IMPORT`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

No incoming route.
