# PGW-METATHEORY-OBJECT-LANGUAGE-SPLIT

Stage: [GENESIS](../stages/GENESIS.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The sealed manuscript declares two levels. The metatheory holds presentation tokens (strings), event sequences, indices, finite data structures and arithmetic; the object language holds only what a regime admits. Token glyphs, component counts, order, concatenation, multiplicity, substring structure, matching and string equality live in the metatheory unless an admitted judgment internalizes a distinction. Presentation identity (token equality) is metatheory only, internal identity is the datum index, and no semantic interpretation is ever assigned.

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

- Declared two-level metatheory/object-language split of genesis_source.txt section 2 (assumption)

## Bottleneck

A declared split, not a theorem: the Lean model has no tokens by construction, so token-blindness is structural there and is checked in Python and Rust by renaming tests; admission order is visible to the token-aware metatheory and erased at the object level.

## Source status

genesis_source.txt section 2 \[declared metatheory\]; Bridge.lean admission-order theorems

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Bridge.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Bridge.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/token.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/token.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0430_metatheory_object_language_split.md`

- file: [dag/derivations/02_genesis/tfq_0430_metatheory_object_language_split.md](../../../dag/derivations/02_genesis/tfq_0430_metatheory_object_language_split.md)
- sha256 (`lf-normalised`): `ddb75d935f4795dded41ebea8cfea497f3220f8931f59c8079463d83389faec1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0430
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/001_oegen/genesis.md`

- file: `omega_engine_education/documentation/001_oegen/genesis.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/iso.py::serialize`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/token.rs::tokens_are_forgotten_by_the_key`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Bridge.lean::order_erased_at_object_level`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Bridge.lean::order_visible_to_metatheory`

## Routes

Incoming (1):

- `PGW-R-METATHEORY-OBJECT-LANGUAGE-SPLIT` `DERIVED_PROSE`: [PG-GEN-REGIME-EVENTS](PG-GEN-REGIME-EVENTS.md) (DEFINITION)

Outgoing (2):

- `PGW-R-CHALLENGE0-INERTIA-SECOND-TOKEN` `DERIVED_LEAN`: [PGW-CHALLENGE0-INERTIA-SECOND-TOKEN](PGW-CHALLENGE0-INERTIA-SECOND-TOKEN.md) (PROVED_LEAN)
- `PGW-R-REGIME-ISOMORPHISM-UNORDERED-PAIRS` `DERIVED_PROSE`: [PGW-REGIME-ISOMORPHISM-UNORDERED-PAIRS](PGW-REGIME-ISOMORPHISM-UNORDERED-PAIRS.md) (DEFINITION)
