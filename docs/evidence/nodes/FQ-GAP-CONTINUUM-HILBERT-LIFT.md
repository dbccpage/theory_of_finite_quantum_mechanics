# FQ-GAP-CONTINUUM-HILBERT-LIFT

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The transition from the finite presented carrier (integer weights, finite report labels) to a continuous infinite-dimensional Hilbert space is not constructed in any source; QM_122 s6 refuses it. M_n(Z\[i\]) is recovered for finite report sets but is not M_n(C): Z\[i\] is not a field and a self-adjoint Gaussian-integer matrix need not have a Gaussian-integer eigenvalue (GAP-F001-S000-009). Construction half (split 2026-10-21): FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION records the completion once the scalar field and the l2 uniformity are supplied; this node keeps the selection of those two hypotheses, which no source derives.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 10
- cited Lean, Rust or Python symbols found in their in-repo files: 22
- cited Lean declarations covered by a current replay receipt: 19
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- scalar field R or C, i.e. the completion of Q or of Q(i) (assumption; the lift is the Hausdorff completion of the finitely supported scalar sequences and nothing selects the field)
- l2 uniformity on the exact carrier (assumption; harmonic_separates_uniformities shows that l1 is a different choice with a different Cauchy structure)
- Cauchy convergence hypothesis: limits exist in the lift for rational-l2-Cauchy sequences of exact vectors and not on the exact carrier itself (harmonic_not_tendsTo)

## Bottleneck

What remains at this node is the selection of the scalar field (R or C) and of the l2 uniformity from finite-theory primitives, which no source derives; the construction, the identification with l2(N, k), the intrinsic-uniformity completion and the lifting of bounded exact operators are recorded at FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION; dynamics and generators remain at FQ-GAP-STONE-CONTINUOUS-TIME. Z\[i\] non-field obstruction and discriminant-5 spectral exit from Q(i) remain mechanized.

## Source status

