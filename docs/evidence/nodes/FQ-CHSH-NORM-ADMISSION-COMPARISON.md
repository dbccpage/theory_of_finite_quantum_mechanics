# FQ-CHSH-NORM-ADMISSION-COMPARISON

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a declared real normed space, unit vectors and contractive linear effects, the CHSH value is bounded by the sum and difference norms and hence by 4. A supplied parallelogram law gives squared bound 8; Mathlib reconstructs the compatible inner product by polarization. Explicit two-dimensional l1 and linfinity witnesses attain 4, and an l2 witness attains 2sqrt2. The common unbiased binary response tables are nonnegative, normalized and no-signalling. A separate nonnegative global mixture of deterministic signs has CHSH bound 2.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 28
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 28 Lean reference(s) cited, 28 in this checkout (replay: none 28). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- real scalar field and real normed vector space: supplied; finite-dimensional examples have infinite underlying carriers
- contractive effects and two vectors of norm at most one: supplied
- unbiased binary probability rule (1+a*b*E)/4: supplied
- parallelogram law: supplied only for the 2sqrt2 branch
- full coordinate state/effect witnesses: declared finite-dimensional comparison examples

## Bottleneck

No derivation of the norm, quadratic readout, tensor composition or probability law from primitive difference. Parallelogram reconstruction reformulates inner-product geometry; the CHSH ceiling alone is not asserted to characterize it. Probability-table validity does not establish arbitrary composites or sequential instruments. The remaining task is to derive or weaken the geometric premises under explicitly supplied upstream assumptions.

## Source status

Fresh CHSHNormAdmission.lean compilation succeeded on 2026-11-06 with 28 theorem anchors and no warnings. Each audited theorem reports propext, Classical.choice and Quot.sound. Kernel statements retain the supplied norm/effect interface and branch-specific parallelogram premise. General inequalities need no finite-dimension hypothesis. Replay commands, hashes and exact checks are recorded by evidence/chsh_norm_admission/verify.py in verification.json.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CHSHNormAdmission.lean`

- file: [lean4/CHSHNormAdmission.lean](../../../lean4/CHSHNormAdmission.lean)
- sha256 (`bytes`): `3e0df03c41166afe952ff5770d9ec72d6a0353fe3d9709a07c34cb0494b9d9fd`
- cited in: node.lean, node.source, record TFQ-2621
- replay: `none`
- check: `cd lean4 && lake build CHSHNormAdmission`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CHSHNormAdmission.algebraic_bound` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.algebraic_bound` |
| `CHSHNormAdmission.chsh_le_two_sqrt_two` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.chsh_le_two_sqrt_two` |
| `CHSHNormAdmission.chsh_sq_le_eight` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.chsh_sq_le_eight` |
| `CHSHNormAdmission.correlator_bound` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.correlator_bound` |
| `CHSHNormAdmission.deterministic_local_bound` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.deterministic_local_bound` |
| `CHSHNormAdmission.dual_sum_difference_bound` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.dual_sum_difference_bound` |
| `CHSHNormAdmission.inner_product_implies_parallelogram` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.inner_product_implies_parallelogram` |
| `CHSHNormAdmission.l1_effect_minus` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.l1_effect_minus` |
| `CHSHNormAdmission.l1_effect_plus` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.l1_effect_plus` |
| `CHSHNormAdmission.l1_fails_parallelogram` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.l1_fails_parallelogram` |
| `CHSHNormAdmission.l1_pr_witness` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.l1_pr_witness` |
| `CHSHNormAdmission.l2_attainment` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.l2_attainment` |
| `CHSHNormAdmission.l2_effect` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.l2_effect` |
| `CHSHNormAdmission.l2_norm_sq` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.l2_norm_sq` |
| `CHSHNormAdmission.l2_parallelogram` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.l2_parallelogram` |
| `CHSHNormAdmission.l2_upper_bound` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.l2_upper_bound` |
| `CHSHNormAdmission.l2_witness_effects` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.l2_witness_effects` |
| `CHSHNormAdmission.linfty_effect_first` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.linfty_effect_first` |
| `CHSHNormAdmission.linfty_effect_second` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.linfty_effect_second` |
| `CHSHNormAdmission.linfty_pr_witness` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.linfty_pr_witness` |
| `CHSHNormAdmission.marginal_alice` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.marginal_alice` |
| `CHSHNormAdmission.marginal_bob` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.marginal_bob` |
| `CHSHNormAdmission.positive_mixture_bound` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.positive_mixture_bound` |
| `CHSHNormAdmission.probability_nonnegative` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.probability_nonnegative` |
| `CHSHNormAdmission.probability_normalized` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.probability_normalized` |
| `CHSHNormAdmission.probability_recovers_correlator` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.probability_recovers_correlator` |
| `CHSHNormAdmission.reconstructed_polarization` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.reconstructed_polarization` |
| `CHSHNormAdmission.unitEffect_iff_dual_bound` | yes | yes | yes | - | `#print axioms CHSHNormAdmission.unitEffect_iff_dual_bound` |

- counts toward the grade: yes

### Python: `code/python/src/qm/chsh_norm_admission.py`

- file: [code/python/src/qm/chsh_norm_admission.py](../../../code/python/src/qm/chsh_norm_admission.py)
- sha256 (`bytes`): `b4992d534d96fbc21edabb377ff56b24834539bb3bf5f47823c99a8e5184fc2b`
- cited in: node.source, record TFQ-2621
- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_2621_chsh_norm_admission_comparison.md`

- file: [dag/derivations/10_finite_qm_core/tfq_2621_chsh_norm_admission_comparison.md](../../../dag/derivations/10_finite_qm_core/tfq_2621_chsh_norm_admission_comparison.md)
- sha256 (`lf-normalised`): `efec2c75972c82a97c83092db50fb658dc0f7963089a32155bcf8b4260475f8a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2621
- counts toward the grade: no

## Routes

Incoming (1):

- `FQ-R-CHSH-NORM-ADMISSION-COMPARISON-CONTEXT` `RECORD_PARENT`: [DS-QM073-FINITE-CHSH-AND-PR-BOX](DS-QM073-FINITE-CHSH-AND-PR-BOX.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

