# PGW-WDP-BRIDGE-REPORT-FIBER-OBSERVER

Stage: [WDP](../stages/WDP.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> GEN-WDP-03: with actual cases X, a declared evaluation report E: X → Reports and a protected admission or permission decision A: X → Decisions, a decoder on the actual image of E exists exactly when E(x) = E(y) implies A(x) = A(y); necessity applies the decoder to equal reports, sufficiency assigns each occupied report the decision of any representative, and equal reports with unequal decisions forbid every decoder and every report-only postprocessor. GEN-WDP-06 records that event multisets can lose final state, final states can lose occurrence counts, and fresh hashes can bind false receipts. This is the fibre criterion of the S(n)/MSS-N hand-off (TFQ-0338) and of WDP adapter descent (TFQ-0553), so a protected question passes from the realized report to a WDP observer exactly when it is constant on the fibres of the declared report.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 8
- cited Lean, Rust or Python symbols found in their in-repo files: 9
- distinct cited Lean declarations covered by a current replay receipt: 8
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared report map from the S(n)/MSS-N realized report image to the WDP observer presentation, with the protected decision on the actual cases (assumption)

## Bottleneck

The maps are declared. The result constructs no evaluator, permission grantor or physical authenticity test. The decoder is classical/noncomputable in general. Unused reports require no default value, and the empty case is included. Original target retained as an obligation: GEN-WDP-03: with actual cases X, a declared evaluation report E: X → Reports and a protected admission or permission decision A: X → Decisions, a decoder on the actual image of E exists exactly when E(x) = E(y) implies A(x) = A(y); necessity applies the decoder to equal reports, sufficiency assigns each occupied report the decision of any representative, and equal reports with unequal decisions forbid every decoder and every report-only postprocessor. GEN-WDP-06 records that event multisets can lose final state, final states can lose occurrence counts, and fresh hashes can bind false receipts. This is the fibre criterion of the S(n)/MSS-N hand-off (TFQ-0338) and of WDP adapter descent (TFQ-0553), so a protected question passes from the realized report to a WDP observer exactly when it is constant on the fibres of the declared report. Prior boundary: Conditional on the declared report and protected question; the criterion derives no evaluator, grantor or permission, and a successful evaluation alone does not determine authorization (GEN-WDP-04).

## Source status

register GEN-WDP-03/06 with Lean ProposalAdmissionBridge; conditional on the declared report

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignReportFiberDescent.lean`

- file: [lean4/CampaignReportFiberDescent.lean](../../../lean4/CampaignReportFiberDescent.lean)
- sha256 (`bytes`): `135356388ee6294757c800db5b96c6d0e9ba670695346c6f7ad44cd469b89b56`
- cited in: node.lean, receipt dag/research/campaign_pgw-wdp-bridge-report-fiber-observer_lean_replay.json (CampaignReportFiberDescent), receipt dag/research/pr_380_round2_replay.json (CampaignReportFiberDescent), record TFQ-0556
- replay: `verified`
  - receipt [dag/research/campaign_pgw-wdp-bridge-report-fiber-observer_lean_replay.json](../../../dag/research/campaign_pgw-wdp-bridge-report-fiber-observer_lean_replay.json) (module `CampaignReportFiberDescent`): recorded sha256 `135356388ee6294757c800db5b96c6d0e9ba670695346c6f7ad44cd469b89b56` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound; only standard axioms: yes
  - receipt [dag/research/pr_380_round2_replay.json](../../../dag/research/pr_380_round2_replay.json) (module `CampaignReportFiberDescent`): recorded sha256 `135356388ee6294757c800db5b96c6d0e9ba670695346c6f7ad44cd469b89b56` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound; only standard axioms: yes
- check: `cd lean4 && lake build CampaignReportFiberDescent`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignReportFiberDescent.ConstantOnFibers` | yes | yes | yes | none | `#print axioms CampaignReportFiberDescent.ConstantOnFibers` |
| `CampaignReportFiberDescent.Image` | yes | yes | yes | none | `#print axioms CampaignReportFiberDescent.Image` |
| `CampaignReportFiberDescent.joint_report_sufficient` | yes | yes | yes | none | `#print axioms CampaignReportFiberDescent.joint_report_sufficient` |
| `CampaignReportFiberDescent.lifted` | yes | yes | yes | none | `#print axioms CampaignReportFiberDescent.lifted` |
| `CampaignReportFiberDescent.lost_bit_obstruction` | yes | yes | yes | none | `#print axioms CampaignReportFiberDescent.lost_bit_obstruction` |
| `CampaignReportFiberDescent.postprocess_obstruction` | yes | yes | yes | none | `#print axioms CampaignReportFiberDescent.postprocess_obstruction` |
| `CampaignReportFiberDescent.unique_decoder_iff` | yes | yes | yes | Classical.choice, Quot.sound | `#print axioms CampaignReportFiberDescent.unique_decoder_iff` |

- counts toward the grade: yes

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/ProposalAdmissionBridge.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/ProposalAdmissionBridge.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/ProposalAdmissionBridge.lean)
- sha256 (`bytes`): `dcf643dc81f991c62aedc6ce427ba87bfde4e5ff1103d15195009cfa7007a822`
- cited in: node.lean, record TFQ-0556
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_pregenesis.json](../../../dag/research/lean_replay_campaign_pregenesis.json) (module `Imported.WitnessedDifference.WitnessedDifference.ProposalAdmissionBridge`): recorded sha256 `dcf643dc81f991c62aedc6ce427ba87bfde4e5ff1103d15195009cfa7007a822` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/ProposalAdmissionBridge.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `factorization_iff_fiber_constancy` | yes | yes | yes | Classical.choice | `#print axioms factorization_iff_fiber_constancy` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_wdp/src/proposal_admission_bridge.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/proposal_admission_bridge.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/proposal_admission_bridge.py`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/proposal_admission_bridge.py](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/proposal_admission_bridge.py)
- sha256 (`bytes`): `fc57a8f34d30455f85dd5f87ec439c6b89b532f45a0e214f0293812632a166f2`
- cited in: record TFQ-0556

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `decision_decoder` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `checks/independent/pgw-wdp-bridge-report-fiber-observer.py`

- file: [checks/independent/pgw-wdp-bridge-report-fiber-observer.py](../../../checks/independent/pgw-wdp-bridge-report-fiber-observer.py)
- sha256 (`bytes`): `c7990400af7bea437cd1760f181c2f681834b89d909e82b04f552fa14d505a50`
- cited in: record TFQ-0556
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_bridge_register.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_bridge_register.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_bridge_register.md)
- sha256 (`lf-normalised`): `e411f9eace9de18c2583922d16d85be03fcbe4c35976ca3d7a33a0c3cfdea143`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md)
- sha256 (`lf-normalised`): `616280b727abb20440caea09709a0e8f5512fbc8de20da8a3db124de2dc262ff`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0556_wdp_bridge_report_fiber_observer.md`

