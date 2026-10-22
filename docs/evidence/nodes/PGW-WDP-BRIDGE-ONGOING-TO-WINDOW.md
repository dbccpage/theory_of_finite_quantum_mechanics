# PGW-WDP-BRIDGE-ONGOING-TO-WINDOW

Stage: [WDP](../stages/WDP.md). Status: `OPEN`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> GEN-WDP-07, a conditional theorem in the bridge register, fixes a carrier and marked triples F, keeps the full directed integer table e(x, y) = M_r(x, y) − M_s(x, y) including loops and independent reverse arcs, treats raising as e ↦ e + d₀g with (d₀g)(x, y) = g(x) − g(y), and uses the marked diagnostic D_F(e)(x, y, z) = e(x, y) + e(y, z) + e(z, x). Cancellation gives D_F d₀ = 0, so D_F(e + d₀g) = D_F e even for unbalanced triples, and rationalizing reflects integer repair equality. This is a repair quotient with descending reports, not automatically cohomology: C¹/im d₀ differs from ker D_F/im d₀, a filled mark may be unbalanced, triangle reports miss loops and two-way defects, and antisymmetric simplicial coordinates need e(x, x) = 0 and e(x, y) + e(y, x) = 0. Term addition and identification can fail to respect the quotient (source 23:D4), so carrier-changing operations need new congruence proofs.

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

- Fixed carrier and declared marked triples F from the chosen Genesis Ongoing source contexts (assumption)

## Bottleneck

Proposed, not derived: the bridge does not produce the window of TFQ-0004 from Genesis admission (TFQ-0344), integer change costs are not identified with a continuous norm, and dynamic carrier changes belong to GEN-WDP-O02 and O03.

## Source status

docs/genesis_to_wdp_derivation_programme.md §4 and register GEN-WDP-07 (conditional, fixed carrier); bridge to the window owed

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/RootGaugeNormalization.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/RootGaugeNormalization.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/genesis_ongoing_adapter.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/genesis_ongoing_adapter.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0555_wdp_bridge_ongoing_to_window.md`

- file: [dag/derivations/06_wdp/tfq_0555_wdp_bridge_ongoing_to_window.md](../../../dag/derivations/06_wdp/tfq_0555_wdp_bridge_ongoing_to_window.md)
- sha256 (`lf-normalised`): `a6ba9a0b1f49c40a4a724cd46929c4ee0cda0658239e7a99b4a3b3eb8c8d434f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0555
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_ongoing_fixed_carrier_bridge.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_ongoing_fixed_carrier_bridge.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/006_oewdp/levels/level_22_genesis_to_wdp_bridges.md`

- file: `omega_engine_education/documentation/006_oewdp/levels/level_22_genesis_to_wdp_bridges.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine/crates_rs/omega_wdp/src/genesis_ongoing_adapter.rs::GenesisOngoingAdapter`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/RootGaugeNormalization.lean::normal_preserves_round_sums`

## Absences recorded by the TFQ records

- TFQ-0555 python: GEN-WDP-07 carries a written proof and the native omega_wdp adapter; no Python binding

## Routes

Incoming (1):

- `PGW-R-WDP-BRIDGE-ONGOING-TO-WINDOW` `GAP_NO_DERIVATION`: [PGW-WDP-GENESIS-BRIDGES-LEDGER](PGW-WDP-GENESIS-BRIDGES-LEDGER.md) (DEFINITION), [PGW-GO-H3-TWIN-FILLS-HOLONOMY](PGW-GO-H3-TWIN-FILLS-HOLONOMY.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-SYNTHESIS-TRUNK-TIERS` `DERIVED_PROSE`: [PGW-WDP-SYNTHESIS-TRUNK-TIERS](PGW-WDP-SYNTHESIS-TRUNK-TIERS.md) (DEFINITION)
