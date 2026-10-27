# DS-QM063-HOLONOMY-COHERENT-INTENSITY

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For two paths, coherent intensity equals the L1 sum plus the real part of relative loop holonomy; holonomy and intensity are invariant under vertex gauge repair; U(1) connections on a tree are gauge-trivial; intensity does not factor through L1 weights when holonomy varies. Higher-form holonomy refused; matrix-valued SU(2) trace bound is a CONJECTURE.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 1 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Lean states the two-path identity |z1 + z2|^2 = |z1|^2 + |z2|^2 + 2 Re(conj(z1) z2) over Gaussian integers, invariance under the common phase i, holonomy zero for coboundaries on closed vertex paths, and a three-edge tree gauge. General U(1) phases and general trees are not in Lean.

## Source status

QCS-C2 two-path coherent intensity identity, vertex gauge invariance, QCS-C4 3-edge spanning-tree gauge triviality, and QCS-C9 L1 non-factorization mechanized in DerivationDagQMClosure.lean and mirrored in finite_quantum_mechanics

## Review

- PFP review: [dag/results/DS-QM063-HOLONOMY-COHERENT-INTENSITY/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM063-HOLONOMY-COHERENT-INTENSITY/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Relative Gaussian holonomy and two-path intensity are invariant under the retained common unit phases; the rational unit-phase conditional is general in Lean.
  - does not support: Prove the full graph connection/tree gauge-trivialization and matrix-valued holonomy transports; no SU(2) trace bound or higher-form result is claimed.
  - next test: Prove the full graph connection/tree gauge-trivialization and matrix-valued holonomy transports; no SU(2) trace bound or higher-form result is claimed.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CoboundaryHolonomy.lean`

- file: [lean4/CoboundaryHolonomy.lean](../../../lean4/CoboundaryHolonomy.lean)
- sha256 (`bytes`): `79c60e8ecd695f4e19de55b0502d2a0236c79d8b4d2ce6079a7516bc89e640fe`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_implementation_sibling.json](../../../dag/research/lean_replay_campaign_implementation_sibling.json) (module `CoboundaryHolonomy`): recorded sha256 `79c60e8ecd695f4e19de55b0502d2a0236c79d8b4d2ce6079a7516bc89e640fe` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CoboundaryHolonomy`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `coboundary_closed_cycle_zero` | yes | yes | yes | Quot.sound, propext | `#print axioms coboundary_closed_cycle_zero` |
| `flux_obstructs_coboundary` | yes | yes | yes | Quot.sound, propext | `#print axioms flux_obstructs_coboundary` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0254
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm063_032_034_destructive_interference_and_cayley_vs_euler_norm` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm063_032_034_destructive_interference_and_cayley_vs_euler_norm` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm063_holonomy_coherent_intensity_and_gauge_invariance` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm063_holonomy_coherent_intensity_and_gauge_invariance` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm063_tree_gauge_triviality_vertex_repair_and_l1_non_factorization` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm063_tree_gauge_triviality_vertex_repair_and_l1_non_factorization` |

- counts toward the grade: yes

### Rust: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche18_ds_qm063_072_073_090_holonomy_bit_shadow_chsh_and_o022_closure_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0254_holonomy_structured_coherent_intensity.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0254_holonomy_structured_coherent_intensity.md](../../../dag/derivations/12_finite_qm_structure/tfq_0254_holonomy_structured_coherent_intensity.md)
- sha256 (`lf-normalised`): `aa1110e6429477296caffe963f3ac7e807a35aeac9b1c306e76429bb2f2e8d5d`
- generated view: listed, not counted
- cited in: record TFQ-0254
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0091_finite_loop_words_stay_on_the_declared_graph_continuum_connection_and_the.md`

- file: [dag/derivations/19_finite_qg/tfq_0091_finite_loop_words_stay_on_the_declared_graph_continuum_connection_and_the.md](../../../dag/derivations/19_finite_qg/tfq_0091_finite_loop_words_stay_on_the_declared_graph_continuum_connection_and_the.md)
- sha256 (`lf-normalised`): `7451e056537e9ece36ef701712354a401dab10f7605f55a631d59f71330b14b6`
- generated view: listed, not counted
- cited in: record TFQ-0091
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche18_ds_qm063_072_073_090_holonomy_bit_shadow_chsh_and_o022_closure_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche4_edgewise_l1_u1_holonomy_chsh_and_cayley_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche9_bloch_gap_cayley_u1_hadamard_coherence_and_destructive_interference_witness`
- `external:sha256:6573cc4b53a02a97b89680e4bce638a9b06c197bb1a8eea2aae104001597f30d::is_gauge_trivial`
- `external:sha256:b4a0392795f1e742a256ae815cdc26550b49a4f6e92e1b8c6beb0d28f159c92d::verify_tranche18_ds_qm063_072_073_090_holonomy_bit_shadow_chsh_and_o022_closure_witness`
- `external:sha256:e7e54ff5b3dc7898d6be8c64e1469ccbabcc130b6d893746f36958121eea9b17#QCS-C11`
- `external:sha256:e7e54ff5b3dc7898d6be8c64e1469ccbabcc130b6d893746f36958121eea9b17#QCS-C2`
- `external:sha256:e7e54ff5b3dc7898d6be8c64e1469ccbabcc130b6d893746f36958121eea9b17#QCS-C4`
- `external:sha256:e7e54ff5b3dc7898d6be8c64e1469ccbabcc130b6d893746f36958121eea9b17#QCS-C9`

## Absences recorded by the TFQ records

- TFQ-0091 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/holonomy_bridge_control.py
- TFQ-0091 rust: no local rust twin located for external:sha256:6573cc4b53a02a97b89680e4bce638a9b06c197bb1a8eea2aae104001597f30d
- TFQ-0254 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm

## Routes

Incoming (1):

- `DS-R-HOLONOMY-INTENSITY` `COMPUTED`: [DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE](DS-QM061-L1-CANNOT-COMPUTE-INTERFERENCE.md) (PROVED_LEAN)

Outgoing (5):

- `APP-R-FSP-U1-WILSON-ACTION` `DERIVED_LEAN`: [FSP-U1-WILSON-ACTION](FSP-U1-WILSON-ACTION.md) (PROVED_LEAN)
- `DS-R-BUILDABILITY` `COMPUTED`: [DS-QM061-BUILDABILITY-SET-S](DS-QM061-BUILDABILITY-SET-S.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-DECOHERENCE-FUNCTIONAL` `DERIVED_LEAN`: [DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY](DS-QM043-OFFDIAG-GLOBAL-WEIGHT-IDENTITY.md) (PROVED_LEAN)
- `DS-R-GR-LQG` `COMPUTED`: [DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS](DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-REDIRECT` `COMPUTED`: [DS-QM064-074-083-ANNEX-REDIRECT-ROWS](DS-QM064-074-083-ANNEX-REDIRECT-ROWS.md) (COMPUTATIONALLY_CHECKED)
