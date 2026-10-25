# PGW-WDP-BRIDGE-REPORT-FIBER-OBSERVER

Stage: [WDP](../stages/WDP.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> GEN-WDP-03: with actual cases X, a declared evaluation report E: X → Reports and a protected admission or permission decision A: X → Decisions, a decoder on the actual image of E exists exactly when E(x) = E(y) implies A(x) = A(y); necessity applies the decoder to equal reports, sufficiency assigns each occupied report the decision of any representative, and equal reports with unequal decisions forbid every decoder and every report-only postprocessor. GEN-WDP-06 records that event multisets can lose final state, final states can lose occurrence counts, and fresh hashes can bind false receipts. This is the fibre criterion of the S(n)/MSS-N hand-off (TFQ-0338) and of WDP adapter descent (TFQ-0553), so a protected question passes from the realized report to a WDP observer exactly when it is constant on the fibres of the declared report.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declaration references covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared report map from the S(n)/MSS-N realized report image to the WDP observer presentation, with the protected decision on the actual cases (assumption)

## Bottleneck

Conditional on the declared report and protected question; the criterion derives no evaluator, grantor or permission, and a successful evaluation alone does not determine authorization (GEN-WDP-04).

## Source status

register GEN-WDP-03/06 with Lean ProposalAdmissionBridge; conditional on the declared report

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

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

### Documents and data: `dag/derivations/06_wdp/tfq_0556_wdp_bridge_report_fiber_observer.md`

- file: [dag/derivations/06_wdp/tfq_0556_wdp_bridge_report_fiber_observer.md](../../../dag/derivations/06_wdp/tfq_0556_wdp_bridge_report_fiber_observer.md)
- sha256 (`lf-normalised`): `19e8eef4aac1da065dcadc14737026f1d87ede48e2763d090d83eabaacc54c2e`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0556
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_bridge_register.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_bridge_register.md`
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

- `external:the_symbol_game/omega_engine/crates_rs/omega_wdp/src/proposal_admission_bridge.rs::ProposalAdmissionModel`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/proposal_admission_bridge.py::decision_decoder`

## Routes

Incoming (1):

- `PGW-R-WDP-BRIDGE-REPORT-FIBER-OBSERVER` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-GENESIS-BRIDGES-LEDGER](PGW-WDP-GENESIS-BRIDGES-LEDGER.md) (DEFINITION), [PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY](PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY.md) (DEFINITION)

Outgoing (3):

- `APP-R-AUTHF-LOGICAL-EXTERNALITY` `DERIVED_LEAN`: [AUTHF-LOGICAL-EXTERNALITY](AUTHF-LOGICAL-EXTERNALITY.md) (PROVED_LEAN)
- `APP-R-AUTHF-SELF-RECEIPT-TOY` `DERIVED_LEAN`: [AUTHF-SELF-RECEIPT-TOY](AUTHF-SELF-RECEIPT-TOY.md) (PROVED_LEAN)
- `PGW-R-WDP-SYNTHESIS-TRUNK-TIERS` `DERIVED_PROSE`: [PGW-WDP-SYNTHESIS-TRUNK-TIERS](PGW-WDP-SYNTHESIS-TRUNK-TIERS.md) (DEFINITION)
