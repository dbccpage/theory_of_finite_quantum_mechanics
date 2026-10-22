# PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT

Stage: [WDP](../stages/WDP.md). Status: `OPEN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> GenesisIncidence.lean reads the declared incidence complex on vertices 0, 1, 2 with signed boundary maps on the edge basis (01, 02, 12), the admitted face 012 entering as the column (1, −1, 1), and establishes that the boundary of that face has zero boundary (boundary_boundary_filled). The WDP window instead uses coboundaries with the simplicial edge order (01, 12, 02), d₀f = (f₁ − f₀, f₂ − f₁, f₂ − f₀) and d₁x = x₀₁ + x₁₂ − x₀₂ (Obstruction.lean), while the cyclic presentation (01, 12, 20) negates the reversed component. The monograph states that every window quantity is invariant once the cochain is transported with its edges, but no declared map takes the GenesisIncidence chains, with their edge order and boundary convention, to the WDP cochain window.

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

None recorded.

## Bottleneck

Neither file states the transport; boundary_boundary_filled is a chain-level fact in the incidence edge order, the incidence construction (TFQ-0460) does not derive the WDP window from Genesis admission (TFQ-0344), and the orientation test in Python stays inside the WDP convention.

## Source status

006_oewdp lean4/GenesisIncidence.lean (boundary order 01,02,12) vs WDP monograph §4.7 orientation convention; transport owed

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Lean: `omega_engine_education/documentation/006_oewdp/lean4/GenesisIncidence.lean`

- file: `omega_engine_education/documentation/006_oewdp/lean4/GenesisIncidence.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0543_wdp_incidence_orientation_transport.md`

- file: [dag/derivations/06_wdp/tfq_0543_wdp_incidence_orientation_transport.md](../../../dag/derivations/06_wdp/tfq_0543_wdp_incidence_orientation_transport.md)
- sha256 (`lf-normalised`): `fb1d6b96b1a6ca82a7b8c1af80f29e6c685c32d5bdd8ae215ca355d4c16e68a7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0543
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/unit_tests/test_obstruction.py::test_reversed_edge_orientation_changes_signs_not_the_signature`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::triD1`
- `external:the_symbol_game/omega_engine_education/documentation/006_oewdp/lean4/GenesisIncidence.lean::boundary_boundary_filled`

## Absences recorded by the TFQ records

- TFQ-0543 rust: no Rust transport between the GenesisIncidence boundary convention and the WDP coboundary window

## Routes

Incoming (1):

- `PGW-R-WDP-INCIDENCE-ORIENTATION-TRANSPORT` `GAP_NO_DERIVATION`: [PGW-WDP-GRAPH-COCHAIN-HOST](PGW-WDP-GRAPH-COCHAIN-HOST.md) (DEFINITION), [PGW-INCIDENCE-CONSTRUCTION-BETTI](PGW-INCIDENCE-CONSTRUCTION-BETTI.md) (PROVED_LEAN)

Outgoing (0):

