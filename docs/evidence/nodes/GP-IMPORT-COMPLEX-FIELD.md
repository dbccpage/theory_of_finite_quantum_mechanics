# GP-IMPORT-COMPLEX-FIELD

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Complex numbers as a complete field. On the finite report host only Z\[i\] (Gaussian integers) is available: 1+i has no inverse, and a self-adjoint Gauss-integer matrix need not have a Gauss-integer eigenvalue.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- complex field C: assumption (completion Q -\> R/C is obstructed on the finite host, PRICE-ALG-01)

## Bottleneck

No derivation of a field with completion from primitive difference; discrete substitute is the cyclotomic ring Z\[zeta_n\].

## Source status

imported / lost on this host (GaussInt is not a field); conditional selection of d = 2 among supplied same-family matrix carriers is established by ComplexFieldSelection (node L1-IMP-COMPLEX-FIELD), but the original complete-field claim remains imported because completeness is not derived

## Review

- PFP review: [dag/results/GP-IMPORT-COMPLEX-FIELD/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/GP-IMPORT-COMPLEX-FIELD/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Exact reciprocals/units and a no-integer-root obstruction control; generally no integer inverse to1+i and no integer square2 in Lean.
  - does not support: Complete complex field, spectral theorem and completeness remain imports. The computed finite polynomial samples do not prove a full spectral theorem.
  - next test: Complete complex field, spectral theorem and completeness remain imports. The computed finite polynomial samples do not prove a full spectral theorem.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1029
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` |
- counts toward the grade: yes

### Lean: `lean4/H017Extras.lean`

- file: [lean4/H017Extras.lean](../../../lean4/H017Extras.lean)
- sha256 (`bytes`): `5ca59147d0613750ef3870907d1b4ac0318c22cf6b85f608a2a09fbfb62637bf`
- cited in: node.lean, record TFQ-1029
- replay: `none`
- check: `cd lean4 && lake build H017Extras`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `remaining_extras_for_ordinary_mnC` | yes | yes | yes | - | `#print axioms remaining_extras_for_ordinary_mnC` |
- counts toward the grade: yes

### Lean: `lean4/H017ExtrasDropone.lean`

- file: [lean4/H017ExtrasDropone.lean](../../../lean4/H017ExtrasDropone.lean)
- sha256 (`bytes`): `919ca08a830f788648e81faf36c5008a51b7a027cd84edd3b2cfca3b63dace7e`
- cited in: node.lean, record TFQ-1029
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `H017ExtrasDropone`): recorded sha256 `919ca08a830f788648e81faf36c5008a51b7a027cd84edd3b2cfca3b63dace7e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build H017ExtrasDropone`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `drop_one_count` | yes | yes | yes | Quot.sound, propext | `#print axioms drop_one_count` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1029
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1029_gp_import_complex_field.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1029_gp_import_complex_field.md](../../../dag/derivations/08_l1_to_l2/tfq_1029_gp_import_complex_field.md)
- sha256 (`lf-normalised`): `6e6c16d6c4f5dce8b806c7aa7b60354b1b6cd461d3d43bea9a46e75f72a47308`
- generated view: listed, not counted
- cited in: record TFQ-1029
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


Outgoing (2):

- `APP-R-MUB-EXACT-PROJECTORS` `CONDITIONAL_ON_IMPORT`: [MUB-EXACT-PROJECTORS](MUB-EXACT-PROJECTORS.md) (DEFINITION)
- `X-R-DROP-ONE-CENSUS` `DERIVED_LEAN`: [GP-DROP-ONE-CENSUS](GP-DROP-ONE-CENSUS.md) (PROVED_LEAN)

No incoming route.
