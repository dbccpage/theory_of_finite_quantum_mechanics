# PGW-WDP-BRIDGE-ONGOING-TO-WINDOW

Stage: [WDP](../stages/WDP.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> GEN-WDP-07, a conditional theorem in the bridge register, fixes a carrier and marked triples F, keeps the full directed integer table e(x, y) = M_r(x, y) − M_s(x, y) including loops and independent reverse arcs, treats raising as e ↦ e + d₀g with (d₀g)(x, y) = g(x) − g(y), and uses the marked diagnostic D_F(e)(x, y, z) = e(x, y) + e(y, z) + e(z, x). Cancellation gives D_F d₀ = 0, so D_F(e + d₀g) = D_F e even for unbalanced triples, and rationalizing reflects integer repair equality. This is a repair quotient with descending reports, not automatically cohomology: C¹/im d₀ differs from ker D_F/im d₀, a filled mark may be unbalanced, triangle reports miss loops and two-way defects, and antisymmetric simplicial coordinates need e(x, x) = 0 and e(x, y) + e(y, x) = 0. Term addition and identification can fail to respect the quotient (source 23:D4), so carrier-changing operations need new congruence proofs.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 13
- distinct cited Lean declarations covered by a current replay receipt: 11
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

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/RootGaugeNormalization.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/RootGaugeNormalization.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/RootGaugeNormalization.lean)
- sha256 (`bytes`): `8b0940cfef8dfc04b1bfab85b772afeab1b45a67baf0d263f9e7c6550237763d`
- cited in: node.lean, record TFQ-0555
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/RootGaugeNormalization.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `normal_preserves_round_sums` | yes | yes | yes | - | `#print axioms normal_preserves_round_sums` |

- counts toward the grade: yes

### Lean: `lean4/PregenesisWdpBridgeOngoing.lean`

- file: [lean4/PregenesisWdpBridgeOngoing.lean](../../../lean4/PregenesisWdpBridgeOngoing.lean)
- sha256 (`bytes`): `70b6d1d23be815c94d992e1b1c3c50617997cdf2f139ef7c41ef9c3d6e68281a`
- cited in: node.lean, receipt dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json (PregenesisWdpBridgeOngoing), receipt dag/research/pr_357_review_replay.json (PregenesisWdpBridgeOngoing), record TFQ-0555
- replay: `verified`
  - receipt [dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json](../../../dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json) (module `PregenesisWdpBridgeOngoing`): recorded sha256 `70b6d1d23be815c94d992e1b1c3c50617997cdf2f139ef7c41ef9c3d6e68281a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_357_review_replay.json](../../../dag/research/pr_357_review_replay.json) (module `PregenesisWdpBridgeOngoing`): recorded sha256 `70b6d1d23be815c94d992e1b1c3c50617997cdf2f139ef7c41ef9c3d6e68281a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build PregenesisWdpBridgeOngoing`

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

### Python: `checks/independent/pgw-wdp-bridge-ongoing-to-window.py`

- file: [checks/independent/pgw-wdp-bridge-ongoing-to-window.py](../../../checks/independent/pgw-wdp-bridge-ongoing-to-window.py)
- sha256 (`bytes`): `001c05df4170a358473308c57bbe9c11be46201a6c2dd4e2ad91582d6e4b7d1c`
- cited in: record TFQ-0555

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_ongoing_fixed_carrier_bridge.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_ongoing_fixed_carrier_bridge.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_ongoing_fixed_carrier_bridge.md)
- sha256 (`lf-normalised`): `491de41d4978bbcdcd06c9857515113700be95b53e2a3700fe0ce540588036f7`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md)
- sha256 (`lf-normalised`): `616280b727abb20440caea09709a0e8f5512fbc8de20da8a3db124de2dc262ff`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0555_wdp_bridge_ongoing_to_window.md`

- file: [dag/derivations/06_wdp/tfq_0555_wdp_bridge_ongoing_to_window.md](../../../dag/derivations/06_wdp/tfq_0555_wdp_bridge_ongoing_to_window.md)
- sha256 (`lf-normalised`): `88162dd3b70af4751f5b980f7bac5dea896284ea820f1ef5a60356a07675041e`
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
- sha256 (`lf-normalised`): `b76132c50ae7b593cba4a85ecc8a0b97ab0256cd706e1632bf63705de9c8a65d`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:718c4c7d2dba17c2e8b55676b4edd2c41584c55fee175f1e129c8df01769c0bf::GenesisOngoingAdapter`
- `external:sha256:a11697dcdf5788b476d5c2e541b635a81c03e665684f69bd260bc463a03ee458:116-137`
- `external:upstream/external:sha256:718c4c7d2dba17c2e8b55676b4edd2c41584c55fee175f1e129c8df01769c0bf::GenesisOngoingAdapter`

## Routes

Incoming (1):

- `PGW-R-WDP-BRIDGE-ONGOING-TO-WINDOW` `GAP_NO_DERIVATION`: [PGW-WDP-GENESIS-BRIDGES-LEDGER](PGW-WDP-GENESIS-BRIDGES-LEDGER.md) (DEFINITION), [PGW-GO-H3-TWIN-FILLS-HOLONOMY](PGW-GO-H3-TWIN-FILLS-HOLONOMY.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-SYNTHESIS-TRUNK-TIERS` `DERIVED_PROSE`: [PGW-WDP-SYNTHESIS-TRUNK-TIERS](PGW-WDP-SYNTHESIS-TRUNK-TIERS.md) (DEFINITION)
