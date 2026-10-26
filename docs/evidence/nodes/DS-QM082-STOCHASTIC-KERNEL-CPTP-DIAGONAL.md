# DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A stochastic kernel preserves states and composes; a CPTP map with Kraus operators induces a column-stochastic population shadow after a basis choice and diagonal read. The induced kernel is basis-relative and the diagonal shadow does not fix the full channel.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- basis choice and diagonal read (lift)
- Kraus operators (assumption)

## Bottleneck

Lean exhibits two channels with the same diagonal shadow (diagonal_shadow_does_not_fix_channel), which settles the last clause. That a Kraus channel induces a column-stochastic shadow is a native check, not Lean.

## Source status

\[PROVEN, MECHANIZED\] ENC-1127 (QM-082-C4)

## Review

- PFP review: [dag/results/DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM082-STOCHASTIC-KERNEL-CPTP-DIAGONAL/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact Kraus completeness, channel outputs, stochastic kernel and same-diagonal distinct-output controls are retained; scalar Cayley and population conservation are kernel checked.
  - does not support: Formalize all matrix/Kraus/tensor positivity transports and physical channel admission. Basis-relative stochastic shadows do not select a unique quantum channel.
  - next test: Formalize all matrix/Kraus/tensor positivity transports and physical channel admission. Basis-relative stochastic shadows do not select a unique quantum channel.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0265
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm081_082_090_093_stochastic_contraction_channel_shadow_firewall_and_cochain` |

- counts toward the grade: yes

### Lean: `lean4/H018Channel.lean`

- file: [lean4/H018Channel.lean](../../../lean4/H018Channel.lean)
- sha256 (`bytes`): `159240e630391d183b9a471093131aaf5eeb4b58c1632b19b0d2bb80d78927e3`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `H018Channel`): recorded sha256 `159240e630391d183b9a471093131aaf5eeb4b58c1632b19b0d2bb80d78927e3` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build H018Channel`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `diagonal_shadow_does_not_fix_channel` | yes | yes | yes | Quot.sound, propext | `#print axioms diagonal_shadow_does_not_fix_channel` |

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

- TFQ-0265 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm
- TFQ-0265 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/exact_channel.rs
- TFQ-0265 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_channel.rs

## Routes

Incoming (2):

- `DS-R-KERNEL-FROM-WEIGHTS` `COMPUTED`: [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) (CONDITIONAL)
- `DS-R-STOCHASTIC-KERNEL` `COMPUTED`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION)

Outgoing (2):

- `DS-R-KERNEL-TO-CPTP` `GAP_NO_DERIVATION`: [DS-CPTP-COMPLETE-POSITIVITY-IMPORT](DS-CPTP-COMPLETE-POSITIVITY-IMPORT.md) (IMPORTED_ASSUMPTION)
- `DS-R-STOCHASTIC-CONTRACTION` `DERIVED_LEAN`: [DS-QM081-STOCHASTIC-L1-CONTRACTION](DS-QM081-STOCHASTIC-L1-CONTRACTION.md) (PROVED_LEAN)
