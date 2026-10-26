# PG-SN-CARRIER

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a Lean restatement of the pinned restricted S(n) model over any glyph alphabet G, the section lift of base presentations is injective with the retraction as left inverse at every stage (old-image law), and its image has 1 + g + 3 g^2 points; the unrestricted lift of SnCarrierDischarge is not injective, admits no recovery and sends the refusal token to the ground presentation, which is the interface to which the WDP-P001-019 defects belong; the advertised carrierCard table is a declaration that is not derived from the model and differs from the stage-independent base total at stages 0, 2, 3 for every g (and at stage 1 unless g = 0); the index-zero carrier is empty by declaration.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 20
- distinct cited Lean declarations covered by a current replay receipt: 20
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Classical.choice in old_image_base (assumption: found in axiom report, against the Fable 05 expectation)

## Bottleneck

A corrected cardinality theorem deriving Carrier n from the lift image or the stage-n shape set (the stage of the directed cut must be settled by the source), off-image refusal completeness (PG-SN-OFF-IMAGE-REFUSAL), and identification of the restatement with the pinned types at G = Glyph; the source old_image_base still reports Classical.choice.

## Source status

Pre-Genesis §10 / SnCarrier base presentation, section lift, retraction outcome; ground carrier empty

## Review

- PFP review: [dag/results/PG-SN-CARRIER/reviews/20261021_batch01a_audit/delivery_review_result.json](../../../dag/results/PG-SN-CARRIER/reviews/20261021_batch01a_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: For a Lean restatement of the pinned restricted S(n) model (SnCarrier.lean sha 357376de..., glyph alphabet abstracted, wrappers flattened), the base-presentation lift is injective with a left-inverse retraction at every stage and its image has 1+g+3g^2 points; the unrestricted lift has no recovery; the declared carrier table differs from the stage-independent base total 1+g+3g^2 at stages 0, 2 and 3 for every g (and at stage 1 unless g = 0), and no alphabet matches the per-shape counts g and g^2 at stages 1 and 2 together; the table is a declaration, not derived from the model.
  - does not support: A corrected cardinality theorem for the S(n) carriers: the table carrierCard remains a declared definition with no theorem relating Carrier n to the base presentations or the lift; off-image refusal completeness (node PG-SN-OFF-IMAGE-REFUSAL); nested lift, retraction or refusal terms as members of the base type; any theorem identifying the restatement with the pinned types at G = Glyph (36 letters and digits), and per-stage shape-count or cumulative-count statements in Lean (native-only); the real 36-glyph syntax beyond the instance baseCard 36 = 3925 and alphabets above six glyphs in the native certificate; wire parsing and the Python/Lean correspondence of the source; the locally defined UnrepairedCarrier of SnCarrierDischarge (a different type from Carrier); any physical, categorical or adjunction reading, including the string metadata of the custody-successor file mssn_functor_bridge.rs.
  - next test: State and prove a corrected cardinality theorem: define Carrier n from the lift image or the stage-n shape set over the 36-glyph alphabet, prove its cardinality for n = 0..3 including the ground token, and decide whether carrierCard equals that derived function or must be replaced by it.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/PreGenesisToMssn/SnCarrier.lean`

- file: [lean4/Imported/PreGenesisToMssn/SnCarrier.lean](../../../lean4/Imported/PreGenesisToMssn/SnCarrier.lean)
- sha256 (`bytes`): `73a91689993eeefb0a501d4dbb23942ac14bb243f05e65fe2b16d78ba207fb4c`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mssn_sn.json](../../../dag/research/lean_replay_campaign_mssn_sn.json) (module `Imported.PreGenesisToMssn.SnCarrier`): recorded sha256 `73a91689993eeefb0a501d4dbb23942ac14bb243f05e65fe2b16d78ba207fb4c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/PreGenesisToMssn/SnCarrier.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BasePresentation` | yes | yes | yes | none | `#print axioms BasePresentation` |
| `RetractOutcome` | yes | yes | yes | none | `#print axioms RetractOutcome` |
| `retractionDownMap` | yes | yes | yes | propext | `#print axioms retractionDownMap` |
| `sectionLift` | yes | yes | yes | none | `#print axioms sectionLift` |

- counts toward the grade: yes

### Lean: `lean4/Imported/PreGenesisToMssn/SnTheorems.lean`

- file: [lean4/Imported/PreGenesisToMssn/SnTheorems.lean](../../../lean4/Imported/PreGenesisToMssn/SnTheorems.lean)
- sha256 (`bytes`): `0b3a26d57be1ddc3d5d808f1d2c6aaabf5ca45822d04e85dc0e51e072e5b1244`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mssn_sn.json](../../../dag/research/lean_replay_campaign_mssn_sn.json) (module `Imported.PreGenesisToMssn.SnTheorems`): recorded sha256 `0b3a26d57be1ddc3d5d808f1d2c6aaabf5ca45822d04e85dc0e51e072e5b1244` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/PreGenesisToMssn/SnTheorems.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ground_carrier_empty` | yes | yes | yes | none | `#print axioms ground_carrier_empty` |
| `old_image_base` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms old_image_base` |

- counts toward the grade: yes

### Lean: `lean4/SnCarrierPfp.lean`

- file: [lean4/SnCarrierPfp.lean](../../../lean4/SnCarrierPfp.lean)
- sha256 (`bytes`): `f55efb45cdedf884efc81d7dd16fd0f2f8bf04fc5e44b2d41f0b2fc36762ec2f`
- cited in: node.lean, receipt dag/research/pfp_batch01_lean_replay.json (SnCarrierPfp)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `SnCarrierPfp`): recorded sha256 `f55efb45cdedf884efc81d7dd16fd0f2f8bf04fc5e44b2d41f0b2fc36762ec2f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SnCarrierPfp`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `SnCarrierPfp.baseCard_36` | yes | yes | yes | propext | `#print axioms SnCarrierPfp.baseCard_36` |
| `SnCarrierPfp.card_base` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms SnCarrierPfp.card_base` |
| `SnCarrierPfp.card_image_sectionLift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms SnCarrierPfp.card_image_sectionLift` |
| `SnCarrierPfp.ground_carrier_empty` | yes | yes | yes | none | `#print axioms SnCarrierPfp.ground_carrier_empty` |
| `SnCarrierPfp.no_alphabet_matches_stages_one_two` | yes | yes | yes | Quot.sound, propext | `#print axioms SnCarrierPfp.no_alphabet_matches_stages_one_two` |
| `SnCarrierPfp.no_recovery_for_unrestricted_lift` | yes | yes | yes | propext | `#print axioms SnCarrierPfp.no_recovery_for_unrestricted_lift` |
| `SnCarrierPfp.old_image_base` | yes | yes | yes | propext | `#print axioms SnCarrierPfp.old_image_base` |
| `SnCarrierPfp.refusal_token_round_trip_changes_input` | yes | yes | yes | propext | `#print axioms SnCarrierPfp.refusal_token_round_trip_changes_input` |
| `SnCarrierPfp.sectionLift_injective` | yes | yes | yes | propext | `#print axioms SnCarrierPfp.sectionLift_injective` |
| `SnCarrierPfp.table_eq_base_stage_one_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms SnCarrierPfp.table_eq_base_stage_one_iff` |
| `SnCarrierPfp.table_ne_base_stage_three` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms SnCarrierPfp.table_ne_base_stage_three` |
| `SnCarrierPfp.table_ne_base_stage_two` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms SnCarrierPfp.table_ne_base_stage_two` |
| `SnCarrierPfp.table_ne_base_stage_zero` | yes | yes | yes | Quot.sound, propext | `#print axioms SnCarrierPfp.table_ne_base_stage_zero` |
| `SnCarrierPfp.unrestricted_lift_not_injective` | yes | yes | yes | propext | `#print axioms SnCarrierPfp.unrestricted_lift_not_injective` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_category_theory/src/mssn_functor_bridge.rs`

- file: `omega_engine/crates_rs/omega_category_theory/src/mssn_functor_bridge.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md`

- file: [atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md](../../../atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md)
- sha256 (`lf-normalised`): `a4a7d840b11e912896032aebc9ead95f7978c0e6f60656f44645c6d8fadf593b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/paper_claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/paper_claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/paper_claim_ledger.md)
- sha256 (`lf-normalised`): `ca7ad135453d393688ceadf73eb214ccc6976589928f1dc43597e287bbfc6209`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0341_refuse_unrestricted_old_image_recovery_and_the_advertised_sncarrier_cardinalities_until_a.md`

- file: [dag/derivations/05_mssn_sn/tfq_0341_refuse_unrestricted_old_image_recovery_and_the_advertised_sncarrier_cardinalities_until_a.md](../../../dag/derivations/05_mssn_sn/tfq_0341_refuse_unrestricted_old_image_recovery_and_the_advertised_sncarrier_cardinalities_until_a.md)
- sha256 (`lf-normalised`): `6f37257bee7116f7d7250d17ad1ab3fa9cb817fb85a90fc92afd9648cf5a5788`
- generated view: listed, not counted
- cited in: record TFQ-0341
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0342_do_not_treat_genesis_events_or_s_n_maps_as_obligation_monoid_morphisms_until.md`

