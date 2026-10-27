# DS-QM064-074-083-ANNEX-REDIRECT-ROWS

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The 064, 074 and 083 annex claims (phase 1-cochain coboundary d1 d0 = 0, gauge invariance of triangle cycle holonomy, no-signaling marginal condition, and L1 contraction of stochastic Markov kernels) are mechanized in DerivationDagQMClosure.lean and NoSignalling.lean.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Lean states triangle holonomy gauge invariance and L1 contraction for 2x2 column-stochastic integer kernels. General kernels and the no-signalling clause are not in the cited Lean.

## Source status

Coboundary, triangle holonomy gauge invariance, and stochastic L1 contraction mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/DS-QM064-074-083-ANNEX-REDIRECT-ROWS/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM064-074-083-ANNEX-REDIRECT-ROWS/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Triangle identities, retained stochastic outputs and contextual marginal residuals are recomputed exactly; generic finite rational contraction is kernel checked.
  - does not support: Supply graph-to-phase, channel-to-kernel and physical composition/causality transports. The three control families do not by packaging close the annex interpretations.
  - next test: Supply graph-to-phase, channel-to-kernel and physical composition/causality transports. The three control families do not by packaging close the annex interpretations.

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
| `QuantumMechanics.DerivationDagQMClosure.qm064_triangle_holonomy_gauge_invariant` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm064_triangle_holonomy_gauge_invariant` |
| `QuantumMechanics.DerivationDagQMClosure.qm081_stochastic_l1_contraction` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm081_stochastic_l1_contraction` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0255_phase_gauge_annex_with_no_independent_derivation.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0255_phase_gauge_annex_with_no_independent_derivation.md](../../../dag/derivations/12_finite_qm_structure/tfq_0255_phase_gauge_annex_with_no_independent_derivation.md)
- sha256 (`lf-normalised`): `af20502cc21fd7ac4562b887afa7316536ae1d31fdec5fd6a973f502a72ad97a`
- generated view: listed, not counted
- cited in: record TFQ-0255
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0267_completely_positive_import_annex.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0267_completely_positive_import_annex.md](../../../dag/derivations/12_finite_qm_structure/tfq_0267_completely_positive_import_annex.md)
- sha256 (`lf-normalised`): `327ba50e1f22adcf109b389647ecd5375d52629a3ece5b90b7755e17ab4ec771`
- generated view: listed, not counted
- cited in: record TFQ-0267 (shared)
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:30aec070f0d0ba7a6c7a79671ca572935ebe155f5b10c29577ee4c127c455799#QM_074-C1`
- `external:sha256:31047098432c406509e13a12c95ce83041a099020c195e61eeb3dfa0d9b10d91#QM_083-C2`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_ds_qm_dynamics_structure_and_majorana_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- `external:sha256:b33b83fbc92bdce32f7ffe9662f6082ef96edc70e233ccf25b47560a6ad6968d#QM_064-C1`

## Routes

Incoming (1):

- `DS-R-REDIRECT` `COMPUTED`: [DS-QM063-HOLONOMY-COHERENT-INTENSITY](DS-QM063-HOLONOMY-COHERENT-INTENSITY.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

