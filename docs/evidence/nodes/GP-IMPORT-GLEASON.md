# GP-IMPORT-GLEASON

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Uniqueness of the Born quadratic form at dimension n \>= 3 needs Gleason-type hypotheses (noncontextuality, sigma-additivity, continuity). On the two-label host the dimension extra already fails; the weaker unit-effect contract has two disagreeing pairings (4 versus 1 on the false-indicator at amplitudes (2,1)).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Gleason hypotheses (noncontextuality, sigma-additivity, continuity): assumption
- dimension \>= 3: assumption

## Bottleneck

Necessity of Gleason uniqueness is OPEN; only rival-readout exclusions (quartic under scale-2 frame additivity) are proved.

## Source status

imported (OracleNeeded firewall, GTOC-8)

## Review

- PFP review: [dag/results/GP-IMPORT-GLEASON/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/GP-IMPORT-GLEASON/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Exact unit-contract rivals and frame quartic obstruction arrays, with general quadratic/quartic frame identities in Lean.
  - does not support: Prove uniqueness only after admitting the full intended Gleason/frame hypotheses and dimension. These counterexamples do not refute Gleason under its hypotheses.
  - next test: Prove uniqueness only after admitting the full intended Gleason/frame hypotheses and dimension. These counterexamples do not refute Gleason under its hypotheses.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1031
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels` |

- counts toward the grade: yes

### Lean: `lean4/H013FrameAdditivity.lean`

- file: [lean4/H013FrameAdditivity.lean](../../../lean4/H013FrameAdditivity.lean)
- sha256 (`bytes`): `626dd1c874e5a1add3f02cb81f5f535c17637c2f55fdffa12a094b1c34f928a8`
- cited in: node.lean, record TFQ-1031
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `H013FrameAdditivity`): recorded sha256 `626dd1c874e5a1add3f02cb81f5f535c17637c2f55fdffa12a094b1c34f928a8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build H013FrameAdditivity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `fourth_power_dies_under_frame_additivity` | yes | yes | yes | propext | `#print axioms fourth_power_dies_under_frame_additivity` |

- counts toward the grade: yes

### Lean: `lean4/H013SameContract.lean`

- file: [lean4/H013SameContract.lean](../../../lean4/H013SameContract.lean)
- sha256 (`bytes`): `47568af5eaa40e031525b641574866c3044176756fb245b6084c96711e8bcca8`
- cited in: node.lean, record TFQ-1031
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `H013SameContract`): recorded sha256 `47568af5eaa40e031525b641574866c3044176756fb245b6084c96711e8bcca8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build H013SameContract`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `two_effect_rules_share_unit_total_and_disagree` | yes | yes | yes | Quot.sound, propext | `#print axioms two_effect_rules_share_unit_total_and_disagree` |

- counts toward the grade: yes

### Lean: `lean4/H017Gleason.lean`

- file: [lean4/H017Gleason.lean](../../../lean4/H017Gleason.lean)
- sha256 (`bytes`): `ceef94bcf70d76a392949b8a9f07a8be3de52fd51f86960f494c3c58bcc95837`
- cited in: node.lean, record TFQ-1031
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `H017Gleason`): recorded sha256 `ceef94bcf70d76a392949b8a9f07a8be3de52fd51f86960f494c3c58bcc95837` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build H017Gleason`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `gleason_pack_uniqueness_still_imported` | yes | yes | yes | none | `#print axioms gleason_pack_uniqueness_still_imported` |
| `two_label_host_not_gleason_dimension` | yes | yes | yes | none | `#print axioms two_label_host_not_gleason_dimension` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1031
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1031_gp_import_gleason.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1031_gp_import_gleason.md](../../../dag/derivations/08_l1_to_l2/tfq_1031_gp_import_gleason.md)
- sha256 (`lf-normalised`): `8595fafb4d5ac5b8f30f0e58366c1bb9f52b1ae1d7decdc3340bcb3e84e06e16`
- generated view: listed, not counted
- cited in: record TFQ-1031
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


Outgoing (1):

- `X-R-DROP-ONE-CENSUS` `DERIVED_LEAN`: [GP-DROP-ONE-CENSUS](GP-DROP-ONE-CENSUS.md) (PROVED_LEAN)

No incoming route.
