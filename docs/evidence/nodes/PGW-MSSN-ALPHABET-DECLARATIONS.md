# PGW-MSSN-ALPHABET-DECLARATIONS

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The MSS-N alphabet Γ38 is 26 lowercase letters, 10 digits and the two marks \< and \>; the grammar's word production uses Σ36, the letters and digits, and raw_glyphs treats \< and \> as ordinary marks, so balanced pairing is not an axiom there. A model must declare eight things separately: terminal spellings, tokenization, grammar, public start, layout, identity policy, annotation decoding and manipulation rules. Three relations that share notation stay apart: an encoded relation E ⊆ V × V, a rewrite relation, and an observation map q: V → O.

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

Alphabet size is independent of atlas row and of Genesis stage, and a glyph has a role only once a grammar gives it one.

## Source status

003_oemssn grammar/mssn.ebnf production 01; curriculum.md Lesson 2

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0530_mssn_alphabet_declarations.md`

- file: [dag/derivations/05_mssn_sn/tfq_0530_mssn_alphabet_declarations.md](../../../dag/derivations/05_mssn_sn/tfq_0530_mssn_alphabet_declarations.md)
- sha256 (`lf-normalised`): `623136df588c5d5ceba05fd5531af1a43180ed21be7769a0eeb2710d1ffebd1f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0530
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:2fa40c612d21ff06c530d2d586cb46d72df8d464d544de8f3536254191df6aac:10-11`
- `external:sha256:ea610e33827464418f0f2786ff65c9af072659bf2884a9411900e07d482e9740:42-43`
- `external:sha256:ea610e33827464418f0f2786ff65c9af072659bf2884a9411900e07d482e9740:44-48`
- `external:upstream/external:sha256:56626b2520b74d365419831189a5f3e91371b527e2f177f6c7a217222aed2ca1::RawGlyphs`

## Absences recorded by the TFQ records

- TFQ-0530 lean4: MssnSyntax.lean holds unrestricted syntax sketches with no recognizer for the alphabet
- TFQ-0530 rust: no Rust MSS-N alphabet check

## Routes

Incoming (1):

- `PGW-R-MSSN-ALPHABET-DECLARATIONS` `DERIVED_PROSE`: [PGW-MSSN-ASCENT-TRIAD](PGW-MSSN-ASCENT-TRIAD.md) (DEFINITION)

Outgoing (1):

- `PGW-R-MSSN-MANY-READINGS` `DERIVED_PROSE`: [PGW-MSSN-MANY-READINGS](PGW-MSSN-MANY-READINGS.md) (DEFINITION)
