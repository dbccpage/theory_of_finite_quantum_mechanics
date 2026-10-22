# FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: general rational-pair fine graining and full rational-root exclusion are kernel checked; retained multi-outcome multiplicities and quadratic-field root coefficients are exact.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- Everett forking tree and equal-weight counting (assumption)

## Bottleneck

Unmet after the PFP review: Prove arbitrary finite-vector fine-graining transport and that the declared quadratic-field coefficients realize the intended physical readout. Counting is an admitted interpretation. The broader source statement is kept in pfp_review.prior_statement.

## Source status

H059 (13 theorems); GAP-F001-S000-011 PRICED_CONTINUUM_INTERFACE

## Review

- PFP review: [dag/results/FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/FQ-EVERETT-RATIONAL-SECTOR-BOUNDARY/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: general rational-pair fine graining and full rational-root exclusion are kernel checked; retained multi-outcome multiplicities and quadratic-field root coefficients are exact.
  - does not support: Prove arbitrary finite-vector fine-graining transport and that the declared quadratic-field coefficients realize the intended physical readout. Counting is an admitted interpretation.
  - next test: Prove arbitrary finite-vector fine-graining transport and that the declared quadratic-field coefficients realize the intended physical readout. Counting is an admitted interpretation.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0276 (shared)
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition` |
- counts toward the grade: yes

### Lean: `lean4/H059RationalSector.lean`

- file: [lean4/H059RationalSector.lean](../../../lean4/H059RationalSector.lean)
- sha256 (`bytes`): `791eb21024574a4781c85ff937f9807656bbe45386d2b08b384ea9f79fe42f90`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build H059RationalSector`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `conductors_with_real_q_yield_rational_finegraining` | yes | yes | yes | - | `#print axioms conductors_with_real_q_yield_rational_finegraining` |
| `rational_finegraining_exists` | yes | yes | yes | - | `#print axioms rational_finegraining_exists` |
| `witness_poly_has_no_candidate_rational_root` | yes | yes | yes | - | `#print axioms witness_poly_has_no_candidate_rational_root` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/branch_finegraining.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/branch_finegraining.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/everett.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/everett.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/13_finite_qm_information/tfq_0276_everettian_relative_state_contact.md`

- file: [dag/derivations/13_finite_qm_information/tfq_0276_everettian_relative_state_contact.md](../../../dag/derivations/13_finite_qm_information/tfq_0276_everettian_relative_state_contact.md)
- sha256 (`lf-normalised`): `583ff49913bc4e3a3472d21eec5373c9d8e1894a59069f3181dd26c6557f4e41`
- generated view: listed, not counted
- cited in: record TFQ-0276 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0276 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm

## Routes

Incoming (1):

- `FQ-R-EVERETT` `DERIVED_LEAN`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION), [FQ-BORN-NORMALIZATION-REDUNDANCY](FQ-BORN-NORMALIZATION-REDUNDANCY.md) (PROVED_LEAN)

Outgoing (0):

