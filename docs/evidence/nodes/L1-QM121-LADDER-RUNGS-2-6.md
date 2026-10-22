# L1-QM121-LADDER-RUNGS-2-6

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Complete retained stochastic path tables and matrix-power equality, diagonal action and exact two-phase readout, with finite composition algebra in Lean.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.
- `broken_reference`: path not found: code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py. A cited in-repo path or symbol cannot be found in this checkout.

## Imported structure

- C / U(1) carrier: assumption
- Gleason: assumption
- continuum / unitarity: assumption

## Bottleneck

Unmet after the PFP review: Prove arbitrary-rung/source representation refinements and discharge the admitted carrier, Born uniqueness and continuous/unitary limits. The broader source statement is kept in pfp_review.prior_statement.

## Source status

QM_121 rungs 2-6: rung 2 PROVED prose (ENC-1126); rungs 1 and 6 'MECHANIZED reuse'; C10 C/U(1) carrier IMPORTED / OPEN (OB-U1); C9 Born-quadratic IMPORTED (OB-BORN)

## Review

- PFP review: [dag/results/L1-QM121-LADDER-RUNGS-2-6/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM121-LADDER-RUNGS-2-6/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Complete retained stochastic path tables and matrix-power equality, diagonal action and exact two-phase readout, with finite composition algebra in Lean.
  - does not support: Prove arbitrary-rung/source representation refinements and discharge the admitted carrier, Born uniqueness and continuous/unitary limits.
  - next test: Prove arbitrary-rung/source representation refinements and discharge the admitted carrier, Born uniqueness and continuous/unitary limits.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_thm7_and_qm121_ladder_rungs_2_to_6_separation` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_thm7_and_qm121_ladder_rungs_2_to_6_separation` |
| `QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation` |
| `QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure` |
| `QuantumMechanics.DerivationDagQMClosure.qm121_ladder_rungs_2_to_6_certificate` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm121_ladder_rungs_2_to_6_certificate` |
- counts toward the grade: yes

### Rust: `code/rust/src/qm/campaigns/density_matrix.rs`

- file: [code/rust/src/qm/campaigns/density_matrix.rs](../../../code/rust/src/qm/campaigns/density_matrix.rs)
- sha256 (`bytes`): `847f1fc1386da04441491f4862781239c7b07e7886d169a2a9fac8b7eb2cff8e`
- cited in: record TFQ-0309
- note: no test is cited for this symbol; its crate is theory_of_finite_qm
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/coherent_interference.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/coherent_interference.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/residual_density_calculus.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/residual_density_calculus.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py`

- file: `code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py`
- resolution: `missing` (not found in this checkout)
- cited in: record TFQ-0309
- counts toward the grade: no

### Documents and data: `dag/derivations/09_finite_hilbert/tfq_0309_ingredient_ladder_stops_before_the_imported_ceiling.md`

- file: [dag/derivations/09_finite_hilbert/tfq_0309_ingredient_ladder_stops_before_the_imported_ceiling.md](../../../dag/derivations/09_finite_hilbert/tfq_0309_ingredient_ladder_stops_before_the_imported_ceiling.md)
- sha256 (`lf-normalised`): `f08c3c792bf8ed2c68ba7fba3caba50b94b7aa31a11d0b61aed5bcd0363ddc38`
- generated view: listed, not counted
- cited in: record TFQ-0309
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/121_the_finite_qm_ingredient_ladder/qm_121_the_finite_qm_ingredient_ladder_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/121_the_finite_qm_ingredient_ladder/qm_121_the_finite_qm_ingredient_ladder_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/121_the_finite_qm_ingredient_ladder/the_finite_qm_ingredient_ladder.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/121_the_finite_qm_ingredient_ladder/the_finite_qm_ingredient_ladder.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0309 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs

## Routes

Incoming (1):

- `L1-R-LADDER` `DERIVED_LEAN`: [L1-QM020-THM1-DIRECT-NORMALIZATION](L1-QM020-THM1-DIRECT-NORMALIZATION.md) (PROVED_LEAN), [L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY](L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY.md) (PROVED_LEAN), [L1-QM020-THM7-REPRESENTATION-CAPACITY](L1-QM020-THM7-REPRESENTATION-CAPACITY.md) (PROVED_LEAN)

Outgoing (0):

