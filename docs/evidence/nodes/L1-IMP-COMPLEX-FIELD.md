# L1-IMP-COMPLEX-FIELD

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Under the imported R/C/H matrix-carrier restriction and the supplied same-family composite dimension multiplicativity K_d(nm) = K_d(n) K_d(m), K_d(n) = n + d binom(n,2), which follows from independent product preparations, factorized nondegenerate tests and (imported) local tomography, the parameter d = 2 is selected over the positive naturals (d = 0 also passes the bare equation but is not a carrier); the exact stand-in is Q(i). The real tag fails (a symmetric product-test-invisible witness over Q), the quaternionic tag fails by a dimension count, and the Gaussian-rational product span is proved for all finite index types. Not derived: local tomography, the carrier restriction (including exclusion of additional spin factors, direct sums and the exceptional algebra), or the completeness of the field. Earlier: Complex scalars as a field are declared, not derived. The finite stand-in is Q(i) / Z\[i\]; Z\[i\] is not a field (H007 gi_not_embedded).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 9
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- distinct cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- matrix carrier restriction, including extra spin-factor, exceptional and direct-sum exclusion
- same-family n*m composites
- independent product preparations and factorized nondegenerate tests
- local tomography (imported; its operational form, an irreducible operation family descending through the product observation, is equivalent to it and so re-expresses rather than derives it: see FQ-OPERATIONAL-LOCAL-TOMOGRAPHY, OperationalFilterFamily.product_resets_irreducible_iff)
- real/complex completeness

## Bottleneck

Local tomography and the carrier restriction are not derived from primitive difference, and the operational form of local tomography is equivalent to it; no continuum completion is supplied by this selection. Next test: derive field-neutral independent product preparations, factorized tests and state separation from operational primitives by a noncircular principle, or exclude additional spin-factor alternatives.

## Source status

Conditional selection kernel-checked in dag/results/L1-IMP-COMPLEX-FIELD/runs/20261021T162659Z_complex_selection (Lean 4.35.0; ComplexFieldSelection, 22 headline axiom audits; exact Python and Rust replays, 291 rejected fixture-integrity mutations) and independently reviewed in dag/results/L1-IMP-COMPLEX-FIELD/reviews/20261021T171132Z_pr138. Local tomography itself is an import here: OperationalTomography re-expresses it (an irreducible operation family that descends through the product observation exists iff local tomography holds; see FQ-OPERATIONAL-LOCAL-TOMOGRAPHY and OperationalFilterFamily.product_resets_irreducible_iff) and OperationalFieldSelection.selected_parameter consumes it (dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T174216Z_operational_tomography). Authority effect: none. Earlier: WDP-CH05-D01/N01: a quantum-capable package declares a complex carrier; QM_122 H007: Gaussian integers are not a field

## Review

- PFP review: [dag/results/L1-IMP-COMPLEX-FIELD/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/L1-IMP-COMPLEX-FIELD/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `CONDITIONAL`; qualifies for E4: yes.
  - narrowest claim: Exact Q(i) multiplication/norm/reciprocal controls, general norm multiplicativity and integer norm5 nonunit control in Lean.
  - does not support: Construct the field instance/refinement and topology/completion required for C; these rational pairs do not admit a complete field.
  - next test: Construct the field instance/refinement and topology/completion required for C; these rational pairs do not admit a complete field.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ComplexFieldSelection.lean`

- file: [lean4/ComplexFieldSelection.lean](../../../lean4/ComplexFieldSelection.lean)
- sha256 (`bytes`): `9fa0607d7e51940ea4e8822333df3f3dbe7f5c9332eec5c01a281c75261a0535`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `ComplexFieldSelection`): recorded sha256 `9fa0607d7e51940ea4e8822333df3f3dbe7f5c9332eec5c01a281c75261a0535` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ComplexFieldSelection`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ComplexFieldSelection.conditional_discharge` | yes | yes | yes | Quot.sound, propext | `#print axioms ComplexFieldSelection.conditional_discharge` |
| `ComplexFieldSelection.dimension_selection` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ComplexFieldSelection.dimension_selection` |
| `ComplexFieldSelection.gaussian_product_span` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ComplexFieldSelection.gaussian_product_span` |
| `ComplexFieldSelection.quaternion_refuted` | yes | yes | yes | Quot.sound, propext | `#print axioms ComplexFieldSelection.quaternion_refuted` |
| `ComplexFieldSelection.rho_same_product_statistics` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ComplexFieldSelection.rho_same_product_statistics` |
| `ComplexFieldSelection.rho_states` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms ComplexFieldSelection.rho_states` |

- counts toward the grade: yes

### Lean: `lean4/Complexification.lean`

- file: [lean4/Complexification.lean](../../../lean4/Complexification.lean)
- sha256 (`bytes`): `c975faaac47ea63dbbbfb40959b5af8c0cee04edb5a5c91f39f912fae741f6cf`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `Complexification`): recorded sha256 `c975faaac47ea63dbbbfb40959b5af8c0cee04edb5a5c91f39f912fae741f6cf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build Complexification`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `gi_not_embedded` | yes | yes | yes | propext | `#print axioms gi_not_embedded` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries` |
| `QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` |

- counts toward the grade: yes

### Lean: `lean4/OperationalFieldSelection.lean`

- file: [lean4/OperationalFieldSelection.lean](../../../lean4/OperationalFieldSelection.lean)
- sha256 (`bytes`): `c754b4ebbd10a6be222a822a885c76d31247739bd3a133c787df6d9775ad5631`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `OperationalFieldSelection`): recorded sha256 `c754b4ebbd10a6be222a822a885c76d31247739bd3a133c787df6d9775ad5631` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build OperationalFieldSelection`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `OperationalFieldSelection.selected_parameter` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms OperationalFieldSelection.selected_parameter` |

- counts toward the grade: yes

### Rust: `code/rust/src/finite_probability/complex_selection.rs`

- file: [code/rust/src/finite_probability/complex_selection.rs](../../../code/rust/src/finite_probability/complex_selection.rs)
- sha256 (`bytes`): `74ce34be9337b687fd0a604bdd8bf8083b4619a80b058dfb5c3afe5bb629dfd0`
- cited in: node.rust
- note: no test is cited for this symbol; its crate is tfqm_finite_probability
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md)
- sha256 (`lf-normalised`): `1596c27b09af32aec26710dacafcbe1dcb5081bc06d35d094b4c0b0353932e64`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0293_complex_field_as_a_declared_carrier.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0293_complex_field_as_a_declared_carrier.md](../../../dag/derivations/08_l1_to_l2/tfq_0293_complex_field_as_a_declared_carrier.md)
- sha256 (`lf-normalised`): `f926ab45dc41ec4a3f69b3968eba8f98de37d4b3f7646ffd9cf51cc0067f4f41`
- generated view: listed, not counted
- cited in: record TFQ-0293
- counts toward the grade: no

### Documents and data: `dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T174216Z_operational_tomography/README.md`

- file: [dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T174216Z_operational_tomography/README.md](../../../dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T174216Z_operational_tomography/README.md)
- sha256 (`lf-normalised`): `9854dc36f40af42797cbdae8a8a115b3ebdc93cf85fd3e0b04dd99bb9f203632`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/results/L1-IMP-COMPLEX-FIELD/runs/20261021T162659Z_complex_selection/README.md`

