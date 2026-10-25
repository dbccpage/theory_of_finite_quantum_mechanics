# PGW-COLLECTION-EXTENSIONALITY

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Python's admitted collections are sets while Lean's are deduplicated lists. Under RegimeExt (equal datum counts and form tables, and membership-equal instance, rule and requirement collections) every stated observable transports: derivability, context well-formedness, collapse, separability, item and delta application, and response validity (derivable_ext through validResponse_ext). Two list representations of the same admitted sets therefore agree on each of those observables.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declaration references covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Lean-to-Lean only: equal datum counts and equal indexed form tables stay premises, that every exported claim factors through these observables is not asserted, and executable comparisons with Python and Rust have their own input populations.

## Source status

genesis_source.txt section 3 membership extensionality \[theorem\]; Ext.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/Genesis19l57g1/Derivation/Ext.lean`

- file: [lean4/Imported/Genesis19l57g1/Derivation/Ext.lean](../../../lean4/Imported/Genesis19l57g1/Derivation/Ext.lean)
- sha256 (`bytes`): `944de2893918819c3bd8e1066b888950f8561541930dd110b3f17948591bbace`
- cited in: node.lean, record TFQ-0437
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.Genesis19l57g1.Derivation.Ext`): recorded sha256 `944de2893918819c3bd8e1066b888950f8561541930dd110b3f17948591bbace` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/Genesis19l57g1/Derivation/Ext.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `collapsed_ext` | yes | yes | yes | propext | `#print axioms collapsed_ext` |
| `derivable_ext` | yes | yes | yes | none | `#print axioms derivable_ext` |
| `separable_ext` | yes | yes | yes | propext | `#print axioms separable_ext` |
| `validResponse_ext` | yes | yes | yes | propext | `#print axioms validResponse_ext` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0437_collection_extensionality.md`

- file: [dag/derivations/02_genesis/tfq_0437_collection_extensionality.md](../../../dag/derivations/02_genesis/tfq_0437_collection_extensionality.md)
- sha256 (`lf-normalised`): `fb598b409c6aefe9ed3aa9cb7d0460c74f43b3bf5ceb98b7832ee1bcbf385689`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0437
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/model.py::Regime`

## Absences recorded by the TFQ records

- TFQ-0437 rust: no Rust statement of RegimeExt; the Rust regime stores instances, rules and requirements as BTreeSet collections, so list order does not arise there

## Routes

Incoming (1):

- `PGW-R-COLLECTION-EXTENSIONALITY` `DERIVED_LEAN`: [PGW-CONTEXTS-PLUGGING-PROFILES](PGW-CONTEXTS-PLUGGING-PROFILES.md) (DEFINITION)

Outgoing (0):

