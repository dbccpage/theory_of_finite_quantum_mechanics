# L1-QM122-CIRCLE-SELECTOR-BOUNDARY

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Actual cyclic regular-representation shift/square matrices and group-order controls, plus finite modular alternatives in Lean.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- circle group: assumption

## Bottleneck

Unmet after the PFP review: Provide genuine topological connectedness, selector uniqueness and source refinement. A Boolean selector pack or finite shadow cannot discharge U(1). The broader source statement is kept in pfp_review.prior_statement.

## Source status

H011U1SelectorBoundary / H011Circle; headers: candidate; sign group excluded only under 'not of exponent two'

## Review

- PFP review: [dag/results/L1-QM122-CIRCLE-SELECTOR-BOUNDARY/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM122-CIRCLE-SELECTOR-BOUNDARY/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: no; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Actual cyclic regular-representation shift/square matrices and group-order controls, plus finite modular alternatives in Lean.
  - does not support: Provide genuine topological connectedness, selector uniqueness and source refinement. A Boolean selector pack or finite shadow cannot discharge U(1).
  - next test: Provide genuine topological connectedness, selector uniqueness and source refinement. A Boolean selector pack or finite shadow cannot discharge U(1).

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
| `QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition` |
- counts toward the grade: yes

### Lean: `lean4/H011Circle.lean`

- file: [lean4/H011Circle.lean](../../../lean4/H011Circle.lean)
- sha256 (`bytes`): `6934713287756fd23f2f44a6bab2ed6ee50fbb128f99db492f926c839ff86d9b`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `H011Circle`): recorded sha256 `6934713287756fd23f2f44a6bab2ed6ee50fbb128f99db492f926c839ff86d9b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build H011Circle`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `sign_excluded_circle_still_imported` | yes | yes | yes | propext | `#print axioms sign_excluded_circle_still_imported` |
| `sign_fails_connectedness_shadow` | yes | yes | yes | none | `#print axioms sign_fails_connectedness_shadow` |
- counts toward the grade: yes

### Lean: `lean4/H011U1SelectorBoundary.lean`

- file: [lean4/H011U1SelectorBoundary.lean](../../../lean4/H011U1SelectorBoundary.lean)
- sha256 (`bytes`): `214f187afdfc0ee196021aa3ce2ab96875b1c13de9b3a560ef1eaf0359622912`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `H011U1SelectorBoundary`): recorded sha256 `214f187afdfc0ee196021aa3ce2ab96875b1c13de9b3a560ef1eaf0359622912` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build H011U1SelectorBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `selector_not_free` | yes | yes | yes | none | `#print axioms selector_not_free` |
| `u1_selector_boundary` | yes | yes | yes | none | `#print axioms u1_selector_boundary` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/complex_structure_selector.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/complex_structure_selector.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/09_finite_hilbert/tfq_0312_four_necessity_verdicts_stay_open_beside_the_matrix_gap.md`

- file: [dag/derivations/09_finite_hilbert/tfq_0312_four_necessity_verdicts_stay_open_beside_the_matrix_gap.md](../../../dag/derivations/09_finite_hilbert/tfq_0312_four_necessity_verdicts_stay_open_beside_the_matrix_gap.md)
- sha256 (`lf-normalised`): `d82577d360b53ddbc9db6555e6d2846e0dff1202830f9b927f60534c64eb562d`
- generated view: listed, not counted
- cited in: record TFQ-0312 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/qm_122_finite_hilbert_boundary_from_primitive_difference_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/qm_122_finite_hilbert_boundary_from_primitive_difference_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0312 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_122/qm122_lib/qm122_dual.py

## Routes

Incoming (1):

- `L1-R-CIRCLE-BOUNDARY` `DERIVED_LEAN`: [L1-IMP-U1-PHASES](L1-IMP-U1-PHASES.md) (IMPORTED_ASSUMPTION)

Outgoing (3):

- `L1-R-MNC-LEFTOVER` `DERIVED_LEAN`: [L1-QM122-LEFTOVER-MNC-NOT-RECOVERED](L1-QM122-LEFTOVER-MNC-NOT-RECOVERED.md) (PROVED_LEAN)
- `L1-R-U1-SELECTOR` `GAP_NO_DERIVATION`: [L1-U1-SELECTOR-OTHER-SEGMENT](L1-U1-SELECTOR-OTHER-SEGMENT.md) (OPEN)
- `UDG-R-TFQ-0313` `GAP_NO_DERIVATION`: [TFQ-0313](TFQ-0313.md) (OPEN)