- file: [dag/results/L1-IMP-COMPLEX-FIELD/runs/20261021T162659Z_complex_selection/README.md](../../../dag/results/L1-IMP-COMPLEX-FIELD/runs/20261021T162659Z_complex_selection/README.md)
- sha256 (`lf-normalised`): `531bd889a8690afcf88b8fe7ce15a1ab00b4ad2cd0ef41496f395ab8823a68a8`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/results/L1-IMP-COMPLEX-FIELD/runs/20261021T162659Z_complex_selection/p5/proposed_node_delta.json`

- file: [dag/results/L1-IMP-COMPLEX-FIELD/runs/20261021T162659Z_complex_selection/p5/proposed_node_delta.json](../../../dag/results/L1-IMP-COMPLEX-FIELD/runs/20261021T162659Z_complex_selection/p5/proposed_node_delta.json)
- sha256 (`lf-normalised`): `ac708482b44b568b9d812fb710d4dc69621b680dd8d69e0d02b13f435efeb4b8`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:1ae9121daca3f6d1f5cb700a325bc1aaa0d5a6988db99eee907e24ca729e876e`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`
- `external:sha256:f4ef85f405ba846ddf92fd6bbd8fc7aaa86d658c4678b4b841989f2cb97ee004`

## Absences recorded by the TFQ records

- TFQ-0293 rust: no local rust twin located for external:sha256:ddaee3d0d77722244a6451750ca1e5acf7a57b4f02e75ecec70e810976d57d9e

## Routes

Incoming (1):

- `L1-R-COMPLEX-GAP` `GAP_NO_DERIVATION`: [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) (CONDITIONAL)

Outgoing (9):

- `APP-R-FSP-CAR-EXTERIOR-FOCK` `DERIVED_PROSE`: [FSP-CAR-EXTERIOR-FOCK](FSP-CAR-EXTERIOR-FOCK.md) (PROVED_PROSE)
- `L1-R-INNER-PRODUCT-GAP` `GAP_NO_DERIVATION`: [L1-IMP-HILBERT-INNER-PRODUCT](L1-IMP-HILBERT-INNER-PRODUCT.md) (CONDITIONAL)
- `L1-R-REALIFICATION-J` `DERIVED_LEAN`: [L1-WDP-REALIFICATION-J](L1-WDP-REALIFICATION-J.md) (DEFINITION)
- `L1-R-THM3` `COMPUTED`: [L1-QM020-THM3-ROW-SPARSITY](L1-QM020-THM3-ROW-SPARSITY.md) (COMPUTATIONALLY_CHECKED)
- `L1-R-THM4` `DERIVED_PROSE`: [L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY](L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY.md) (PROVED_PROSE)
- `L1-R-THM6-P2` `CONDITIONAL_ON_IMPORT`: [L1-QM020-THM6-P2-GLEASON](L1-QM020-THM6-P2-GLEASON.md) (IMPORTED_ASSUMPTION)
- `L1-R-U1-GAP` `GAP_NO_DERIVATION`: [L1-IMP-U1-PHASES](L1-IMP-U1-PHASES.md) (IMPORTED_ASSUMPTION)
- `X-R-GAUSS-ALGEBRA-FROM-Z-I` `DERIVED_LEAN`: [GP-FIN-GAUSS-MATRIX-ALGEBRA](GP-FIN-GAUSS-MATRIX-ALGEBRA.md) (PROVED_LEAN)
- `X-R-IMPORTS-TO-DECLARED-INTERFACE` `CONDITIONAL_ON_IMPORT`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)