Split on 2026-10-21: the construction (completion, embeddings, l2 model, intrinsic-uniformity completion, bounded operator lift) is recorded at FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION (PROVED_LEAN with named hypotheses) from dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion and dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261021T003000Z_lift_steps; this node keeps the selection question. Earlier record: Controlled completion kernel-checked in dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion: the exact finite carriers Fin n -\> Q form a tower under zero padding whose directed union N -\>0 Q is exhausted by the finite stages (HilbertLiftFiniteTower: exhaustion, qinner_sq_le); the l2 Cauchy condition is stated with rational tolerances and the harmonic witness h_N = sum_{i\<N} e_i/(i+1) is l2-Cauchy with the explicit modulus k -\> k+1, is not l1-Cauchy, and converges to no exact vector (HilbertLiftRationalUniformity: harmonic_separates_uniformities); the Hausdorff completion of the pre-Hilbert carrier N -\>0 k (k = R or C) is a complete inner product space into which the exact carrier embeds inner-product-preservingly, injectively and compatibly with padding, Cauchy-ness in the lift is exactly the rational l2 condition, every such sequence converges, and over R the exact carrier is dense, continuous maps out of the lift are determined on exact vectors, and the lift is strictly larger than the exact carrier (HilbertLiftCompletion: controlled_completion); over C the Gaussian-rational pairs a + ib are dense with the exact inner-product identity and the lift is strictly larger (HilbertLiftComplexCarrier: controlled_completion_complex). Exact replays: code/python/src/qm/hilbert_lift_completion.py (16 tests), code/rust/src/qm/hilbert_lift_completion.rs (14 inline tests). Earlier: Z\[i\] non-field obstruction (2*(a^2+b^2) != 1) and symmetric integer matrix M=\[\[2,1\],\[1,1\]\] characteristic discriminant 5 non-square obstruction in Q(i) mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/reviews/20261019_scope_audit/review_result.json](../../../dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/reviews/20261019_scope_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `CONDITIONAL`; qualifies for E4: yes.
  - narrowest claim: 2 has no Gaussian-integer inverse because its real equation 2a=1 has no integer solution; the stated matrix has characteristic polynomial l^2-l-1 and discriminant identity 4p(l)+5=(2l-1)^2.
  - does not support: Construct an actual completion with specified topology, carrier and embedding; prove any claimed rational/Gaussian spectral exit separately. No impossibility of completion follows from this obstruction.
  - next test: Construct an actual completion with specified topology, carrier and embedding; prove any claimed rational/Gaussian spectral exit separately. No impossibility of completion follows from this obstruction.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates` |
| `QuantumMechanics.DerivationDagQMClosure.fq_gap_stone_rational_rotation_infinite_order_and_zi_non_field_obstruction` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_gap_stone_rational_rotation_infinite_order_and_zi_non_field_obstruction` |
- counts toward the grade: yes

### Lean: `lean4/FiniteDensity.lean`

- file: [lean4/FiniteDensity.lean](../../../lean4/FiniteDensity.lean)
- sha256 (`bytes`): `e62172019a4407f5101e62681d2139ff9fa2a7201e4424ad8b0a6143f5eae763`
- cited in: record TFQ-0086 (shared)
- replay: `none`
- check: `cd lean4 && lake build FiniteDensity`
- counts toward the grade: no

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: record TFQ-0234 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`
- counts toward the grade: no

### Lean: `lean4/HilbertLiftCompletion.lean`

- file: [lean4/HilbertLiftCompletion.lean](../../../lean4/HilbertLiftCompletion.lean)
- sha256 (`bytes`): `2e188609f0a08148273e9ad7e6a0f931d0799b626df9872c7f26bda4c6dde106`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `HilbertLiftCompletion`): recorded sha256 `2e188609f0a08148273e9ad7e6a0f931d0799b626df9872c7f26bda4c6dde106` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build HilbertLiftCompletion`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `HilbertLift.cauchySeq_lift_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms HilbertLift.cauchySeq_lift_iff` |
| `HilbertLift.controlled_completion` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms HilbertLift.controlled_completion` |
| `HilbertLift.denseRange_lift_real` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms HilbertLift.denseRange_lift_real` |
| `HilbertLift.exists_limit_of_isCauchyL2` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms HilbertLift.exists_limit_of_isCauchyL2` |
| `HilbertLift.inner_lift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms HilbertLift.inner_lift` |
| `HilbertLift.lift_not_surjective` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms HilbertLift.lift_not_surjective` |
- counts toward the grade: yes

### Lean: `lean4/HilbertLiftComplexCarrier.lean`

- file: [lean4/HilbertLiftComplexCarrier.lean](../../../lean4/HilbertLiftComplexCarrier.lean)
- sha256 (`bytes`): `4151b5f8a74cdf10988dcf93ca24c2fbcc7562b6e53454cb4b3062d9dcac7309`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `HilbertLiftComplexCarrier`): recorded sha256 `4151b5f8a74cdf10988dcf93ca24c2fbcc7562b6e53454cb4b3062d9dcac7309` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build HilbertLiftComplexCarrier`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `HilbertLift.controlled_completion_complex` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms HilbertLift.controlled_completion_complex` |
| `HilbertLift.denseRange_liftPair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms HilbertLift.denseRange_liftPair` |
| `HilbertLift.inner_liftPair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms HilbertLift.inner_liftPair` |
- counts toward the grade: yes

### Lean: `lean4/HilbertLiftFiniteTower.lean`

- file: [lean4/HilbertLiftFiniteTower.lean](../../../lean4/HilbertLiftFiniteTower.lean)
- sha256 (`bytes`): `3b4e86865b4a0e63724cb7ca0b876479f3ac0a9d3364a030d6cc8d2de560e341`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `HilbertLiftFiniteTower`): recorded sha256 `3b4e86865b4a0e63724cb7ca0b876479f3ac0a9d3364a030d6cc8d2de560e341` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build HilbertLiftFiniteTower`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `HilbertLift.exhaustion` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms HilbertLift.exhaustion` |
| `HilbertLift.qinner_sq_le` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms HilbertLift.qinner_sq_le` |
- counts toward the grade: yes

### Lean: `lean4/HilbertLiftIntrinsicUniformity.lean`

- file: [lean4/HilbertLiftIntrinsicUniformity.lean](../../../lean4/HilbertLiftIntrinsicUniformity.lean)
- sha256 (`bytes`): `25339d6949deb4aa4113a686415e8ba9d40c5ce957d7015d1b8f3d05d06af1ed`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `HilbertLiftIntrinsicUniformity`): recorded sha256 `25339d6949deb4aa4113a686415e8ba9d40c5ce957d7015d1b8f3d05d06af1ed` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build HilbertLiftIntrinsicUniformity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `HilbertLift.intrinsic_completion` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms HilbertLift.intrinsic_completion` |
- counts toward the grade: yes

