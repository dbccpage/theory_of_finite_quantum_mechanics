# DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Relative to a declared finite family of product points, a separating functional (phi(P_k)\>=t, phi(w)\<t) shows w is not in the convex hull. Soundness only; every entangled state having a witness is not claimed; general separability is not addressed.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `receipt_not_current`: lean4/DualWitness.lean: replay failed against 1 receipt(s). A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit.

## Imported structure

- declared product-point family (assumption)
- coherence coordinates in the carrier (assumption)

## Bottleneck

Completeness converse (finite LP duality) is an upgrade target.

## Source status

\[PROVEN\] mechanized witness_certifies_not_separable, ENC-1124 (QM-071-C5); completeness not claimed (C9)

## Review

- PFP review: [dag/results/DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: no; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Exact product-density and Bell-fidelity controls plus a general rational normalized-product gap and finite convex separator soundness are kernel/native checked.
  - does not support: Supply complex/tensor physical imports, arbitrary mixed-state separability and full matrix-functional transport. Soundness for a declared family is not completeness of witnesses.
  - next test: Supply complex/tensor physical imports, arbitrary mixed-state separability and full matrix-functional transport. Soundness for a declared family is not completeness of witnesses.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0257
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm070_071_product_nonfactorization_and_entanglement_witness` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm070_071_product_nonfactorization_and_entanglement_witness` |
- counts toward the grade: yes

### Lean: `lean4/DualWitness.lean`

- file: [lean4/DualWitness.lean](../../../lean4/DualWitness.lean)
- sha256 (`bytes`): `b69a5a5b0f7e69541787915ccd48e7b29b687e04a54d838b556936e034e7f7f7`
- cited in: node.lean
- replay: `failed`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DualWitness`): recorded sha256 `b69a5a5b0f7e69541787915ccd48e7b29b687e04a54d838b556936e034e7f7f7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: no; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build DualWitness`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `dual_witness_certifies_trace_distance` | yes | yes | yes | - | `#print axioms dual_witness_certifies_trace_distance` |
- counts toward the grade: yes

### Lean: `lean4/Entanglement.lean`

- file: [lean4/Entanglement.lean](../../../lean4/Entanglement.lean)
- sha256 (`bytes`): `bccd871b9f8db03c35b564c1a3e41d10d51095a936f2ff4c8980a4bc1195f79d`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_constructor_theory.json](../../../dag/research/lean_replay_campaign_constructor_theory.json) (module `Entanglement`): recorded sha256 `bccd871b9f8db03c35b564c1a3e41d10d51095a936f2ff4c8980a4bc1195f79d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build Entanglement`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `bell_state_is_entangled` | yes | yes | yes | Quot.sound, propext | `#print axioms bell_state_is_entangled` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/entanglement.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/entanglement.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0257_separability_witness_relative_to_a_declared_family.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0257_separability_witness_relative_to_a_declared_family.md](../../../dag/derivations/12_finite_qm_structure/tfq_0257_separability_witness_relative_to_a_declared_family.md)
- sha256 (`lf-normalised`): `576d21d6ccb1ca8fc339e395b819411c274ace40062c05e0f5e738a1ba35fb37`
- generated view: listed, not counted
- cited in: record TFQ-0257
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/071_entanglement_as_a_separability_obstruction/qm_071_entanglement_as_a_separability_obstruction_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/071_entanglement_as_a_separability_obstruction/qm_071_entanglement_as_a_separability_obstruction_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0257 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm
- TFQ-0257 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/entanglement.rs

## Routes

Incoming (1):

- `DS-R-PRODUCT-TO-ENTANGLEMENT` `DERIVED_LEAN`: [DS-QM070-PRODUCT-NONFACTORIZATION](DS-QM070-PRODUCT-NONFACTORIZATION.md) (PROVED_LEAN)

Outgoing (3):

- `DS-R-ENTANGLEMENT-TO-BELL` `DERIVED_LEAN`: [DS-QM073-FINITE-CHSH-AND-PR-BOX](DS-QM073-FINITE-CHSH-AND-PR-BOX.md) (PROVED_LEAN)
- `FRO-R-CT-ENTANGLING-PHASE-FINITE-TARGET` `DERIVED_LEAN`: [CT-ENTANGLING-PHASE-FINITE-TARGET](CT-ENTANGLING-PHASE-FINITE-TARGET.md) (PROVED_LEAN)
- `FRO-R-CT-MARLETTO-VEDRAL-2017-SOURCE` `RECORD_PARENT`: [CT-MARLETTO-VEDRAL-2017-SOURCE](CT-MARLETTO-VEDRAL-2017-SOURCE.md) (SOURCE_RECORD)
