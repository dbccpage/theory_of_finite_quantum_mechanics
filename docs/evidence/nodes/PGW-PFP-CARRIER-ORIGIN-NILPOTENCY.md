# PGW-PFP-CARRIER-ORIGIN-NILPOTENCY

Stage: [IMPLEMENTATION](../stages/IMPLEMENTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> CarrierOrigin.lean (namespace SymbolGame.V02) establishes two small facts about its own declarations. no_difference_without_distinguishability: a Simplex1 V carries a proof that its source and target differ, so when src = tgt no 1-simplex with those endpoints exists. nilpotency_composition: for d₀ : α → β and d₁ : β → γ with a zero on γ and the hypothesis ∀ x, d₁ (d₀ x) = 0, the composite vanishes at every 0-cochain a; the proof applies the hypothesis to a. The file has no imports and elaborates under Lean 4.33.1 with no sorry.

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

- `proved_lean_below_e3`: grade E0; 2 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 2 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

None recorded.

## Bottleneck

nilpotency_composition restates its hypothesis and establishes d₁ ∘ d₀ = 0 for no complex; the ProtoSupport obligations and the trilemma classification in the same file are declarations with no theorem about them.

## Source status

004_oepfp lean4/CarrierOrigin.lean lines 55-79; elaborated with Lean 4.33.1, no sorry

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_education/documentation/004_oepfp/lean4/CarrierOrigin.lean`

- file: `omega_engine_education/documentation/004_oepfp/lean4/CarrierOrigin.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/04_authorization/tfq_0507_pfp_carrier_origin_nilpotency.md`

- file: [dag/derivations/04_authorization/tfq_0507_pfp_carrier_origin_nilpotency.md](../../../dag/derivations/04_authorization/tfq_0507_pfp_carrier_origin_nilpotency.md)
- sha256 (`lf-normalised`): `8e2c096e881be934b34cdf2704d71d570c2a46940b81152f064f3153980d0e37`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0507
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_education/documentation/004_oepfp/lean4/CarrierOrigin.lean::nilpotency_composition`
- `external:the_symbol_game/omega_engine_education/documentation/004_oepfp/lean4/CarrierOrigin.lean::no_difference_without_distinguishability`

## Absences recorded by the TFQ records

- TFQ-0507 python: no Python counterpart of CarrierOrigin.lean
- TFQ-0507 rust: no Rust counterpart of CarrierOrigin.lean

## Routes

Incoming (1):

- `PGW-R-PFP-CARRIER-ORIGIN-NILPOTENCY` `DERIVED_LEAN`: [TFQ-0506](TFQ-0506.md) (DEFINITION)

Outgoing (1):

- `UDG-R-TFQ-0508` `DERIVED_PROSE`: [TFQ-0508](TFQ-0508.md) (DEFINITION)
