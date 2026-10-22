# DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact Kraus completeness, channel outputs, stochastic kernel and same-diagonal distinct-output controls are retained; scalar Cayley and population conservation are kernel checked.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- basis choice and diagonal read (lift)
- Kraus operators (assumption)

## Bottleneck

Unmet after the PFP review: Formalize all matrix/Kraus/tensor positivity transports and physical channel admission. Basis-relative stochastic shadows do not select a unique quantum channel. The broader source statement is kept in pfp_review.prior_statement.

## Source status

\[PROVEN, MECHANIZED\] ENC-1127 (QM-082-C4)

## Review

- PFP review: [dag/results/DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact Kraus completeness, channel outputs, stochastic kernel and same-diagonal distinct-output controls are retained; scalar Cayley and population conservation are kernel checked.
  - does not support: Formalize all matrix/Kraus/tensor positivity transports and physical channel admission. Basis-relative stochastic shadows do not select a unique quantum channel.
  - next test: Formalize all matrix/Kraus/tensor positivity transports and physical channel admission. Basis-relative stochastic shadows do not select a unique quantum channel.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0265
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain` |
- counts toward the grade: yes

### Lean: `lean4/H018Channel.lean`

- file: [lean4/H018Channel.lean](../../../lean4/H018Channel.lean)
- sha256 (`bytes`): `159240e630391d183b9a471093131aaf5eeb4b58c1632b19b0d2bb80d78927e3`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build H018Channel`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `diagonal_shadow_does_not_fix_channel` | yes | yes | yes | - | `#print axioms diagonal_shadow_does_not_fix_channel` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0265_stochastic_population_shadow_of_a_channel.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0265_stochastic_population_shadow_of_a_channel.md](../../../dag/derivations/12_finite_qm_structure/tfq_0265_stochastic_population_shadow_of_a_channel.md)
- sha256 (`lf-normalised`): `2d9b455b4987fec79de8d3cf90fac11d6191df9101791239e797027089c833e0`
- generated view: listed, not counted
- cited in: record TFQ-0265
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/031_finite_path_sum_as_graded_transport/qm_031_finite_path_sum_as_graded_transport_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/031_finite_path_sum_as_graded_transport/qm_031_finite_path_sum_as_graded_transport_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/082_channels_as_stochastic_kernels_and_the_cptp_lift/qm_082_channels_as_stochastic_kernels_and_the_cptp_lift_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/082_channels_as_stochastic_kernels_and_the_cptp_lift/qm_082_channels_as_stochastic_kernels_and_the_cptp_lift_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0265 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm
- TFQ-0265 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/exact_channel.rs
- TFQ-0265 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_channel.rs

## Routes

Incoming (2):

- `DS-R-KERNEL-FROM-WEIGHTS` `DERIVED_LEAN`: [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) (CONDITIONAL)
- `DS-R-STOCHASTIC-KERNEL` `DERIVED_LEAN`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION)

Outgoing (2):

- `DS-R-KERNEL-TO-CPTP` `GAP_NO_DERIVATION`: [DS-CPTP-COMPLETE-POSITIVITY-IMPORT](DS-CPTP-COMPLETE-POSITIVITY-IMPORT.md) (IMPORTED_ASSUMPTION)
- `DS-R-STOCHASTIC-CONTRACTION` `DERIVED_LEAN`: [DS-QM081-STOCHASTIC-L1-CONTRACTION](DS-QM081-STOCHASTIC-L1-CONTRACTION.md) (PROVED_LEAN)
