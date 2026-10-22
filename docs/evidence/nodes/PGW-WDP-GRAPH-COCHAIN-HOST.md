# PGW-WDP-GRAPH-COCHAIN-HOST

Stage: [WDP](../stages/WDP.md). Status: `DEFINITION`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On a finite oriented graph G = (V, E) with a normed coefficient space A, the host sets C⁰ = A^V, C¹ = A^E and (d₀f)(u, v) = f(v) − f(u); an edge field δ is exact when δ = d₀f. Q¹ = C¹/im d₀ records edge fields modulo vertex-potential repair, relative to the declared graph, coefficient space and repair map, and it is not the first cohomology group unless a next differential d₁ is supplied with d₁d₀ = 0. Worked cases: on the path 0 → 1 → 2, δ = (2, 3) = d₀(0, 2, 5) is exact; on the hollow cyclic triangle (01, 12, 20) every repair of δ = (1, 1, 1) still sums to 3, a quotient obstruction that is not contextuality without a measurement cover and an empirical model.

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

- Declared finite oriented graph and normed coefficient space (assumption)

## Bottleneck

The graph, orientation and coefficients are declared inputs, not derived from Genesis admission (TFQ-0344); a repair-quotient class is not a cohomology class, and the host carries no measurement cover or empirical model.

## Source status

WDP monograph §4.1 graph-cochain host (definition)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/cochains.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/cochains.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0542_wdp_graph_cochain_host.md`

- file: [dag/derivations/06_wdp/tfq_0542_wdp_graph_cochain_host.md](../../../dag/derivations/06_wdp/tfq_0542_wdp_graph_cochain_host.md)
- sha256 (`lf-normalised`): `2a4bcfa767de5b8eed566783e83d72a1b75853441dbe38f824a75245da282b46`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0542
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/006_oewdp/levels/level_03_discrete_complex_cochains.md`

- file: `omega_engine_education/documentation/006_oewdp/levels/level_03_discrete_complex_cochains.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine/crates_rs/omega_wdp/src/cochains.rs::FiniteComplex`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/cochains.py::FiniteComplex`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/cochains.py::d0`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::Q1`

## Routes

Incoming (1):

- `PGW-R-WDP-GRAPH-COCHAIN-HOST` `DERIVED_PROSE`: [PG-ADMISSION-FLOOR](PG-ADMISSION-FLOOR.md) (PROVED_LEAN)

Outgoing (3):

- `PGW-R-WDP-CLOSURE-NEEDS-DEGREE` `DERIVED_PROSE`: [PGW-WDP-CLOSURE-NEEDS-DEGREE](PGW-WDP-CLOSURE-NEEDS-DEGREE.md) (DEFINITION)
- `PGW-R-WDP-INCIDENCE-ORIENTATION-TRANSPORT` `GAP_NO_DERIVATION`: [PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT](PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT.md) (OPEN)
- `PGW-R-WDP-PHI-WELL-DEFINED-L1-DUALITY` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY](PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY.md) (CONDITIONAL)
