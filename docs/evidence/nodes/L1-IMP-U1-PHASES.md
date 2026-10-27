# L1-IMP-U1-PHASES

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> U(1) phases (unit complex numbers) act on sector amplitudes. QM_122 shows a sign carrier suffices for some finite tasks and that excluding it needs an extra non-exponent-two condition. The selector for C / U(1) belongs to QM_028 / QM_062 (another segment).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- circle group U(1): assumption

## Bottleneck

See L1-U1-SELECTOR-OTHER-SEGMENT.

## Source status

QM_122 H011: circle selector boundary; sign group excluded only under 'not of exponent two'; circle stays imported

## Review

- PFP review: [dag/results/L1-IMP-U1-PHASES/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-IMP-U1-PHASES/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Full relative-phase readouts and common-phase invariance, with generic interference identities and the two sign controls in Lean.
  - does not support: Supply a justified circle selector, continuity and source representation bridge. A finite subgroup or one rational unit phase is not U(1) selection.
  - next test: Supply a justified circle selector, continuity and source representation bridge. A finite subgroup or one rational unit phase is not U(1) selection.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` |

- counts toward the grade: yes

### Lean: `lean4/HilbertWalkCircle.lean`

- file: [lean4/HilbertWalkCircle.lean](../../../lean4/HilbertWalkCircle.lean)
- sha256 (`bytes`): `c3326f87aa656cbec551fc23ecf89675379ae738888b497b8ecc3c748093acfa`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `HilbertWalkCircle`): recorded sha256 `c3326f87aa656cbec551fc23ecf89675379ae738888b497b8ecc3c748093acfa` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build HilbertWalkCircle`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `sign_excluded_circle_still_imported` | yes | yes | yes | propext | `#print axioms sign_excluded_circle_still_imported` |

- counts toward the grade: yes

### Lean: `lean4/U1SelectorBoundary.lean`

- file: [lean4/U1SelectorBoundary.lean](../../../lean4/U1SelectorBoundary.lean)
- sha256 (`bytes`): `003d1730941ba102f39cdd82a0f647131050d93ef99d3e532c49e2a873a2376a`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `U1SelectorBoundary`): recorded sha256 `003d1730941ba102f39cdd82a0f647131050d93ef99d3e532c49e2a873a2376a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build U1SelectorBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `selector_not_free` | yes | yes | yes | none | `#print axioms selector_not_free` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0294_circle_phases_as_an_imported_unit_group.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0294_circle_phases_as_an_imported_unit_group.md](../../../dag/derivations/08_l1_to_l2/tfq_0294_circle_phases_as_an_imported_unit_group.md)
- sha256 (`lf-normalised`): `9c76c771cb03a3bf6146900e6299b36965daaccf2675e868e966af303a9657a5`
- generated view: listed, not counted
- cited in: record TFQ-0294 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/14_finite_gauge/tfq_0053_each_language_must_carry_a_unit_gaussian_edge_connection_covariant_difference_vertex.md`

- file: [dag/derivations/14_finite_gauge/tfq_0053_each_language_must_carry_a_unit_gaussian_edge_connection_covariant_difference_vertex.md](../../../dag/derivations/14_finite_gauge/tfq_0053_each_language_must_carry_a_unit_gaussian_edge_connection_covariant_difference_vertex.md)
- sha256 (`lf-normalised`): `3b89d84355253adb91b6cab1ff8de82e84c48bea6adc7e49603890463649038b`
- generated view: listed, not counted
- cited in: record TFQ-0053 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/14_finite_gauge/tfq_0055_each_language_must_carry_no_rational_homomorphism_supplies_the_missing_square_root.md`

- file: [dag/derivations/14_finite_gauge/tfq_0055_each_language_must_carry_no_rational_homomorphism_supplies_the_missing_square_root.md](../../../dag/derivations/14_finite_gauge/tfq_0055_each_language_must_carry_no_rational_homomorphism_supplies_the_missing_square_root.md)
- sha256 (`lf-normalised`): `8555f29d93d2a5613dab291139edc56748d7d471012998854a1a6f49e74f1cbb`
- generated view: listed, not counted
- cited in: record TFQ-0055 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- `external:sha256:86710ba8ef7db719a42a2165e71d3bc72ac5db63d0b2a51e57f48f14e137754e`
- `external:sha256:a2c0d7450948662c89ffb80f0ebcfa02f1f013179a207d3d24db3421e81e84c6::UnitPhaseGroup`
- `external:sha256:ddaee3d0d77722244a6451750ca1e5acf7a57b4f02e75ecec70e810976d57d9e`

## Absences recorded by the TFQ records

- TFQ-0053 lean4: not located
- TFQ-0053 python: not located
- TFQ-0053 rust: no local rust twin located for external:sha256:c2b85e3d42e7b05c158b418cbf2a803bdc86262cde384177ac8264c9c67ef6fe
- TFQ-0055 lean4: not located
- TFQ-0055 python: not located
- TFQ-0055 rust: no local rust twin located for external:sha256:e86ad3309b090c78f09e92fa9833a87b325a0513396663cbf2bd5c2ea1fd0c7b
- TFQ-0294 rust: no local rust twin located for external:sha256:726fa8afa05803e040d092cf665b4a775fb5f3626f1631071aac9763510e15d5
- TFQ-0294 rust: no local rust twin located for external:sha256:a2c0d7450948662c89ffb80f0ebcfa02f1f013179a207d3d24db3421e81e84c6
- TFQ-0294 rust: no local rust twin located for external:sha256:ddaee3d0d77722244a6451750ca1e5acf7a57b4f02e75ecec70e810976d57d9e

## Routes

Incoming (1):

- `L1-R-U1-GAP` `GAP_NO_DERIVATION`: [L1-IMP-COMPLEX-FIELD](L1-IMP-COMPLEX-FIELD.md) (CONDITIONAL)

Outgoing (6):

- `L1-R-CIRCLE-BOUNDARY` `COMPUTED`: [L1-QM122-CIRCLE-SELECTOR-BOUNDARY](L1-QM122-CIRCLE-SELECTOR-BOUNDARY.md) (COMPUTATIONALLY_CHECKED)
- `L1-R-HAAR-GAP` `GAP_NO_DERIVATION`: [L1-IMP-HAAR-INDEPENDENT-PHASES](L1-IMP-HAAR-INDEPENDENT-PHASES.md) (IMPORTED_ASSUMPTION)
- `L1-R-PHASE-BLIND-INTERFERENCE` `DERIVED_LEAN`: [L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE](L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE.md) (PROVED_LEAN)
- `L1-R-THM3` `COMPUTED`: [L1-QM020-THM3-ROW-SPARSITY](L1-QM020-THM3-ROW-SPARSITY.md) (COMPUTATIONALLY_CHECKED)
- `L1-R-THM4` `DERIVED_PROSE`: [L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY](L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY.md) (PROVED_PROSE)
- `X-R-IMPORTS-TO-DECLARED-INTERFACE` `CONDITIONAL_ON_IMPORT`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)
