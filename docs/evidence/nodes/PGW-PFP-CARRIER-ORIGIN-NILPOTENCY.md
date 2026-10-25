# PGW-PFP-CARRIER-ORIGIN-NILPOTENCY

Stage: [IMPLEMENTATION](../stages/IMPLEMENTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> CarrierOrigin.lean (namespace SymbolGame.V02) establishes two small facts about its own declarations. no_difference_without_distinguishability: a Simplex1 V carries a proof that its source and target differ, so when src = tgt no 1-simplex with those endpoints exists. nilpotency_composition: for d₀ : α → β and d₁ : β → γ with a zero on γ and the hypothesis ∀ x, d₁ (d₀ x) = 0, the composite vanishes at every 0-cochain a; the proof applies the hypothesis to a. The file has no imports and elaborates under Lean 4.33.1 with no sorry.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declaration references covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

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

### Lean: `lean4/Imported/OePfp/CarrierOrigin.lean`

- file: [lean4/Imported/OePfp/CarrierOrigin.lean](../../../lean4/Imported/OePfp/CarrierOrigin.lean)
- sha256 (`bytes`): `bab619832676544fc9cef04b2bfe975dd91a5b450ca1eb112ac82afd9e2e1f34`
- cited in: node.lean, node.source, record TFQ-0507
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_implementation.json](../../../dag/research/lean_replay_campaign_implementation.json) (module `Imported.OePfp.CarrierOrigin`): recorded sha256 `bab619832676544fc9cef04b2bfe975dd91a5b450ca1eb112ac82afd9e2e1f34` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/OePfp/CarrierOrigin.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `nilpotency_composition` | yes | yes | yes | none | `#print axioms nilpotency_composition` |
| `no_difference_without_distinguishability` | yes | yes | yes | none | `#print axioms no_difference_without_distinguishability` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/04_authorization/tfq_0507_pfp_carrier_origin_nilpotency.md`

- file: [dag/derivations/04_authorization/tfq_0507_pfp_carrier_origin_nilpotency.md](../../../dag/derivations/04_authorization/tfq_0507_pfp_carrier_origin_nilpotency.md)
- sha256 (`lf-normalised`): `3c5d2acd65ff35864436395713f00c8c8e0126425e7497f978fbf95ebf2663f1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0507
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0507 python: no Python counterpart of CarrierOrigin.lean
- TFQ-0507 rust: no Rust counterpart of CarrierOrigin.lean

## Routes

Incoming (1):

- `PGW-R-PFP-CARRIER-ORIGIN-NILPOTENCY` `DERIVED_LEAN`: [TFQ-0506](TFQ-0506.md) (DEFINITION)

Outgoing (1):

- `UDG-R-TFQ-0508` `DERIVED_PROSE`: [TFQ-0508](TFQ-0508.md) (DEFINITION)
