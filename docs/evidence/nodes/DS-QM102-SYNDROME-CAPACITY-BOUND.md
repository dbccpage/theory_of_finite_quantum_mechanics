# DS-QM102-SYNDROME-CAPACITY-BOUND

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Complete retained repetition-code error tables and zero-syndrome logical controls are exact; the distance arithmetic and three-bit correction statement are kernel checked.

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

- code distance d and error model (assumption)

## Bottleneck

Unmet after the PFP review: Prove the arbitrary code/homology distance and decoder transport under the actual error model. A guaranteed-correctable lower bound is not a general upper-bound theorem. The broader source statement is kept in pfp_review.prior_statement.

## Source status

Quantum Hamming / syndrome capacity bounds for \[\[5,1,3\]\] (1+3*5=16=2^4) and \[\[7,1,3\]\] (1+3*7=22\<=2^6, 22\>2^4) mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/DS-QM102-SYNDROME-CAPACITY-BOUND/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/DS-QM102-SYNDROME-CAPACITY-BOUND/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Complete retained repetition-code error tables and zero-syndrome logical controls are exact; the distance arithmetic and three-bit correction statement are kernel checked.
  - does not support: Prove the arbitrary code/homology distance and decoder transport under the actual error model. A guaranteed-correctable lower bound is not a general upper-bound theorem.
  - next test: Prove the arbitrary code/homology distance and decoder transport under the actual error model. A guaranteed-correctable lower bound is not a general upper-bound theorem.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0270
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm080_090_093_094_101_102_206_207_structure_and_qec_bounds` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_majorana/src/repair_capacity.rs`

- file: `omega_engine/crates_rs/omega_majorana/src/repair_capacity.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/13_finite_qm_information/tfq_0270_syndrome_distance_and_repair_capacity.md`

- file: [dag/derivations/13_finite_qm_information/tfq_0270_syndrome_distance_and_repair_capacity.md](../../../dag/derivations/13_finite_qm_information/tfq_0270_syndrome_distance_and_repair_capacity.md)
- sha256 (`lf-normalised`): `6abb30d785a1b712a331240e3dded0fb8676eeaf503fb279ce96da3863dd1d4e`
- generated view: listed, not counted
- cited in: record TFQ-0270
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/102_fault_tolerance_repair_capacity/qm_102_fault_tolerance_repair_capacity_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/102_fault_tolerance_repair_capacity/qm_102_fault_tolerance_repair_capacity_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0270 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm

## Routes

Incoming (1):

- `DS-R-CAPACITY` `DERIVED_LEAN`: [DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE](DS-QM101-THRESHOLD-AS-CONDITIONAL-REPAIR-CERTIFICATE.md) (PROVED_LEAN)

Outgoing (3):

- `APP-R-MAJ-LGGR-TORUS-INSTANCE` `COMPUTED`: [MAJ-LGGR-TORUS-INSTANCE](MAJ-LGGR-TORUS-INSTANCE.md) (COMPUTATIONALLY_CHECKED)
- `APP-R-MAJ-SYNDROME-RECOVERY-CRITERION` `DERIVED_PROSE`: [MAJ-SYNDROME-RECOVERY-CRITERION](MAJ-SYNDROME-RECOVERY-CRITERION.md) (PROVED_PROSE)
- `APP-R-QCV-QUESTION-SELF-LIMITING-REPAIR` `GAP_NO_DERIVATION`: [QCV-QUESTION-SELF-LIMITING-REPAIR](QCV-QUESTION-SELF-LIMITING-REPAIR.md) (OPEN)
