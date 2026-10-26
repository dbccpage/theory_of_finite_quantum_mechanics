# PGW-WDP-HANDOFF-TO-L1

Stage: [WDP](../stages/WDP.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP hands onward a declared, certified degree-1 window: Φ₁(\[h\]) = Φ_J(\[h\]), the quotient infimum over repairs, certified for weighted ℓ¹ over ℚ by a matching repair and bounded circulation; Γ₂(\[h\]) = ‖d₁h‖₁; the diagnostic trichotomy; and the observer discipline that a protected question passes through a report only when constant on its fibres. The 007 Local-Green/Global-Red series refuses the case in which every local check passes and the global check fails, and its Symbol Game integration sets the global verdict to 0 when Φ₁ \> 0 or Γ₂ \> 0, but it writes Φ₁(h) = ‖d₀h‖₁ (boundary leakage), which is not WDP's quotient infimum. The 007 lesson states that no automatic identification with the PFP quantities phi1 or gamma2 is supplied, so an adapter from WDP's quotient Φ₁ and Γ₂ to the LGGR global evaluator is owed. The DAG's next stage is L1_EMERGENCE (TFQ-0005 declared L1 sector weights, TFQ-0349).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 22
- distinct cited Lean declarations covered by a current replay receipt: 20
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

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

### Python: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py)
- sha256 (`bytes`): `2c39d5d66e90bfe5675526a4018e66a8290aa1daef019fdaceb85c4326a356d1`
- cited in: record TFQ-0558

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `obstruction_signature` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/pgw-wdp-handoff-to-l1.py`

- file: [checks/independent/pgw-wdp-handoff-to-l1.py](../../../checks/independent/pgw-wdp-handoff-to-l1.py)
- sha256 (`bytes`): `17e8d8a3b1f5426719fb9589c850f2eae641474161268e6c1c1d52e65d8dbf17`
- cited in: record TFQ-0558

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0558_wdp_handoff_to_l1.md`

- file: [dag/derivations/06_wdp/tfq_0558_wdp_handoff_to_l1.md](../../../dag/derivations/06_wdp/tfq_0558_wdp_handoff_to_l1.md)
- sha256 (`lf-normalised`): `1274b1cbd19efef0473fb28c2e1f182fff23d36c17e154161b17d3eae7b69bf9`
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

- `external:upstream/omega_engine/crates_rs/omega_local_green_global_red_lggr/src/ledger.rs::register_stabilized_family`

## Routes

Incoming (1):

- `PGW-R-WDP-HANDOFF-TO-L1` `GAP_NO_DERIVATION`: [PGW-WDP-SYNTHESIS-TRUNK-TIERS](PGW-WDP-SYNTHESIS-TRUNK-TIERS.md) (DEFINITION)

Outgoing (0):