### Lean: `lean4/HilbertLiftL2Model.lean`

- file: [lean4/HilbertLiftL2Model.lean](../../../lean4/HilbertLiftL2Model.lean)
- sha256 (`bytes`): `3fade85d7333f166567e8a5927b87219377aaede1e4602655ceb6043d90469ad`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `HilbertLiftL2Model`): recorded sha256 `3fade85d7333f166567e8a5927b87219377aaede1e4602655ceb6043d90469ad` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build HilbertLiftL2Model`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `HilbertLift.l2_model_summary` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms HilbertLift.l2_model_summary` |
- counts toward the grade: yes

### Lean: `lean4/HilbertLiftOperators.lean`

- file: [lean4/HilbertLiftOperators.lean](../../../lean4/HilbertLiftOperators.lean)
- sha256 (`bytes`): `d7ffd585fc01353bb69bf7534de6c788ca43525084bdb3654bc3161639b72573`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `HilbertLiftOperators`): recorded sha256 `d7ffd585fc01353bb69bf7534de6c788ca43525084bdb3654bc3161639b72573` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build HilbertLiftOperators`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `HilbertLift.operator_lift_summary` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms HilbertLift.operator_lift_summary` |
- counts toward the grade: yes

### Lean: `lean4/HilbertLiftRationalUniformity.lean`

- file: [lean4/HilbertLiftRationalUniformity.lean](../../../lean4/HilbertLiftRationalUniformity.lean)
- sha256 (`bytes`): `554a6e9f0b593cbda1346c32126615e8b07c769b2ec800bb486cd21d2e6fd27d`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `HilbertLiftRationalUniformity`): recorded sha256 `554a6e9f0b593cbda1346c32126615e8b07c769b2ec800bb486cd21d2e6fd27d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build HilbertLiftRationalUniformity`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `HilbertLift.harmonic_hasModulus` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms HilbertLift.harmonic_hasModulus` |
| `HilbertLift.harmonic_separates_uniformities` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms HilbertLift.harmonic_separates_uniformities` |
- counts toward the grade: yes

### Rust: `code/rust/src/qm/hilbert_lift_completion.rs`

- file: [code/rust/src/qm/hilbert_lift_completion.rs](../../../code/rust/src/qm/hilbert_lift_completion.rs)
- sha256 (`bytes`): `dd5e7d6aa4a5447328499f964867e2da125b9ed1fd74b6133dc8fcd8a10135e3`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `grid_approximation` (rust_symbol) | yes | yes | yes | - | - |
| `harmonic_nonconvergence_bound_holds` (rust_symbol) | yes | yes | yes | - | - |
| `modulus_holds` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Python: `code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py`

- file: `code/python/src/majorana/tests/support/finite_qm/use_cases/density_matrix.py`
- resolution: `missing` (not found in this checkout)
- cited in: record TFQ-0086 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_0234_supplied_hilbert_carrier_after_the_conditional_lift.md`

- file: [dag/derivations/10_finite_qm_core/tfq_0234_supplied_hilbert_carrier_after_the_conditional_lift.md](../../../dag/derivations/10_finite_qm_core/tfq_0234_supplied_hilbert_carrier_after_the_conditional_lift.md)
- sha256 (`lf-normalised`): `6d982adae0ff3da0e19f4cd971e50eb7d55233d37d62353f37b3e171d2ed5ea5`
- generated view: listed, not counted
- cited in: record TFQ-0234 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/14_finite_gauge/tfq_0055_each_language_must_carry_no_rational_homomorphism_supplies_the_missing_square_root.md`