- file: [dag/derivations/05_mssn_sn/tfq_0342_do_not_treat_genesis_events_or_s_n_maps_as_obligation_monoid_morphisms_until.md](../../../dag/derivations/05_mssn_sn/tfq_0342_do_not_treat_genesis_events_or_s_n_maps_as_obligation_monoid_morphisms_until.md)
- sha256 (`lf-normalised`): `3c5506026eeada78ccc327f0bd2ee297d044bb4e3c6fc875975ee080d25bacb1`
- generated view: listed, not counted
- cited in: record TFQ-0342 (shared)
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0341 lean4: no local lean twin located for atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/lean4/SnCarrierDischarge.lean
- TFQ-0341 python: no local python twin located for atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/code/sn_mssn_checks.py
- TFQ-0342 rust: no local rust twin located for omega_engine/crates_rs/omega_kernel/src/obligation.rs

## Routes

Incoming (1):

- `PG-R-SN-CARRIER` `DERIVED_LEAN`: [PG-OLD-IMAGE-INJECTIVE](PG-OLD-IMAGE-INJECTIVE.md) (PROVED_LEAN)

Outgoing (4):

- `PG-R-GAP-EVENT-OBLIGATION` `DERIVED_LEAN`: [PG-OBLIGATION-MONOID](PG-OBLIGATION-MONOID.md) (PROVED_LEAN)
- `PG-R-GENESIS-TO-WDP` `GAP_NO_DERIVATION`: [PG-WDP-GENESIS-BRIDGE-OBLIGATIONS](PG-WDP-GENESIS-BRIDGE-OBLIGATIONS.md) (OPEN)
- `PG-R-MONOID-NONISO` `DERIVED_LEAN`: [PG-FREE-MONOID-NONISO](PG-FREE-MONOID-NONISO.md) (PROVED_LEAN)
- `PG-R-OFF-IMAGE` `DERIVED_LEAN`: [PG-SN-OFF-IMAGE-REFUSAL](PG-SN-OFF-IMAGE-REFUSAL.md) (PROVED_LEAN)
