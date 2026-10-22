# FQ-INTERFERENCE-NONDESCENT

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Hadamard-style mixing separates points of one phase-blind fiber: no function f satisfies readout = f o phaseBlind once mixing is applied (no_descent_through_fiber, mix_separates). Phase information is observable only after a non-diagonal operation.

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

- non-diagonal measurement context (assumption)

## Bottleneck

The second (non-diagonal) context is admitted, not derived (QM-209 residual import).

## Source status

ledger: LEAN PROVED (RECEIPTED); H010 header Candidate only

## Review

- PFP review: [dag/results/FQ-INTERFERENCE-NONDESCENT/reviews/20261019_scope_audit/review_result.json](../../../dag/results/FQ-INTERFERENCE-NONDESCENT/reviews/20261019_scope_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: No function of the original exact populations can reproduce the source mixed readout for all Gaussian-integer vectors. The source Hadamard witness doubles total weight; the rational rotation control separately preserves mass.
  - does not support: Derive or explicitly admit the non-diagonal context, preparation access and any physical interpretation. The raw Hadamard output is not normalized probability.
  - next test: Derive or explicitly admit the non-diagonal context, preparation access and any physical interpretation. The raw Hadamard output is not normalized probability.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: record TFQ-0252 (shared)
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`
- counts toward the grade: no

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: record TFQ-0252 (shared)
- replay: `none`
- check: `cd lean4 && lake build FiniteQM`
- counts toward the grade: no

### Lean: `lean4/H010InterferenceNonDescent.lean`

- file: [lean4/H010InterferenceNonDescent.lean](../../../lean4/H010InterferenceNonDescent.lean)
- sha256 (`bytes`): `e46f995a5af051ddb72746a7dfb674cccc95a3eb3a499d52a0287e5700f06703`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build H010InterferenceNonDescent`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `mix_separates` | yes | yes | yes | - | `#print axioms mix_separates` |
| `no_descent_through_fiber` | yes | yes | yes | - | `#print axioms no_descent_through_fiber` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/coherent_interference.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/coherent_interference.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0252_interference_as_a_resource_outside_l1_bookkeeping.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0252_interference_as_a_resource_outside_l1_bookkeeping.md](../../../dag/derivations/12_finite_qm_structure/tfq_0252_interference_as_a_resource_outside_l1_bookkeeping.md)
- sha256 (`lf-normalised`): `97f3fbb9777b27f143ba1ce853c88170987c15d90a4a9e59f9a310a89ff96995`
- generated view: listed, not counted
- cited in: record TFQ-0252 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/finite_quantum_mechanics_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/finite_quantum_mechanics_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0252 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm

## Routes

Incoming (1):

- `FQ-R-NONDESCENT` `DERIVED_LEAN`: [FQ-PHASE-FIBER-QUOTIENT](FQ-PHASE-FIBER-QUOTIENT.md) (PROVED_LEAN)

Outgoing (0):

