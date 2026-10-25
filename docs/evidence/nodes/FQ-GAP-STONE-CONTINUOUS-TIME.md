# FQ-GAP-STONE-CONTINUOUS-TIME

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Continuous time and the Stone theorem are not constructed: strong continuity, one-parameter group and generator selection are priced interfaces; rational entries alone do not imply infinite order. Causal order between events is also admitted externally (GAP-C1000-001, declared_assumption, non-blocking): Q(zeta_n) carriers supply no relation between spacetime events.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 16
- cited Lean declaration references covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

- `receipt_not_current`: lean4/U1PhaseSynthesis.lean: replay failed against 1 receipt(s). A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit.
- `receipt_not_current`: lean4/U1QuadraticTowerAndCayleyStone.lean: replay failed against 1 receipt(s). A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit.
- `receipt_not_current`: lean4/U1QuadraticTowerAndCayleyStone.lean: replay failed against 1 receipt(s). A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit.
- `receipt_not_current`: lean4/U1QuadraticTowerAndCayleyStone.lean: replay failed against 1 receipt(s). A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit.
- `receipt_not_current`: lean4/U1QuadraticTowerAndCayleyStone.lean: replay failed against 1 receipt(s). A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit.
- `receipt_not_current`: lean4/U1QuadraticTowerAndCayleyStone.lean: replay failed against 1 receipt(s). A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit.

## Imported structure

- continuous time / Stone theorem (assumption; on the finite carrier the strongest available notion is a Q-parameter group, and no Q-parameter group of invertible rational 2x2 matrices has the Pythagorean rotation as its unit step; over Q(i) or larger carriers the question is open)
- generator selection (assumption: half-steps come in pairs, no canonical choice)
- external causal order datum (assumption)

## Bottleneck

Specified on the carrier: continuous time = a Q-parameter group extending the Z-action of a unit step; this needs roots of every order, which the rational 2x2 Pythagorean rotation lacks already at order two (no rational half-step; a half-step exists only after adjoining sqrt 5), so continuous time requires a carrier extension and a generator choice. Discrete Cayley unitary steps U_H(t) = (I - i t H)(I + i t H)^(-1) on 2x2 Hermitian Q(i) generators (with projective-tangent composition law (t1+t2)/(1 - t1*t2*||H||^2), south-pole collision -I_2 at t1*t2*||H||^2 = 1, and Born trace invariance) are kernel-checked. Open: the general triviality of Q-parameter groups over Q(i) (needs unique factorisation in Z\[i\]); strong continuity and the R-completion remain declared external imports. Discrete step aliasing and non-trivial Pythagorean rotation powers without rational angle logarithms remain mechanized.

## Source status

Carrier-level specification kernel-checked in dag/results/FQ-GAP-STONE-CONTINUOUS-TIME/runs/20261020T225000Z_discrete_time_spec (lean4/DiscreteTimeStoneSpec.lean): a Q-parameter group (QParamGroup) restricts to the Z-action of its unit step (U_eq_discreteEvolution) and needs roots of every order (roots_of_all_orders); half-steps come in pairs +-V, so generator selection is a choice (matrix_half_step_not_unique); the rational 2x2 Pythagorean rotation R345 is a reversible discrete evolution (R345_pow_orthogonal) with no rational half-step (no_rational_half_step: any root is p*1 + r*J with p^2 = 4/5, whose denominator 5 is not a square), hence no Q-parameter group of rational 2x2 matrices passes through it (no_qparam_group_through_R345). Exact replays: code/python/src/qm/discrete_time_stone.py, code/rust/src/qm/discrete_time_stone.rs. Discrete Cayley unitary step U_H(t) = (I - i t H)(I + i t H)^(-1) on 2x2 traceless Hermitian matrices over Q(i) (exact resolvent identity, left/right unitarity, det = 1, projective-tangent composition law when 1 - t1*t2*||H||^2 != 0, south-pole collision -I_2 when 1 - t1*t2*||H||^2 = 0, and Born trace invariance) kernel-checked in lean4/U1QuadraticTowerAndCayleyStone.lean and lean4/U1PhaseSynthesis.lean (run 20261020T223000Z_u1_phase_completion_lean) and replayed in code/python/src/qm/u1_phase_completion.py and code/rust/src/qm/u1_phase_completion.rs. Earlier: Pythagorean rotation powers (3+4i)^k (k=1..4) and discrete modular frequency aliasing (k + N) % N = k % N mechanized in DerivationDagQMClosure.lean; continuous-time Stone generator remains an external import

## Review

