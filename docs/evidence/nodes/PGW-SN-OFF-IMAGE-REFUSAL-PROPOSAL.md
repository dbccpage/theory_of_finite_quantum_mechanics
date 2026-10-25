# PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For the pinned education SnCarrier model, SnOffImage.lean compiles the domain restriction of the S(6) retraction law: retractionDownMap n p = accepted q implies p = sectionLift n b and q = b.toPresentation for some base presentation b (accepted_only_from_section), refusal holds exactly off the section image (nonDescent_iff_off_image), the witness b is unique (sectionLift_injective), a lift at stage m ≠ n is refused by r_n (retraction_stage_strict), and image membership is a Bool test computed from the syntax (inImage_iff). With old_image_base this gives a left inverse on the image and refusal off it. The accompanying note is a proposal with AuthorityEffect None and records a Lean 4.34.0 build whose six axiom lines stay within propext and Quot.sound.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- cited Lean declaration references covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Pinned education SnCarrier model: BasePresentation, sectionLift and retractionDownMap in 002_oesn/lean4/SnCarrier.lean (assumption)

## Bottleneck

A proposal only: ledger row WDP-P001-019 is untouched and TFQ-0372 is not discharged by this record; the corrected cardinality theorem, OB-1, carrierCard, the wire grammar, the Python codec and any stage beyond the five base shapes are outside its scope, and S6Descent checks the separate integer example u(x) = (x,0).

## Source status

002_oesn lean4/SnOffImage.lean and docs/off_image_refusal_note.md (proposal, AuthorityEffect None)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/OeSn/SnOffImage.lean`

- file: [lean4/Imported/OeSn/SnOffImage.lean](../../../lean4/Imported/OeSn/SnOffImage.lean)
- sha256 (`bytes`): `2f6b3ed0fde0a25ccca9d065300752f7e897f4d4d488e6c6607adb82d236a20f`
- cited in: node.lean, node.source, record TFQ-0518
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mssn_sn.json](../../../dag/research/lean_replay_campaign_mssn_sn.json) (module `Imported.OeSn.SnOffImage`): recorded sha256 `2f6b3ed0fde0a25ccca9d065300752f7e897f4d4d488e6c6607adb82d236a20f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/OeSn/SnOffImage.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `accepted_only_from_section` | yes | yes | yes | Quot.sound, propext | `#print axioms accepted_only_from_section` |
| `inImage_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms inImage_iff` |
| `nonDescent_iff_off_image` | yes | yes | yes | Quot.sound, propext | `#print axioms nonDescent_iff_off_image` |
| `retraction_stage_strict` | yes | yes | yes | Quot.sound, propext | `#print axioms retraction_stage_strict` |
| `sectionLift_injective` | yes | yes | yes | propext | `#print axioms sectionLift_injective` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0518_sn_off_image_refusal_proposal.md`

- file: [dag/derivations/05_mssn_sn/tfq_0518_sn_off_image_refusal_proposal.md](../../../dag/derivations/05_mssn_sn/tfq_0518_sn_off_image_refusal_proposal.md)
- sha256 (`lf-normalised`): `52bc1e08eb547dbedc62f5bbd0e96d700bca612508ba38ef66876bf02746605f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0518
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/docs/off_image_refusal_note.md`

- file: `omega_engine_education/documentation/002_oesn/docs/off_image_refusal_note.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_education/documentation/002_oesn/code/sn_core.py::S6Descent`

## Absences recorded by the TFQ records

- TFQ-0518 rust: no Rust implementation of the SnCarrier retraction

## Routes

Incoming (1):

- `PGW-R-SN-OFF-IMAGE-REFUSAL-PROPOSAL` `DERIVED_LEAN`: [PGW-SN5-CONTINUATION-RECORDED-REQUEST](PGW-SN5-CONTINUATION-RECORDED-REQUEST.md) (DEFINITION), [PG-OLD-IMAGE-INJECTIVE](PG-OLD-IMAGE-INJECTIVE.md) (PROVED_LEAN), [PG-SN-OFF-IMAGE-REFUSAL](PG-SN-OFF-IMAGE-REFUSAL.md) (PROVED_LEAN)

Outgoing (4):

- `PGW-R-MSSN-ATLAS-NOT-DERIVATION` `DERIVED_PROSE`: [PGW-MSSN-ATLAS-NOT-DERIVATION](PGW-MSSN-ATLAS-NOT-DERIVATION.md) (DEFINITION)
- `PGW-R-SN-POSTNIKOV-REFUSAL` `DERIVED_PROSE`: [PGW-SN-POSTNIKOV-REFUSAL](PGW-SN-POSTNIKOV-REFUSAL.md) (PROVED_PROSE)
- `PGW-R-SN-PROTECTED-ANSWER-TRANSPORT` `GAP_NO_DERIVATION`: [PGW-SN-PROTECTED-ANSWER-TRANSPORT](PGW-SN-PROTECTED-ANSWER-TRANSPORT.md) (OPEN)
- `PGW-R-SN-REPRESENTATION-QUOTIENT` `DERIVED_LEAN`: [PGW-SN-REPRESENTATION-QUOTIENT](PGW-SN-REPRESENTATION-QUOTIENT.md) (PROVED_LEAN)
