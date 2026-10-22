# PGW-BOUNDED-TIE-CENSUS

Stage: [GENESIS](../stages/GENESIS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Within the declared bounds of at most two items and form arity at most two, exhaustive enumeration under mu1, cross-checked against the unpruned space, finds at (2,2) six valid deltas in three isomorphism classes for reading L (unary mark, binary link, binary self-loop) and ten valid deltas in five classes for reading F. Reading F's two extra classes link to and from the never-required genesis datum, and they are non-isomorphic to each other because the bijection must preserve the requirement pair. Under mu2 each reading has two minimal deltas in one class. The standalone replay reproduces all four counts.

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

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- Declared resource bounds max_items 2 and max_arity 2 and the implemented isomorphism relation (assumption)

## Bottleneck

A bounded census: it is the max_arity = 2 slice of the infinite mu1 tie family of reading L (TFQ-0441), and no reading-F Lean non-uniqueness statement exists.

## Source status

genesis_source.txt section 7.3 \[bounded theorem\] engine enumeration at (2,2); reproduce.py minimum census

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0442_bounded_tie_census.md`

- file: [dag/derivations/02_genesis/tfq_0442_bounded_tie_census.md](../../../dag/derivations/02_genesis/tfq_0442_bounded_tie_census.md)
- sha256 (`lf-normalised`): `57b6f20a9ca8a9420601f1cf1987a2a97d1a0ded0d531d515e582a3fd478976c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0442
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

### Documents and data: `omega_engine_education/documentation/001_oegen/genesis.md`

- file: `omega_engine_education/documentation/001_oegen/genesis.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/candidates.py::min_responses`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/reproduce.py::python_replay`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs::sealed_challenge3_reading_f`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/minima.rs::sealed_challenge3_reading_l`

## Absences recorded by the TFQ records

- TFQ-0442 lean4: no Lean census of the bounded tie classes; reading-F non-uniqueness has no Lean statement

## Routes

Incoming (1):

- `PGW-R-BOUNDED-TIE-CENSUS` `COMPUTED`: [PGW-MU1-MINIMUM-NOT-UNIQUE-L](PGW-MU1-MINIMUM-NOT-UNIQUE-L.md) (PROVED_LEAN)

Outgoing (0):