- file: [dag/derivations/14_finite_gauge/tfq_0055_each_language_must_carry_no_rational_homomorphism_supplies_the_missing_square_root.md](../../../dag/derivations/14_finite_gauge/tfq_0055_each_language_must_carry_no_rational_homomorphism_supplies_the_missing_square_root.md)
- sha256 (`lf-normalised`): `8555f29d93d2a5613dab291139edc56748d7d471012998854a1a6f49e74f1cbb`
- generated view: listed, not counted
- cited in: record TFQ-0055 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0056_each_language_must_carry_clifford_admission_slash_square_exact_solution_rank_and_a.md`

- file: [dag/derivations/15_finite_qed/tfq_0056_each_language_must_carry_clifford_admission_slash_square_exact_solution_rank_and_a.md](../../../dag/derivations/15_finite_qed/tfq_0056_each_language_must_carry_clifford_admission_slash_square_exact_solution_rank_and_a.md)
- sha256 (`lf-normalised`): `39f4c3c06256d4dca93b1c0e9d48f2ed8731bbe0a3610b1c8fa9cb2e707ed87d`
- generated view: listed, not counted
- cited in: record TFQ-0056 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0071_each_language_must_carry_hermitian_k_yields_a_unitary_cayley_s_on.md`

- file: [dag/derivations/15_finite_qed/tfq_0071_each_language_must_carry_hermitian_k_yields_a_unitary_cayley_s_on.md](../../../dag/derivations/15_finite_qed/tfq_0071_each_language_must_carry_hermitian_k_yields_a_unitary_cayley_s_on.md)
- sha256 (`lf-normalised`): `b4f76c09d7ffde16cc737b032458b0737899d4a6562182e7780d16f55f36b9e0`
- generated view: listed, not counted
- cited in: record TFQ-0071 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0073_each_language_must_carry_isotony_locality_and_optional_complement_duality_on_a.md`

- file: [dag/derivations/15_finite_qed/tfq_0073_each_language_must_carry_isotony_locality_and_optional_complement_duality_on_a.md](../../../dag/derivations/15_finite_qed/tfq_0073_each_language_must_carry_isotony_locality_and_optional_complement_duality_on_a.md)
- sha256 (`lf-normalised`): `8422d79c4dbb10d10e91c4857c0c47bf6ea69dfb2763047b54bed9d3ae700b63`
- generated view: listed, not counted
- cited in: record TFQ-0073
- counts toward the grade: no

### Documents and data: `dag/derivations/16_finite_electroweak/tfq_0083_each_language_must_carry_an_explicit_gap_record_the_finite_gauge_dirac.md`

- file: [dag/derivations/16_finite_electroweak/tfq_0083_each_language_must_carry_an_explicit_gap_record_the_finite_gauge_dirac.md](../../../dag/derivations/16_finite_electroweak/tfq_0083_each_language_must_carry_an_explicit_gap_record_the_finite_gauge_dirac.md)
- sha256 (`lf-normalised`): `55926d07640196e84281a1e438d0cb9792d3df0d4781e8db3f75aa94df39ff8b`
- generated view: listed, not counted
- cited in: record TFQ-0083 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0086_fq_gap_continuum_hilbert_lift_stays_unpaid_no_continuum_hilbert_space_is_admitted_at_the_root.md`

