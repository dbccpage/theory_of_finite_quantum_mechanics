# PGW-SN-OFF-IMAGE-REFUSAL-PROPOSAL

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For the pinned education SnCarrier model, SnOffImage.lean compiles the domain restriction of the S(6) retraction law: retractionDownMap n p = accepted q implies p = sectionLift n b and q = b.toPresentation for some base presentation b (accepted_only_from_section), refusal holds exactly off the section image (nonDescent_iff_off_image), the witness b is unique (sectionLift_injective), a lift at stage m ≠ n is refused by r_n (retraction_stage_strict), and image membership is a Bool test computed from the syntax (inImage_iff). With old_image_base this gives a left inverse on the image and refusal off it. The accompanying note is a proposal with AuthorityEffect None and records a Lean 4.34.0 build whose six axiom lines stay within propext and Quot.sound.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

- `proved_lean_below_e3`: grade E0; 5 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 5 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

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

### Lean: `omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean`

- file: `omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0518_sn_off_image_refusal_proposal.md`

- file: [dag/derivations/05_mssn_sn/tfq_0518_sn_off_image_refusal_proposal.md](../../../dag/derivations/05_mssn_sn/tfq_0518_sn_off_image_refusal_proposal.md)
- sha256 (`lf-normalised`): `50157678baddd27d90b440cdc24bd31c9030fd007eaeb6403dd3235b80577d1c`
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
- `external:the_symbol_game/omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean::accepted_only_from_section`
- `external:the_symbol_game/omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean::inImage_iff`
- `external:the_symbol_game/omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean::nonDescent_iff_off_image`
- `external:the_symbol_game/omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean::retraction_stage_strict`
- `external:the_symbol_game/omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean::sectionLift_injective`

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
