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

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0255_phase_gauge_annex_with_no_independent_derivation.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0255_phase_gauge_annex_with_no_independent_derivation.md](../../../dag/derivations/12_finite_qm_structure/tfq_0255_phase_gauge_annex_with_no_independent_derivation.md)
- sha256 (`lf-normalised`): `d9550d315f9a93fdeacf37fbcf43979ad633bc9c83d8a57913b54d2d6c468d88`
- generated view: listed, not counted
- cited in: record TFQ-0255
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0267_completely_positive_import_annex.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0267_completely_positive_import_annex.md](../../../dag/derivations/12_finite_qm_structure/tfq_0267_completely_positive_import_annex.md)
- sha256 (`lf-normalised`): `d15381a243e254164c16e1eafedefccb868275f35a792b8564ec7f910f8138f5`
- generated view: listed, not counted
- cited in: record TFQ-0267 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/064_phase_gauge_residual/qm_064_phase_gauge_residual_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/064_phase_gauge_residual/qm_064_phase_gauge_residual_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/074_no_signaling_finite_shadow/qm_074_no_signaling_finite_shadow_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/074_no_signaling_finite_shadow/qm_074_no_signaling_finite_shadow_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/083_completely_positive_import_boundary/qm_083_completely_positive_import_boundary_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/083_completely_positive_import_boundary/qm_083_completely_positive_import_boundary_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `DS-R-REDIRECT` `COMPUTED`: [DS-QM063-HOLONOMY-COHERENT-INTENSITY](DS-QM063-HOLONOMY-COHERENT-INTENSITY.md) (COMPUTATIONALLY_CHECKED)

Outgoing (0):

