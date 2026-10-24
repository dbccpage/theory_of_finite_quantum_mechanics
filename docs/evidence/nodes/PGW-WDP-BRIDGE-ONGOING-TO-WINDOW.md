# PGW-WDP-BRIDGE-ONGOING-TO-WINDOW

Stage: [WDP](../stages/WDP.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For three positions labeled 0, 1, and 2, every integer triple (g0, g1, g2) has coboundary round sum (g0 - g1) + (g1 - g2) + (g2 - g0) = 0, and adding those differences leaves e01 + e12 + e20 unchanged, including the unbalanced mark 1 + 1 + 1 = 3, which stays 3 after the differences from (2, 5, 11). For every integer g the diagonal g - g is 0, so the loop value 4 is not a diagonal coboundary, while the oriented arcs 0, 0, 0 have diagnostic 0. The forward arc 3 with the other oriented arcs 0 has diagnostic 3, and the two-way values 3 and 5 sum to 8.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 9
- cited Lean declarations covered by a current replay receipt: 7
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Fixed carrier and declared marked triples F from the chosen Genesis Ongoing source contexts (assumption)

## Bottleneck

The cancellation is the three-term integer identity on one ordered triple of positions. It does not identify the repair quotient with cohomology, and it does not produce the window of TFQ-0004 from Genesis admission (TFQ-0344). Rational repair equality, term addition, identification, a continuous norm, and carrier changes GEN-WDP-O02 and O03 stay open. normal_preserves_round_sums is gauge normalization of a whole table. The loop 4 and the pair 3, 5 are witnesses on this triple.

## Source status

docs/genesis_to_wdp_derivation_programme.md §4 and register GEN-WDP-07 (conditional, fixed carrier); bridge to the window owed

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwWdpBridgeOngoingToWindow.lean`

- file: [lean4/CampaignPgwWdpBridgeOngoingToWindow.lean](../../../lean4/CampaignPgwWdpBridgeOngoingToWindow.lean)
- sha256 (`bytes`): `6942e82d06122f8ac06bce53e0eccc0562bef569ddfd1fa4c7c1d7a811e5ca1e`
- cited in: node.lean, node.source, receipt dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json (CampaignPgwWdpBridgeOngoingToWindow), record TFQ-0555
- replay: `verified`
  - receipt [dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json](../../../dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json) (module `CampaignPgwWdpBridgeOngoingToWindow`): recorded sha256 `6942e82d06122f8ac06bce53e0eccc0562bef569ddfd1fa4c7c1d7a811e5ca1e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwWdpBridgeOngoingToWindow`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `pgwBr_gradient_round` | yes | yes | yes | Quot.sound, propext | `#print axioms pgwBr_gradient_round` |
| `pgwBr_loop_diag` | yes | yes | yes | Quot.sound, propext | `#print axioms pgwBr_loop_diag` |
| `pgwBr_loop_not_coboundary` | yes | yes | yes | Quot.sound, propext | `#print axioms pgwBr_loop_not_coboundary` |
| `pgwBr_loop_report` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms pgwBr_loop_report` |
| `pgwBr_shift_preserves` | yes | yes | yes | Quot.sound, propext | `#print axioms pgwBr_shift_preserves` |
| `pgwBr_two_way` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms pgwBr_two_way` |
| `pgwBr_unbalanced` | yes | yes | yes | Quot.sound, propext | `#print axioms pgwBr_unbalanced` |
- counts toward the grade: yes

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/RootGaugeNormalization.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/RootGaugeNormalization.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/RootGaugeNormalization.lean)
- sha256 (`bytes`): `f5903c5710b93073138dc258841b75247dfb4f9a4d9b8cba8975934d000f44a3`
- cited in: node.lean, record TFQ-0555
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/RootGaugeNormalization.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `normal_preserves_round_sums` | yes | yes | yes | - | `#print axioms normal_preserves_round_sums` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_wdp/src/genesis_ongoing_adapter.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/genesis_ongoing_adapter.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `checks/independent/pgw-wdp-bridge-ongoing-to-window.py`

- file: [checks/independent/pgw-wdp-bridge-ongoing-to-window.py](../../../checks/independent/pgw-wdp-bridge-ongoing-to-window.py)
- sha256 (`bytes`): `624e00227b11cb5d4e864730d2baa452c01ba4647e6e7ba9ed05349edd5c1183`
- cited in: record TFQ-0555

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0555_wdp_bridge_ongoing_to_window.md`

- file: [dag/derivations/06_wdp/tfq_0555_wdp_bridge_ongoing_to_window.md](../../../dag/derivations/06_wdp/tfq_0555_wdp_bridge_ongoing_to_window.md)
- sha256 (`lf-normalised`): `b3eee44180d02abe58070b5593013c5b688adf19c8189cd479256fa91a6616e0`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0555
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-wdp-bridge-ongoing-to-window.md`

- file: [dag/derivations/independent/pgw-wdp-bridge-ongoing-to-window.md](../../../dag/derivations/independent/pgw-wdp-bridge-ongoing-to-window.md)
- sha256 (`lf-normalised`): `952cd7b98138e12567899645498237a3c252438d34c7e98977226aa6ed547577`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json`

- file: [dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json](../../../dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json)
- sha256 (`lf-normalised`): `a28bdb68cf56ccf696b7a510f09efc6e16b55ee28eda411fd72c7dca605842d9`
- cited in: node.source
- counts toward the grade: yes

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

## Absences recorded by the TFQ records

- TFQ-0555 python: GEN-WDP-07 carries a written proof and the native omega_wdp adapter; no Python binding

## Routes

Incoming (1):

- `PGW-R-WDP-BRIDGE-ONGOING-TO-WINDOW` `GAP_NO_DERIVATION`: [PGW-WDP-GENESIS-BRIDGES-LEDGER](PGW-WDP-GENESIS-BRIDGES-LEDGER.md) (DEFINITION), [PGW-GO-H3-TWIN-FILLS-HOLONOMY](PGW-GO-H3-TWIN-FILLS-HOLONOMY.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-SYNTHESIS-TRUNK-TIERS` `DERIVED_PROSE`: [PGW-WDP-SYNTHESIS-TRUNK-TIERS](PGW-WDP-SYNTHESIS-TRUNK-TIERS.md) (DEFINITION)
