# PG-SN-OFF-IMAGE-REFUSAL

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> S(n) off-image refusal closing the domain-restriction half of WDP-P001-019: off-image points fail s(r(y)) = y and are refused by SnOffImage.nonDescent_iff_off_image.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 21
- distinct cited Lean declarations covered by a current replay receipt: 21
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Off-image points are refused because the retraction is sound (accepted only from section images); the old-image law alone does not refuse. Nested terms as base members and the WDP-P001-019 ledger closure remain open.

## Source status

MECHANIZED in SnOffImage.lean (off-image non-descent and section-image characterization) with Rust witness

## Review

- PFP review: [dag/results/PG-SN-OFF-IMAGE-REFUSAL/reviews/20261021_batch01b_audit/delivery_review_result.json](../../../dag/results/PG-SN-OFF-IMAGE-REFUSAL/reviews/20261021_batch01b_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: For a restatement over an arbitrary glyph alphabet of the pinned S(n) section and retraction (five base shapes at a given stage), the retraction refuses exactly the presentations that are not section images at that stage, and the restated pair is a section/retraction pair (law and soundness) in the abstract sense, where refusal is the failure of the round trip s(r(p)) = p; this rests on the soundness of the specific retraction (accepted_only_from_section), because the old-image law alone is satisfied by a retraction that refuses nothing.
  - does not support: The claim that this closes the domain-restriction half of ledger row WDP-P001-019 (a ledger interpretation, not examined); the external prompt file fable_theorems_2026-10-17/05_sn_off_image_refusal.md named in the DAG source list, which was not read; off-image refusal for sections other than the five base shapes (nested lift, retraction or refusal terms as base members are outside the model); any cardinality claim about Carrier n or the declared table (node PG-SN-CARRIER); unrestricted old-image recovery (ledger row WDP-P001-019 stays a negative boundary for the unrestricted interface); the 36-glyph source alphabet beyond the generic statement, and alphabets above three glyphs in the native universes; wire parsing of the source grammar; decidability beyond this syntactic model (the source itself says the image condition is not a general computability theorem); the circular reading in which off-image is defined as failure of the round trip; any physical interpretation.
  - next test: With the bridge sn_is_section_retraction proved, extend the refusal characterisation to a grammar that admits nested lift, retraction and refusal terms as base members: add them to Base, restate sectionLift and retr on the enlarged type, and decide whether accepted_only_from_section and sectionLift injectivity still hold or whether a new off-image class appears.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/OeSn/SnOffImage.lean`

- file: [lean4/Imported/OeSn/SnOffImage.lean](../../../lean4/Imported/OeSn/SnOffImage.lean)
- sha256 (`bytes`): `2f6b3ed0fde0a25ccca9d065300752f7e897f4d4d488e6c6607adb82d236a20f`
- cited in: node.lean, node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mssn_sn.json](../../../dag/research/lean_replay_campaign_mssn_sn.json) (module `Imported.OeSn.SnOffImage`): recorded sha256 `2f6b3ed0fde0a25ccca9d065300752f7e897f4d4d488e6c6607adb82d236a20f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/OeSn/SnOffImage.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `SnOffImage.accepted_only_from_section` | yes | yes | yes | Quot.sound, propext | `#print axioms SnOffImage.accepted_only_from_section` |
| `SnOffImage.nonDescent_iff_off_image` | yes | yes | yes | Quot.sound, propext | `#print axioms SnOffImage.nonDescent_iff_off_image` |
| `SnOffImage.old_image_base'` | yes | yes | yes | propext | `#print axioms SnOffImage.old_image_base'` |

- counts toward the grade: yes

### Lean: `lean4/SnOffImageRefusal.lean`

- file: [lean4/SnOffImageRefusal.lean](../../../lean4/SnOffImageRefusal.lean)
- sha256 (`bytes`): `fd9d0acd0e1a3985cc23bc94ceff041a7e80a5ae6c1845c3d6ff9a252629d972`
- cited in: node.lean, receipt dag/research/pfp_batch01_lean_replay.json (SnOffImageRefusal)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `SnOffImageRefusal`): recorded sha256 `fd9d0acd0e1a3985cc23bc94ceff041a7e80a5ae6c1845c3d6ff9a252629d972` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SnOffImageRefusal`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `SnOffImageRefusal.SectionRetraction.injective` | yes | yes | yes | none | `#print axioms SnOffImageRefusal.SectionRetraction.injective` |
| `SnOffImageRefusal.accepted_iff` | yes | yes | yes | propext | `#print axioms SnOffImageRefusal.accepted_iff` |
| `SnOffImageRefusal.accepted_only_from_section` | yes | yes | yes | propext | `#print axioms SnOffImageRefusal.accepted_only_from_section` |
| `SnOffImageRefusal.inImage_iff` | yes | yes | yes | propext | `#print axioms SnOffImageRefusal.inImage_iff` |
| `SnOffImageRefusal.instance_refusals` | yes | yes | yes | propext | `#print axioms SnOffImageRefusal.instance_refusals` |
| `SnOffImageRefusal.lax_breaks_refusal_characterisation` | yes | yes | yes | propext | `#print axioms SnOffImageRefusal.lax_breaks_refusal_characterisation` |
| `SnOffImageRefusal.lax_retraction_obeys_law_but_accepts_off_image` | yes | yes | yes | propext | `#print axioms SnOffImageRefusal.lax_retraction_obeys_law_but_accepts_off_image` |
| `SnOffImageRefusal.nonDescent_iff_off_image` | yes | yes | yes | propext | `#print axioms SnOffImageRefusal.nonDescent_iff_off_image` |
| `SnOffImageRefusal.old_image_base` | yes | yes | yes | propext | `#print axioms SnOffImageRefusal.old_image_base` |
| `SnOffImageRefusal.refuseOffImage_isSectionRetraction` | yes | yes | yes | propext | `#print axioms SnOffImageRefusal.refuseOffImage_isSectionRetraction` |
| `SnOffImageRefusal.refused_iff_off_image` | yes | yes | yes | none | `#print axioms SnOffImageRefusal.refused_iff_off_image` |
| `SnOffImageRefusal.retraction_stage_strict` | yes | yes | yes | propext | `#print axioms SnOffImageRefusal.retraction_stage_strict` |
| `SnOffImageRefusal.roundtrip_fails_off_image` | yes | yes | yes | none | `#print axioms SnOffImageRefusal.roundtrip_fails_off_image` |
| `SnOffImageRefusal.roundtrip_iff_in_image` | yes | yes | yes | none | `#print axioms SnOffImageRefusal.roundtrip_iff_in_image` |
| `SnOffImageRefusal.sectionLift_injective` | yes | yes | yes | propext | `#print axioms SnOffImageRefusal.sectionLift_injective` |
| `SnOffImageRefusal.sn_is_section_retraction` | yes | yes | yes | propext | `#print axioms SnOffImageRefusal.sn_is_section_retraction` |
| `SnOffImageRefusal.sn_refused_iff_off_image` | yes | yes | yes | propext | `#print axioms SnOffImageRefusal.sn_refused_iff_off_image` |
| `SnOffImageRefusal.toy_refused_iff_odd` | yes | yes | yes | Quot.sound, propext | `#print axioms SnOffImageRefusal.toy_refused_iff_odd` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/01_pregenesis/tfq_0372_off_image_refusal_half.md`

- file: [dag/derivations/01_pregenesis/tfq_0372_off_image_refusal_half.md](../../../dag/derivations/01_pregenesis/tfq_0372_off_image_refusal_half.md)
- sha256 (`lf-normalised`): `1e8abee0e6abe01280b9297401837bbcd5ea1d7e0236c5faaebd0261761eec9d`
- generated view: listed, not counted
- cited in: record TFQ-0372
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0335_from_typed_old_image_recovery_record_injectivity_of_the_lift_only_and_refuse.md`

