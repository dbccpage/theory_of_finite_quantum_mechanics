# PG-INERT-DIAMOND

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> \<\> is a literal inscription, supplied or mentioned but carrying no object-language meaning until a separate admission event treats it as a datum. It is NOT defined in the source papers as the root Real_0 = Difference ⊔ Structure. MSS-0 is the stage that admits only \<\>.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 18
- cited Lean declarations covered by a current replay receipt: 18
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/InertDiamond.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

None recorded.

## Bottleneck

The identification '\<\> = Real_0 = Difference join Structure' remains without derivation; the model covers three of six events and its correspondence to admission.rs is by reading.

## Source status

inert, opaque inscription; no object-language meaning (Pre-Genesis paper §1 table; Genesis paper §1)

## Review

- PFP review: [dag/results/PG-INERT-DIAMOND/reviews/20261021_batch01a_audit/delivery_review_result.json](../../../dag/results/PG-INERT-DIAMOND/reviews/20261021_batch01a_audit/delivery_review_result.json); file present and sha256 matches the node's record: no; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `DEFINITION`; qualifies for E4: no.
  - narrowest claim: In a three-event admission model where supply is the identity by stipulation: in the unrooted replay a mention of \<\> (or any token) is invisible to every function of the admitted state; in the rooted replay the first supply of \<\> is an admission precondition and only later supplies are inert; the model predicate HasCoproduct is independent of inscribing \<\> (the identification Real_0 = Difference join Structure is not modelled), and coproduct without inscription occurs only in the unrooted model; inertness is the model rule rather than a consequence of the spelling; verified exhaustively for all traces of length \<= 5.
  - does not support: The identification Real_0 = Difference joined with Structure (it is not modelled; only a stand-in predicate is shown independent of the inscription); the remaining three events of the six-operation alphabet (instance, rule, imposition) and their refusal rules; the Rust partial admission rules beyond the three-event fragment; any claim that supply is inert independently of the stipulated step rule; inertness of the FIRST supply in the rooted replay; any physical or interpretive reading of \<\>.
  - next test: Extend the finite model to the remaining three events of the six-operation alphabet (admit instance, admit rule, impose) with the refusal rules of admission.rs, and prove that supply stays inert and that no supply history forces a coproduct structure on the admitted state.

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
| `QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_root_coproduct_inert_diamond_and_six_operation_separation` |
- counts toward the grade: yes

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/GenesisConstruction.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/GenesisConstruction.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/GenesisConstruction.lean)
- sha256 (`bytes`): `acec76637d43d318ff6f73f77b3162e380d28b7c0ffdd824bd810c3b39818b1b`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.WitnessedDifference.WitnessedDifference.GenesisConstruction`): recorded sha256 `acec76637d43d318ff6f73f77b3162e380d28b7c0ffdd824bd810c3b39818b1b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/GenesisConstruction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `literalRoot` | yes | yes | yes | none | `#print axioms literalRoot` |
- counts toward the grade: yes

### Lean: `lean4/InertDiamond.lean`

- file: [lean4/InertDiamond.lean](../../../lean4/InertDiamond.lean)
- sha256 (`bytes`): `3981d4df4b464251865c5b3553c96467f64024927f11710f0769f1bef4880dd7`
- cited in: receipt dag/research/pfp_batch01_lean_replay.json (InertDiamond)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `InertDiamond`): recorded sha256 `3981d4df4b464251865c5b3553c96467f64024927f11710f0769f1bef4880dd7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build InertDiamond`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `InertDiamond.admit_changes_state` | yes | yes | yes | Quot.sound, propext | `#print axioms InertDiamond.admit_changes_state` |
| `InertDiamond.coproduct_without_inscription` | yes | yes | yes | propext | `#print axioms InertDiamond.coproduct_without_inscription` |
| `InertDiamond.inscription_does_not_determine_coproduct` | yes | yes | yes | propext | `#print axioms InertDiamond.inscription_does_not_determine_coproduct` |
| `InertDiamond.inscription_without_coproduct` | yes | yes | yes | propext | `#print axioms InertDiamond.inscription_without_coproduct` |
| `InertDiamond.mention_count_irrelevant` | yes | yes | yes | propext | `#print axioms InertDiamond.mention_count_irrelevant` |
| `InertDiamond.no_coproduct_of_single_token` | yes | yes | yes | none | `#print axioms InertDiamond.no_coproduct_of_single_token` |
| `InertDiamond.replay_eq_of_same_admissions` | yes | yes | yes | propext | `#print axioms InertDiamond.replay_eq_of_same_admissions` |
| `InertDiamond.replay_filter_supply` | yes | yes | yes | propext | `#print axioms InertDiamond.replay_filter_supply` |
| `InertDiamond.rival_supply_not_inert` | yes | yes | yes | propext | `#print axioms InertDiamond.rival_supply_not_inert` |
| `InertDiamond.root_only_no_coproduct` | yes | yes | yes | propext | `#print axioms InertDiamond.root_only_no_coproduct` |
| `InertDiamond.rooted_later_supply_inert` | yes | yes | yes | propext | `#print axioms InertDiamond.rooted_later_supply_inert` |
| `InertDiamond.rooted_refuses_without_root` | yes | yes | yes | propext | `#print axioms InertDiamond.rooted_refuses_without_root` |
| `InertDiamond.rooted_root_supply_is_precondition` | yes | yes | yes | propext | `#print axioms InertDiamond.rooted_root_supply_is_precondition` |
| `InertDiamond.rooted_with_coproduct` | yes | yes | yes | propext | `#print axioms InertDiamond.rooted_with_coproduct` |
| `InertDiamond.step_changes_only_by_admission` | yes | yes | yes | propext | `#print axioms InertDiamond.step_changes_only_by_admission` |
| `InertDiamond.supply_then_admit_root` | yes | yes | yes | propext | `#print axioms InertDiamond.supply_then_admit_root` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/genesis_construction.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/genesis_construction.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0000_inert_inscription.md`

- file: [dag/derivations/01_pregenesis/tfq_0000_inert_inscription.md](../../../dag/derivations/01_pregenesis/tfq_0000_inert_inscription.md)
- sha256 (`lf-normalised`): `a8b58aa4aaf032cb531aaa6bd3b05397d641cf37a5169865f396dce2de36c094`
- generated view: listed, not counted
- cited in: record TFQ-0000
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0361_inert_literal_inscription.md`

