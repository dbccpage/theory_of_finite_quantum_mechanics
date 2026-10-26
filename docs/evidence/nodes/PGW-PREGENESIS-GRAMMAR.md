# PGW-PREGENESIS-GRAMMAR

Stage: [PREGENESIS](../stages/PREGENESIS.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The Pre-Genesis host grammar declares the inscription alphabet {\<, \>, a, b} and three public starts: ground_token (exactly \<\>), inscription (one balanced, non-nested bracketed inscription) and pre_genesis_regime (zero or more inscriptions between braces, where {} is host list notation and not the empty word). It keeps four states apart: absent input, the empty word, the literal token \<\> and the ground carrier that S(0) adopts. It has no event productions: the first event, supply(\<\>), is the Genesis boundary, and parsing a word admits no carrier, transition or observational operation.

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

- Declared host grammar pre_genesis.ebnf, a later host notation not tested by the model trials (assumption)

## Bottleneck

A grammar verdict is a syntax check of host notation; it assigns no semantics to \<\> and does not decide whether an inscription is admitted.

## Source status

000_oepregen grammar/pre_genesis.ebnf lines 1-37; 30 conformance cases PG_001-PG_030

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/01_pregenesis/tfq_0417_pregenesis_grammar.md`

- file: [dag/derivations/01_pregenesis/tfq_0417_pregenesis_grammar.md](../../../dag/derivations/01_pregenesis/tfq_0417_pregenesis_grammar.md)
- sha256 (`lf-normalised`): `7af474a89ed417f1e4c52c43d41d36466aaabeec3f15e4e9e255b9f382c280fa`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0417
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/000_oepregen/grammar/pre_genesis.ebnf`

- file: `omega_engine_education/documentation/000_oepregen/grammar/pre_genesis.ebnf`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:upstream/omega_engine_education/documentation/000_oepregen/code/check_pre_genesis.py::validate_cases`
- `external:upstream/omega_engine_education/documentation/000_oepregen/code/tests/test_pre_genesis_grammar.py::test_four_state_separation`

## Absences recorded by the TFQ records

- TFQ-0417 lean4: no Lean statement of the Pre-Genesis grammar; the grammar is checked in Python only
- TFQ-0417 rust: no Rust parser for pre_genesis.ebnf

## Routes

Incoming (1):

- `PGW-R-PREGENESIS-GRAMMAR` `DERIVED_PROSE`: [PG-INERT-DIAMOND](PG-INERT-DIAMOND.md) (DEFINITION)

Outgoing (1):

- `PGW-R-NO-TRANSITION-QUIESCENCE` `DERIVED_PROSE`: [PGW-NO-TRANSITION-QUIESCENCE](PGW-NO-TRANSITION-QUIESCENCE.md) (DEFINITION)
