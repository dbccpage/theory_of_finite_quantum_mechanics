# DS-QM120-MERMIN-PERES-F2-OBSTRUCTION

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Actual subset solution counts and five-context witnesses are exact; global signed-parity obstruction and each explicit dropped-context witness are kernel checked.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Transport the enumeration to a fully formal incidence/cochain object and any physical observable realization. This finite parity packet does not derive Hilbert space or quantum mechanics. The broader source statement is kept in pfp_review.prior_statement.

## Source status

MECHANIZED / PYTHON-EXACT (QM-120-C5, C7, C11)

## Review

- PFP review: [dag/results/DS-QM120-MERMIN-PERES-F2-OBSTRUCTION/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/DS-QM120-MERMIN-PERES-F2-OBSTRUCTION/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Actual subset solution counts and five-context witnesses are exact; global signed-parity obstruction and each explicit dropped-context witness are kernel checked.
  - does not support: Transport the enumeration to a fully formal incidence/cochain object and any physical observable realization. This finite parity packet does not derive Hilbert space or quantum mechanics.
  - next test: Transport the enumeration to a fully formal incidence/cochain object and any physical observable realization. This finite parity packet does not derive Hilbert space or quantum mechanics.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ContextualityObstruction.lean`

- file: [lean4/ContextualityObstruction.lean](../../../lean4/ContextualityObstruction.lean)
- sha256 (`bytes`): `712a6a817e5b6991910e8e6ed1a394997262e62b71fc89908426866e60773627`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build ContextualityObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `d0_of_global_section` | yes | yes | yes | - | `#print axioms d0_of_global_section` |
- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0250 (shared)
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm120_mermin_peres_f2_no_global_section` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm120_mermin_peres_f2_no_global_section` |
- counts toward the grade: yes

### Lean: `lean4/DualWitness.lean`

- file: [lean4/DualWitness.lean](../../../lean4/DualWitness.lean)
- sha256 (`bytes`): `b69a5a5b0f7e69541787915ccd48e7b29b687e04a54d838b556936e034e7f7f7`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build DualWitness`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `mermin_peres_parity_obstruction` | yes | yes | yes | - | `#print axioms mermin_peres_parity_obstruction` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/contextuality_obstruction.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/contextuality_obstruction.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0250_mermin_peres_contextuality_on_a_finite_cochain.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0250_mermin_peres_contextuality_on_a_finite_cochain.md](../../../dag/derivations/12_finite_qm_structure/tfq_0250_mermin_peres_contextuality_on_a_finite_cochain.md)
- sha256 (`lf-normalised`): `557a53d1afb9d856952c871b81e9a733c8e8224a6a47012fac461759b0f157c9`
- generated view: listed, not counted
- cited in: record TFQ-0250 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/120_mermin_peres_contextuality_cochain_obstruction/qm_120_mermin_peres_contextuality_cochain_obstruction_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/120_mermin_peres_contextuality_cochain_obstruction/qm_120_mermin_peres_contextuality_cochain_obstruction_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0250 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm
- TFQ-0250 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/kochen_specker.rs

## Routes

Incoming (2):

- `DS-R-MERMIN-PERES-F2` `DERIVED_LEAN`: [FQ-CONTEXTUALITY-CECH-F2](FQ-CONTEXTUALITY-CECH-F2.md) (PROVED_LEAN)
- `DS-R-MP-FROM-COCHAIN` `DERIVED_LEAN`: [L1-CHAIN-D1D0-AXIOM](L1-CHAIN-D1D0-AXIOM.md) (ADMITTED_PRIMITIVE)

Outgoing (2):

- `DS-R-MERMIN-PERES-TO-CONTEXTUALITY` `COMPUTED`: [DS-QM206-BOUNDARY-SYNTHESIS](DS-QM206-BOUNDARY-SYNTHESIS.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-MP-UNKNOWN` `DERIVED_LEAN`: [DS-QM212-MAJORANA-PROBLEM](DS-QM212-MAJORANA-PROBLEM.md) (PROVED_LEAN)
