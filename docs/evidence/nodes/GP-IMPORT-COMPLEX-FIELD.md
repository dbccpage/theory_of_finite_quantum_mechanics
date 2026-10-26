# GP-IMPORT-COMPLEX-FIELD

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Complex numbers as a complete field. On the finite report host only Z\[i\] (Gaussian integers) is available: 1+i has no inverse, and a self-adjoint Gauss-integer matrix need not have a Gauss-integer eigenvalue.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 38
- distinct cited Lean declarations covered by a current replay receipt: 33
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- complex field C: assumption (completion Q -\> R/C is obstructed on the finite host, PRICE-ALG-01)

## Bottleneck

The example rules out Gaussian-integer eigenpairs for this one matrix. A spectral theorem after extending scalars to a complete complex field, and a derivation or selection of that field from primitive difference, remain imported. This obstruction does not prove that completion or the complex numbers are uniquely necessary; the cyclotomic ring Z\[zeta_n\] remains a recorded discrete substitute.

## Source status

imported / lost on this host (GaussInt is not a field); conditional selection of d = 2 among supplied same-family matrix carriers is established by ComplexFieldSelection (node L1-IMP-COMPLEX-FIELD), but the original complete-field claim remains imported because completeness is not derived

## Review

- PFP review: [dag/research/pr_390_current_scope_review.json](../../../dag/research/pr_390_current_scope_review.json); file present and sha256 matches the node's record: yes; verdict `scoped_gaussian_integer_result_reviewed`; scope effect `caveat_added`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: For a Gaussian integer a+bi, the product (1+i)*(a+bi) equals (a-b)+(a+b)i and differs from the real unit, and (a+bi)*(1+i) differs from the real unit. The matrix with entries 0, 1, 1, 1 in row-major order has each diagonal entry equal to its own conjugate and each off-diagonal entry equal to the conjugate of the other, and it sends a column (x, y) to (y, x+y). When (x, y) differs from the zero column, (y, x+y) differs from lam*(x, y) for each Gaussian integer lam.
  - does not support: The example rules out Gaussian-integer eigenpairs for this one matrix. A spectral theorem after extending scalars to a complete complex field, and a derivation or selection of that field from primitive difference, remain imported. This obstruction does not prove that completion or the complex numbers are uniquely necessary; the cyclotomic ring Z\[zeta_n\] remains a recorded discrete substitute.
  - next test: Keep the complete-field import explicit while reusing the exact Gaussian-integer obstruction.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignGpImportComplexField.lean`

- file: [lean4/CampaignGpImportComplexField.lean](../../../lean4/CampaignGpImportComplexField.lean)
- sha256 (`bytes`): `c090c3aa370fd870e88362aa4cd9f27302b427773acf8bf97c2a2f936929c5a6`
- cited in: node.lean, receipt dag/research/campaign_gp-import-complex-field_lean_replay.json (CampaignGpImportComplexField), receipt dag/research/pr_390_round2_replay.json (CampaignGpImportComplexField), record TFQ-1029
- replay: `verified`
  - receipt [dag/research/campaign_gp-import-complex-field_lean_replay.json](../../../dag/research/campaign_gp-import-complex-field_lean_replay.json) (module `CampaignGpImportComplexField`): recorded sha256 `c090c3aa370fd870e88362aa4cd9f27302b427773acf8bf97c2a2f936929c5a6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_390_round2_replay.json](../../../dag/research/pr_390_round2_replay.json) (module `CampaignGpImportComplexField`): recorded sha256 `c090c3aa370fd870e88362aa4cd9f27302b427773acf8bf97c2a2f936929c5a6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignGpImportComplexField`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignGpImportComplexField.fib` | yes | yes | yes | none | `#print axioms CampaignGpImportComplexField.fib` |
