# L1-QM020-THM7-REPRESENTATION-CAPACITY

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The Hilbert lift is probability-redundant (Thm 4) but dynamics-capable: it can host interference and reversible linear dynamics that l1 weights alone cannot. This is a capacity statement about the representation, not a derivation that physical dynamics are linear or unitary.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- linear isometric dynamics: assumption
- complex Hilbert space: assumption

## Bottleneck

No Lean located. The interference non-descent boundary is in the QM_122 nodes.

## Source status

Thm 7 \[PROVEN\], representation-capacity

## Review

- PFP review: [dag/results/L1-QM020-THM7-REPRESENTATION-CAPACITY/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM020-THM7-REPRESENTATION-CAPACITY/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Actual rotation/inverse product, conserved norm and sign-dependent probability arrays, with generic norm and interference identities in Lean.
  - does not support: Justify physical linear isometric dynamics, source refinement and the complex Hilbert carrier. Capacity does not supply these hypotheses.
  - next test: Justify physical linear isometric dynamics, source refinement and the complex Hilbert carrier. Capacity does not supply these hypotheses.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornRedundancy.lean`

- file: [lean4/BornRedundancy.lean](../../../lean4/BornRedundancy.lean)
- sha256 (`bytes`): `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b`
- cited in: record TFQ-0304
- replay: `none`
- check: `cd lean4 && lake build BornRedundancy`
- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_thm7_and_qm121_ladder_rungs_2_to_6_separation` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_thm7_and_qm121_ladder_rungs_2_to_6_separation` |
| `QuantumMechanics.DerivationDagQMClosure.qm020_thm7_representation_capacity` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm020_thm7_representation_capacity` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/coherent_interference.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/coherent_interference.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0304_lift_capacity_is_not_a_dynamics_derivation.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0304_lift_capacity_is_not_a_dynamics_derivation.md](../../../dag/derivations/08_l1_to_l2/tfq_0304_lift_capacity_is_not_a_dynamics_derivation.md)
- sha256 (`lf-normalised`): `b250145994d50c0398c477d627846c539e3d795dcf8fda60ee9ed94ed365889e`
- generated view: listed, not counted
- cited in: record TFQ-0304
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/020_born_normalization_and_conditional_hilbert_lift/born_normalization_and_conditional_hilbert_lift.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0304 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_state.rs

## Routes

Incoming (1):

- `L1-R-THM7` `DERIVED_LEAN`: [L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY](L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY.md) (PROVED_LEAN), [L1-IMP-LINEAR-ISOMETRIC-DYNAMICS](L1-IMP-LINEAR-ISOMETRIC-DYNAMICS.md) (CONDITIONAL)

Outgoing (1):

- `L1-R-LADDER` `DERIVED_LEAN`: [L1-QM121-LADDER-RUNGS-2-6](L1-QM121-LADDER-RUNGS-2-6.md) (PROVED_LEAN)
