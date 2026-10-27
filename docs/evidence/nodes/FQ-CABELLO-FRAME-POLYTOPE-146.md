# FQ-CABELLO-FRAME-POLYTOPE-146

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Independently exhaustive exact basis computations and every actual finite matrix witness, with a separate literal integer-list kernel certificate; the general real-polytope completeness bridge remains open.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- real-symmetric operator representative H_f (assumption)

## Bottleneck

Unmet after the PFP review: A formal Lean theorem identifying the entire real polytope vertex set, a general real spectral/PSD transport theorem, or positivity from finite frame additivity. The broader source statement is kept in pfp_review.prior_statement.

## Source status

paper s11.5: exact enumeration and exact characteristic-polynomial certificates (supplement s11.52)

## Review

- PFP review: [dag/results/FQ-CABELLO-FRAME-POLYTOPE-146/reviews/20261019_next_ten_audit/review_result.json](../../../dag/results/FQ-CABELLO-FRAME-POLYTOPE-146/reviews/20261019_next_ten_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Independently exhaustive exact basis computations and every actual finite matrix witness, with a separate literal integer-list kernel certificate; the general real-polytope completeness bridge remains open.
  - does not support: A formal Lean theorem identifying the entire real polytope vertex set, a general real spectral/PSD transport theorem, or positivity from finite frame additivity.
  - next test: Review basis coverage, source geometry, generated-data translation and the exact strict/non-strict spectral tests before promoting any broader claim.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1016
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.cabello_18_9_two_regular_and_146_census` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.cabello_18_9_two_regular_and_146_census` |
| `QuantumMechanics.DerivationDagQMClosure.fq_power_p2_cabello_146_and_weyl_commutant_irreducibility` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_power_p2_cabello_146_and_weyl_commutant_irreducibility` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1016_fq_cabello_frame_polytope_146.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1016_fq_cabello_frame_polytope_146.md](../../../dag/derivations/10_finite_qm_core/tfq_1016_fq_cabello_frame_polytope_146.md)
- sha256 (`lf-normalised`): `44626c0b00cbd58f65d406a07181880e51cd315ae7abdd9fe86b4931dd088adb`
- generated view: listed, not counted
- cited in: record TFQ-1016
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `85ca7b22b1c1e360a4c17ad8a9e0bddae03433592585b01d23a74cd09c82929e`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_fq_core_and_k23_duality_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:ae888a69f68011cf2bdbe26b173cbe6cf818f2a9c044b25aa7b39f5592b688c5::FrameSystem::is_vertex`
- `external:sha256:ae888a69f68011cf2bdbe26b173cbe6cf818f2a9c044b25aa7b39f5592b688c5::FrameSystem::vertices`

## Routes

Incoming (1):

- `FQ-R-CABELLO-POLYTOPE` `COMPUTED`: [FQ-CABELLO-NO-INTEGER-FRAME](FQ-CABELLO-NO-INTEGER-FRAME.md) (PROVED_LEAN)

Outgoing (1):

- `FQ-R-GAP-BORN-UNIQUENESS` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-BORN-UNIQUENESS-GLEASON](FQ-GAP-BORN-UNIQUENESS-GLEASON.md) (CONDITIONAL)
