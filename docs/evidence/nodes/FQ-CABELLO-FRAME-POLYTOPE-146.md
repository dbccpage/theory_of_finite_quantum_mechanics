# FQ-CABELLO-FRAME-POLYTOPE-146

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Independently exhaustive exact basis computations and every actual finite matrix witness, with a separate literal integer-list kernel certificate; the general real-polytope completeness bridge remains open.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- real-symmetric operator representative H_f (assumption)

## Bottleneck

Unmet after the PFP review: A formal Lean theorem identifying the entire real polytope vertex set, a general real spectral/PSD transport theorem, or positivity from finite frame additivity. The broader source statement is kept in pfp_review.prior_statement.

## Source status

paper s11.5: exact enumeration and exact characteristic-polynomial certificates (supplement s11.52)

## Review

- PFP review: [dag/results/FQ-CABELLO-FRAME-POLYTOPE-146/reviews/20261019_next_ten_audit/review_result.json](../../../dag/results/FQ-CABELLO-FRAME-POLYTOPE-146/reviews/20261019_next_ten_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Independently exhaustive exact basis computations and every actual finite matrix witness, with a separate literal integer-list kernel certificate; the general real-polytope completeness bridge remains open.
  - does not support: A formal Lean theorem identifying the entire real polytope vertex set, a general real spectral/PSD transport theorem, or positivity from finite frame additivity.
  - next test: Review basis coverage, source geometry, generated-data translation and the exact strict/non-strict spectral tests before promoting any broader claim.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1016
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.cabello_18_9_two_regular_and_146_census` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.cabello_18_9_two_regular_and_146_census` |
| `QuantumMechanics.DerivationDagQMClosure.fq_power_p2_cabello_146_and_weyl_commutant_irreducibility` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_power_p2_cabello_146_and_weyl_commutant_irreducibility` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/frame_function_polytope.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/frame_function_polytope.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1016
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1016
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1016_fq_cabello_frame_polytope_146.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1016_fq_cabello_frame_polytope_146.md](../../../dag/derivations/10_finite_qm_core/tfq_1016_fq_cabello_frame_polytope_146.md)
- sha256 (`lf-normalised`): `1bf1753c7ed8538e1407baa4b67ce1601ce4315f80be3b2df1fb8ea9ffd58eae`
- generated view: listed, not counted
- cited in: record TFQ-1016
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `FQ-R-CABELLO-POLYTOPE` `COMPUTED`: [FQ-CABELLO-NO-INTEGER-FRAME](FQ-CABELLO-NO-INTEGER-FRAME.md) (PROVED_LEAN)

Outgoing (1):

- `FQ-R-GAP-BORN-UNIQUENESS` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-BORN-UNIQUENESS-GLEASON](FQ-GAP-BORN-UNIQUENESS-GLEASON.md) (CONDITIONAL)
