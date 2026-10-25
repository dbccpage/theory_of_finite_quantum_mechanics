# DS-QM103-SHOW-THE-PACKET-PROTOCOL

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A scalable physical-QC claim is terminalized only when it exposes the declared finite evidence packet fields; refusal terminals include NoHumanSignificantScale and ClaimOverreach. Open: lambda vs mu growth, decoder throughput, leakage tails, p_pair -\> 0, overhead (QM-101-C10 as labelled in the 103 ledger).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Rotated-surface-code packet is an illustrative placeholder (no measured numbers).

## Source status

\[DEFINITION / OPERATIONAL RULE\] (QM-103 ledger rows are labelled QM-101-C1..C14, a labeling clash)

## Review

- PFP review: [dag/results/DS-QM103-SHOW-THE-PACKET-PROTOCOL/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/DS-QM103-SHOW-THE-PACKET-PROTOCOL/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `DEFINITION`; qualifies for E4: yes.
  - narrowest claim: Exact field-completeness/scale/refusal controls are checked; presence of fields is not logical validation of their contents.
  - does not support: Provide substantive verified packet contents and meaningful scale/noise/throughput/leakage/overhead evidence. Eligibility for audit is not a physical or authority terminal.
  - next test: Provide substantive verified packet contents and meaningful scale/noise/throughput/leakage/overhead evidence. Eligibility for audit is not a physical or authority terminal.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall` |
| `QuantumMechanics.DerivationDagQMClosure.qm090_authority_firewall_zero_defect_iff` | yes | yes | yes | propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm090_authority_firewall_zero_defect_iff` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/13_finite_qm_information/tfq_0271_show_the_packet_protocol_for_a_finite_computation.md`

- file: [dag/derivations/13_finite_qm_information/tfq_0271_show_the_packet_protocol_for_a_finite_computation.md](../../../dag/derivations/13_finite_qm_information/tfq_0271_show_the_packet_protocol_for_a_finite_computation.md)
- sha256 (`lf-normalised`): `6825eba11bad81327a12c685a56130cad70a5ec743ea5e249dd6593541e3e918`
- generated view: listed, not counted
- cited in: record TFQ-0271
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/103_show_the_packet_protocol/qm_103_show_the_packet_protocol_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/103_show_the_packet_protocol/qm_103_show_the_packet_protocol_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0271 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm

## Routes

Incoming (1):

- `DS-R-PACKET` `DERIVED_LEAN`: [DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE](DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-QCV-PHYSICAL-SATISFIABILITY-OPEN` `GAP_NO_DERIVATION`: [QCV-PHYSICAL-SATISFIABILITY-OPEN](QCV-PHYSICAL-SATISFIABILITY-OPEN.md) (OPEN)
