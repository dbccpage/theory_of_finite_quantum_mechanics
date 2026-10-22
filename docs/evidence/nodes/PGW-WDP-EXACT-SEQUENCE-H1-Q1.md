# PGW-WDP-EXACT-SEQUENCE-H1-Q1

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH04-P03: in a window with d₁d₀ = 0, κ¹(\[h\]) = d₁h is well defined on Q¹ because d₁(h + d₀α) = d₁h + d₁d₀α = d₁h, and 0 → H¹ → Q¹ → im d₁ → 0 is exact with H¹ = ker κ¹; closedness of a class does not depend on the representative, so H¹ is the usual Z¹/B¹ of the window. The sequence is an extension: in finite dimension it splits, but a splitting Q¹ ≅ H¹ ⊕ im d₁ requires a chosen section and is not canonical. Lean kappa_exact_sequence, with kappa_well_defined and kappa_mk, establishes on the literal quotient Quot (Repair d₀), for an additive d₁ with d₁ ∘ d₀ = 0, that the inclusion of H¹ is injective, its image is the kernel of κ, a class has zero charge exactly when every representative is closed, and κ maps onto the image of d₁; these three declarations use no axioms.

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

- `proved_lean_below_e3`: grade E0; 3 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 3 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

- Declared window with additive d₁ and a d₁d₀ = 0 certificate (assumption)

## Bottleneck

The Lean statement is narrower than the row: set-level exactness on the literal quotient, without additive structure on Q¹, additivity of κ¹ or the splitting remark; it takes the window as declared and is not a Genesis derivation of it (TFQ-0344).

## Source status

WDP monograph §4.8 WDP-CH04-P03; Lean Obstruction.kappa_exact_sequence (narrower set-level statement)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0546_wdp_exact_sequence_h1_q1.md`

- file: [dag/derivations/06_wdp/tfq_0546_wdp_exact_sequence_h1_q1.md](../../../dag/derivations/06_wdp/tfq_0546_wdp_exact_sequence_h1_q1.md)
- sha256 (`lf-normalised`): `f996a9647e9eda952e62878efb8dcbeb11e1841fb6e27e6d006949bdfbdc16fe`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0546
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/006_oewdp/levels/level_03_discrete_complex_cochains.md`

- file: `omega_engine_education/documentation/006_oewdp/levels/level_03_discrete_complex_cochains.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::kappa_exact_sequence`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::kappa_mk`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::kappa_well_defined`

## Absences recorded by the TFQ records

- TFQ-0546 python: the ledger binds WDP-CH04-P03 to no executable; obstruction.py computes signatures, not the sequence
- TFQ-0546 rust: no Rust statement of the degree-1 exact sequence

## Routes

Incoming (1):

- `PGW-R-WDP-EXACT-SEQUENCE-H1-Q1` `DERIVED_LEAN`: [PG-WDP-DEGREE1-WINDOW](PG-WDP-DEGREE1-WINDOW.md) (DEFINITION), [PG-WDP-QUOTIENT-EXACT-SEQUENCE](PG-WDP-QUOTIENT-EXACT-SEQUENCE.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-TRICHOTOMY-BOUNDS` `DERIVED_PROSE`: [PGW-WDP-TRICHOTOMY-BOUNDS](PGW-WDP-TRICHOTOMY-BOUNDS.md) (PROVED_PROSE)
