# PGW-SN-ENDPOINT-LEMMA

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a supplied irreflexive relation R, R(a,b) implies a ≠ b, since a = b would turn the witness into R(a,a); so the support of an asserted pair has exactly two elements, |{a,b}| = 2. This counts endpoints, not witnesses: single_oriented_witness_consistent builds a model with one forward witness and no reverse witness, so endpoints are 2 while witnesses can be 1. For the pointed two-element directed graph D₂ = ({0,1}, 0→1), each asserted pair (a,b) receives exactly one point-preserving map with f(0) = a and f(1) = b, and that map preserves the edge (D2_initial_pointed).

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

- Irreflexivity and orientation of R as declared inputs, not consequences of \<\> (assumption)

## Bottleneck

D₂ is initial only among pointed structures with an asserted pair; the combined paper says this does not make D₂ initial in an unspecified category of all systems. The sn-wire grammar accepts \<a-\>a\>, so irreflexivity is checked by verify_wir and not by parsing.

## Source status

000_pre_genesis_to_mssn paper.md section 9; 002_oesn sn.md section 3; Lean SnTheorems and Derivation/PrimDiff

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PrimDiff.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PrimDiff.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Lean: `omega_engine_education/documentation/002_oesn/lean4/SnTheorems.lean`

- file: `omega_engine_education/documentation/002_oesn/lean4/SnTheorems.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0515_sn_endpoint_lemma.md`

- file: [dag/derivations/05_mssn_sn/tfq_0515_sn_endpoint_lemma.md](../../../dag/derivations/05_mssn_sn/tfq_0515_sn_endpoint_lemma.md)
- sha256 (`lf-normalised`): `5c5a7c835cc5eee7052971956833267b94290b4b3d68bf413c430e30db94032a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0515
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/reading_guide.md`

- file: `omega_engine_education/documentation/002_oesn/reading_guide.md`
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

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PrimDiff.lean::D2_initial_pointed`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PrimDiff.lean::irrefl_witness_ne`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/PrimDiff.lean::single_oriented_witness_consistent`
- `external:the_symbol_game/omega_engine_education/documentation/002_oesn/code/sn_audit.py::verify_wir`
- `external:the_symbol_game/omega_engine_education/documentation/002_oesn/lean4/SnTheorems.lean::irrefl_witness_distinct`

## Absences recorded by the TFQ records

- TFQ-0515 rust: no Rust check of the endpoint lemma in the S(n) strand

## Routes

Incoming (1):

- `PGW-R-SN-ENDPOINT-LEMMA` `DERIVED_LEAN`: [PGW-SN3-COST-TWO-UNARY-MARK](PGW-SN3-COST-TWO-UNARY-MARK.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-POINTED-APARTNESS` `DERIVED_LEAN`: [PGW-WDP-POINTED-APARTNESS](PGW-WDP-POINTED-APARTNESS.md) (PROVED_LEAN)
