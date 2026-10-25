# PGW-WDP-HANDOFF-TO-L1

Stage: [WDP](../stages/WDP.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On vertices 0, 1, 2 with values (0, 1, 0), the coboundary in slot order (01, 12, 02) is (1, -1, 0). Its L1 norm is 2. Subtracting that coboundary leaves residual (0, 0, 0), whose L1 norm is 0, and 0 is at most every natural number, so this repair cost is a minimum. The leakage number 2 is not that minimum. The oriented sum 1 + (-1) - 0 equals 0.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 15
- cited Lean declarations covered by a current replay receipt: 14
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

This is one exact coboundary on three vertices. It does not certify weighted l1 over the rationals by a bounded circulation, does not identify a general quotient with the 007 leakage formula, does not make sector weights or a quantum state (TFQ-0004), and does not derive the L1 stage. The observer fibre discipline and the LGGR local-pass global-fail refusal stay open.

## Source status

WDP monograph §4.8 WDP-CH04-D02 vs 007 LGGR series §4 and lesson 1000_01 §3; adapter owed

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignPgwWdpHandoffToL1.lean`

- file: [lean4/CampaignPgwWdpHandoffToL1.lean](../../../lean4/CampaignPgwWdpHandoffToL1.lean)
- sha256 (`bytes`): `1e7dc5bae582d57721e5f841970a4fc45899796995469b50b67d3deb0989613d`
- cited in: node.lean, node.source, receipt dag/research/campaign_pgw-wdp-handoff-to-l1_lean_replay.json (CampaignPgwWdpHandoffToL1), record TFQ-0558
- replay: `verified`
  - receipt [dag/research/campaign_pgw-wdp-handoff-to-l1_lean_replay.json](../../../dag/research/campaign_pgw-wdp-handoff-to-l1_lean_replay.json) (module `CampaignPgwWdpHandoffToL1`): recorded sha256 `1e7dc5bae582d57721e5f841970a4fc45899796995469b50b67d3deb0989613d` matches the current file; exit code 0; Lean Lean 4.35.0 (eb6cafb7290e8bd5f2937522d8d804f58f02bafc); Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignPgwWdpHandoffToL1`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignPgwWdpHandoffToL1.pgwHo_coboundary` | yes | yes | yes | none | `#print axioms CampaignPgwWdpHandoffToL1.pgwHo_coboundary` |
| `CampaignPgwWdpHandoffToL1.pgwHo_leakage` | yes | yes | yes | none | `#print axioms CampaignPgwWdpHandoffToL1.pgwHo_leakage` |
| `CampaignPgwWdpHandoffToL1.pgwHo_leakage_not_min` | yes | yes | yes | none | `#print axioms CampaignPgwWdpHandoffToL1.pgwHo_leakage_not_min` |
| `CampaignPgwWdpHandoffToL1.pgwHo_oriented` | yes | yes | yes | none | `#print axioms CampaignPgwWdpHandoffToL1.pgwHo_oriented` |
| `CampaignPgwWdpHandoffToL1.pgwHo_repair` | yes | yes | yes | none | `#print axioms CampaignPgwWdpHandoffToL1.pgwHo_repair` |
| `CampaignPgwWdpHandoffToL1.pgwHo_residual_l1` | yes | yes | yes | none | `#print axioms CampaignPgwWdpHandoffToL1.pgwHo_residual_l1` |
| `CampaignPgwWdpHandoffToL1.pgwHo_zero_le` | yes | yes | yes | none | `#print axioms CampaignPgwWdpHandoffToL1.pgwHo_zero_le` |
| `pgwHo_coboundary` | yes | yes | yes | none | `#print axioms pgwHo_coboundary` |
| `pgwHo_leakage` | yes | yes | yes | none | `#print axioms pgwHo_leakage` |
| `pgwHo_leakage_not_min` | yes | yes | yes | none | `#print axioms pgwHo_leakage_not_min` |
| `pgwHo_oriented` | yes | yes | yes | none | `#print axioms pgwHo_oriented` |
| `pgwHo_repair` | yes | yes | yes | none | `#print axioms pgwHo_repair` |
| `pgwHo_residual_l1` | yes | yes | yes | none | `#print axioms pgwHo_residual_l1` |
| `pgwHo_zero_le` | yes | yes | yes | none | `#print axioms pgwHo_zero_le` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_local_green_global_red_lggr/src/ledger.rs`

- file: `omega_engine/crates_rs/omega_local_green_global_red_lggr/src/ledger.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `checks/independent/pgw-wdp-handoff-to-l1.py`

- file: [checks/independent/pgw-wdp-handoff-to-l1.py](../../../checks/independent/pgw-wdp-handoff-to-l1.py)
- sha256 (`bytes`): `25a32f4e18cef4e536f70dab0a99c4efdfa63762321739a544470d1482cc2002`
- cited in: node.source, record TFQ-0558

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0558_wdp_handoff_to_l1.md`

- file: [dag/derivations/06_wdp/tfq_0558_wdp_handoff_to_l1.md](../../../dag/derivations/06_wdp/tfq_0558_wdp_handoff_to_l1.md)
- sha256 (`lf-normalised`): `561fa31aea66b8377f3af72017143860b8dc205873dff5e722f402b1d06c5360`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0558
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-wdp-handoff-to-l1.md`

- file: [dag/derivations/independent/pgw-wdp-handoff-to-l1.md](../../../dag/derivations/independent/pgw-wdp-handoff-to-l1.md)
- sha256 (`lf-normalised`): `8d1216ed8d42213484db016d1f965a40930a236585a0182743c5de1c3cc588a0`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-wdp-handoff-to-l1_lean_replay.json`

- file: [dag/research/campaign_pgw-wdp-handoff-to-l1_lean_replay.json](../../../dag/research/campaign_pgw-wdp-handoff-to-l1_lean_replay.json)
- sha256 (`lf-normalised`): `e965d8337389e7794973120cd056a8964b036498d50099e285adf4a1656c1aad`
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

## Absences recorded by the TFQ records

- TFQ-0558 lean4: no Lean statement of an adapter from the WDP quotient Phi1 to the LGGR evaluator defect

## Routes

Incoming (1):

- `PGW-R-WDP-HANDOFF-TO-L1` `GAP_NO_DERIVATION`: [PGW-WDP-SYNTHESIS-TRUNK-TIERS](PGW-WDP-SYNTHESIS-TRUNK-TIERS.md) (DEFINITION)

Outgoing (0):

