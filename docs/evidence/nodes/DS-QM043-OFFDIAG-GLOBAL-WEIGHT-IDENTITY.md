# DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For D=(d11,d12,d22) in Z^3, globalWeight(D) - localDiagonalWeight(D) = 2 d12. Phase-class descent to H^1(G;U(1)) for a declared U(1) cocycle (C5) is OPEN.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- declared U(1) 1-cocycle (assumption)

## Bottleneck

C5 phase-class descent has a Lean obligation only.

## Source status

Global weight decompositions (a0 + a1)^2 and (a0 + a1 + a2)^2 into diagonal + off-diagonal cross terms mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact global and diagonal weights differ by twice the off-diagonal coefficient, with a sign-flip control.
  - does not support: Prove the actual phase quotient/H1 descent conditions and state the permitted history and readout maps.
  - next test: Prove the actual phase quotient/H1 descent conditions and state the permitted history and readout maps.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0248 (shared)
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm021_040_041_043_commutator_heisenberg_global_weight_and_conditioning` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0248_finite_history_decoherence_matrix.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0248_finite_history_decoherence_matrix.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0248_finite_history_decoherence_matrix.md)
- sha256 (`lf-normalised`): `27696629d6b8396320e708909f4c1abd64b63339fb9a15634ca0398ea578ef6c`
- generated view: listed, not counted
- cited in: record TFQ-0248 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/043_gellmann_hartle_cochain_decoherence/qm_043_gellmann_hartle_cochain_decoherence_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/043_gellmann_hartle_cochain_decoherence/qm_043_gellmann_hartle_cochain_decoherence_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0248 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm

## Routes

Incoming (1):

- `DS-R-DECOHERENCE-FUNCTIONAL` `DERIVED_LEAN`: [DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT](DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT.md) (IMPORTED_ASSUMPTION), [DS-QM063-HOLONOMY-COHERENT-INTENSITY](DS-QM063-HOLONOMY-COHERENT-INTENSITY.md) (PROVED_LEAN)

Outgoing (0):

