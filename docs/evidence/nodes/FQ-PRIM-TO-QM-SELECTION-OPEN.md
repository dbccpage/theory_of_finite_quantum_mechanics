# FQ-PRIM-TO-QM-SELECTION-OPEN

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For amplitudes 1 and 2, quadratic numerators are 1 and 4 with sum 5, and quartic numerators are 1 and 16 with sum 17. Both pairs are positive. The products 1*17 and 1*5 differ, so the normalized first weights 1/5 and 1/17 differ. For equal amplitudes 1 and 1, quadratic numerators are 1 and 1 with sum 2, and quartic numerators are 1 and 1 with sum 2.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

- `receipt_not_current`: lean4/CoupledRelationalProjectors.lean: replay failed against 1 receipt(s). A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit.

## Imported structure

- all of FQ-DECLARED-QUANTUM-INTERFACE (assumption)

## Bottleneck

Selection of a declared quantum model or readout from primitive difference stays open. Packet-walk execution, the complexes, the Cayley parameter, cyclotomic weights, the detector and a squared-amplitude readout are not this integer witness. Continuum M_n(C) and Gleason n\>=3 remain external imports. The D2, D3, D2xD3, D3^2 and D3^3 counts and the gap d-1 \< d^2-1 for d \>= 2 stay outside this witness.

## Source status

7-stage finite relational operad chain (D2, D3, D2xD3, D3^2, D3^3) and d-dimensional diagonal vs rebit vs qubit state-parameter gap (d-1 \< d^2-1) mechanized in CoupledRelationalProjectors.lean and DerivationDagQMClosure.lean; continuum Hilbert/Gleason imports remain external

## Review

- PFP review: [dag/results/FQ-PRIM-TO-QM-SELECTION-OPEN/reviews/20261019_structure_audit/review_result.json](../../../dag/results/FQ-PRIM-TO-QM-SELECTION-OPEN/reviews/20261019_structure_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `CONDITIONAL`; qualifies for E4: yes.
  - narrowest claim: Identical two-label input carrier and amplitudes admit distinct positive normalized quadratic and quartic rules, with a symmetric agreement control; the 1:2 example is checked in Lean.
  - does not support: Derive a quantum carrier/readout selection principle and its hypotheses. Full continuum matrix/Hilbert/Gleason imports are not discharged by executing a declared packet walk.
  - next test: Derive a quantum carrier/readout selection principle and its hypotheses. Full continuum matrix/Hilbert/Gleason imports are not discharged by executing a declared packet walk.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFqPrimToQmSelection.lean`

- file: [lean4/CampaignFqPrimToQmSelection.lean](../../../lean4/CampaignFqPrimToQmSelection.lean)
- sha256 (`bytes`): `df3bc709da599a889424f62769a2524e54753a69bfa0e5214319542215dcb1a4`
- cited in: node.lean, receipt dag/research/campaign_fq-prim-to-qm-selection-open_lean_replay.json (CampaignFqPrimToQmSelection), receipt dag/research/pr_365_review_replay.json (CampaignFqPrimToQmSelection), record TFQ-1010
- replay: `verified`
  - receipt [dag/research/campaign_fq-prim-to-qm-selection-open_lean_replay.json](../../../dag/research/campaign_fq-prim-to-qm-selection-open_lean_replay.json) (module `CampaignFqPrimToQmSelection`): recorded sha256 `df3bc709da599a889424f62769a2524e54753a69bfa0e5214319542215dcb1a4` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_365_review_replay.json](../../../dag/research/pr_365_review_replay.json) (module `CampaignFqPrimToQmSelection`): recorded sha256 `df3bc709da599a889424f62769a2524e54753a69bfa0e5214319542215dcb1a4` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFqPrimToQmSelection`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `normalized_first_weights_differ` | yes | yes | yes | none | `#print axioms normalized_first_weights_differ` |
| `quad_weights` | yes | yes | yes | none | `#print axioms quad_weights` |
| `quart_weights` | yes | yes | yes | none | `#print axioms quart_weights` |
| `symmetric_agreement` | yes | yes | yes | none | `#print axioms symmetric_agreement` |
- counts toward the grade: yes

### Lean: `lean4/CoupledRelationalProjectors.lean`

- file: [lean4/CoupledRelationalProjectors.lean](../../../lean4/CoupledRelationalProjectors.lean)
- sha256 (`bytes`): `22fcce9a754950721bc56674fef83ff3910b73d73f8919c6bd576f6e28500d60`
- cited in: node.lean, record TFQ-1010
- replay: `failed`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `CoupledRelationalProjectors`): recorded sha256 `22fcce9a754950721bc56674fef83ff3910b73d73f8919c6bd576f6e28500d60` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: no; axioms recorded: none (not itemised); only standard axioms: yes
- check: `cd lean4 && lake build CoupledRelationalProjectors`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.CoupledRelationalProjectors.coupled_bipartite_and_tripartite_relational_master_certificate` | yes | yes | yes | - | `#print axioms QuantumMechanics.CoupledRelationalProjectors.coupled_bipartite_and_tripartite_relational_master_certificate` |
- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1010
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` |
| `QuantumMechanics.DerivationDagQMClosure.fq_prim_to_qm_selection_finite_quotient_vs_continuum_gap` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_prim_to_qm_selection_finite_quotient_vs_continuum_gap` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/coupled_relational_operad.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/coupled_relational_operad.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1010
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1010
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/amplitude_bridge.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/amplitude_bridge.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1010
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/genesis_realification_adapter.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/genesis_realification_adapter.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1010
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1010_fq_prim_to_qm_selection_open.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1010_fq_prim_to_qm_selection_open.md](../../../dag/derivations/10_finite_qm_core/tfq_1010_fq_prim_to_qm_selection_open.md)
- sha256 (`lf-normalised`): `bf0db59bb1fdcfb48fc9d373e2e51ccade9a314ce0986b2ba5ce4c58d6b5cebc`
- generated view: listed, not counted
- cited in: record TFQ-1010
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: [sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml](../../../sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `16a418a93748cef695fad3c1fab0fd14dd95c6985b23ee8a814b171eca60a445`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `5e43f206b08726fd4b27888d6fed3f211aac8398d5f8bf3dce712c415d7d81cc`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQ-R-GAP-PRIM-TO-SELECTION` `CONDITIONAL_ON_IMPORT`: [FQ-PRIMDIFF-QUOTIENT-KERNEL](FQ-PRIMDIFF-QUOTIENT-KERNEL.md) (PROVED_LEAN)

Outgoing (0):

