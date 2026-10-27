# DS-QM033-SCHRODINGER-DISCRETE-COCHAIN

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Full Gaussian Hψ and derivative coordinates reproduce zero instantaneous mass rate and the nonzero exact Euler drift formula.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 1 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Unmet after the PFP review: Derive H and its units/interface; construct an exact propagator and prove the formal matrix-to-rate transport. No differential equation solution or continuum limit is provided. The broader source statement is kept in pfp_review.prior_statement.

## Source status

QM_033-C1..C3 discrete 2-vertex Hermitian graph Schrodinger L1/L2 probability mass conservation and LGGR 3-cycle phase holonomy gauge invariance mechanized in DerivationDagQMClosure.lean and mirrored in finite_quantum_mechanics

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
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm033_hermitian_graph_schrodinger_mass_conservation_and_lggr_holonomy` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm033_hermitian_graph_schrodinger_mass_conservation_and_lggr_holonomy` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm033_skew_hermitian_l2_norm_conservation_and_stochastic_separation` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm033_skew_hermitian_l2_norm_conservation_and_stochastic_separation` |

- counts toward the grade: yes

### Rust: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche20_ds_qm032_033_073_090_207_feynman_schrodinger_exchange_and_five_import_cascade_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0244_discrete_schrodinger_cochain_on_a_finite_graph.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0244_discrete_schrodinger_cochain_on_a_finite_graph.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0244_discrete_schrodinger_cochain_on_a_finite_graph.md)
- sha256 (`lf-normalised`): `1d644bd57f4dc76d31e1ada2f6fbf8c99582817c4ab8cd602c13ed771509c670`
- generated view: listed, not counted
- cited in: record TFQ-0244
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:3d06e736ecbda88104eb42b1cbd6f6ffec0e50bb507af4f70f50113c731c40d7#QM_033-C1`
- `external:sha256:3d06e736ecbda88104eb42b1cbd6f6ffec0e50bb507af4f70f50113c731c40d7#QM_033-C2`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche20_ds_qm032_033_073_090_207_feynman_schrodinger_exchange_and_five_import_cascade_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche6_conditional_and_open_boundary_certificates_witness`
- `external:sha256:6ab07bdd1ae577a675dc767e612844d3f4d1a9efd78e8392959395026af2e92e::cycle_product`
- `external:sha256:6ab07bdd1ae577a675dc767e612844d3f4d1a9efd78e8392959395026af2e92e::euler_propagator`
- `external:sha256:6ab07bdd1ae577a675dc767e612844d3f4d1a9efd78e8392959395026af2e92e::norm_rate`
- `external:sha256:894812d28e3737288b66ac176480953a3d7a0023e824ab5f1e4879892d4db6b5::cayley_transform_toggle`
- `external:sha256:9c7a84b488781585a8580b14ac3f57bc03609c55b38c436a194b0991bd901eaf`
- `external:sha256:b4a0392795f1e742a256ae815cdc26550b49a4f6e92e1b8c6beb0d28f159c92d::verify_tranche20_ds_qm032_033_073_090_207_feynman_schrodinger_exchange_and_five_import_cascade_witness`

## Absences recorded by the TFQ records

- TFQ-0244 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm

## Routes

Incoming (2):

- `DS-R-SCHRODINGER-CONDITIONAL` `COMPUTED`: [DS-QM030-TRANSFER-OPERATOR-SHADOW](DS-QM030-TRANSFER-OPERATOR-SHADOW.md) (COMPUTATIONALLY_CHECKED), [DS-CONTINUOUS-TIME-EXP-GENERATOR](DS-CONTINUOUS-TIME-EXP-GENERATOR.md) (IMPORTED_ASSUMPTION), [DS-QM062-U1-RESIDUES-IMPORT](DS-QM062-U1-RESIDUES-IMPORT.md) (IMPORTED_ASSUMPTION)
- `DS-R-SCHRODINGER-FROM-PATHSUM` `COMPUTED`: [DS-QM030-TRANSFER-OPERATOR-SHADOW](DS-QM030-TRANSFER-OPERATOR-SHADOW.md) (COMPUTATIONALLY_CHECKED)

Outgoing (3):

- `DS-R-HEISENBERG` `COMPUTED`: [DS-QM041-HEISENBERG-PICTURE-FINITE](DS-QM041-HEISENBERG-PICTURE-FINITE.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-QM034-051-FINITE-SHADOWS` `CONDITIONAL_ON_IMPORT`: [DS-QM034-035-050-051-095-RESERVED-STUBS](DS-QM034-035-050-051-095-RESERVED-STUBS.md) (CONDITIONAL)
- `DS-R-UNITARY-SHADOW-STUB` `CONDITIONAL_ON_IMPORT`: [DS-QM034-035-050-051-095-RESERVED-STUBS](DS-QM034-035-050-051-095-RESERVED-STUBS.md) (CONDITIONAL)
