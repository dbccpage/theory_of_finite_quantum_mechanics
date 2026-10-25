# PGW-WDP-BRIDGE-ONGOING-TO-WINDOW

Stage: [WDP](../stages/WDP.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Narrowed in Lean 4 to the carrier {0, 1}. The directed slots are e(0,0), e(1,1), e(0,1) and e(1,0). The coboundary of vertex values (g0, g1) is (0, 0, g0 - g1, g1 - g0). The unbalanced mark (0, 1, 0) has diagnostic e(0,1) + e(1,0) + e(0,0). That diagnostic is 0 on every coboundary and is unchanged when a coboundary is added. If a nonzero integer b scales an integer slot difference onto a coboundary, the difference is already the integer coboundary of (0, -d01). The table (1, 0, 0, -1) has diagnostic 0 and is not a coboundary. The table (0, 1, 0, 0) has diagnostic 0 and is not a coboundary. The one-arc table (0, 0, 1, 0) has diagnostic 1. The two-way table (0, 0, 1, 1) has arc sum 2 and arc difference 0. A general carrier, an arbitrary marked family, the degree-1 window of TFQ-0004, a continuous norm, and carrier-changing term operations stay open.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 13
- cited Lean declaration references covered by a current replay receipt: 11
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Fixed carrier and declared marked triples F from the chosen Genesis Ongoing source contexts (assumption)

## Bottleneck

Open. One two-vertex carrier is checked. The coboundary cancellation, the denominator reflection, the two kernel witnesses, the one-arc diagnostic, and the two-way sum are checked. A general carrier, an arbitrary marked family, the window of TFQ-0004, a continuous norm, and carrier-changing term operations stay open.

## Source status

docs/genesis_to_wdp_derivation_programme.md §4 and register GEN-WDP-07 (conditional, fixed carrier); bridge to the window owed

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwWdpBridgeOngoing.lean`

- file: [lean4/CampaignPgwWdpBridgeOngoing.lean](../../../lean4/CampaignPgwWdpBridgeOngoing.lean)
- sha256 (`bytes`): `70b6d1d23be815c94d992e1b1c3c50617997cdf2f139ef7c41ef9c3d6e68281a`
- cited in: node.lean, receipt dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json (CampaignPgwWdpBridgeOngoing), receipt dag/research/pr_357_review_replay.json (CampaignPgwWdpBridgeOngoing), record TFQ-0555
- replay: `verified`
  - receipt [dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json](../../../dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json) (module `CampaignPgwWdpBridgeOngoing`): recorded sha256 `70b6d1d23be815c94d992e1b1c3c50617997cdf2f139ef7c41ef9c3d6e68281a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_357_review_replay.json](../../../dag/research/pr_357_review_replay.json) (module `CampaignPgwWdpBridgeOngoing`): recorded sha256 `70b6d1d23be815c94d992e1b1c3c50617997cdf2f139ef7c41ef9c3d6e68281a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwWdpBridgeOngoing`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `cob_slots` | yes | yes | yes | none | `#print axioms cob_slots` |
| `compensated_loop_closed` | yes | yes | yes | none | `#print axioms compensated_loop_closed` |
| `compensated_loop_not_coboundary` | yes | yes | yes | Quot.sound, propext | `#print axioms compensated_loop_not_coboundary` |
| `denominator_clears` | yes | yes | yes | Quot.sound, propext | `#print axioms denominator_clears` |
| `diag_after_repair` | yes | yes | yes | Quot.sound, propext | `#print axioms diag_after_repair` |
| `diag_on_coboundary` | yes | yes | yes | Quot.sound, propext | `#print axioms diag_on_coboundary` |
| `one_arc_diagnostic` | yes | yes | yes | none | `#print axioms one_arc_diagnostic` |
| `silent_loop_closed` | yes | yes | yes | none | `#print axioms silent_loop_closed` |
| `silent_loop_not_coboundary` | yes | yes | yes | Quot.sound, propext | `#print axioms silent_loop_not_coboundary` |
| `two_way_difference` | yes | yes | yes | none | `#print axioms two_way_difference` |
| `two_way_sum` | yes | yes | yes | none | `#print axioms two_way_sum` |

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
- sha256 (`bytes`): `001c05df4170a358473308c57bbe9c11be46201a6c2dd4e2ad91582d6e4b7d1c`
- cited in: record TFQ-0555

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0555_wdp_bridge_ongoing_to_window.md`

- file: [dag/derivations/06_wdp/tfq_0555_wdp_bridge_ongoing_to_window.md](../../../dag/derivations/06_wdp/tfq_0555_wdp_bridge_ongoing_to_window.md)
- sha256 (`lf-normalised`): `6adcdc2b55a098a79115cddc98c2692ddf78d1a69efb1dfa80788f167fc719c7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0555
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-wdp-bridge-ongoing-to-window.md`

- file: [dag/derivations/independent/pgw-wdp-bridge-ongoing-to-window.md](../../../dag/derivations/independent/pgw-wdp-bridge-ongoing-to-window.md)
- sha256 (`lf-normalised`): `a9d56a8a8799692e0a9002db1fa44b6baba175ee7e35fa026500f9efac47569f`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json`

- file: [dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json](../../../dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json)
- sha256 (`lf-normalised`): `41e1e2fc219982a3db616fd8080b0b9ede517c31e7fb877c476edc895bdb208c`
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

## Routes

Incoming (1):

- `PGW-R-WDP-BRIDGE-ONGOING-TO-WINDOW` `GAP_NO_DERIVATION`: [PGW-WDP-GENESIS-BRIDGES-LEDGER](PGW-WDP-GENESIS-BRIDGES-LEDGER.md) (DEFINITION), [PGW-GO-H3-TWIN-FILLS-HOLONOMY](PGW-GO-H3-TWIN-FILLS-HOLONOMY.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-SYNTHESIS-TRUNK-TIERS` `DERIVED_PROSE`: [PGW-WDP-SYNTHESIS-TRUNK-TIERS](PGW-WDP-SYNTHESIS-TRUNK-TIERS.md) (DEFINITION)
