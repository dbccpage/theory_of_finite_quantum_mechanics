# FQ-OPERATIONAL-LOCAL-TOMOGRAPHY

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Under calibration, a nonzero observation and descent of an admitted operation family, irreducibility of that family on the global state space forces injectivity of the observation (Schur-type; tomography_of_irreducible, calibrated_tomography). The existence of such a family is equivalent to local tomography, so this re-expresses rather than derives local tomography. Converse (OperationalFilterFamily): for a calibrated observation, irreducibility of the lifted coordinate (product-test) resets, and descent of all visibly normalized global resets, are each equivalent to local tomography (product_resets_irreducible_iff, global_reset_descent_iff_tomography). Under explicit closure rules (sequential admission, generating cone, preparability of all normalized states, bounded globally separating admitted effects) test-then-prepare resets are constructed as a positive, subnormalized, irreducible family (normalized_reset_family); this construction does not discharge the descent premise non-circularly. With the same-family dimension law K(d,n) = n + d binom(n,2), d \> 0, local tomography selects d = 2 (OperationalFieldSelection.selected_parameter). The classical doubled-pair control satisfies calibration, factorization and descent yet violates irreducibility and tomography. Narrowest claim of the filter-family run: Under explicit closure rules (sequential admission, generating cone, preparability of all normalized states, bounded globally separating admitted effects), test-then-prepare resets form a positive, subnormalized, irreducible family. For a calibrated observation, irreducibility of the lifted coordinate resets, and descent of all visibly normalized global resets, are each equivalent to local tomography. So resets cannot non-circularly discharge the descent-plus-irreducibility premise of OperationalTomography.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 10
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- cited Lean declaration references covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- local tomography (equivalent to the existence of an irreducible operation family that descends through the observation)
- field-linear state and effect spaces (not derived from primitive difference)
- independent dual product-frame calibration and factorization
- same-family dimension law and positive parameter (for the selection bridge)

## Bottleneck

Under calibration, a nonzero observation and descent of an admitted operation family, irreducibility of that family on the global state space forces injectivity (Schur-type). The existence of such a family is equivalent to local tomography, so this re-expresses rather than derives local tomography. A noncircular operational principle excluding hidden sectors is open; general tensor-cone uniqueness and operational classification remain open (FQ-GAP-TENSOR-UNIQUENESS). Does not support: A derivation of local tomography from primitive difference or from weaker operational premises; a noncircular principle excluding hidden sectors; tensor-cone uniqueness; physical availability of the constructed resets in any particular operational theory.

## Source status

Local tomography is imported. dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T174216Z_operational_tomography (Lean 4.35.0, OperationalTomography and OperationalFieldSelection; independent review in dag/results/FQ-GAP-TENSOR-UNIQUENESS/reviews/20261021T182843Z_pr144) establishes a field-neutral conditional theorem, and dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T185210Z_filter_family (OperationalFilterFamily) establishes that its operational premise is equivalent to local tomography, so the pair re-expresses local tomography and does not derive it. Replays: Python Fraction and Rust BigRational; fixture-integrity mutations rejected (277 for the tomography fixtures, 623 for the filter fixtures). Authority effect: none.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/OperationalFieldSelection.lean`

- file: [lean4/OperationalFieldSelection.lean](../../../lean4/OperationalFieldSelection.lean)
- sha256 (`bytes`): `c754b4ebbd10a6be222a822a885c76d31247739bd3a133c787df6d9775ad5631`
- cited in: node.lean, record TFQ-1048
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `OperationalFieldSelection`): recorded sha256 `c754b4ebbd10a6be222a822a885c76d31247739bd3a133c787df6d9775ad5631` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build OperationalFieldSelection`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `OperationalFieldSelection.selected_parameter` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms OperationalFieldSelection.selected_parameter` |

- counts toward the grade: yes

### Lean: `lean4/OperationalFilterFamily.lean`

- file: [lean4/OperationalFilterFamily.lean](../../../lean4/OperationalFilterFamily.lean)
- sha256 (`bytes`): `7fa9ff1021788c9f3840cf95d71786fdb4c0fbe16bfa1cff0ebcb0fcaba7d192`
- cited in: node.lean, record TFQ-1048
- replay: `none`
- check: `cd lean4 && lake build OperationalFilterFamily`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `OperationalFilterFamily.global_reset_descent_iff_tomography` | yes | yes | yes | - | `#print axioms OperationalFilterFamily.global_reset_descent_iff_tomography` |
| `OperationalFilterFamily.normalized_reset_family` | yes | yes | yes | - | `#print axioms OperationalFilterFamily.normalized_reset_family` |
| `OperationalFilterFamily.product_resets_irreducible_iff` | yes | yes | yes | - | `#print axioms OperationalFilterFamily.product_resets_irreducible_iff` |
| `OperationalFilterFamily.product_test_pullback` | yes | yes | yes | - | `#print axioms OperationalFilterFamily.product_test_pullback` |

