# PGW-MSSN-MANY-READINGS

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> mssn.ebnf declares 22 public starts, and every conformance case names its start; there is no guessed union or default start. The string a\>b\>c\>a is accepted by raw_glyphs, label_path and glyph_path and refused by suffix_path, whose vertices need a digit annotation; a0\>b2\>c1\>a0 is accepted by raw_glyphs, label_path and suffix_path and refused by glyph_path, which reads a0 as two adjacent vertices with no direction. check_mssn.py runs 39 cases over the 22 starts.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The 22 starts are syntax profiles, not 22 completed semantic adapters (WDP-P001-014), and the historical inventory of 22 starts with six runtime profiles is not evidence of 28 evaluators.

## Source status

003_oemssn grammar/mssn.ebnf header; curriculum.md Lesson 3; 39 conformance cases MSSN_001 onward

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0531_mssn_many_readings.md`

- file: [dag/derivations/05_mssn_sn/tfq_0531_mssn_many_readings.md](../../../dag/derivations/05_mssn_sn/tfq_0531_mssn_many_readings.md)
- sha256 (`lf-normalised`): `3b232b9974ee75cf0a0c7fb3c315dc3d96f7a8a8c3633b3ff2847fa2369c77ba`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0531
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/003_oemssn/curriculum.md`

- file: `omega_engine_education/documentation/003_oemssn/curriculum.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/003_oemssn/grammar/mssn.ebnf`

- file: `omega_engine_education/documentation/003_oemssn/grammar/mssn.ebnf`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/code/sn_mssn_checks.py::grammar_inventory_matches`
- `external:upstream/omega_engine_education/documentation/003_oemssn/code/check_mssn.py::main`

## Absences recorded by the TFQ records

- TFQ-0531 lean4: MssnSyntax.lean holds unrestricted syntax sketches with no recognizer or parser-correspondence theorem
- TFQ-0531 rust: no Rust recognizer for mssn.ebnf

## Routes

Incoming (1):

- `PGW-R-MSSN-MANY-READINGS` `DERIVED_PROSE`: [PGW-MSSN-ALPHABET-DECLARATIONS](PGW-MSSN-ALPHABET-DECLARATIONS.md) (DEFINITION)

Outgoing (1):

- `PGW-R-MSSN-SYNTAX-NOT-DECODING` `DERIVED_PROSE`: [PGW-MSSN-SYNTAX-NOT-DECODING](PGW-MSSN-SYNTAX-NOT-DECODING.md) (DEFINITION)