- file: [dag/derivations/01_pregenesis/tfq_0361_inert_literal_inscription.md](../../../dag/derivations/01_pregenesis/tfq_0361_inert_literal_inscription.md)
- sha256 (`lf-normalised`): `887c0eeee0ddac63426e90c068952011c3fd39113353031e8d4a8b911a3f8442`
- generated view: listed, not counted
- cited in: record TFQ-0361
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0362_four_host_conditions.md`

- file: [dag/derivations/01_pregenesis/tfq_0362_four_host_conditions.md](../../../dag/derivations/01_pregenesis/tfq_0362_four_host_conditions.md)
- sha256 (`lf-normalised`): `3ddb9558c2fac39189b3c84e6c1c7844d5338b5a2e1a2e9e0df276ee07ed4340`
- generated view: listed, not counted
- cited in: record TFQ-0362
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0392_inscription_to_coproduct_gap.md`

- file: [dag/derivations/01_pregenesis/tfq_0392_inscription_to_coproduct_gap.md](../../../dag/derivations/01_pregenesis/tfq_0392_inscription_to_coproduct_gap.md)
- sha256 (`lf-normalised`): `12b8df2a8a5beebd90a38c0cd77b219190e4711fa38464adaf8425f12b18300d`
- generated view: listed, not counted
- cited in: record TFQ-0392 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_product_planning_office/architecture_review/06_genesis_native_route.md`

- file: `omega_engine_product_planning_office/architecture_review/06_genesis_native_route.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0361 lean4: missing declaration obligation: a literal inscription type in 000_pre_genesis_to_mssn/lean4/Paper.lean, which was opened and does not declare that token
- TFQ-0361 python: missing obligation: a typed token constructor in 000_pre_genesis_to_mssn/code/preservation.py that stores literal <> without turning it into an empty word or a carrier
- TFQ-0361 rust: missing obligation: a host token in omega_ooutwire_primitives that rejects equating <> with an admitted ground
- TFQ-0361 rust: no local rust twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/token.rs
- TFQ-0362 lean4: missing declaration obligation: a four-constructor host condition in 000_pre_genesis_to_mssn/lean4/Paper.lean matching ledger row WDP-P000-001
- TFQ-0362 python: missing obligation: four-way classifier beside preservation.report_factor for absent payload, empty word, literal <>, and admitted ground
- TFQ-0362 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/preservation.py
- TFQ-0362 rust: missing obligation: an enum in crate pre_mssn_preservation with those four host conditions
- TFQ-0362 rust: no local rust twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/code/rust/src/main.rs
- TFQ-0392 lean4: missing declaration obligation: no arrow in 000_pre_genesis_to_mssn/lean4/Paper.lean from a literal inscription to a coproduct root
- TFQ-0392 python: missing obligation: a negative check that no function in 000_pre_genesis_to_mssn/code/preservation.py sends literal <> to a two-channel coproduct
- TFQ-0392 rust: missing obligation: a refused conversion in omega_ooutwire_primitives from the inscription token to a Difference-Structure value

## Routes

Incoming (0):


Outgoing (5):

- `APP-R-COMP-C1-FIRST-SEPARATION-REPLAY` `COMPUTED`: [COMP-C1-FIRST-SEPARATION-REPLAY](COMP-C1-FIRST-SEPARATION-REPLAY.md) (COMPUTATIONALLY_CHECKED)
- `PG-R-DIAMOND-TO-MSS0` `DERIVED_LEAN`: [PG-MSS0-ONLY-DIAMOND](PG-MSS0-ONLY-DIAMOND.md) (DEFINITION)
- `PG-R-GAP-DIAMOND-TO-ROOT` `GAP_NO_DERIVATION`: [PG-ROOT-DIFF-STRUCTURE](PG-ROOT-DIFF-STRUCTURE.md) (ADMITTED_PRIMITIVE)
- `PGW-R-OBSERVATIONAL-EQUIVALENCE` `DERIVED_PROSE`: [PGW-OBSERVATIONAL-EQUIVALENCE](PGW-OBSERVATIONAL-EQUIVALENCE.md) (DEFINITION)
- `PGW-R-PREGENESIS-GRAMMAR` `DERIVED_PROSE`: [PGW-PREGENESIS-GRAMMAR](PGW-PREGENESIS-GRAMMAR.md) (DEFINITION)

No incoming route.
