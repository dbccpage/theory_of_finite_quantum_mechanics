# FQ-CABELLO-NO-INTEGER-FRAME

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The 18 Cabello integer rays with 9 orthogonal tetrads admit no Int-valued 0/1-type frame assignment (odd count 9 = 2k has no solution: cabello_parity_obstruction); frame additivity and bounded nonnegativity do not force PSD (frame_function_additivity_not_force_psd).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- real-symmetric representative of frame function (assumption)

## Bottleneck

Scope is the integer/real-symmetric Cabello system, not arbitrary complex-Hermitian matrices.

## Source status

H054 header carries "PR #205 scope correction" demotion; ledger typed LEAN PROVED (RECEIPTED)

## Review

- PFP review: [dag/results/FQ-CABELLO-NO-INTEGER-FRAME/reviews/20261019_next_ten_audit/review_result.json](../../../dag/results/FQ-CABELLO-NO-INTEGER-FRAME/reviews/20261019_next_ten_audit/review_result.json); file present and sha256 matches the node's record: no; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Literal general integer parity, full measured-ray/source scaled checks, and the independently verified normalized M_bad/2 countermodel with a negative quadratic direction.
  - does not support: Arbitrary complex-Hermitian frame systems, general even-parity sufficiency, or a fully instantiated refined-carrier operad.
  - next test: Batch review must compare the source scaled integer checks with actual rational readouts and preserve the even-control limitation.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/H053EverettForkingTree.lean`

- file: [lean4/H053EverettForkingTree.lean](../../../lean4/H053EverettForkingTree.lean)
- sha256 (`bytes`): `8730f0cdd32665b8aa902d31fe2bc2b99a5dcde35cf3ccb8f99019c952698b59`
- cited in: node.lean, record TFQ-1015
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `H053EverettForkingTree`): recorded sha256 `8730f0cdd32665b8aa902d31fe2bc2b99a5dcde35cf3ccb8f99019c952698b59` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build H053EverettForkingTree`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `cabello_parity_obstruction` | yes | yes | yes | Quot.sound, propext | `#print axioms cabello_parity_obstruction` |
- counts toward the grade: yes

### Lean: `lean4/H054GleasonCyclotomicObstruction.lean`

- file: [lean4/H054GleasonCyclotomicObstruction.lean](../../../lean4/H054GleasonCyclotomicObstruction.lean)
- sha256 (`bytes`): `9a4cb7494e8a8af61e7d060e556c6da868d917b05b4fd7e4c56dda12b2f63d11`
- cited in: node.lean, record TFQ-1015
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `H054GleasonCyclotomicObstruction`): recorded sha256 `9a4cb7494e8a8af61e7d060e556c6da868d917b05b4fd7e4c56dda12b2f63d11` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build H054GleasonCyclotomicObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `cabello_no_integer_frame_assignment` | yes | yes | yes | Quot.sound, propext | `#print axioms cabello_no_integer_frame_assignment` |
| `frame_additivity_not_force_psd` | yes | yes | yes | none | `#print axioms frame_additivity_not_force_psd` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/kochen_specker.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/kochen_specker.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1015
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1015
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1015_fq_cabello_no_integer_frame.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1015_fq_cabello_no_integer_frame.md](../../../dag/derivations/10_finite_qm_core/tfq_1015_fq_cabello_no_integer_frame.md)
- sha256 (`lf-normalised`): `a240a57cc28368399736bba826ef3a6fb98f569635db5c8d738d5338ba1bb1e7`
- generated view: listed, not counted
- cited in: record TFQ-1015
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

- `FQ-R-CABELLO` `DERIVED_LEAN`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

Outgoing (3):

- `FQ-R-BUSCH` `DERIVED_LEAN`: [FQ-BUSCH-EFFECT-FRAME](FQ-BUSCH-EFFECT-FRAME.md) (PROVED_LEAN)
- `FQ-R-CABELLO-POLYTOPE` `COMPUTED`: [FQ-CABELLO-FRAME-POLYTOPE-146](FQ-CABELLO-FRAME-POLYTOPE-146.md) (COMPUTATIONALLY_CHECKED)
- `FQ-R-CONTEXTUALITY` `DERIVED_LEAN`: [FQ-CONTEXTUALITY-CECH-F2](FQ-CONTEXTUALITY-CECH-F2.md) (PROVED_LEAN)
