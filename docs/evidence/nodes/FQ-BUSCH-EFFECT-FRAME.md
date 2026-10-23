# FQ-BUSCH-EFFECT-FRAME

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Exact six-effect readouts and reconstruction, plus a finite-probe-versus-PSD counterexample, are native/kernel checked at the stated scalar/coordinate scopes.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- effect algebra and trace frame function (assumption)
- declared real places (assumption)

## Bottleneck

Unmet after the PFP review: Prove full effect positivity, matrix/trace transport, arbitrary Busch hypotheses and the separate real-place/Galois/SOS claims. Finite informational completeness alone is not full positivity or Born uniqueness. The broader source statement is kept in pfp_review.prior_statement.

## Source status

H058 theorem family (38 theorems); Rust exact effects at declared cyclotomic real places

## Review

- PFP review: [dag/results/FQ-BUSCH-EFFECT-FRAME/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/FQ-BUSCH-EFFECT-FRAME/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact six-effect readouts and reconstruction, plus a finite-probe-versus-PSD counterexample, are native/kernel checked at the stated scalar/coordinate scopes.
  - does not support: Prove full effect positivity, matrix/trace transport, arbitrary Busch hypotheses and the separate real-place/Galois/SOS claims. Finite informational completeness alone is not full positivity or Born uniqueness.
  - next test: Prove full effect positivity, matrix/trace transport, arbitrary Busch hypotheses and the separate real-place/Galois/SOS claims. Finite informational completeness alone is not full positivity or Born uniqueness.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1017
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition` |
- counts toward the grade: yes

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: node.lean, record TFQ-1017
- replay: `none`
- check: `cd lean4 && lake build FiniteQM`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `busch_ic_povm_vs_polyhedral_frame_cone` | yes | yes | yes | - | `#print axioms busch_ic_povm_vs_polyhedral_frame_cone` |
| `galois_conjugate_negativity_vs_sos_total_positivity` | yes | yes | yes | - | `#print axioms galois_conjugate_negativity_vs_sos_total_positivity` |
- counts toward the grade: yes

### Lean: `lean4/H058EffectFrameBusch.lean`

- file: [lean4/H058EffectFrameBusch.lean](../../../lean4/H058EffectFrameBusch.lean)
- sha256 (`bytes`): `84caf3702b68295713e3dcdcbd92860b9fceb21999b6c3059a8685645afbd698`
- cited in: node.lean, record TFQ-1017
- replay: `none`
- check: `cd lean4 && lake build H058EffectFrameBusch`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `two_mul_half` | yes | yes | yes | - | `#print axioms two_mul_half` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/busch_effects.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/busch_effects.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1017
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1017
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_1017_fq_busch_effect_frame.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_1017_fq_busch_effect_frame.md](../../../dag/derivations/12_finite_qm_structure/tfq_1017_fq_busch_effect_frame.md)
- sha256 (`lf-normalised`): `8ade015083685222d6bc20de56cc99dff1e8519d35759352f3c3b57e61b92f0f`
- generated view: listed, not counted
- cited in: record TFQ-1017
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `5e43f206b08726fd4b27888d6fed3f211aac8398d5f8bf3dce712c415d7d81cc`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics_claim_ledger.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics_claim_ledger.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics_claim_ledger.md)
- sha256 (`lf-normalised`): `b9adbe593870ae277067c746b426f7b937a9cf98319cd4c8c0b712d9059dd5ac`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQ-R-BUSCH` `DERIVED_LEAN`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION), [FQ-CABELLO-NO-INTEGER-FRAME](FQ-CABELLO-NO-INTEGER-FRAME.md) (PROVED_LEAN)

Outgoing (1):

- `FQ-R-EMBEDDING` `COMPUTED`: [FQ-GAP-REAL-EMBEDDING-CHOICE](FQ-GAP-REAL-EMBEDDING-CHOICE.md) (COMPUTATIONALLY_CHECKED)
