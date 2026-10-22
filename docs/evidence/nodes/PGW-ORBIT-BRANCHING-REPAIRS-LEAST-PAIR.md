# PGW-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Raw least-pair selection is not isomorphism-equivariant. On the regression regime (four data, one unary form, instances on data 2 and 3) both the regime and its renaming by the double transposition 0↔2, 1↔3 collapse the pair (0, 1), yet the renaming carries (0, 1) to (2, 3) (least_pair_selection_not_congruent); that the two same-index choices give non-isomorphic children is a computational test. The repair branches once per automorphism orbit of collapsed pairs. Under datum renamings with forms fixed, the selection-free transition relation over every collapsed pair and every valid response transports (transStep_rename_fwd, transStep_image_total), and valid-response counts over caller-supplied candidate lists transport (validCount_rename).

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

- `proved_lean_below_e3`: grade E0; 4 Lean reference(s) cited, 0 in this checkout. PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `proved_lean_external_only`: all 4 cited Lean reference(s) lie outside this checkout. PROVED_LEAN whose cited Lean lies only in external or sibling-atlas paths, none in this checkout.

## Imported structure

None recorded.

## Bottleneck

The congruence is relation-level with forms fixed; conversion to equal canonical-key class sets, form-bijection transport and minimum-family transport stay computational with CL-ISO-SOUND, and no exported run reached a state with more than one orbit.

## Source status

genesis_source.txt section 8.2 \[counterexample\] and relation-level \[theorem\] (R7); TransitionTransport.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/TransitionTransport.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/TransitionTransport.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/automorphism.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/automorphism.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0444_orbit_branching_repairs_least_pair.md`

- file: [dag/derivations/02_genesis/tfq_0444_orbit_branching_repairs_least_pair.md](../../../dag/derivations/02_genesis/tfq_0444_orbit_branching_repairs_least_pair.md)
- sha256 (`lf-normalised`): `0113852fefc8e2dca4bde7727b8b78a3eaef76792fdc3ec60b247ed165642d57`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0444
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/iso.py::pair_orbits`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/automorphism.rs::orbits_are_equivariant_under_renaming`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/automorphism.rs::pair_orbits`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/TransitionTransport.lean::least_pair_selection_not_congruent`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/TransitionTransport.lean::transStep_image_total`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/TransitionTransport.lean::transStep_rename_fwd`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/lean4/Derivation/TransitionTransport.lean::validCount_rename`

## Routes

Incoming (1):

- `PGW-R-ORBIT-BRANCHING-REPAIRS-LEAST-PAIR` `DERIVED_LEAN`: [PGW-CHALLENGE-SOURCE-POLICIES](PGW-CHALLENGE-SOURCE-POLICIES.md) (DEFINITION)

Outgoing (2):

- `PGW-R-COUNT-INVARIANCE-TRANSPORT` `DERIVED_LEAN`: [PGW-COUNT-INVARIANCE-TRANSPORT](PGW-COUNT-INVARIANCE-TRANSPORT.md) (PROVED_LEAN)
- `PGW-R-RESPONSE-EXISTENCE-MARK-PROGRESS` `DERIVED_LEAN`: [PGW-RESPONSE-EXISTENCE-MARK-PROGRESS](PGW-RESPONSE-EXISTENCE-MARK-PROGRESS.md) (PROVED_LEAN)
