# PGW-MSSN-ALPHABET-DECLARATIONS

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The MSS-N alphabet Γ38 is 26 lowercase letters, 10 digits and the two marks \< and \>; the grammar's word production uses Σ36, the letters and digits, and raw_glyphs treats \< and \> as ordinary marks, so balanced pairing is not an axiom there. A model must declare eight things separately: terminal spellings, tokenization, grammar, public start, layout, identity policy, annotation decoding and manipulation rules. Three relations that share notation stay apart: an encoded relation E ⊆ V × V, a rewrite relation, and an observation map q: V → O.

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

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Alphabet size is independent of atlas row and of Genesis stage, and a glyph has a role only once a grammar gives it one.

## Source status

003_oemssn grammar/mssn.ebnf production 01; curriculum.md Lesson 2

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0530_mssn_alphabet_declarations.md`

- file: [dag/derivations/05_mssn_sn/tfq_0530_mssn_alphabet_declarations.md](../../../dag/derivations/05_mssn_sn/tfq_0530_mssn_alphabet_declarations.md)
- sha256 (`lf-normalised`): `c0351dfc79a2a8442d8368f91b22b154ab088747f6d565bfa71e6d6fac1c939a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0530
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

- `external:the_symbol_game/omega_engine_education/documentation/003_oemssn/code/mssn_codec.py::RawGlyphs`

## Absences recorded by the TFQ records

- TFQ-0530 lean4: MssnSyntax.lean holds unrestricted syntax sketches with no recognizer for the alphabet
- TFQ-0530 rust: no Rust MSS-N alphabet check

## Routes

Incoming (1):

- `PGW-R-MSSN-ALPHABET-DECLARATIONS` `DERIVED_PROSE`: [PGW-MSSN-ASCENT-TRIAD](PGW-MSSN-ASCENT-TRIAD.md) (DEFINITION)

Outgoing (1):

- `PGW-R-MSSN-MANY-READINGS` `DERIVED_PROSE`: [PGW-MSSN-MANY-READINGS](PGW-MSSN-MANY-READINGS.md) (DEFINITION)
