# GP-FIN-GAUSS-MATRIX-ALGEBRA

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Over Gauss-integer coefficients and a finite enumerated report set Q (|Q| = n), every additive homogeneous endomorphism is left multiplication by a unique n x n Gauss-integer matrix; product is composition and conjugate transpose is the adjoint of the admitted pairing. This is M_n(Z\[i\]), not M_n(C).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Gaussian-integer coefficients: assumption
- admitted pairing: assumption

## Bottleneck

Scoped recovery only; spectral theorem, completeness, CPTP, unique tensor, circle, continuous time remain separate imports.

## Source status

Lean-compiled; axioms propext, Quot.sound

## Review

- PFP review: [dag/results/GP-FIN-GAUSS-MATRIX-ALGEBRA/reviews/20261019_structure_audit/review_result.json](../../../dag/results/GP-FIN-GAUSS-MATRIX-ALGEBRA/reviews/20261019_structure_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Finite Gauss-integer matrix recovery, uniqueness, composition and adjoint laws are rechecked generally on the source finite enumeration interface; exact native 2x2 examples independently verify the concrete laws.
  - does not support: Gaussian coefficients, linearity, finite enumeration and pairing remain assumptions. M_n(Z\[i\]) supplies neither M_n(C), spectral completeness, CPTP, unique tensor nor continuous time.
  - next test: Gaussian coefficients, linearity, finite enumeration and pairing remain assumptions. M_n(Z\[i\]) supplies neither M_n(C), spectral completeness, CPTP, unique tensor nor continuous time.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1037
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_impl_wdp_amplitude_realification_pairing_and_gauss_matrix_algebra` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_impl_wdp_amplitude_realification_pairing_and_gauss_matrix_algebra` |
- counts toward the grade: yes

### Lean: `lean4/H017Fin.lean`

- file: [lean4/H017Fin.lean](../../../lean4/H017Fin.lean)
- sha256 (`bytes`): `2294ae2512eac4a7c5167954b86118c7f02638dafbdb42b4b894fc1fbdc4dea2`
- cited in: node.lean, record TFQ-1037
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `H017Fin`): recorded sha256 `2294ae2512eac4a7c5167954b86118c7f02638dafbdb42b4b894fc1fbdc4dea2` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build H017Fin`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `finite_gauss_matrix_algebra` | yes | yes | yes | Quot.sound, propext | `#print axioms finite_gauss_matrix_algebra` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1037
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1037_gp_fin_gauss_matrix_algebra.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1037_gp_fin_gauss_matrix_algebra.md](../../../dag/derivations/10_finite_qm_core/tfq_1037_gp_fin_gauss_matrix_algebra.md)
- sha256 (`lf-normalised`): `9a73f8702b513e7ebb3dc6e15be18b86ff620a8528225bb98e4b23037386ddcf`
- generated view: listed, not counted
- cited in: record TFQ-1037
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/finite_hilbert_boundary_from_primitive_difference.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/122_finite_hilbert_boundary_from_primitive_difference/finite_hilbert_boundary_from_primitive_difference.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `X-R-GAUSS-ALGEBRA-FROM-Z-I` `DERIVED_LEAN`: [L1-IMP-COMPLEX-FIELD](L1-IMP-COMPLEX-FIELD.md) (CONDITIONAL)

Outgoing (1):

- `APP-R-MUB-EXACT-PROJECTORS` `CONDITIONAL_ON_IMPORT`: [MUB-EXACT-PROJECTORS](MUB-EXACT-PROJECTORS.md) (DEFINITION)
