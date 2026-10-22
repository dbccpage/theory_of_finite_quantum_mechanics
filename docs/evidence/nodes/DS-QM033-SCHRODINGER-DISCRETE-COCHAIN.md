# DS-QM033-SCHRODINGER-DISCRETE-COCHAIN

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Full Gaussian Hψ and derivative coordinates reproduce zero instantaneous mass rate and the nonzero exact Euler drift formula.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Derive H and its units/interface; construct an exact propagator and prove the formal matrix-to-rate transport. No differential equation solution or continuum limit is provided. The broader source statement is kept in pfp_review.prior_statement.

## Source status

QM_033-C1..C3 discrete 2-vertex Hermitian graph Schrodinger L1/L2 probability mass conservation and LGGR 3-cycle phase holonomy gauge invariance mechanized in DerivationDagQMClosure.lean and mirrored in 006_finite_qm

## Review

- PFP review: [dag/results/DS-QM033-SCHRODINGER-DISCRETE-COCHAIN/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/DS-QM033-SCHRODINGER-DISCRETE-COCHAIN/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Full Gaussian Hψ and derivative coordinates reproduce zero instantaneous mass rate and the nonzero exact Euler drift formula.
  - does not support: Derive H and its units/interface; construct an exact propagator and prove the formal matrix-to-rate transport. No differential equation solution or continuum limit is provided.
  - next test: Derive H and its units/interface; construct an exact propagator and prove the formal matrix-to-rate transport. No differential equation solution or continuum limit is provided.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0244
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm033_hermitian_graph_schrodinger_mass_conservation_and_lggr_holonomy` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm033_hermitian_graph_schrodinger_mass_conservation_and_lggr_holonomy` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm033_skew_hermitian_l2_norm_conservation_and_stochastic_separation` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm033_skew_hermitian_l2_norm_conservation_and_stochastic_separation` |
- counts toward the grade: yes

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/dynamics.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/dynamics.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/finite_schrodinger_step.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/finite_schrodinger_step.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0244_discrete_schrodinger_cochain_on_a_finite_graph.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0244_discrete_schrodinger_cochain_on_a_finite_graph.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0244_discrete_schrodinger_cochain_on_a_finite_graph.md)
- sha256 (`lf-normalised`): `6640d197ae41d47ca78026d04fd1f33fa55ddfe9fba32c67d101490dd05aaf1e`
- generated view: listed, not counted
- cited in: record TFQ-0244
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/033_schrodinger_finite_shadow/qm_033_schrodinger_finite_shadow_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/033_schrodinger_finite_shadow/qm_033_schrodinger_finite_shadow_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/033_schrodinger_finite_shadow/schrodinger_finite_shadow.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/033_schrodinger_finite_shadow/schrodinger_finite_shadow.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0244 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm

## Routes

Incoming (2):

- `DS-R-SCHRODINGER-CONDITIONAL` `COMPUTED`: [DS-QM030-TRANSFER-OPERATOR-SHADOW](DS-QM030-TRANSFER-OPERATOR-SHADOW.md) (COMPUTATIONALLY_CHECKED), [DS-CONTINUOUS-TIME-EXP-GENERATOR](DS-CONTINUOUS-TIME-EXP-GENERATOR.md) (IMPORTED_ASSUMPTION), [DS-QM062-U1-RESIDUES-IMPORT](DS-QM062-U1-RESIDUES-IMPORT.md) (IMPORTED_ASSUMPTION)
- `DS-R-SCHRODINGER-FROM-PATHSUM` `COMPUTED`: [DS-QM030-TRANSFER-OPERATOR-SHADOW](DS-QM030-TRANSFER-OPERATOR-SHADOW.md) (COMPUTATIONALLY_CHECKED)

Outgoing (3):

- `DS-R-HEISENBERG` `COMPUTED`: [DS-QM041-HEISENBERG-PICTURE-FINITE](DS-QM041-HEISENBERG-PICTURE-FINITE.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-QM034-051-FINITE-SHADOWS` `CONDITIONAL_ON_IMPORT`: [DS-QM034-035-050-051-095-RESERVED-STUBS](DS-QM034-035-050-051-095-RESERVED-STUBS.md) (CONDITIONAL)
- `DS-R-UNITARY-SHADOW-STUB` `CONDITIONAL_ON_IMPORT`: [DS-QM034-035-050-051-095-RESERVED-STUBS](DS-QM034-035-050-051-095-RESERVED-STUBS.md) (CONDITIONAL)
