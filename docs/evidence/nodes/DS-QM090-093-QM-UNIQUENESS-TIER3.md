# DS-QM090-093-QM-UNIQUENESS-TIER3

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> That contextual obstruction plus the five conditions (finite contexts, overlap, no global repair, probabilistic pairing, no-signalling) uniquely select complex Hilbert QM is open; non-QM contextual packet theories are not excluded. Tier-4 ontological derivation is refused.

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

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The node records an open question. The cited Lean is integer arithmetic and Boolean conjunctions.

## Source status

QM-093-C4/C5/C18/C20 survival theorem under finite descent, sealed_can_fail witness, Tier-4 ontological non-promotion, real-rebit local-tomography dimension failure (9 != 10), and 24-vertex (2,2,2) no-signaling PR-box counter-theory mechanized in DerivationDagQMClosure.lean and mirrored in finite_quantum_mechanics

## Review

- PFP review: [dag/results/DS-QM090-093-QM-UNIQUENESS-TIER3/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/DS-QM090-093-QM-UNIQUENESS-TIER3/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Actual context tables, global-assignment exclusion and spectator marginal recovery are exact; the odd-cycle and rational recovery statements are kernel checked.
  - does not support: Give the full theory/equivalence notion and exclude competing packet theories before Tier-3 complex-Hilbert uniqueness. No ontology or arbitrary non-QM theory classification is asserted.
  - next test: Give the full theory/equivalence notion and exclude competing packet theories before Tier-3 complex-Hilbert uniqueness. No ontology or arbitrary non-QM theory classification is asserted.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0274
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_and_207_211_tier3_survival_rebit_tomography_and_five_import_cascade` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_and_207_211_tier3_survival_rebit_tomography_and_five_import_cascade` |
| `QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_qm_uniqueness_tier3_gpt_dimension_and_pr_box_exclusion` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm090_093_qm_uniqueness_tier3_gpt_dimension_and_pr_box_exclusion` |

- counts toward the grade: yes

### Rust: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche20_ds_qm032_033_073_090_207_feynman_schrodinger_exchange_and_five_import_cascade_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0274_tier_3_uniqueness_left_without_a_derivation.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0274_tier_3_uniqueness_left_without_a_derivation.md](../../../dag/derivations/12_finite_qm_structure/tfq_0274_tier_3_uniqueness_left_without_a_derivation.md)
- sha256 (`lf-normalised`): `c36094f16de5f5853e91e390fbcdc7b8187bb10e87e484075cb15487958d4d9c`
- generated view: listed, not counted
- cited in: record TFQ-0274
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche10_chsh_tsirelson_pr_box_tier3_uniqueness_edgewise_l1_and_import_boundaries_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche20_ds_qm032_033_073_090_207_feynman_schrodinger_exchange_and_five_import_cascade_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`
- `external:sha256:a1b05e0aea6beef6d9ccc993952ce0d4c00dc695716e48d1800112e2b77284f8#QM-090-C3`
- `external:sha256:a2f7562df5b5aeb03fb8dbd451d2007e85bf133ddf4d625c5b59f92b37ab489e#QM-093-C4`
- `external:sha256:a2f7562df5b5aeb03fb8dbd451d2007e85bf133ddf4d625c5b59f92b37ab489e#QM-093-C5`
- `external:sha256:b4a0392795f1e742a256ae815cdc26550b49a4f6e92e1b8c6beb0d28f159c92d::verify_tranche20_ds_qm032_033_073_090_207_feynman_schrodinger_exchange_and_five_import_cascade_witness`

## Routes

Incoming (1):

- `DS-R-UNIQUENESS` `GAP_NO_DERIVATION`: [DS-QM090-093-O022-REGISTRY-RELATIVE-MINIMALITY](DS-QM090-093-O022-REGISTRY-RELATIVE-MINIMALITY.md) (PROVED_LEAN)

Outgoing (0):

