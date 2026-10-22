# PGW-NO-ENDOGENOUS-DEMAND-GENERATOR

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_PROSE`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The continuation question asks whether the admitted structure can generate its next unresolved requirement without inspecting token glyphs, supplying a fresh datum, importing a new goal or assuming the continuation. The sealed answer is that no object-language endogenous demand generator was derived: a collapsed pair is not an active obstruction by itself, and the declared closure policy only reissues the admitted requirement pattern. Under that policy the fixed finite datum set reaches the all-pairs-separated fixpoint within n(n−1)/2 rounds, the size of the requirement language (allPairs_length). At the fixpoint no unresolved requirement exists in that language, so any further requirement needs a fresh datum (external supply) or a new requirement kind (external goal).

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

- `proved_prose_no_in_repo_document`: no in-repo non-generated document among the counted sources. PROVED_PROSE with no in-repo source document cited.

## Imported structure

- Declared pair-separation closure policy, genesis_source.txt section 3.9 (assumption)

## Bottleneck

This reports that no generator was derived, not that none exists in an extended language; raw rule admission can still erase a separation (TFQ-0385), and no longer or infinite tower is forced.

## Source status

genesis_source.txt section 9 written result with \[theorem\] and \[bounded theorem\] parts; Counting.lean allPairs_length

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Counting.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Counting.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Rounds.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Rounds.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0451_no_endogenous_demand_generator.md`

- file: [dag/derivations/02_genesis/tfq_0451_no_endogenous_demand_generator.md](../../../dag/derivations/02_genesis/tfq_0451_no_endogenous_demand_generator.md)
- sha256 (`lf-normalised`): `3f7d3afc7f4ff0c76c57b0dcd68d6250e9bdf9daa8cc6d94d9bacaf0c12cd42d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0451
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/engine.py::closure_challenge_orbits`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/closure.rs::closure_round_bound`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Counting.lean::allPairs_length`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/Rounds.lean::closedRun_round_bound_from_empty`

## Routes

Incoming (1):

- `PGW-R-NO-ENDOGENOUS-DEMAND-GENERATOR` `DERIVED_PROSE`: [PGW-POLICY-ENDPOINT-ALL-SEPARATED](PGW-POLICY-ENDPOINT-ALL-SEPARATED.md) (PROVED_LEAN), [TFQ-0385](TFQ-0385.md) (OPEN)

Outgoing (5):

- `APP-R-COMP-C4-UNBOUNDED-SUPPLY-IMPORT` `CONDITIONAL_ON_IMPORT`: [COMP-C4-UNBOUNDED-SUPPLY-IMPORT](COMP-C4-UNBOUNDED-SUPPLY-IMPORT.md) (IMPORTED_ASSUMPTION)
- `PGW-R-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS` `DERIVED_LEAN`: [PGW-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS](PGW-ENDOGENOUS-DEMANDS-EXOGENOUS-PAYMENTS.md) (PROVED_LEAN)
- `PGW-R-IDENTITY-IS-INDEX-NOT-PROFILE` `DERIVED_PROSE`: [PGW-IDENTITY-IS-INDEX-NOT-PROFILE](PGW-IDENTITY-IS-INDEX-NOT-PROFILE.md) (PROVED_PROSE)
- `PGW-R-MINIMAL-OR-INITIAL-REFUSED` `DERIVED_PROSE`: [PGW-MINIMAL-OR-INITIAL-REFUSED](PGW-MINIMAL-OR-INITIAL-REFUSED.md) (PROVED_PROSE)
- `PGW-R-SEALED-TERMINAL-STATEMENT` `DERIVED_PROSE`: [PGW-SEALED-TERMINAL-STATEMENT](PGW-SEALED-TERMINAL-STATEMENT.md) (PROVED_PROSE)
