# FQ-POWER-RULE-P2-SELECTION

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Within the declared positive-power family P_p(i) = |c_i|^p / sum_j |c_j|^p on two rational orthonormal contexts sharing a ray (psi = (1,1,0), (3,4,5) rotation), context-independence holds iff (3/5)^p + (4/5)^p = 1, whose unique positive solution is p = 2. Classifies the power family; not a Gleason theorem. Sorkin I3 does not select p (vanishes at p=1 and p=2).

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

- power-law family of rules (assumption)
- declared real orthonormal contexts (assumption)

## Bottleneck

The real equation (3/5)^p + (4/5)^p = 1 iff p = 2 is stated in lean4/PromptStructure.lean (power_real_unique). The step that context-independence on the declared pair of contexts is equivalent to this equation is checked natively for integer p = 1..8, not in Lean.

## Source status

paper s11.6 (proof in supplement s11.58); rational controls in Rust

## Review

- PFP review: [dag/results/FQ-POWER-RULE-P2-SELECTION/reviews/20261019_structure_audit/review_result.json](../../../dag/results/FQ-POWER-RULE-P2-SELECTION/reviews/20261019_structure_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: The real power equation (3/5)^p+(4/5)^p=1 iff p=2 is kernel checked. Integer p=1..8 reproduce actual shared-ray context weights; mixed-sign p=1 supplies a retained counterexample to unrestricted Sorkin vanishing.
  - does not support: The power-law family, real exponentiation and the real orthonormal contexts are admitted; formal transport of the concrete context normalization to the Real.rpow equation remains a separate bridge. No unrestricted readout uniqueness or Gleason theorem follows.
  - next test: The power-law family, real exponentiation and the real orthonormal contexts are admitted; formal transport of the concrete context normalization to the Real.rpow equation remains a separate bridge. No unrestricted readout uniqueness or Gleason theorem follows.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1012
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_power_p2_cabello_146_and_weyl_commutant_irreducibility` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_power_p2_cabello_146_and_weyl_commutant_irreducibility` |
| `QuantumMechanics.DerivationDagQMClosure.power_rule_p2_unique_even_exponent` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.power_rule_p2_unique_even_exponent` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/power_rule_outcomes.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/power_rule_outcomes.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1012
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1012
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1012_fq_power_rule_p2_selection.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1012_fq_power_rule_p2_selection.md](../../../dag/derivations/10_finite_qm_core/tfq_1012_fq_power_rule_p2_selection.md)
- sha256 (`lf-normalised`): `554b9e3b133d1b0f8a952eec855303e5f3d68cc59eedc69ef6b041672cff1a3c`
- generated view: listed, not counted
- cited in: record TFQ-1012
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `85ca7b22b1c1e360a4c17ad8a9e0bddae03433592585b01d23a74cd09c82929e`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQ-R-POWER-RULE` `COMPUTED`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `FQ-R-GAP-BORN-UNIQUENESS` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-BORN-UNIQUENESS-GLEASON](FQ-GAP-BORN-UNIQUENESS-GLEASON.md) (CONDITIONAL)
