# PGW-SN0-GROUND-INERTIA

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> S(0) supplies the literal \<\> as one opaque token: one presentation-token slot and two ASCII bytes, and neither count is the number of admitted data. In the sealed Genesis model nothing is derivable at genesis (genesis_underivable) and a bare supply leaves every regime unchanged (supply_no_op). The sealed Challenge 0 computation records admitted data empty in reading L and the single opaque datum in reading F, with no internal observables in either reading. The local S(n) Lean model has carrierCard 0 = 0 beside the two-character wire form of the ground token (ground_presentation_vs_carrier), and Carrier 0 has no inhabitant (ground_carrier_empty).

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

- `proved_lean_below_e3`: grade E0; 4 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 4 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

- Declared S(n) example carrier table carrierCard in SnCarrier.lean, chosen and not derived from 19L57G1 (assumption)

## Bottleneck

Zero admitted data is the reading-L and initial-regime statement; in reading F the inscription \<\> is the single admitted datum after its admission event, so the education phrase does not cover reading F. ground_carrier_empty concerns the declared example carrier, not a source replay.

## Source status

genesis_source.txt section 4 (Challenge 0); 002_oesn level_00_ground.md; Lean SnTheorems and Derivation/Inertia

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Lean: `omega_engine_education/documentation/002_oesn/lean4/SnTheorems.lean`

- file: `omega_engine_education/documentation/002_oesn/lean4/SnTheorems.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0511_sn0_ground_inertia.md`

- file: [dag/derivations/05_mssn_sn/tfq_0511_sn0_ground_inertia.md](../../../dag/derivations/05_mssn_sn/tfq_0511_sn0_ground_inertia.md)
- sha256 (`lf-normalised`): `12ecf2a2ca928c30e3c548a73aca71566714648ad0275ba32e0dd9263b895f55`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0511
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/levels/level_00_ground.md`

- file: `omega_engine_education/documentation/002_oesn/levels/level_00_ground.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/sn.md`

- file: `omega_engine_education/documentation/002_oesn/sn.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean::genesis_underivable`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean::supply_no_op`
- `external:the_symbol_game/omega_engine_education/documentation/002_oesn/code/sn_core.py::S0Ground`
- `external:the_symbol_game/omega_engine_education/documentation/002_oesn/lean4/SnTheorems.lean::ground_carrier_empty`
- `external:the_symbol_game/omega_engine_education/documentation/002_oesn/lean4/SnTheorems.lean::ground_presentation_vs_carrier`

## Absences recorded by the TFQ records

- TFQ-0511 rust: no Rust check of the S(0) ground in the S(n) strand

## Routes

Incoming (1):

- `PGW-R-SN0-GROUND-INERTIA` `DERIVED_LEAN`: [PGW-SN-TWO-BOXED-LAWS](PGW-SN-TWO-BOXED-LAWS.md) (DEFINITION)

Outgoing (1):

- `PGW-R-SN1-SUPPLY-NOT-ADMISSION` `DERIVED_LEAN`: [PGW-SN1-SUPPLY-NOT-ADMISSION](PGW-SN1-SUPPLY-NOT-ADMISSION.md) (PROVED_LEAN)
