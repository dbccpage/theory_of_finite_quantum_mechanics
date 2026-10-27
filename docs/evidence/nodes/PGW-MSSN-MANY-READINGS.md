# PGW-MSSN-MANY-READINGS

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `DEFINITION`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> mssn.ebnf declares 22 public starts, and every conformance case names its start; there is no guessed union or default start. The string a\>b\>c\>a is accepted by raw_glyphs, label_path and glyph_path and refused by suffix_path, whose vertices need a digit annotation; a0\>b2\>c1\>a0 is accepted by raw_glyphs, label_path and suffix_path and refused by glyph_path, which reads a0 as two adjacent vertices with no direction. check_mssn.py runs 39 cases over the 22 starts.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

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

### Python: `atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/code/sn_mssn_checks.py`

- file: [atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/code/sn_mssn_checks.py](../../../atlas/papers/finite_obstruction_calculus/symmetric_groups_and_minimal_symbol_systems/code/sn_mssn_checks.py)
- sha256 (`bytes`): `2580dc90a3c22fa19894aa4e17c0a60f68d24946394a5e1f2827abc00b9ff429`
- cited in: record TFQ-0531

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `grammar_inventory_matches` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md`

- file: [atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md](../../../atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md)
- sha256 (`lf-normalised`): `a4a7d840b11e912896032aebc9ead95f7978c0e6f60656f44645c6d8fadf593b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0531_mssn_many_readings.md`

- file: [dag/derivations/05_mssn_sn/tfq_0531_mssn_many_readings.md](../../../dag/derivations/05_mssn_sn/tfq_0531_mssn_many_readings.md)
- sha256 (`lf-normalised`): `39a2df749cd641bde126c5833fcabb47f51e2a10e5f8aa8e5a74e70f0134b48c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0531
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:2fa40c612d21ff06c530d2d586cb46d72df8d464d544de8f3536254191df6aac:3-4`
- `external:sha256:ea610e33827464418f0f2786ff65c9af072659bf2884a9411900e07d482e9740:58-67`
- `external:upstream/external:sha256:f2944b0fca54f5d5a13593c337da8f9887447e447a6ffe2cc7c4731e750cec63::main`

## Absences recorded by the TFQ records

- TFQ-0531 lean4: MssnSyntax.lean holds unrestricted syntax sketches with no recognizer or parser-correspondence theorem
- TFQ-0531 rust: no Rust recognizer for mssn.ebnf

## Routes

Incoming (1):

- `PGW-R-MSSN-MANY-READINGS` `DERIVED_PROSE`: [PGW-MSSN-ALPHABET-DECLARATIONS](PGW-MSSN-ALPHABET-DECLARATIONS.md) (DEFINITION)

Outgoing (1):

- `PGW-R-MSSN-SYNTAX-NOT-DECODING` `DERIVED_PROSE`: [PGW-MSSN-SYNTAX-NOT-DECODING](PGW-MSSN-SYNTAX-NOT-DECODING.md) (DEFINITION)
