# L1-QM122-BORN-PAIRING-NONUNIQUE

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact quadratic/quartic/swapped atom values, honest normalization contracts and Gaussian Hadamard/rotated frame countercontrols; literal unit and frame identities in Lean.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- cited Lean declaration references covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Gleason: assumption

## Bottleneck

Unmet after the PFP review: Formalize full source pairing refinement and the additional frame/POVM/Gleason uniqueness hypotheses. These rivals share only their stated weak contracts. The broader source statement is kept in pfp_review.prior_statement.

## Source status

H013BornPairingBoundary: Candidate only. Not PROVEN. Kind: IMPORT BOUNDARY (file header)

## Review

- PFP review: [dag/results/L1-QM122-BORN-PAIRING-NONUNIQUE/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM122-BORN-PAIRING-NONUNIQUE/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact quadratic/quartic/swapped atom values, honest normalization contracts and Gaussian Hadamard/rotated frame countercontrols; literal unit and frame identities in Lean.
  - does not support: Formalize full source pairing refinement and the additional frame/POVM/Gleason uniqueness hypotheses. These rivals share only their stated weak contracts.
  - next test: Formalize full source pairing refinement and the additional frame/POVM/Gleason uniqueness hypotheses. These rivals share only their stated weak contracts.

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

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: record TFQ-0306
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`
- counts toward the grade: yes

### Lean: `lean4/H013BornPairingBoundary.lean`

- file: [lean4/H013BornPairingBoundary.lean](../../../lean4/H013BornPairingBoundary.lean)
- sha256 (`bytes`): `debafe0eefb016e289a18fb9a308224f73464282e15c17eef143e5ea5342b642`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `H013BornPairingBoundary`): recorded sha256 `debafe0eefb016e289a18fb9a308224f73464282e15c17eef143e5ea5342b642` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build H013BornPairingBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `born_nonuniqueness_open` | yes | yes | yes | none | `#print axioms born_nonuniqueness_open` |
| `pairing_exists` | yes | yes | yes | propext | `#print axioms pairing_exists` |
| `quartic_rival` | yes | yes | yes | propext | `#print axioms quartic_rival` |
| `uniqueness_not_discharged` | yes | yes | yes | none | `#print axioms uniqueness_not_discharged` |

- counts toward the grade: yes

### Lean: `lean4/H017Gleason.lean`

- file: [lean4/H017Gleason.lean](../../../lean4/H017Gleason.lean)
- sha256 (`bytes`): `ceef94bcf70d76a392949b8a9f07a8be3de52fd51f86960f494c3c58bcc95837`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `H017Gleason`): recorded sha256 `ceef94bcf70d76a392949b8a9f07a8be3de52fd51f86960f494c3c58bcc95837` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build H017Gleason`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `two_label_host_not_gleason_dimension` | yes | yes | yes | none | `#print axioms two_label_host_not_gleason_dimension` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/pairing_audit.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/pairing_audit.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0306_born_uniqueness_stays_an_imported_boundary.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0306_born_uniqueness_stays_an_imported_boundary.md](../../../dag/derivations/08_l1_to_l2/tfq_0306_born_uniqueness_stays_an_imported_boundary.md)
- sha256 (`lf-normalised`): `5f67f96080dc9f7fd4e9d5d0b275beec16cb1b7014ee22bc301ea09a07687cdb`
- generated view: listed, not counted
- cited in: record TFQ-0306
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

- TFQ-0306 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_state.rs
- TFQ-0312 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_122/qm122_lib/qm122_dual.py

## Routes

Incoming (1):

- `L1-R-BORN-PAIRING-BOUNDARY` `DERIVED_LEAN`: [L1-QM020-THM6-P1-SCOPE-FENCE](L1-QM020-THM6-P1-SCOPE-FENCE.md) (PROVED_LEAN), [L1-IMP-ORTHOGONAL-ADDITIVITY](L1-IMP-ORTHOGONAL-ADDITIVITY.md) (CONDITIONAL)

Outgoing (1):

- `L1-R-MNC-LEFTOVER` `DERIVED_LEAN`: [L1-QM122-LEFTOVER-MNC-NOT-RECOVERED](L1-QM122-LEFTOVER-MNC-NOT-RECOVERED.md) (PROVED_LEAN)