- file: [dag/derivations/05_mssn_sn/tfq_0335_from_typed_old_image_recovery_record_injectivity_of_the_lift_only_and_refuse.md](../../../dag/derivations/05_mssn_sn/tfq_0335_from_typed_old_image_recovery_record_injectivity_of_the_lift_only_and_refuse.md)
- sha256 (`lf-normalised`): `8f89fd7a8a1e5586b501a9066cb2970205e03f31262fbe69b43061d36ff930a8`
- generated view: listed, not counted
- cited in: record TFQ-0335 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/paper_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/paper_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml`

- file: [sources/atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml](../../../sources/atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml)
- sha256 (`lf-normalised`): `2bfb4441352c4206cbd84f3e500e4c3ba817364aff49623a001087ecf12df5a6`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:prompts/fable_theorems_2026-10-17/05_sn_off_image_refusal.md`

## Absences recorded by the TFQ records

- TFQ-0335 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean
- TFQ-0335 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/code/sn_mssn_checks.py
- TFQ-0372 lean4: missing declaration obligation: off-image non-descent inside this package, not an unread education module
- TFQ-0372 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/SnCarrier.lean
- TFQ-0372 python: missing obligation: an off-image refusal predicate in 000_pre_genesis_to_mssn/code/preservation.py that does not call recover_word a total inverse
- TFQ-0372 rust: missing obligation: section-retraction refusal in crate pre_mssn_preservation for points outside the section image

## Routes

Incoming (1):

- `PG-R-OFF-IMAGE` `DERIVED_LEAN`: [PG-SN-CARRIER](PG-SN-CARRIER.md) (PROVED_LEAN), [PG-OLD-IMAGE-INJECTIVE](PG-OLD-IMAGE-INJECTIVE.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-SN-OFF-IMAGE-REFUSAL-PROPOSAL` `DERIVED_LEAN`: [PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL](PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL.md) (PROVED_LEAN)
