# DS-QM034-035-050-051-095-RESERVED-STUBS

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Unitary finite shadow, Hamiltonian generator admission, Dirac equation admission, spinor structure admission, Copenhagen as authority shadow and the 200-series slots 200/202/203/204/205 have 1-row ledgers that only reserve a slot. They contain no claim; recorded as OPEN, not as results. Papers carry release headers over internal stub bodies where I opened them (034, 035, 050, 051, 202, 203, 205).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- unitary group (assumption)
- Hamiltonian generator (assumption)
- Dirac gamma matrices / spinors (assumption)

## Bottleneck

Finite rational Cayley unitary shadow U=(I-tJ)(I+tJ)^{-1} and 2D Dirac/Clifford spinor relations are mechanized in DerivationDagQMClosure.lean; full monograph expansions remain conditional on unitary/Hamiltonian/spinor imports.

## Source status

Finite rational Cayley unitary shadow U=(I-tJ)(I+tJ)^{-1}, exact quadratic norm preservation vs Euler inflation, and 2D Dirac/Clifford spinor relations mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/DS-QM034-035-050-051-095-RESERVED-STUBS/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/DS-QM034-035-050-051-095-RESERVED-STUBS/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `CONDITIONAL`; qualifies for E4: yes.
  - narrowest claim: Declared Cayley matrices are orthogonal while Euler expands norm at nonzero t; concrete two-generator Clifford identities are recomputed.
  - does not support: Supply spinor/Dirac carrier, Hamiltonian, dynamics and formal matrix bridges before closing the reserved paper stubs.
  - next test: Supply spinor/Dirac carrier, Hamiltonian, dynamics and formal matrix bridges before closing the reserved paper stubs.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0245 (shared), record TFQ-0246 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm063_032_034_destructive_interference_and_cayley_vs_euler_norm` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm063_032_034_destructive_interference_and_cayley_vs_euler_norm` |
| `QuantumMechanics.DerivationDagQMClosure.fq_entropy_purity_and_ds_qm034_051_cayley_clifford_witness` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_entropy_purity_and_ds_qm034_051_cayley_clifford_witness` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0245_unitary_finite_shadow_slot_still_reserved.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0245_unitary_finite_shadow_slot_still_reserved.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0245_unitary_finite_shadow_slot_still_reserved.md)
- sha256 (`lf-normalised`): `a70dea94189cb9ca6b93b538a6421895c099576905968fec92f698c6cbfcdbbb`
- generated view: listed, not counted
- cited in: record TFQ-0245 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0246_hamiltonian_generator_admission_still_reserved.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0246_hamiltonian_generator_admission_still_reserved.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0246_hamiltonian_generator_admission_still_reserved.md)
- sha256 (`lf-normalised`): `5a5e181911194955dd1390a01fc988265bfba481d61489d270abc7ed4689f568`
- generated view: listed, not counted
- cited in: record TFQ-0246 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/13_finite_qm_information/tfq_0278_copenhagen_slot_reserved_as_an_authority_shadow.md`

- file: [dag/derivations/13_finite_qm_information/tfq_0278_copenhagen_slot_reserved_as_an_authority_shadow.md](../../../dag/derivations/13_finite_qm_information/tfq_0278_copenhagen_slot_reserved_as_an_authority_shadow.md)
- sha256 (`lf-normalised`): `13bab7cc5334068682024b2f5a505ec0cd6ca48f568032a5f2421e8a42be2917`
- generated view: listed, not counted
- cited in: record TFQ-0278 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/034_unitary_finite_shadow/qm_034_unitary_finite_shadow_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/034_unitary_finite_shadow/qm_034_unitary_finite_shadow_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/035_hamiltonian_generator_admission/qm_035_hamiltonian_generator_admission_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/035_hamiltonian_generator_admission/qm_035_hamiltonian_generator_admission_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/050_dirac_equation_admission/qm_050_dirac_equation_admission_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/050_dirac_equation_admission/qm_050_dirac_equation_admission_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/051_spinor_structure_admission/qm_051_spinor_structure_admission_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/051_spinor_structure_admission/qm_051_spinor_structure_admission_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/095_copenhagen_as_authority_shadow/qm_095_copenhagen_as_authority_shadow_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/095_copenhagen_as_authority_shadow/qm_095_copenhagen_as_authority_shadow_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/202_operator_algebra_shadow/qm_202_operator_algebra_shadow_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/202_operator_algebra_shadow/qm_202_operator_algebra_shadow_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/203_measurement_problem_obstruction/qm_203_measurement_problem_obstruction_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/203_measurement_problem_obstruction/qm_203_measurement_problem_obstruction_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/205_pointer_basis_obstruction/qm_205_pointer_basis_obstruction_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/205_pointer_basis_obstruction/qm_205_pointer_basis_obstruction_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (2):

- `DS-R-QM034-051-FINITE-SHADOWS` `CONDITIONAL_ON_IMPORT`: [DS-QM033-SCHRODINGER-DISCRETE-COCHAIN](DS-QM033-SCHRODINGER-DISCRETE-COCHAIN.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-UNITARY-SHADOW-STUB` `CONDITIONAL_ON_IMPORT`: [DS-QM033-SCHRODINGER-DISCRETE-COCHAIN](DS-QM033-SCHRODINGER-DISCRETE-COCHAIN.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