- file: [dag/derivations/19_finite_qg/tfq_0086_fq_gap_continuum_hilbert_lift_stays_unpaid_no_continuum_hilbert_space_is_admitted_at_the_root.md](../../../dag/derivations/19_finite_qg/tfq_0086_fq_gap_continuum_hilbert_lift_stays_unpaid_no_continuum_hilbert_space_is_admitted_at_the_root.md)
- sha256 (`lf-normalised`): `878199cafd2c1775202016787f8d29ad515ee87124dc446accd96e04f3a1741c`
- generated view: listed, not counted
- cited in: record TFQ-0086 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0111_the_interface_stays_open_gap_f000_f002_001_and_gap_f002_s001_001_are_not_discharged.md`

- file: [dag/derivations/19_finite_qg/tfq_0111_the_interface_stays_open_gap_f000_f002_001_and_gap_f002_s001_001_are_not_discharged.md](../../../dag/derivations/19_finite_qg/tfq_0111_the_interface_stays_open_gap_f000_f002_001_and_gap_f002_s001_001_are_not_discharged.md)
- sha256 (`lf-normalised`): `95fe120b3c9f0ba8e8f01d0f95aabdd704d0682fc157a7308d8c3d8ddca32207`
- generated view: listed, not counted
- cited in: record TFQ-0111
- counts toward the grade: no

### Documents and data: `dag/derivations/20_continuum_interface/tfq_0115_gap_f002_limit_and_gap_f002_topology_stay_open_the_continuum_limit_is_not_discharged.md`

- file: [dag/derivations/20_continuum_interface/tfq_0115_gap_f002_limit_and_gap_f002_topology_stay_open_the_continuum_limit_is_not_discharged.md](../../../dag/derivations/20_continuum_interface/tfq_0115_gap_f002_limit_and_gap_f002_topology_stay_open_the_continuum_limit_is_not_discharged.md)
- sha256 (`lf-normalised`): `c3a6f2eed6b3a490c88884c968376d74421668ecfc317d2e4854b84935de4387`
- generated view: listed, not counted
- cited in: record TFQ-0115
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: [sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml](../../../sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `16a418a93748cef695fad3c1fab0fd14dd95c6985b23ee8a814b171eca60a445`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0055 lean4: not located
- TFQ-0055 python: not located
- TFQ-0055 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/u1_gauge_triviality.rs
- TFQ-0056 lean4: not located
- TFQ-0056 python: not located
- TFQ-0056 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/dirac_gamma_admission.rs
- TFQ-0071 lean4: not located
- TFQ-0071 python: not located
- TFQ-0071 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/s_matrix.rs
- TFQ-0073 lean4: not located
- TFQ-0073 python: not located
- TFQ-0073 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/algebraic_qft.rs
- TFQ-0083 lean4: not located
- TFQ-0083 python: not located
- TFQ-0083 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/s_matrix.rs
- TFQ-0111 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent/002_from_primitive_difference_to_mtheory/lean4/FromPrimitiveDifferenceToMTheory/ContinuumLimit.lean
- TFQ-0115 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent/002_from_primitive_difference_to_mtheory/lean4/FromPrimitiveDifferenceToMTheory/ContinuumLimit.lean
- TFQ-0115 python: no local python twin located for omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent/002_from_primitive_difference_to_mtheory/python/src/mtheory_interfaces/cochain_limit.py
- TFQ-0234 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm

## Routes

Incoming (2):

- `FQ-R-GAP-CONTINUUM` `CONDITIONAL_ON_IMPORT`: [FQ-COMMUTATOR-TRACE-OBSTRUCTION](FQ-COMMUTATOR-TRACE-OBSTRUCTION.md) (PROVED_LEAN), [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION)
- `FQ-R-GAP-CONTINUUM-FROM-CONSTRUCTION` `GAP_NO_DERIVATION`: [FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION](FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION.md) (PROVED_LEAN)

Outgoing (10):

- `APP-R-DFM-CONTINUUM-INTERFACE` `GAP_NO_DERIVATION`: [DFM-CONTINUUM-INTERFACE](DFM-CONTINUUM-INTERFACE.md) (OPEN)
- `FRO-R-CQFT-REEH-SCHLIEDER-THEOREM-IMPORT-X1` `GAP_NO_DERIVATION`: [CQFT-REEH-SCHLIEDER-THEOREM-IMPORT](CQFT-REEH-SCHLIEDER-THEOREM-IMPORT.md) (IMPORTED_ASSUMPTION)
- `UDG-R-TFQ-0112` `RECORD_PARENT`: [TFQ-0112](TFQ-0112.md) (SOURCE_RECORD)
- `UDG-R-TFQ-0116` `RECORD_PARENT`: [TFQ-0116](TFQ-0116.md) (SOURCE_RECORD)
- `UDG-R-TFQ-0117` `GAP_NO_DERIVATION`: [TFQ-0117](TFQ-0117.md) (OPEN)
- `UDG-R-TFQ-0118` `GAP_NO_DERIVATION`: [TFQ-0118](TFQ-0118.md) (OPEN)
- `UDG-R-TFQ-0119` `GAP_NO_DERIVATION`: [TFQ-0119](TFQ-0119.md) (OPEN)
- `UDG-R-TFQ-0120` `RECORD_PARENT`: [TFQ-0120](TFQ-0120.md) (SOURCE_RECORD)
- `UDG-R-TFQ-0121` `RECORD_PARENT`: [TFQ-0121](TFQ-0121.md) (SOURCE_RECORD)
- `UDG-R-TFQ-0123` `GAP_NO_DERIVATION`: [TFQ-0123](TFQ-0123.md) (OPEN)
