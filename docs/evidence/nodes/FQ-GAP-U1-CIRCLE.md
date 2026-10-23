# FQ-GAP-U1-CIRCLE

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `CONDITIONAL`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The circle group U(1) is not constructed on the finite host; continuity of a one-parameter phase group remains a hypothesis. In Q(i), u=(3+4i)/5 has no square root and n -\> u^n is injective, so no homomorphism (Q,+) -\> U(1)(Q(i)) sends 1 to u.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 10
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `broken_reference`: symbol U1Fable.CauchyCircleCompletion.RegPhaseSeq.add_assoc_equiv not found in lean4/U1CauchyCircleCompletion.lean. A cited in-repo path or symbol cannot be found in this checkout.
- `broken_reference`: symbol U1Fable.CauchyCircleCompletion.quad_half_angle_squares_to_u345 not found in lean4/U1CauchyCircleCompletion.lean. A cited in-repo path or symbol cannot be found in this checkout.
- `broken_reference`: symbol U1Fable.ChebyshevCauchyBridge.HermitianMat2Qi.pureProjector_born_pairing not found in lean4/U1ChebyshevCauchyBridge.lean. A cited in-repo path or symbol cannot be found in this checkout.
- `broken_reference`: symbol U1Fable.ChebyshevCauchyBridge.circleRatPow_eq_chebyshev not found in lean4/U1ChebyshevCauchyBridge.lean. A cited in-repo path or symbol cannot be found in this checkout.
- `broken_reference`: symbol U1Fable.ChebyshevCauchyBridge.taylor_circle_norm_defect_identity not found in lean4/U1ChebyshevCauchyBridge.lean. A cited in-repo path or symbol cannot be found in this checkout.
- `broken_reference`: symbol U1Fable.CyclotomicTorsionTower.ratPhaseQuot_divisible not found in lean4/U1CyclotomicTorsionTower.lean. A cited in-repo path or symbol cannot be found in this checkout.
- `broken_reference`: symbol U1Fable.PhaseSynthesis.u1_phase_completion_synthesis not found in lean4/U1PhaseSynthesis.lean. A cited in-repo path or symbol cannot be found in this checkout.
- `broken_reference`: symbol U1Fable.PythagoreanObstruction.no_rational_one_param_group_through_u345 not found in lean4/U1PythagoreanObstruction.lean. A cited in-repo path or symbol cannot be found in this checkout.
- `broken_reference`: symbol U1Fable.QuadraticTowerAndCayleyStone.chebT2Pow_succ not found in lean4/U1QuadraticTowerAndCayleyStone.lean. A cited in-repo path or symbol cannot be found in this checkout.
- `broken_reference`: symbol U1Fable.QuadraticTowerAndCayleyStone.u345_k2_double_angle_recovery not found in lean4/U1QuadraticTowerAndCayleyStone.lean. A cited in-repo path or symbol cannot be found in this checkout.

## Imported structure

- circle group U(1) (assumption)
- continuity of one-parameter phase group (assumption)

## Bottleneck

Projective P^1(Q) Cayley compactification, 5-adic half-angle obstruction, mod-5 Gaussian power injectivity, Q/Z torsion-tower divisibility, quadratic sqrt(5) half-angle restoration + iterated real quadratic square-root tower K_{m+1} = K_m(sqrt((1+c_m)/2)), rational Chebyshev/Taylor Cauchy approximations over RegPhaseSeq, 4D Q(i) Hermitian Born trace representation, and discrete Cayley unitary steps U_H(t) = (I - i t H)(I + i t H)^(-1) are kernel-checked; compact continuous R/Z circle topology remains an explicit completion structure.

## Source status

Projective Cayley compactification P^1(Q) \<-\> S^1(Q), 5-adic half-angle obstruction (4/5 and 1/5 not squares), mod-5 Gaussian power injectivity, Q/Z torsion-tower m-divisibility and finite Haar character orthogonality, quadratic sqrt(5) half-angle restoration + iterated real quadratic square-root tower K_{m+1} = K_m(sqrt((1+c_m)/2)) (explicit K_2 = Q(sqrt(5))(sqrt((5+2*sqrt(5))/10)) with N_{Q(sqrt(5))/Q}((5+2*sqrt(5))/10) = 1/20 and general 2^m-step Chebyshev recursion T_{2^{m+1}} = T_2 o T_{2^m}), rational Chebyshev/Taylor Cauchy approximations to (cos(2*pi*q), sin(2*pi*q)) over RegPhaseSeq, 4D Q(i) Hermitian Born trace representation, and discrete Cayley unitary steps U_H(t) = (I - i t H)(I + i t H)^(-1) kernel-checked in lean4/U1PythagoreanObstruction.lean, lean4/U1PowerMapInjectivity.lean, lean4/U1CayleyProjectiveCircle.lean, lean4/U1CyclotomicTorsionTower.lean, lean4/U1CauchyCircleCompletion.lean, lean4/U1ChebyshevCauchyBridge.lean, lean4/U1QuadraticTowerAndCayleyStone.lean, and lean4/U1PhaseSynthesis.lean (run 20261020T223000Z_u1_phase_completion_lean) and replayed in code/python/src/qm/u1_phase_completion.py and code/rust/src/qm/u1_phase_completion.rs; compact continuous R/Z circle topology remains an explicit completion structure

