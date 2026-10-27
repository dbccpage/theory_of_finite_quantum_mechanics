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

### Lean: `lean4/ComplexFieldImport.lean`

- file: [lean4/ComplexFieldImport.lean](../../../lean4/ComplexFieldImport.lean)
- sha256 (`bytes`): `52a15ed0308e195b78b3d7659c1cea35fc148dfef6c5557c99be30d545d29559`
- cited in: node.lean, receipt dag/research/campaign_gp-import-complex-field_lean_replay.json (ComplexFieldImport), receipt dag/research/pr_390_round2_replay.json (ComplexFieldImport), record TFQ-1029
- replay: `verified`
  - receipt [dag/research/campaign_gp-import-complex-field_lean_replay.json](../../../dag/research/campaign_gp-import-complex-field_lean_replay.json) (module `ComplexFieldImport`): recorded sha256 `52a15ed0308e195b78b3d7659c1cea35fc148dfef6c5557c99be30d545d29559` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_390_round2_replay.json](../../../dag/research/pr_390_round2_replay.json) (module `ComplexFieldImport`): recorded sha256 `52a15ed0308e195b78b3d7659c1cea35fc148dfef6c5557c99be30d545d29559` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ComplexFieldImport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ComplexFieldImport.fib` | yes | yes | yes | none | `#print axioms ComplexFieldImport.fib` |
| `ComplexFieldImport.fib_conjugate_transpose` | yes | yes | yes | none | `#print axioms ComplexFieldImport.fib_conjugate_transpose` |
| `ComplexFieldImport.fib_mulVec` | yes | yes | yes | propext | `#print axioms ComplexFieldImport.fib_mulVec` |
| `ComplexFieldImport.fib_no_gauss_eigenpair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ComplexFieldImport.fib_no_gauss_eigenpair` |
| `ComplexFieldImport.gAdd` | yes | yes | yes | none | `#print axioms ComplexFieldImport.gAdd` |
| `ComplexFieldImport.gAdd_zero_left` | yes | yes | yes | propext | `#print axioms ComplexFieldImport.gAdd_zero_left` |
| `ComplexFieldImport.gConj` | yes | yes | yes | none | `#print axioms ComplexFieldImport.gConj` |
| `ComplexFieldImport.gMul` | yes | yes | yes | none | `#print axioms ComplexFieldImport.gMul` |
| `ComplexFieldImport.gMul_add_left` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ComplexFieldImport.gMul_add_left` |
| `ComplexFieldImport.gMul_assoc` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ComplexFieldImport.gMul_assoc` |
| `ComplexFieldImport.gMul_comm` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ComplexFieldImport.gMul_comm` |
| `ComplexFieldImport.gMul_eq_zero` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ComplexFieldImport.gMul_eq_zero` |
| `ComplexFieldImport.gMul_one_left` | yes | yes | yes | propext | `#print axioms ComplexFieldImport.gMul_one_left` |
| `ComplexFieldImport.gMul_sub_left` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ComplexFieldImport.gMul_sub_left` |
| `ComplexFieldImport.gMul_zero_left` | yes | yes | yes | propext | `#print axioms ComplexFieldImport.gMul_zero_left` |
| `ComplexFieldImport.gMul_zero_right` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ComplexFieldImport.gMul_zero_right` |
| `ComplexFieldImport.gNorm` | yes | yes | yes | none | `#print axioms ComplexFieldImport.gNorm` |
| `ComplexFieldImport.gNorm_eq_zero_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ComplexFieldImport.gNorm_eq_zero_iff` |
| `ComplexFieldImport.gNorm_mul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ComplexFieldImport.gNorm_mul` |
| `ComplexFieldImport.gOne` | yes | yes | yes | none | `#print axioms ComplexFieldImport.gOne` |
| `ComplexFieldImport.gSq` | yes | yes | yes | none | `#print axioms ComplexFieldImport.gSq` |
| `ComplexFieldImport.gSub` | yes | yes | yes | none | `#print axioms ComplexFieldImport.gSub` |
| `ComplexFieldImport.gSub_eq_zero_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms ComplexFieldImport.gSub_eq_zero_iff` |
| `ComplexFieldImport.gZero` | yes | yes | yes | none | `#print axioms ComplexFieldImport.gZero` |
| `ComplexFieldImport.gauss_sq_ne_succ` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ComplexFieldImport.gauss_sq_ne_succ` |
| `ComplexFieldImport.intSqNeFive` | yes | yes | yes | Quot.sound, propext | `#print axioms ComplexFieldImport.intSqNeFive` |
| `ComplexFieldImport.int_sq_nonneg` | yes | yes | yes | propext | `#print axioms ComplexFieldImport.int_sq_nonneg` |
| `ComplexFieldImport.mulVec` | yes | yes | yes | none | `#print axioms ComplexFieldImport.mulVec` |
| `ComplexFieldImport.onePlusI_mul_coords` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ComplexFieldImport.onePlusI_mul_coords` |
| `ComplexFieldImport.onePlusI_mul_ne_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ComplexFieldImport.onePlusI_mul_ne_one` |
| `ComplexFieldImport.onePlusI_not_unit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ComplexFieldImport.onePlusI_not_unit` |
| `ComplexFieldImport.scaleVec` | yes | yes | yes | none | `#print axioms ComplexFieldImport.scaleVec` |
| `ComplexFieldImport.twice_sub_one_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ComplexFieldImport.twice_sub_one_sq` |
| `fib_conjugate_transpose` | yes | yes | yes | none | `#print axioms fib_conjugate_transpose` |
| `fib_mulVec` | yes | yes | yes | propext | `#print axioms fib_mulVec` |
| `fib_no_gauss_eigenpair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms fib_no_gauss_eigenpair` |
| `onePlusI_mul_coords` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms onePlusI_mul_coords` |
| `onePlusI_not_unit` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms onePlusI_not_unit` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1029_gp_import_complex_field.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1029_gp_import_complex_field.md](../../../dag/derivations/08_l1_to_l2/tfq_1029_gp_import_complex_field.md)
- sha256 (`lf-normalised`): `a8237bc45d01a4aa4ac026cda9c89f276cf7a3e0c9ecbd8e81d28b8ca8e4151f`
- generated view: listed, not counted
- cited in: record TFQ-1029
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:49250fc3940b574236fe8aeb8acabb9673af35fe28f17474e9deb52ecd18a713#GAP-F001-S000-009`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`
- `external:sha256:a635008d68c51a062b794996dc85a68693522928a157d619d01ffada1ba595f1#PRICE-ALG-01`
- `external:sha256:a635008d68c51a062b794996dc85a68693522928a157d619d01ffada1ba595f1#PRICE-HD-01`
- `external:sha256:f4ef85f405ba846ddf92fd6bbd8fc7aaa86d658c4678b4b841989f2cb97ee004:148`

## Routes

Incoming (0):


Outgoing (2):

- `APP-R-MUB-EXACT-PROJECTORS` `CONDITIONAL_ON_IMPORT`: [MUB-EXACT-PROJECTORS](MUB-EXACT-PROJECTORS.md) (DEFINITION)
- `X-R-DROP-ONE-CENSUS` `DERIVED_LEAN`: [GP-DROP-ONE-CENSUS](GP-DROP-ONE-CENSUS.md) (PROVED_LEAN)

No incoming route.
