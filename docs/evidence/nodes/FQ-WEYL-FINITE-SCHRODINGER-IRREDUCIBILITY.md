# FQ-WEYL-FINITE-SCHRODINGER-IRREDUCIBILITY

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact d=3 Weyl basis reconstruction and commutator controls, plus the generic conditional scalar-commutant theorem and literal cubic-root algebra.

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

- anchored Weyl seed (assumption)
- primitive d-th root of unity in the field (assumption)

## Bottleneck

Unmet after the PFP review: Transport the array model to field/matrix semantics and prove representation irreducibility for all admitted odd primes. Primitive-root existence, seed selection and infinite-dimensional results are not derived. The broader source statement is kept in pfp_review.prior_statement.

## Source status

paper s1.3 finite Weyl construction from an anchored seed; clock/shift commutant scalar

## Review

- PFP review: [dag/results/FQ-WEYL-FINITE-SCHRODINGER-IRREDUCIBILITY/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/FQ-WEYL-FINITE-SCHRODINGER-IRREDUCIBILITY/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact d=3 Weyl basis reconstruction and commutator controls, plus the generic conditional scalar-commutant theorem and literal cubic-root algebra.
  - does not support: Transport the array model to field/matrix semantics and prove representation irreducibility for all admitted odd primes. Primitive-root existence, seed selection and infinite-dimensional results are not derived.
  - next test: Transport the array model to field/matrix semantics and prove representation irreducibility for all admitted odd primes. Primitive-root existence, seed selection and infinite-dimensional results are not derived.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1020
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_power_p2_cabello_146_and_weyl_commutant_irreducibility` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_power_p2_cabello_146_and_weyl_commutant_irreducibility` |
- counts toward the grade: yes

### Lean: `lean4/WeylCommutant.lean`

- file: [lean4/WeylCommutant.lean](../../../lean4/WeylCommutant.lean)
- sha256 (`bytes`): `c83b1a430883d0f0eb2d7c6bc37e0f6cfda80f2aa71fd7901d5a565cbebb4185`
- cited in: node.lean, record TFQ-1020
- replay: `none`
- check: `cd lean4 && lake build WeylCommutant`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `clock_shift_commutant_scalar` | yes | yes | yes | - | `#print axioms clock_shift_commutant_scalar` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/heisenberg_representation_uniqueness.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/heisenberg_representation_uniqueness.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1020
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/mub/odd_prime_weyl.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/mub/odd_prime_weyl.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1020
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1020
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_1020_fq_weyl_finite_schrodinger_irreducibility.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_1020_fq_weyl_finite_schrodinger_irreducibility.md](../../../dag/derivations/12_finite_qm_structure/tfq_1020_fq_weyl_finite_schrodinger_irreducibility.md)
- sha256 (`lf-normalised`): `b5aece42ccbda95fb1136f5522a113d92eb9048202daf7b5b85733a3d5e2734d`
- generated view: listed, not counted
- cited in: record TFQ-1020
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `FQ-R-WEYL` `DERIVED_LEAN`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION)

Outgoing (1):

- `FQ-R-COMMUTATOR` `DERIVED_LEAN`: [FQ-COMMUTATOR-TRACE-OBSTRUCTION](FQ-COMMUTATOR-TRACE-OBSTRUCTION.md) (PROVED_LEAN)
