# PGW-WDP-HANDOFF-TO-L1

Stage: [WDP](../stages/WDP.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Narrowed boundary, status left OPEN. On one triangle with edges (01, 12, 02) and unit integer weights, the coboundary of vertex values (f0, f1, f2) is (f1 - f0, f2 - f1, f2 - f0), and the face of an edge triple (x01, x12, x02) is x01 + x12 - x02. For every integer edge triple and every integer vertex repair, the unit l1 length of the residual is at least the absolute face value. When the face is negative, the repair (0, h01, h01 + h12) leaves residual (0, 0, -face); otherwise the repair (0, h01 - face, h02) leaves residual (face, 0, 0). Both residuals have unit l1 length equal to the absolute face value, so on this triangle that length is the distance to integer coboundaries. A face of 0 means the edge triple is the coboundary of the non-negative repair. Vertex values (0, 1, 0) have coboundary l1 length 2, the edge triple (1, -1, 0) is that coboundary, and the residual of (1, -1, 0) against itself has length 0, so 2 is not the quotient value. The edge triple (1, 0, 0) has face 1. The verdict of (1, 1) is 0 and the verdict of (0, 0) is 1. Equal fibre decisions (1, 1) pass and (0, 1) does not.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 21
- cited Lean declaration references covered by a current replay receipt: 20
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Terminal for the WDP stage on the original window. This triangle case does not identify WDP's quotient value with 007's coboundary length (the LGGR crate's register_stabilized_family consumes verified quotient evidence for ClosedResidual families only), does not make the two window quantities sector weights or a quantum state (TFQ-0004), and does not derive the L1 stage. The weighted certificate over the rationals, the bounded-circulation dual on a general carrier, the LGGR adapter, sector weights, general complexes, and the full diagnostic trichotomy stay open. A face of 0 is an integer coboundary on this triangle only.

## Source status

WDP monograph §4.8 WDP-CH04-D02 vs 007 LGGR series §4 and lesson 1000_01 §3; adapter owed

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwWdpHandoffToL1.lean`

- file: [lean4/CampaignPgwWdpHandoffToL1.lean](../../../lean4/CampaignPgwWdpHandoffToL1.lean)
- sha256 (`bytes`): `76c53d24a47e5ccda8f2c96488dabea2430d984caf7221e2beb3a69dcc221c85`
- cited in: node.lean, receipt dag/research/campaign_pgw-wdp-handoff-to-l1_lean_replay.json (CampaignPgwWdpHandoffToL1), receipt dag/research/pr_358_review_replay.json (CampaignPgwWdpHandoffToL1), record TFQ-0558
- replay: `verified`
  - receipt [dag/research/campaign_pgw-wdp-handoff-to-l1_lean_replay.json](../../../dag/research/campaign_pgw-wdp-handoff-to-l1_lean_replay.json) (module `CampaignPgwWdpHandoffToL1`): recorded sha256 `76c53d24a47e5ccda8f2c96488dabea2430d984caf7221e2beb3a69dcc221c85` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/pr_358_review_replay.json](../../../dag/research/pr_358_review_replay.json) (module `CampaignPgwWdpHandoffToL1`): recorded sha256 `76c53d24a47e5ccda8f2c96488dabea2430d984caf7221e2beb3a69dcc221c85` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwWdpHandoffToL1`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `closed_verdict` | yes | yes | yes | none | `#print axioms closed_verdict` |
| `coboundary_of_repair_vertex` | yes | yes | yes | none | `#print axioms coboundary_of_repair_vertex` |
| `d0_components` | yes | yes | yes | none | `#print axioms d0_components` |
| `distance_at_least` | yes | yes | yes | Quot.sound, propext | `#print axioms distance_at_least` |
| `equal_report_passes` | yes | yes | yes | none | `#print axioms equal_report_passes` |
| `face_of_coboundary` | yes | yes | yes | Quot.sound, propext | `#print axioms face_of_coboundary` |
| `face_of_obstruction` | yes | yes | yes | none | `#print axioms face_of_obstruction` |
| `face_zero_is_coboundary` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms face_zero_is_coboundary` |
| `l1_ge_face` | yes | yes | yes | Quot.sound, propext | `#print axioms l1_ge_face` |
| `leakage_is_not_quotient` | yes | yes | yes | none | `#print axioms leakage_is_not_quotient` |
| `leakage_of_repair_vertex` | yes | yes | yes | none | `#print axioms leakage_of_repair_vertex` |
| `meet_neg` | yes | yes | yes | Quot.sound, propext | `#print axioms meet_neg` |
| `meet_nonneg` | yes | yes | yes | Quot.sound, propext | `#print axioms meet_nonneg` |
| `obstructed_verdict` | yes | yes | yes | none | `#print axioms obstructed_verdict` |
| `quotient_of_that_coboundary` | yes | yes | yes | none | `#print axioms quotient_of_that_coboundary` |
| `repair_picks_neg` | yes | yes | yes | none | `#print axioms repair_picks_neg` |
| `repair_picks_nonneg` | yes | yes | yes | none | `#print axioms repair_picks_nonneg` |
| `repair_residual_neg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms repair_residual_neg` |
| `repair_residual_nonneg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms repair_residual_nonneg` |
| `unequal_report_fails` | yes | yes | yes | none | `#print axioms unequal_report_fails` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_local_green_global_red_lggr/src/ledger.rs`

- file: `omega_engine/crates_rs/omega_local_green_global_red_lggr/src/ledger.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `checks/independent/pgw-wdp-handoff-to-l1.py`

- file: [checks/independent/pgw-wdp-handoff-to-l1.py](../../../checks/independent/pgw-wdp-handoff-to-l1.py)
- sha256 (`bytes`): `17e8d8a3b1f5426719fb9589c850f2eae641474161268e6c1c1d52e65d8dbf17`
- cited in: record TFQ-0558

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0558_wdp_handoff_to_l1.md`

- file: [dag/derivations/06_wdp/tfq_0558_wdp_handoff_to_l1.md](../../../dag/derivations/06_wdp/tfq_0558_wdp_handoff_to_l1.md)
- sha256 (`lf-normalised`): `3b41067f5659cf04b63ae8632c45b655764838e6ff01f144ccc7914050bdedc5`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0558
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-wdp-handoff-to-l1.md`

- file: [dag/derivations/independent/pgw-wdp-handoff-to-l1.md](../../../dag/derivations/independent/pgw-wdp-handoff-to-l1.md)
- sha256 (`lf-normalised`): `df7ced669ccd6f3ba56a9f5d323987587c30a9d681f09d9978f8704b28d06d6e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-wdp-handoff-to-l1_lean_replay.json`

- file: [dag/research/campaign_pgw-wdp-handoff-to-l1_lean_replay.json](../../../dag/research/campaign_pgw-wdp-handoff-to-l1_lean_replay.json)
- sha256 (`lf-normalised`): `fca23581df4e7ac69a1504f254d424f9a0b73f1e1514f2e4d2d3e8e6931bd826`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/007_oelggr/curriculum/1000_local_green_global_red_foundations/concepts/lesson_1000_01_local_green_global_red_foundations.md`

- file: `omega_engine_education/documentation/007_oelggr/curriculum/1000_local_green_global_red_foundations/concepts/lesson_1000_01_local_green_global_red_foundations.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/007_oelggr/local_green_global_red_foundational_series.md`

- file: `omega_engine_education/documentation/007_oelggr/local_green_global_red_foundational_series.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine/crates_rs/omega_local_green_global_red_lggr/src/ledger.rs::register_stabilized_family`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/obstruction.py::obstruction_signature`

## Routes

Incoming (1):

- `PGW-R-WDP-HANDOFF-TO-L1` `GAP_NO_DERIVATION`: [PGW-WDP-SYNTHESIS-TRUNK-TIERS](PGW-WDP-SYNTHESIS-TRUNK-TIERS.md) (DEFINITION)

Outgoing (0):

