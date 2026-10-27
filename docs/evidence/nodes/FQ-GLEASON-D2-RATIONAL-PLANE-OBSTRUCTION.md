# FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On rational 2-vectors there is a binary-valued, scale-invariant frame function (additive on orthogonal frames) with no quadratic representation (no_quadratic_representation); in dimension 2 the Gleason dimension condition fails.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- rational plane Q^2 with orthogonality (assumption)

## Bottleneck

Says nothing for d \>= 3.

## Source status

repository module GleasonRationalPlane.lean (gap register S000-004/010); older GleasonTheorem.lean supplies arithmetic witnesses

## Review

- PFP review: [dag/results/FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION/reviews/20261019_scope_audit/review_result.json](../../../dag/results/FQ-GLEASON-D2-RATIONAL-PLANE-OBSTRUCTION/reviews/20261019_scope_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: The source rational-plane binary frame function is generally scale-invariant, additive on nonzero orthogonal frames, and has no quadratic representation; the concrete fitting residual is reproduced exactly.
  - does not support: No extension to dimension at least three, arbitrary real frames or a general Gleason reconstruction is supplied. A complete refined-carrier operad remains open.
  - next test: No extension to dimension at least three, arbitrary real frames or a general Gleason reconstruction is supplied. A complete refined-carrier operad remains open.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/GleasonRationalPlane.lean`

- file: [lean4/GleasonRationalPlane.lean](../../../lean4/GleasonRationalPlane.lean)
- sha256 (`bytes`): `91a4852b4de9cca52e348a22b6cb01a13bb27545c7be8cfef3793c337e2f46fb`
- cited in: node.lean, record TFQ-1014
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `GleasonRationalPlane`): recorded sha256 `91a4852b4de9cca52e348a22b6cb01a13bb27545c7be8cfef3793c337e2f46fb` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GleasonRationalPlane`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `binary_values` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms binary_values` |
| `no_quadratic_representation` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms no_quadratic_representation` |

- counts toward the grade: yes

### Lean: `lean4/GleasonTheorem.lean`

- file: [lean4/GleasonTheorem.lean](../../../lean4/GleasonTheorem.lean)
- sha256 (`bytes`): `881e01ee20e9af8f1d0f184edb5062447928fc98916c7a18f546d700fc839343`
- cited in: node.lean, record TFQ-1014
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `GleasonTheorem`): recorded sha256 `881e01ee20e9af8f1d0f184edb5062447928fc98916c7a18f546d700fc839343` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build GleasonTheorem`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `d2_binary_non_bornian_obstruction` | yes | yes | yes | Quot.sound, propext | `#print axioms d2_binary_non_bornian_obstruction` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1014_fq_gleason_d2_rational_plane_obstruction.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1014_fq_gleason_d2_rational_plane_obstruction.md](../../../dag/derivations/10_finite_qm_core/tfq_1014_fq_gleason_d2_rational_plane_obstruction.md)
- sha256 (`lf-normalised`): `4b0afcd82b553b954f90065e50fdbaa31634795f8c8309bde1480a5c263d1839`
- generated view: listed, not counted
- cited in: record TFQ-1014
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml`

- file: [sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml](../../../sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `722a38e963f9ae31ac005968a71e39dff5964e452f5aca1e5cb4506dc0ece190`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:ae888a69f68011cf2bdbe26b173cbe6cf818f2a9c044b25aa7b39f5592b688c5::FrameSystem`

## Routes

Incoming (1):

- `FQ-R-GLEASON-D2` `DERIVED_LEAN`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `FQ-R-GAP-BORN-UNIQUENESS` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-BORN-UNIQUENESS-GLEASON](FQ-GAP-BORN-UNIQUENESS-GLEASON.md) (CONDITIONAL)
