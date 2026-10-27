# FQ-DISCRETE-DYNAMICS-DICHOTOMY

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a declared finite unitary step, finite order is decided by cyclotomic characteristic factors with replay; the Lean example is the Pythagorean rotation (3/5,4/5), whose powers never return to the identity (pythagorean_rotation_order_infinite). Two bookkeeping theorems (periodic_sector_requires_declaration, aperiodic_sector_closure_no_declaration) hold by rfl on declared price constants and carry no independent mathematical content.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- declared unitary step (assumption)
- generator branch selection for periodic sector (assumption)

## Bottleneck

Lean states that no power of the Pythagorean rotation (3/5, 4/5) is the identity (pythagorean_rotation_order_infinite). The cyclotomic decision procedure for a general declared step is a native replay. periodic_sector_requires_declaration evaluates a declared constant.

## Source status

H061; Rust exact periodic/aperiodic classification

## Review

- PFP review: [dag/results/FQ-DISCRETE-DYNAMICS-DICHOTOMY/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/FQ-DISCRETE-DYNAMICS-DICHOTOMY/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: An all-natural-index integer numerator is nonzero in Lean; actual normalized retained powers have unit mass and never equal identity, unlike periodic controls.
  - does not support: Prove the recurrence-to-normalized-matrix bridge for all powers, then formulate any closure/topology or generator selection claim. No full dynamics dichotomy is inferred.
  - next test: Prove the recurrence-to-normalized-matrix bridge for all powers, then formulate any closure/topology or generator selection claim. No full dynamics dichotomy is inferred.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: record TFQ-0245 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`
- counts toward the grade: no

### Lean: `lean4/DynamicsDichotomy.lean`

- file: [lean4/DynamicsDichotomy.lean](../../../lean4/DynamicsDichotomy.lean)
- sha256 (`bytes`): `05fb05316c51102e92e1d613434e93b41e84b96b51308a1e34a5fb60f3318c9a`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_dynamics.json](../../../dag/research/lean_replay_campaign_finite_qm_dynamics.json) (module `DynamicsDichotomy`): recorded sha256 `05fb05316c51102e92e1d613434e93b41e84b96b51308a1e34a5fb60f3318c9a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DynamicsDichotomy`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `periodic_sector_requires_declaration` | yes | yes | yes | none | `#print axioms periodic_sector_requires_declaration` |
| `pythagorean_rotation_order_infinite` | yes | yes | yes | Quot.sound, propext | `#print axioms pythagorean_rotation_order_infinite` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0245_unitary_finite_shadow_slot_still_reserved.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0245_unitary_finite_shadow_slot_still_reserved.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0245_unitary_finite_shadow_slot_still_reserved.md)
- sha256 (`lf-normalised`): `e2513e40c2ecce086e21e2854c8fe5265bcc64d468c32f322951cdebceca3fa9`
- generated view: listed, not counted
- cited in: record TFQ-0245 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/14_finite_gauge/tfq_0052_each_language_must_carry_on_a_declared_m_2_q_i_packet_d0_of_an.md`

- file: [dag/derivations/14_finite_gauge/tfq_0052_each_language_must_carry_on_a_declared_m_2_q_i_packet_d0_of_an.md](../../../dag/derivations/14_finite_gauge/tfq_0052_each_language_must_carry_on_a_declared_m_2_q_i_packet_d0_of_an.md)
- sha256 (`lf-normalised`): `9d6162aed312ba2ddb1cf7c9c064ff94f92a33337fb7a8ffd5001b7600c2c036`
- generated view: listed, not counted
- cited in: record TFQ-0052 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/15_finite_qed/tfq_0062_each_language_must_carry_a_truncated_intermediate_normalization_series_a.md`

- file: [dag/derivations/15_finite_qed/tfq_0062_each_language_must_carry_a_truncated_intermediate_normalization_series_a.md](../../../dag/derivations/15_finite_qed/tfq_0062_each_language_must_carry_a_truncated_intermediate_normalization_series_a.md)
- sha256 (`lf-normalised`): `a9bdb52dd01224b852a23cf101788a30e114d78102039865913146343120437d`
- generated view: listed, not counted
- cited in: record TFQ-0062
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml`

- file: [sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml](../../../sources/atlas/papers/finite_quantum_mechanics/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `722a38e963f9ae31ac005968a71e39dff5964e452f5aca1e5cb4506dc0ece190`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `85ca7b22b1c1e360a4c17ad8a9e0bddae03433592585b01d23a74cd09c82929e`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- `external:sha256:c1723f5ad590b2aa43e5882c6479aa8af966b86b3312b09cfc4051749dd507f1::classify_unitary_orbit`

## Absences recorded by the TFQ records

- TFQ-0052 lean4: not located
- TFQ-0052 python: not located
- TFQ-0052 rust: no local rust twin located for external:sha256:1716598040aa40ee83bed4fdf0e76ab6111debd683decf50bbbe5df6dbc71b65
- TFQ-0062 lean4: not located
- TFQ-0062 python: not located
- TFQ-0062 rust: no local rust twin located for external:sha256:a60d347705d09f5b9f8544dc54af5241d756b5b8e476337baf9eb9d4f93d82b3

## Routes

Incoming (1):

- `FQ-R-DYN-DICHOTOMY` `COMPUTED`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION), [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `FQ-R-STONE-AMBIGUITY` `COMPUTED`: [FQ-DISCRETE-TIME-STONE-AMBIGUITY](FQ-DISCRETE-TIME-STONE-AMBIGUITY.md) (COMPUTATIONALLY_CHECKED)
