# PGW-MSSN-SYNTAX-NOT-DECODING

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A grammar verdict is recognition, not decoding: a:1/0 parses in scalar_path, and division by zero is a later numeric refusal unless the grammar is changed to exclude zero denominators. Side conditions fall into three classes: zero denominators can be excluded lexically, bracket matching is context-free, and acyclicity or triangle inequalities are semantic obligations. a\>2\<b is refused in edge_weight_path because both marks on a step must agree. Recognition, AST construction, decoding, evaluation and exact serialization are distinct checks.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Conformance cases MSSN_020 (a:1/0\>b:2 accepted) and MSSN_023 (a\>2\<b refused) check syntax only, and finite differential tests are not an all-input argument for the codec.

## Source status

000_pre_genesis_to_mssn paper.md section 14; 003_oemssn curriculum.md Lesson 4

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0532_mssn_syntax_not_decoding.md`

- file: [dag/derivations/05_mssn_sn/tfq_0532_mssn_syntax_not_decoding.md](../../../dag/derivations/05_mssn_sn/tfq_0532_mssn_syntax_not_decoding.md)
- sha256 (`lf-normalised`): `718ea5a77f8590335dbcb9a1c21eb59715c9bb16ea040a0b4cf5ea7984bed051`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0532
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

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_education/documentation/003_oemssn/code/check_mssn.py::main`

## Absences recorded by the TFQ records

- TFQ-0532 lean4: no Lean statement separating lexical, context-free and semantic conditions
- TFQ-0532 rust: no Rust MSS-N decoder for scalar or edge-weight paths

## Routes

Incoming (1):

- `PGW-R-MSSN-SYNTAX-NOT-DECODING` `DERIVED_PROSE`: [PGW-MSSN-MANY-READINGS](PGW-MSSN-MANY-READINGS.md) (DEFINITION)

Outgoing (1):

- `PGW-R-MSSN-ROWS-1-TO-6-SPECIFIED` `DERIVED_PROSE`: [PGW-MSSN-ROWS-1-TO-6-SPECIFIED](PGW-MSSN-ROWS-1-TO-6-SPECIFIED.md) (DEFINITION)