- PFP review: [dag/results/FQ-GAP-STONE-CONTINUOUS-TIME/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/FQ-GAP-STONE-CONTINUOUS-TIME/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `CONDITIONAL`; qualifies for E4: yes.
  - narrowest claim: All-integer modulo-four aliasing is kernel checked; exact modulo-eight controls distinguish declared half-step tags.
  - does not support: Supply topology, strong continuity, actual exponentials and generator domains before invoking Stone; finite tags do not prove existence.
  - next test: Supply topology, strong continuity, actual exponentials and generator domains before invoking Stone; finite tags do not prove existence.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0246 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` |
| `QuantumMechanics.DerivationDagQMClosure.fq_gap_stone_aliasing_and_real_embedding_conjugate` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gap_stone_aliasing_and_real_embedding_conjugate` |
| `QuantumMechanics.DerivationDagQMClosure.fq_gap_stone_rational_rotation_infinite_order_and_zi_non_field_obstruction` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gap_stone_rational_rotation_infinite_order_and_zi_non_field_obstruction` |

- counts toward the grade: yes

### Lean: `lean4/DiscreteTimeStoneSpec.lean`

- file: [lean4/DiscreteTimeStoneSpec.lean](../../../lean4/DiscreteTimeStoneSpec.lean)
- sha256 (`bytes`): `78e72d0c08b7980ee60a6c6370e3a7c65d43bd6befcf0b816d89c22048a77eda`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_dynamics.json](../../../dag/research/lean_replay_campaign_finite_qm_dynamics.json) (module `DiscreteTimeStoneSpec`): recorded sha256 `78e72d0c08b7980ee60a6c6370e3a7c65d43bd6befcf0b816d89c22048a77eda` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DiscreteTimeStoneSpec`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BornFable.DiscreteTime.QParamGroup` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.DiscreteTime.QParamGroup` |
| `BornFable.DiscreteTime.QParamGroup.U_eq_discreteEvolution` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.DiscreteTime.QParamGroup.U_eq_discreteEvolution` |
| `BornFable.DiscreteTime.QParamGroup.roots_of_all_orders` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.DiscreteTime.QParamGroup.roots_of_all_orders` |
| `BornFable.DiscreteTime.R345_pow_orthogonal` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.DiscreteTime.R345_pow_orthogonal` |
| `BornFable.DiscreteTime.matrix_half_step_not_unique` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.DiscreteTime.matrix_half_step_not_unique` |
| `BornFable.DiscreteTime.no_qparam_group_through_R345` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.DiscreteTime.no_qparam_group_through_R345` |
| `BornFable.DiscreteTime.no_rational_half_step` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms BornFable.DiscreteTime.no_rational_half_step` |

- counts toward the grade: yes

### Lean: `lean4/U1PhaseSynthesis.lean`

- file: [lean4/U1PhaseSynthesis.lean](../../../lean4/U1PhaseSynthesis.lean)
- sha256 (`bytes`): `6b9c6fae68d1695cb84ce8ae4622f357af51d8c5fa1a8747f11aaaf45a4afd2c`
- cited in: node.lean
- replay: `failed`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `U1PhaseSynthesis`): recorded sha256 `6b9c6fae68d1695cb84ce8ae4622f357af51d8c5fa1a8747f11aaaf45a4afd2c` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: no; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build U1PhaseSynthesis`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `U1Fable.PhaseSynthesis.iterated_quadratic_tower_and_cayley_stone_bridge` | yes | yes | yes | - | `#print axioms U1Fable.PhaseSynthesis.iterated_quadratic_tower_and_cayley_stone_bridge` |

- counts toward the grade: yes

### Lean: `lean4/U1QuadraticTowerAndCayleyStone.lean`

- file: [lean4/U1QuadraticTowerAndCayleyStone.lean](../../../lean4/U1QuadraticTowerAndCayleyStone.lean)
- sha256 (`bytes`): `660009a462e0569e2e02c8e8c61826b502394dc86b88faa566864052bdcf5c35`
- cited in: node.lean
- replay: `failed`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `U1QuadraticTowerAndCayleyStone`): recorded sha256 `660009a462e0569e2e02c8e8c61826b502394dc86b88faa566864052bdcf5c35` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: no; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build U1QuadraticTowerAndCayleyStone`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `U1Fable.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_comp_pole` | yes | yes | yes | - | `#print axioms U1Fable.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_comp_pole` |
| `U1Fable.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_comp_regular` | yes | yes | yes | - | `#print axioms U1Fable.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_comp_regular` |
| `U1Fable.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_preserves_born_trace` | yes | yes | yes | - | `#print axioms U1Fable.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_preserves_born_trace` |
| `U1Fable.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_resolvent_right` | yes | yes | yes | - | `#print axioms U1Fable.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_resolvent_right` |
| `U1Fable.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_unitary_left` | yes | yes | yes | - | `#print axioms U1Fable.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_unitary_left` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0246_hamiltonian_generator_admission_still_reserved.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0246_hamiltonian_generator_admission_still_reserved.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0246_hamiltonian_generator_admission_still_reserved.md)
- sha256 (`lf-normalised`): `5a5e181911194955dd1390a01fc988265bfba481d61489d270abc7ed4689f568`
- generated view: listed, not counted
- cited in: record TFQ-0246 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0083_each_language_must_carry_an_explicit_gap_record_the_finite_gauge_dirac.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0083_each_language_must_carry_an_explicit_gap_record_the_finite_gauge_dirac.md](../../../dag/derivations/16_finite_electroweak/tfq_0083_each_language_must_carry_an_explicit_gap_record_the_finite_gauge_dirac.md)
- sha256 (`lf-normalised`): `55926d07640196e84281a1e438d0cb9792d3df0d4781e8db3f75aa94df39ff8b`
- generated view: listed, not counted
- cited in: record TFQ-0083 (shared)
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: [sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml](../../../sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `16a418a93748cef695fad3c1fab0fd14dd95c6985b23ee8a814b171eca60a445`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0083 lean4: not located
- TFQ-0083 python: not located
- TFQ-0083 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/s_matrix.rs

## Routes

Incoming (1):

- `FQ-R-GAP-STONE` `CONDITIONAL_ON_IMPORT`: [FQ-DISCRETE-TIME-STONE-AMBIGUITY](FQ-DISCRETE-TIME-STONE-AMBIGUITY.md) (PROVED_LEAN), [FQ-COMMUTATOR-TRACE-OBSTRUCTION](FQ-COMMUTATOR-TRACE-OBSTRUCTION.md) (PROVED_LEAN)

Outgoing (1):

- `FRO-R-CQFT-REEH-SCHLIEDER-THEOREM-IMPORT-X1` `GAP_NO_DERIVATION`: [CQFT-REEH-SCHLIEDER-THEOREM-IMPORT](CQFT-REEH-SCHLIEDER-THEOREM-IMPORT.md) (IMPORTED_ASSUMPTION)
