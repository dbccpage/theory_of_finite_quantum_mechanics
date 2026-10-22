# PGW-MSSN-CIRCULATION-OBSTRUCTION

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> MssnObstructionDetector.lean defines a Boolean active-obstruction predicate obstP on a passage state with witness pairs, protected pairs and an optional list of observation columns, and shows that it equals the conjunction of four gates: retained, protected, observation declared, and declared observation not separating the pair (obstP_factors, obst_of_gates). On the triangle a→b→c→a it shows that the cycle circulation vanishes on every integer coboundary d₀g (cycle_circulation_coboundary_vanishes), that x = (1,0,0) has circulation 1 (circulation_flux_obstruction), and that no integer potential g has d₀g = (1,0,0) (no_scalar_potential_for_unit_flux). candidateLiftCondition is a necessary condition on supplied metadata, not an implementation of the lift laws or an authorization decision.

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

- Supplied observation columns in PState, not a checked partition or the full Genesis passage state (assumption)

## Bottleneck

The circulation results are relative to the displayed d₀ over ℤ; candidateLiftCondition consumes a supplied Boolean and verifies neither that an edit resolves an obstruction nor that it is authorized, and the Rust audit returns the circulation value without a potential search.

## Source status

003_oemssn lean4/MssnObstructionDetector.lean and lean4/README.md inventory row

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean`

- file: `omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Rust: `omega_engine_education/documentation/003_oemssn/code/rust/src/obstruction_detector.rs`

- file: `omega_engine_education/documentation/003_oemssn/code/rust/src/obstruction_detector.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0534_mssn_circulation_obstruction.md`

- file: [dag/derivations/05_mssn_sn/tfq_0534_mssn_circulation_obstruction.md](../../../dag/derivations/05_mssn_sn/tfq_0534_mssn_circulation_obstruction.md)
- sha256 (`lf-normalised`): `7d1082904fb2b81a29f5cca64daf1a049ceee20199e8f71c6c200d918503973e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0534
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/003_oemssn/lean4/README.md`

- file: `omega_engine_education/documentation/003_oemssn/lean4/README.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_education/documentation/003_oemssn/code/rust/src/obstruction_detector.rs::audit_layer_2_circulation_flux`
- `external:the_symbol_game/omega_engine_education/documentation/003_oemssn/code/rust/src/obstruction_detector.rs::verify_four_gate_factorization`
- `external:the_symbol_game/omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean::circulation_flux_obstruction`
- `external:the_symbol_game/omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean::cycle_circulation_coboundary_vanishes`
- `external:the_symbol_game/omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean::no_scalar_potential_for_unit_flux`
- `external:the_symbol_game/omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean::obstP_factors`
- `external:the_symbol_game/omega_engine_education/documentation/003_oemssn/lean4/MssnObstructionDetector.lean::obst_of_gates`

## Absences recorded by the TFQ records

- TFQ-0534 python: no Python check of the four-gate detector or the triangle circulation in 003_oemssn

## Routes

Incoming (1):

- `PGW-R-MSSN-CIRCULATION-OBSTRUCTION` `DERIVED_LEAN`: [PGW-MSSN-ROWS-1-TO-6-SPECIFIED](PGW-MSSN-ROWS-1-TO-6-SPECIFIED.md) (DEFINITION), [PGW-SN-E12-CIRCULATION-FUNCTIONAL](PGW-SN-E12-CIRCULATION-FUNCTIONAL.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-MSSN-L1-CUTS-HODGE-ROWS` `DERIVED_PROSE`: [PGW-MSSN-L1-CUTS-HODGE-ROWS](PGW-MSSN-L1-CUTS-HODGE-ROWS.md) (DEFINITION)
