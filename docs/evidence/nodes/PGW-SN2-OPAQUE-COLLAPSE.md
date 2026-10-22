# PGW-SN2-OPAQUE-COLLAPSE

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> S(2) retains opaque wholes: reading L admits (\<a\>, \<ab\>) and reading F admits (\<\>, \<a\>, \<ab\>). R2L_collapsed and R2F_collapsed show that every pair of admitted data stays observationally collapsed before distinguishing instances are admitted, so two externally different inscriptions remain internally indistinguishable, and the source does not decompose \<ab\> into a and b. A collapsed pair by itself is not an active obstruction; it becomes one only when a supplied question or separation requirement demands different answers. The later flat grammar sn.ebnf parses \<ab\> as a pair of glyphs, which is a new interpretation with its own parser.

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

Collapse is relative to the source's derivability profiles; the ledger value s₂ = 1 needs a supplied separation demand, and a two-vertex graph or permutation representation of the pair (as in S2Collapse) is declared structure, not an admitted directed relation.

## Source status

genesis_source.txt sections 6 and 9 (Challenge 2, continuation); 002_oesn level_02_relational_pairings.md; Lean Derivation/Inertia

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0513_sn2_opaque_collapse.md`

- file: [dag/derivations/05_mssn_sn/tfq_0513_sn2_opaque_collapse.md](../../../dag/derivations/05_mssn_sn/tfq_0513_sn2_opaque_collapse.md)
- sha256 (`lf-normalised`): `837be3aea059133e393073302ecf06a5a18d66230b3a9ef48a142aaaad3b4c74`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0513
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/002_oesn/levels/level_02_relational_pairings.md`

- file: `omega_engine_education/documentation/002_oesn/levels/level_02_relational_pairings.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean::R2F_collapsed`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Inertia.lean::R2L_collapsed`
- `external:the_symbol_game/omega_engine_education/documentation/002_oesn/code/sn_core.py::S2Collapse`

## Absences recorded by the TFQ records

- TFQ-0513 rust: no Rust check of opaque collapse in the S(n) strand

## Routes

Incoming (1):

- `PGW-R-SN2-OPAQUE-COLLAPSE` `DERIVED_LEAN`: [PGW-SN1-SUPPLY-NOT-ADMISSION](PGW-SN1-SUPPLY-NOT-ADMISSION.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-SN3-COST-TWO-UNARY-MARK` `DERIVED_LEAN`: [PGW-SN3-COST-TWO-UNARY-MARK](PGW-SN3-COST-TWO-UNARY-MARK.md) (PROVED_LEAN)
