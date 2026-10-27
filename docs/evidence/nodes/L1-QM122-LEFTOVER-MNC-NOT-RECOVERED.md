# L1-QM122-LEFTOVER-MNC-NOT-RECOVERED

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The finite Hilbert boundary from primitive difference does not recover ordinary M_n(C). Open: Gleason at n \>= 3, CPTP, tensor uniqueness, circle, Python dual. Imports listed in section 7: complex scalars as a field, circle phases, Born uniqueness (Gleason), Hilbert tensor, CPTP, continuous time. HilbertWalkGleasonFinish gives a declared finish table, not a derivation.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
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

This node records that no derivation of M_n(C) exists here; that is not a theorem. The cited Lean is a census of a declared Boolean table and Gaussian-integer norm identities. The listed imports stay imported.

## Source status

QM-122-C31..C37 eight-extra finish table (3 derived, 4 conditional, 1 false), Z\[i\] two-mode mixing weight-doubling identity, swapI unitary norm preservation outside real permutations, and 2x2=4 reversible dilation classification mechanized in DerivationDagQMClosure.lean and mirrored in finite_quantum_mechanics

## Review

- PFP review: [dag/results/L1-QM122-LEFTOVER-MNC-NOT-RECOVERED/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM122-LEFTOVER-MNC-NOT-RECOVERED/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: All matrix-unit products and noncommutativity are exact, alongside Gaussian unit/nonunit controls; generic matrix-unit scalar multiplication and a commutator control in Lean.
  - does not support: Recover the claimed complex field, circle, Born uniqueness, tensor/CPTP class, continuous time and source carrier maps, or retain them as admitted. A finish table is not completion evidence.
  - next test: Recover the claimed complex field, circle, Born uniqueness, tensor/CPTP class, continuous time and source carrier maps, or retain them as admitted. A finish table is not completion evidence.

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
| `QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm072_073_090_and_fq_import_boundary_certificates` |
| `QuantumMechanics.DerivationDagQMClosure.fq_entropy_renyi_purity_dichotomy_and_qm122_six_import_drop_one_census` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_entropy_renyi_purity_dichotomy_and_qm122_six_import_drop_one_census` |
| `QuantumMechanics.DerivationDagQMClosure.l1_qm122_leftover_mnc_eight_extra_finish_table_and_dilation_classifications` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm122_leftover_mnc_eight_extra_finish_table_and_dilation_classifications` |

- counts toward the grade: yes

### Lean: `lean4/FiniteQM.lean`

- file: [lean4/FiniteQM.lean](../../../lean4/FiniteQM.lean)
- sha256 (`bytes`): `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759`
- cited in: record TFQ-0311
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qcd.json](../../../dag/research/lean_replay_campaign_finite_qcd.json) (module `FiniteQM`): recorded sha256 `94cde0a3e760e5f17f309b950f2a02cfa40c895c8523a3986ab93123d7bd2759` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build FiniteQM`
- counts toward the grade: yes

### Lean: `lean4/HilbertWalkGleasonFin.lean`

- file: [lean4/HilbertWalkGleasonFin.lean](../../../lean4/HilbertWalkGleasonFin.lean)
- sha256 (`bytes`): `a33c2aa3109d5a5c9cf79e8e032720afc39d76841c9ee781eedaddb13c98b0d9`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `HilbertWalkGleasonFin`): recorded sha256 `a33c2aa3109d5a5c9cf79e8e032720afc39d76841c9ee781eedaddb13c98b0d9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build HilbertWalkGleasonFin`
- counts toward the grade: yes

### Lean: `lean4/HilbertWalkGleasonFinish.lean`

- file: [lean4/HilbertWalkGleasonFinish.lean](../../../lean4/HilbertWalkGleasonFinish.lean)
- sha256 (`bytes`): `d17eada69f37e9abb28ebc93122facd32716683618eed2c8e19e2b952b84daeb`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `HilbertWalkGleasonFinish`): recorded sha256 `d17eada69f37e9abb28ebc93122facd32716683618eed2c8e19e2b952b84daeb` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build HilbertWalkGleasonFinish`
- counts toward the grade: yes

### Rust: `sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs`

- file: [sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs](../../../sources/atlas/papers/finite_quantum_mechanics/native/src/derivation_dag_witnesses.rs)
- sha256 (`bytes`): `38c6a37e816f4f73e2a152eb2b657dfec6d350375f624886b0a45f613a20005a`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_tranche21_pg_wdp_bridge_sector_weights_qm122_finish_embedding_and_baker_witness` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/09_finite_hilbert/tfq_0311_ordinary_matrix_algebra_over_c_is_not_recovered.md`

- file: [dag/derivations/09_finite_hilbert/tfq_0311_ordinary_matrix_algebra_over_c_is_not_recovered.md](../../../dag/derivations/09_finite_hilbert/tfq_0311_ordinary_matrix_algebra_over_c_is_not_recovered.md)
- sha256 (`lf-normalised`): `33e7738d1da87b7cebb39dbce12aa731d8f63f6fc3526aa2dd11bcd3c80bd406`
- generated view: listed, not counted
- cited in: record TFQ-0311
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche21_pg_wdp_bridge_sector_weights_qm122_finish_embedding_and_baker_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche8_tensor_stone_continuum_embedding_and_leftover_mnc_witness`
- `external:sha256:86710ba8ef7db719a42a2165e71d3bc72ac5db63d0b2a51e57f48f14e137754e#C16`
- `external:sha256:b4a0392795f1e742a256ae815cdc26550b49a4f6e92e1b8c6beb0d28f159c92d::verify_tranche21_pg_wdp_bridge_sector_weights_qm122_finish_embedding_and_baker_witness`
- `external:sha256:f4ef85f405ba846ddf92fd6bbd8fc7aaa86d658c4678b4b841989f2cb97ee004`

## Absences recorded by the TFQ records

- TFQ-0311 python: no local python twin located for sources/atlas/papers/quantum_foundations/_code/qm_122/qm122_lib/qm122_dual.py

## Routes

Incoming (1):

- `L1-R-MNC-LEFTOVER` `GAP_NO_DERIVATION`: [L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE](L1-QM122-PHASE-BLIND-FIBER-INTERFERENCE.md) (PROVED_LEAN), [L1-QM122-CIRCLE-SELECTOR-BOUNDARY](L1-QM122-CIRCLE-SELECTOR-BOUNDARY.md) (COMPUTATIONALLY_CHECKED), [L1-QM122-BORN-PAIRING-NONUNIQUE](L1-QM122-BORN-PAIRING-NONUNIQUE.md) (COMPUTATIONALLY_CHECKED), [L1-IMP-HILBERT-INNER-PRODUCT](L1-IMP-HILBERT-INNER-PRODUCT.md) (CONDITIONAL)

Outgoing (0):

