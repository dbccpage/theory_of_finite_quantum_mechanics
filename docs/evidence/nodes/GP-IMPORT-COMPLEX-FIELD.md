# GP-IMPORT-COMPLEX-FIELD

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a Gaussian integer a+bi, the product (1+i)*(a+bi) equals (a-b)+(a+b)i and differs from the real unit, and (a+bi)*(1+i) differs from the real unit. The matrix with entries 0, 1, 1, 1 in row-major order has each diagonal entry equal to its own conjugate and each off-diagonal entry equal to the conjugate of the other, and it sends a column (x, y) to (y, x+y). When (x, y) differs from the zero column, (y, x+y) differs from lam*(x, y) for each Gaussian integer lam.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- complex field C: assumption (completion Q -\> R/C is obstructed on the finite host, PRICE-ALG-01)

## Bottleneck

A complete complex field, a spectral theorem for a general self-adjoint Gauss-integer matrix, and a derivation of completion from primitive difference stay imported. The cyclotomic ring Z\[zeta_n\] stays a recorded discrete substitute.

## Source status

imported / lost on this host (GaussInt is not a field); conditional selection of d = 2 among supplied same-family matrix carriers is established by ComplexFieldSelection (node L1-IMP-COMPLEX-FIELD), but the original complete-field claim remains imported because completeness is not derived

## Review

- PFP review: [dag/results/GP-IMPORT-COMPLEX-FIELD/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/GP-IMPORT-COMPLEX-FIELD/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Exact reciprocals/units and a no-integer-root obstruction control; generally no integer inverse to1+i and no integer square2 in Lean.
  - does not support: Complete complex field, spectral theorem and completeness remain imports. The computed finite polynomial samples do not prove a full spectral theorem.
  - next test: Complete complex field, spectral theorem and completeness remain imports. The computed finite polynomial samples do not prove a full spectral theorem.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignGpImportComplexField.lean`

- file: [lean4/CampaignGpImportComplexField.lean](../../../lean4/CampaignGpImportComplexField.lean)
- sha256 (`bytes`): `c090c3aa370fd870e88362aa4cd9f27302b427773acf8bf97c2a2f936929c5a6`
- cited in: node.lean, receipt dag/research/campaign_gp-import-complex-field_lean_replay.json (CampaignGpImportComplexField), record TFQ-1029
- replay: `verified`
  - receipt [dag/research/campaign_gp-import-complex-field_lean_replay.json](../../../dag/research/campaign_gp-import-complex-field_lean_replay.json) (module `CampaignGpImportComplexField`): recorded sha256 `c090c3aa370fd870e88362aa4cd9f27302b427773acf8bf97c2a2f936929c5a6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignGpImportComplexField`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignGpImportComplexField.fib_conjugate_transpose` | yes | yes | yes | none | `#print axioms CampaignGpImportComplexField.fib_conjugate_transpose` |
| `CampaignGpImportComplexField.fib_mulVec` | yes | yes | yes | propext | `#print axioms CampaignGpImportComplexField.fib_mulVec` |
| `CampaignGpImportComplexField.fib_no_gauss_eigenpair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGpImportComplexField.fib_no_gauss_eigenpair` |
| `CampaignGpImportComplexField.onePlusI_mul_coords` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGpImportComplexField.onePlusI_mul_coords` |
| `CampaignGpImportComplexField.onePlusI_not_unit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGpImportComplexField.onePlusI_not_unit` |
| `fib_conjugate_transpose` | yes | yes | yes | none | `#print axioms fib_conjugate_transpose` |
| `fib_mulVec` | yes | yes | yes | propext | `#print axioms fib_mulVec` |
| `fib_no_gauss_eigenpair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms fib_no_gauss_eigenpair` |
| `onePlusI_mul_coords` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms onePlusI_mul_coords` |
| `onePlusI_not_unit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms onePlusI_not_unit` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1029
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1029_gp_import_complex_field.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1029_gp_import_complex_field.md](../../../dag/derivations/08_l1_to_l2/tfq_1029_gp_import_complex_field.md)
- sha256 (`lf-normalised`): `cad8ae4b9e638b34cdc8389bf18657a124408d1bb09f672b6a9117431f63eacc`
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
