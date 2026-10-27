# L1-QM020-THM7-REPRESENTATION-CAPACITY

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The Hilbert lift is probability-redundant (Thm 4) but dynamics-capable: it can host interference and reversible linear dynamics that l1 weights alone cannot. This is a capacity statement about the representation, not a derivation that physical dynamics are linear or unitary.

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

- linear isometric dynamics: assumption
- complex Hilbert space: assumption

## Bottleneck

Lean states one separation: two diagonal states with the same weights have the same plus/minus expectation at zero coherence and different ones at nonzero coherence c (qm020_thm7_representation_capacity). The capacity statement about reversible linear dynamics is not formalised.

## Source status

Thm 7 \[PROVEN\], representation-capacity

## Review

- PFP review: [dag/results/L1-QM020-THM7-REPRESENTATION-CAPACITY/reviews/20261020_born_boundary_audit/delivery_review_result.json](../../../dag/results/L1-QM020-THM7-REPRESENTATION-CAPACITY/reviews/20261020_born_boundary_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Actual rotation/inverse product, conserved norm and sign-dependent probability arrays, with generic norm and interference identities in Lean.
  - does not support: Justify physical linear isometric dynamics, source refinement and the complex Hilbert carrier. Capacity does not supply these hypotheses.
  - next test: Justify physical linear isometric dynamics, source refinement and the complex Hilbert carrier. Capacity does not supply these hypotheses.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BornRedundancy.lean`

- file: [lean4/BornRedundancy.lean](../../../lean4/BornRedundancy.lean)
- sha256 (`bytes`): `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b`
- cited in: record TFQ-0304
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_l1_to_l2.json](../../../dag/research/lean_replay_campaign_l1_to_l2.json) (module `BornRedundancy`): recorded sha256 `8868c1ceab52414128cac38a298bd28ca9cfc723613053c01ee90f23933b830b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build BornRedundancy`
- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_thm7_and_qm121_ladder_rungs_2_to_6_separation` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_thm7_and_qm121_ladder_rungs_2_to_6_separation` |
| `QuantumMechanics.DerivationDagQMClosure.qm020_thm7_representation_capacity` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm020_thm7_representation_capacity` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_0304_lift_capacity_is_not_a_dynamics_derivation.md`

- file: [dag/derivations/08_l1_to_l2/tfq_0304_lift_capacity_is_not_a_dynamics_derivation.md](../../../dag/derivations/08_l1_to_l2/tfq_0304_lift_capacity_is_not_a_dynamics_derivation.md)
- sha256 (`lf-normalised`): `b250145994d50c0398c477d627846c539e3d795dcf8fda60ee9ed94ed365889e`
- generated view: listed, not counted
- cited in: record TFQ-0304
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_l1_to_l2_bridges_and_ladder_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- `external:sha256:8534bf2948b65ab72605a33c219105f09458247c00aa57acc8beb275df568d27:881`
- `external:sha256:be048d5e98615cff70b3cdc1ebaa78a56395d67d55ca655cbb41494e307cde65`

## Absences recorded by the TFQ records

- TFQ-0304 rust: no local rust twin located for external:sha256:d58eb2c1f4ae2ac65cc7145554cd2a5c955e096776c1f6d9daafb2065b14450e

## Routes

Incoming (1):

- `L1-R-THM7` `COMPUTED`: [L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY](L1-QM020-THM4-HILBERT-LIFT-REDUNDANCY.md) (PROVED_PROSE), [L1-IMP-LINEAR-ISOMETRIC-DYNAMICS](L1-IMP-LINEAR-ISOMETRIC-DYNAMICS.md) (CONDITIONAL)

Outgoing (1):

- `L1-R-LADDER` `COMPUTED`: [L1-QM121-LADDER-RUNGS-2-6](L1-QM121-LADDER-RUNGS-2-6.md) (COMPUTATIONALLY_CHECKED)