## Review

- PFP review: [dag/results/FQ-GAP-U1-CIRCLE/reviews/20261019_scope_audit/review_result.json](../../../dag/results/FQ-GAP-U1-CIRCLE/reviews/20261019_scope_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `CONDITIONAL`; qualifies for E4: yes.
  - narrowest claim: The rational Cayley parametrization satisfies the unit-circle equation on retained points, with exact inverse t=y/(x+1), and a general cleared identity. The square-root equations force a^2=4/5; bounded powers are computed exactly.
  - does not support: Prove 4/5 is not a rational square, full power-map injectivity, and the additive-Q homomorphism obstruction without bounded-search substitution; compact continuous U(1) remains imported.
  - next test: Prove 4/5 is not a rational square, full power-map injectivity, and the additive-Q homomorphism obstruction without bounded-search substitution; compact continuous U(1) remains imported.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0253 (shared)
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` |
| `QuantumMechanics.DerivationDagQMClosure.fq_gap_u1_circle_pythagorean_half_exponent_obstruction` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gap_u1_circle_pythagorean_half_exponent_obstruction` |
| `QuantumMechanics.DerivationDagQMClosure.fq_u1_selector_split_real_zero_divisors_and_cayley_unit_circle` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_u1_selector_split_real_zero_divisors_and_cayley_unit_circle` |
- counts toward the grade: yes

### Lean: `lean4/U1CauchyCircleCompletion.lean`

- file: [lean4/U1CauchyCircleCompletion.lean](../../../lean4/U1CauchyCircleCompletion.lean)
- sha256 (`bytes`): `455a4ea001d022fc5538ed9be16f9473f30ba43c019bbec2bb01dc32baaff299`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build U1CauchyCircleCompletion`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `U1Fable.CauchyCircleCompletion.RegPhaseSeq.add_assoc_equiv` | yes | no | no | - | `#print axioms U1Fable.CauchyCircleCompletion.RegPhaseSeq.add_assoc_equiv` |
| `U1Fable.CauchyCircleCompletion.quad_half_angle_squares_to_u345` | yes | no | no | - | `#print axioms U1Fable.CauchyCircleCompletion.quad_half_angle_squares_to_u345` |
- counts toward the grade: yes

### Lean: `lean4/U1CayleyProjectiveCircle.lean`

- file: [lean4/U1CayleyProjectiveCircle.lean](../../../lean4/U1CayleyProjectiveCircle.lean)
- sha256 (`bytes`): `07fd439e150502d9b8603a0097fcf5dc11d039f9b92f83948494c2a25dae8e94`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build U1CayleyProjectiveCircle`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `U1Fable.CayleyProjectiveCircle.homCayley_projMul` | yes | yes | yes | - | `#print axioms U1Fable.CayleyProjectiveCircle.homCayley_projMul` |
| `U1Fable.CayleyProjectiveCircle.homCayley_surjective` | yes | yes | yes | - | `#print axioms U1Fable.CayleyProjectiveCircle.homCayley_surjective` |
- counts toward the grade: yes

### Lean: `lean4/U1ChebyshevCauchyBridge.lean`

- file: [lean4/U1ChebyshevCauchyBridge.lean](../../../lean4/U1ChebyshevCauchyBridge.lean)
- sha256 (`bytes`): `c630dab388010bf38230a1bba1e1e621d76686831097bb915141bd8901f1e114`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build U1ChebyshevCauchyBridge`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `U1Fable.ChebyshevCauchyBridge.HermitianMat2Qi.pureProjector_born_pairing` | yes | no | no | - | `#print axioms U1Fable.ChebyshevCauchyBridge.HermitianMat2Qi.pureProjector_born_pairing` |
| `U1Fable.ChebyshevCauchyBridge.circleRatPow_eq_chebyshev` | yes | no | no | - | `#print axioms U1Fable.ChebyshevCauchyBridge.circleRatPow_eq_chebyshev` |
| `U1Fable.ChebyshevCauchyBridge.taylor_circle_norm_defect_identity` | yes | no | no | - | `#print axioms U1Fable.ChebyshevCauchyBridge.taylor_circle_norm_defect_identity` |
- counts toward the grade: yes

### Lean: `lean4/U1CyclotomicTorsionTower.lean`

- file: [lean4/U1CyclotomicTorsionTower.lean](../../../lean4/U1CyclotomicTorsionTower.lean)
- sha256 (`bytes`): `cb8619f0f06352e79cc546363d75cecf21c07724abef520a516ef245d4e4e720`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build U1CyclotomicTorsionTower`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `U1Fable.CyclotomicTorsionTower.ratPhaseQuot_divisible` | yes | no | no | - | `#print axioms U1Fable.CyclotomicTorsionTower.ratPhaseQuot_divisible` |
- counts toward the grade: yes

### Lean: `lean4/U1PhaseSynthesis.lean`

- file: [lean4/U1PhaseSynthesis.lean](../../../lean4/U1PhaseSynthesis.lean)
- sha256 (`bytes`): `6b9c6fae68d1695cb84ce8ae4622f357af51d8c5fa1a8747f11aaaf45a4afd2c`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build U1PhaseSynthesis`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `U1Fable.PhaseSynthesis.chebyshev_taylor_and_hermitian_qi_bridge` | yes | yes | yes | - | `#print axioms U1Fable.PhaseSynthesis.chebyshev_taylor_and_hermitian_qi_bridge` |
| `U1Fable.PhaseSynthesis.iterated_quadratic_tower_and_cayley_stone_bridge` | yes | yes | yes | - | `#print axioms U1Fable.PhaseSynthesis.iterated_quadratic_tower_and_cayley_stone_bridge` |
| `U1Fable.PhaseSynthesis.u1_phase_completion_synthesis` | yes | no | no | - | `#print axioms U1Fable.PhaseSynthesis.u1_phase_completion_synthesis` |
- counts toward the grade: yes

### Lean: `lean4/U1PowerMapInjectivity.lean`

- file: [lean4/U1PowerMapInjectivity.lean](../../../lean4/U1PowerMapInjectivity.lean)
- sha256 (`bytes`): `6c4960e3ea9a15b3543991eaf10802a74665d2716731ff88875ebe7b641159c3`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build U1PowerMapInjectivity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `U1Fable.PowerMapInjectivity.u345_infinite_order` | yes | yes | yes | - | `#print axioms U1Fable.PowerMapInjectivity.u345_infinite_order` |
- counts toward the grade: yes

### Lean: `lean4/U1PythagoreanObstruction.lean`

- file: [lean4/U1PythagoreanObstruction.lean](../../../lean4/U1PythagoreanObstruction.lean)
- sha256 (`bytes`): `13baa7587d8920d330fff37e45ca7876f6caab126ea3e9ffdc1f652833e6c2b0`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build U1PythagoreanObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `U1Fable.PythagoreanObstruction.no_rational_one_param_group_through_u345` | yes | no | no | - | `#print axioms U1Fable.PythagoreanObstruction.no_rational_one_param_group_through_u345` |
- counts toward the grade: yes

### Lean: `lean4/U1QuadraticTowerAndCayleyStone.lean`

- file: [lean4/U1QuadraticTowerAndCayleyStone.lean](../../../lean4/U1QuadraticTowerAndCayleyStone.lean)
- sha256 (`bytes`): `660009a462e0569e2e02c8e8c61826b502394dc86b88faa566864052bdcf5c35`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build U1QuadraticTowerAndCayleyStone`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `U1Fable.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_comp_regular` | yes | yes | yes | - | `#print axioms U1Fable.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_comp_regular` |
| `U1Fable.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_preserves_born_trace` | yes | yes | yes | - | `#print axioms U1Fable.QuadraticTowerAndCayleyStone.TracelessHerm2Qi.cayleyStep_preserves_born_trace` |
| `U1Fable.QuadraticTowerAndCayleyStone.chebT2Pow_succ` | yes | no | no | - | `#print axioms U1Fable.QuadraticTowerAndCayleyStone.chebT2Pow_succ` |
| `U1Fable.QuadraticTowerAndCayleyStone.u345_k2_double_angle_recovery` | yes | no | no | - | `#print axioms U1Fable.QuadraticTowerAndCayleyStone.u345_k2_double_angle_recovery` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/amplitude_bridge.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/amplitude_bridge.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0294_circle_phases_as_an_imported_unit_group.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0294_circle_phases_as_an_imported_unit_group.md](../../../dag/derivations/08_l1_to_l2/tfq_0294_circle_phases_as_an_imported_unit_group.md)
- sha256 (`lf-normalised`): `9c76c771cb03a3bf6146900e6299b36965daaccf2675e868e966af303a9657a5`
- generated view: listed, not counted
- cited in: record TFQ-0294 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0253_conditional_complex_carrier_selector.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0253_conditional_complex_carrier_selector.md](../../../dag/derivations/12_finite_qm_structure/tfq_0253_conditional_complex_carrier_selector.md)
- sha256 (`lf-normalised`): `156cf03a6e2efbe4a97922fe7e41bc0342db70068c5c46b2a82d79eb6b94f6cc`
- generated view: listed, not counted
- cited in: record TFQ-0253 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/14_finite_gauge/tfq_0053_each_language_must_carry_a_unit_gaussian_edge_connection_covariant_difference_vertex.md`

- file: [dag/derivations/14_finite_gauge/tfq_0053_each_language_must_carry_a_unit_gaussian_edge_connection_covariant_difference_vertex.md](../../../dag/derivations/14_finite_gauge/tfq_0053_each_language_must_carry_a_unit_gaussian_edge_connection_covariant_difference_vertex.md)
- sha256 (`lf-normalised`): `3b89d84355253adb91b6cab1ff8de82e84c48bea6adc7e49603890463649038b`
- generated view: listed, not counted
- cited in: record TFQ-0053 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/14_finite_gauge/tfq_0054_each_language_must_carry_pure_gauge_iff_every_off_forest_edge_is_1.md`