- file: [dag/derivations/06_wdp/tfq_0556_wdp_bridge_report_fiber_observer.md](../../../dag/derivations/06_wdp/tfq_0556_wdp_bridge_report_fiber_observer.md)
- sha256 (`lf-normalised`): `521e481b359cf38d54b8df7be4dd82e996757c71f215f991af86bffd7ac224f9`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0556
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/pgw-wdp-bridge-report-fiber-observer.md`

- file: [dag/derivations/independent/pgw-wdp-bridge-report-fiber-observer.md](../../../dag/derivations/independent/pgw-wdp-bridge-report-fiber-observer.md)
- sha256 (`lf-normalised`): `fbb509b3be63cfe7d2b150e228deee54d05c690ff312f2f00352f849cba89255`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_pgw-wdp-bridge-report-fiber-observer_lean_replay.json`

- file: [dag/research/campaign_pgw-wdp-bridge-report-fiber-observer_lean_replay.json](../../../dag/research/campaign_pgw-wdp-bridge-report-fiber-observer_lean_replay.json)
- sha256 (`lf-normalised`): `8e190dbfdaaccca9127a1b1da7f41cd30b457d2905a09c295d94a3247f773e52`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `omega_engine_education/documentation/006_oewdp/levels/level_22_genesis_to_wdp_bridges.md`

- file: `omega_engine_education/documentation/006_oewdp/levels/level_22_genesis_to_wdp_bridges.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:upstream/omega_engine/crates_rs/omega_wdp/src/proposal_admission_bridge.rs::ProposalAdmissionModel`

## Routes

Incoming (1):

- `PGW-R-WDP-BRIDGE-REPORT-FIBER-OBSERVER` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-GENESIS-BRIDGES-LEDGER](PGW-WDP-GENESIS-BRIDGES-LEDGER.md) (DEFINITION), [PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY](PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY.md) (DEFINITION)

Outgoing (3):

- `APP-R-AUTHF-LOGICAL-EXTERNALITY` `DERIVED_LEAN`: [AUTHF-LOGICAL-EXTERNALITY](AUTHF-LOGICAL-EXTERNALITY.md) (PROVED_LEAN)
- `APP-R-AUTHF-SELF-RECEIPT-TOY` `DERIVED_LEAN`: [AUTHF-SELF-RECEIPT-TOY](AUTHF-SELF-RECEIPT-TOY.md) (PROVED_LEAN)
- `PGW-R-WDP-SYNTHESIS-TRUNK-TIERS` `DERIVED_PROSE`: [PGW-WDP-SYNTHESIS-TRUNK-TIERS](PGW-WDP-SYNTHESIS-TRUNK-TIERS.md) (DEFINITION)