- counts toward the grade: yes

### Lean: `lean4/OperationalTomography.lean`

- file: [lean4/OperationalTomography.lean](../../../lean4/OperationalTomography.lean)
- sha256 (`bytes`): `d98cd34c7b11ed96ac0763486145c53e09fcb3eccd956cda45f1a5b887cdfd68`
- cited in: node.lean, record TFQ-1048
- replay: `none`
- check: `cd lean4 && lake build OperationalTomography`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `OperationalTomography.calibrated_tomography` | yes | yes | yes | - | `#print axioms OperationalTomography.calibrated_tomography` |
| `OperationalTomography.tomography_of_irreducible` | yes | yes | yes | - | `#print axioms OperationalTomography.tomography_of_irreducible` |

- counts toward the grade: yes

### Rust: `code/rust/src/finite_probability/operational_filters.rs`

- file: [code/rust/src/finite_probability/operational_filters.rs](../../../code/rust/src/finite_probability/operational_filters.rs)
- sha256 (`bytes`): `3c1d70ce8391f43e228666b7a59c119e27190111adb2a853a35229efac81d47f`
- cited in: node.rust, record TFQ-1048
- note: no test is cited for this symbol; its crate is tfqm_finite_probability
- counts toward the grade: yes

### Rust: `code/rust/src/finite_probability/operational_tomography.rs`

- file: [code/rust/src/finite_probability/operational_tomography.rs](../../../code/rust/src/finite_probability/operational_tomography.rs)
- sha256 (`bytes`): `dc92ab3fbdd8501ccb89d970a053e780e7c036c5ab3892c127f26cfccf48fbfb`
- cited in: node.rust, record TFQ-1048
- note: no test is cited for this symbol; its crate is tfqm_finite_probability
- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1048_fq_operational_local_tomography.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1048_fq_operational_local_tomography.md](../../../dag/derivations/10_finite_qm_core/tfq_1048_fq_operational_local_tomography.md)
- sha256 (`lf-normalised`): `020322fa4d2e632a9c1212a2b918b9e06c13663b040bad2a0a03ce39f710ba13`
- generated view: listed, not counted
- cited in: record TFQ-1048
- counts toward the grade: no

### Documents and data: `dag/results/FQ-GAP-TENSOR-UNIQUENESS/reviews/20261021T182843Z_pr144/README.md`

- file: [dag/results/FQ-GAP-TENSOR-UNIQUENESS/reviews/20261021T182843Z_pr144/README.md](../../../dag/results/FQ-GAP-TENSOR-UNIQUENESS/reviews/20261021T182843Z_pr144/README.md)
- sha256 (`lf-normalised`): `8169e62c96e8661ea92e3c0b8252867e82499a28c3daf478576b6932dcaf3d33`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T174216Z_operational_tomography/README.md`

- file: [dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T174216Z_operational_tomography/README.md](../../../dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T174216Z_operational_tomography/README.md)
- sha256 (`lf-normalised`): `9854dc36f40af42797cbdae8a8a115b3ebdc93cf85fd3e0b04dd99bb9f203632`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T174216Z_operational_tomography/p5/proposed_dag_delta.json`

- file: [dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T174216Z_operational_tomography/p5/proposed_dag_delta.json](../../../dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T174216Z_operational_tomography/p5/proposed_dag_delta.json)
- sha256 (`lf-normalised`): `b6710d3c563d633cd6b634ed85ca691cf9a61ad7d5f675b8755bf497bd234291`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T185210Z_filter_family/README.md`

- file: [dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T185210Z_filter_family/README.md](../../../dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T185210Z_filter_family/README.md)
- sha256 (`lf-normalised`): `d30cabed719b04a2673c7038fef9a5d54c138ae7b23940245e7a8c85a883d440`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T185210Z_filter_family/proposed_dag_delta.json`

- file: [dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T185210Z_filter_family/proposed_dag_delta.json](../../../dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T185210Z_filter_family/proposed_dag_delta.json)
- sha256 (`lf-normalised`): `bdd193bfe7eda1ba885e46a8c367090a9d7d1b2c6c673cbadaaaf87ed9342141`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQ-R-OPERATIONAL-LOCAL-TOMOGRAPHY` `CONDITIONAL_ON_IMPORT`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