- file: [dag/derivations/14_finite_gauge/tfq_0054_each_language_must_carry_pure_gauge_iff_every_off_forest_edge_is_1.md](../../../dag/derivations/14_finite_gauge/tfq_0054_each_language_must_carry_pure_gauge_iff_every_off_forest_edge_is_1.md)
- sha256 (`lf-normalised`): `bec1ff23684877868f7c92f7a5a339d288796a72cf8e04e3c4fb96610dd8206f`
- generated view: listed, not counted
- cited in: record TFQ-0054 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/14_finite_gauge/tfq_0055_each_language_must_carry_no_rational_homomorphism_supplies_the_missing_square_root.md`

- file: [dag/derivations/14_finite_gauge/tfq_0055_each_language_must_carry_no_rational_homomorphism_supplies_the_missing_square_root.md](../../../dag/derivations/14_finite_gauge/tfq_0055_each_language_must_carry_no_rational_homomorphism_supplies_the_missing_square_root.md)
- sha256 (`lf-normalised`): `8555f29d93d2a5613dab291139edc56748d7d471012998854a1a6f49e74f1cbb`
- generated view: listed, not counted
- cited in: record TFQ-0055 (shared)
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: [sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml](../../../sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `16a418a93748cef695fad3c1fab0fd14dd95c6985b23ee8a814b171eca60a445`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0053 lean4: not located
- TFQ-0053 python: not located
- TFQ-0053 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/u1_graph_connection.rs
- TFQ-0054 lean4: not located
- TFQ-0054 python: not located
- TFQ-0054 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/u1_gauge_triviality.rs
- TFQ-0055 lean4: not located
- TFQ-0055 python: not located
- TFQ-0055 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/u1_gauge_triviality.rs
- TFQ-0294 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/complex_structure_selector.rs
- TFQ-0294 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/phase_averaged_shadow.rs
- TFQ-0294 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs

## Routes

Incoming (1):

- `FQ-R-GAP-U1` `CONDITIONAL_ON_IMPORT`: [FQ-U1-TRANSPORT-N-TORSION](FQ-U1-TRANSPORT-N-TORSION.md) (PROVED_LEAN), [FQ-IMPL-WDP-AMPLITUDE-BRIDGE](FQ-IMPL-WDP-AMPLITUDE-BRIDGE.md) (PROVED_LEAN)

Outgoing (1):

- `FRO-R-LQG-SPIN-NETWORK-STATES-IMPORT-X1` `GAP_NO_DERIVATION`: [LQG-SPIN-NETWORK-STATES-IMPORT](LQG-SPIN-NETWORK-STATES-IMPORT.md) (IMPORTED_ASSUMPTION)
