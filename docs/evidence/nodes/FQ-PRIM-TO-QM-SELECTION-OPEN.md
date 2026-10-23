# FQ-PRIM-TO-QM-SELECTION-OPEN

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Primitive difference does not select the declared quantum model or readout. Direct packet-walk execution is an integration result: the complexes, Cayley parameter, cyclotomic weights, detector and squared-amplitude readout were supplied independently of the computed difference value.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

- `receipt_not_current`: lean4/CoupledRelationalProjectors.lean: replay failed against 1 receipt(s). A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit.

## Imported structure

- all of FQ-DECLARED-QUANTUM-INTERFACE (assumption)

## Bottleneck

Finite D2, D3, D2xD3, D3^2, and D3^3 projectors and the state-manifold dimension gap d-1 \< d^2-1 are mechanized without free parameters; full continuum M_n(C) and Gleason n\>=3 remain explicit external imports.

## Source status

7-stage finite relational operad chain (D2, D3, D2xD3, D3^2, D3^3) and d-dimensional diagonal vs rebit vs qubit state-parameter gap (d-1 \< d^2-1) mechanized in CoupledRelationalProjectors.lean and DerivationDagQMClosure.lean; continuum Hilbert/Gleason imports remain external

## Review

- PFP review: [dag/results/FQ-PRIM-TO-QM-SELECTION-OPEN/reviews/20261019_structure_audit/review_result.json](../../../dag/results/FQ-PRIM-TO-QM-SELECTION-OPEN/reviews/20261019_structure_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `CONDITIONAL`; qualifies for E4: yes.
  - narrowest claim: Identical two-label input carrier and amplitudes admit distinct positive normalized quadratic and quartic rules, with a symmetric agreement control; the 1:2 example is checked in Lean.
  - does not support: Derive a quantum carrier/readout selection principle and its hypotheses. Full continuum matrix/Hilbert/Gleason imports are not discharged by executing a declared packet walk.
  - next test: Derive a quantum carrier/readout selection principle and its hypotheses. Full continuum matrix/Hilbert/Gleason imports are not discharged by executing a declared packet walk.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

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
- sha256 (`lf-normalised`): `f531934d19931276c0e0242fd54a305c6db1e555ee45abac3bf41e75d72917d6`
- generated view: listed, not counted
- cited in: record TFQ-1010
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `FQ-R-GAP-PRIM-TO-SELECTION` `CONDITIONAL_ON_IMPORT`: [FQ-PRIMDIFF-QUOTIENT-KERNEL](FQ-PRIMDIFF-QUOTIENT-KERNEL.md) (PROVED_LEAN)

Outgoing (0):