| `CampaignGpImportComplexField.fib_conjugate_transpose` | yes | yes | yes | none | `#print axioms CampaignGpImportComplexField.fib_conjugate_transpose` |
| `CampaignGpImportComplexField.fib_mulVec` | yes | yes | yes | propext | `#print axioms CampaignGpImportComplexField.fib_mulVec` |
| `CampaignGpImportComplexField.fib_no_gauss_eigenpair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGpImportComplexField.fib_no_gauss_eigenpair` |
| `CampaignGpImportComplexField.gAdd` | yes | yes | yes | none | `#print axioms CampaignGpImportComplexField.gAdd` |
| `CampaignGpImportComplexField.gAdd_zero_left` | yes | yes | yes | propext | `#print axioms CampaignGpImportComplexField.gAdd_zero_left` |
| `CampaignGpImportComplexField.gConj` | yes | yes | yes | none | `#print axioms CampaignGpImportComplexField.gConj` |
| `CampaignGpImportComplexField.gMul` | yes | yes | yes | none | `#print axioms CampaignGpImportComplexField.gMul` |
| `CampaignGpImportComplexField.gMul_add_left` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGpImportComplexField.gMul_add_left` |
| `CampaignGpImportComplexField.gMul_assoc` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGpImportComplexField.gMul_assoc` |
| `CampaignGpImportComplexField.gMul_comm` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGpImportComplexField.gMul_comm` |
| `CampaignGpImportComplexField.gMul_eq_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGpImportComplexField.gMul_eq_zero` |
| `CampaignGpImportComplexField.gMul_one_left` | yes | yes | yes | propext | `#print axioms CampaignGpImportComplexField.gMul_one_left` |
| `CampaignGpImportComplexField.gMul_sub_left` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGpImportComplexField.gMul_sub_left` |
| `CampaignGpImportComplexField.gMul_zero_left` | yes | yes | yes | propext | `#print axioms CampaignGpImportComplexField.gMul_zero_left` |
| `CampaignGpImportComplexField.gMul_zero_right` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGpImportComplexField.gMul_zero_right` |
| `CampaignGpImportComplexField.gNorm` | yes | yes | yes | none | `#print axioms CampaignGpImportComplexField.gNorm` |
| `CampaignGpImportComplexField.gNorm_eq_zero_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGpImportComplexField.gNorm_eq_zero_iff` |
| `CampaignGpImportComplexField.gNorm_mul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGpImportComplexField.gNorm_mul` |
| `CampaignGpImportComplexField.gOne` | yes | yes | yes | none | `#print axioms CampaignGpImportComplexField.gOne` |
| `CampaignGpImportComplexField.gSq` | yes | yes | yes | none | `#print axioms CampaignGpImportComplexField.gSq` |
| `CampaignGpImportComplexField.gSub` | yes | yes | yes | none | `#print axioms CampaignGpImportComplexField.gSub` |
| `CampaignGpImportComplexField.gSub_eq_zero_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignGpImportComplexField.gSub_eq_zero_iff` |
| `CampaignGpImportComplexField.gZero` | yes | yes | yes | none | `#print axioms CampaignGpImportComplexField.gZero` |
| `CampaignGpImportComplexField.gauss_sq_ne_succ` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGpImportComplexField.gauss_sq_ne_succ` |
| `CampaignGpImportComplexField.intSqNeFive` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignGpImportComplexField.intSqNeFive` |
| `CampaignGpImportComplexField.int_sq_nonneg` | yes | yes | yes | propext | `#print axioms CampaignGpImportComplexField.int_sq_nonneg` |
| `CampaignGpImportComplexField.mulVec` | yes | yes | yes | none | `#print axioms CampaignGpImportComplexField.mulVec` |
| `CampaignGpImportComplexField.onePlusI_mul_coords` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGpImportComplexField.onePlusI_mul_coords` |
| `CampaignGpImportComplexField.onePlusI_mul_ne_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGpImportComplexField.onePlusI_mul_ne_one` |
| `CampaignGpImportComplexField.onePlusI_not_unit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGpImportComplexField.onePlusI_not_unit` |
| `CampaignGpImportComplexField.scaleVec` | yes | yes | yes | none | `#print axioms CampaignGpImportComplexField.scaleVec` |
| `CampaignGpImportComplexField.twice_sub_one_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignGpImportComplexField.twice_sub_one_sq` |
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
- sha256 (`lf-normalised`): `67585207e087cf0bbce831d28fbb75cebb94018c1205c5c7384c7932e0095821`
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
