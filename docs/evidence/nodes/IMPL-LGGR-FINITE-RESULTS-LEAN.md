# IMPL-LGGR-FINITE-RESULTS-LEAN

Stage: [IMPLEMENTATION](../stages/IMPLEMENTATION.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> LggrFiniteResults.lean under lean4/quantum_mechanics: finite LGGR results only, from the QDDC, LGGR and no-go implementation-status thread. Gaps named by that thread: the l1 defect and LP dual live only in Rust, the Lean gate model is not linked to the Rust gate, and Proposition II-open stays OPEN.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- cited Lean declaration references covered by a current replay receipt: 7
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Not covered by the PFP review: Prove the external Rust gate/representation and arbitrary LP/cycle refinements. Proposition II-open and physical-selection claims remain open; a census/route partition is not this proof.

## Source status

MECHANIZED in LggrFiniteResults.lean (B1, B2', B11, B11', and Part 6 LP dual 2/3 bound + gate alignment) with Rust witness

## Review

- PFP review: [dag/results/IMPL-LGGR-FINITE-RESULTS-LEAN/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json](../../../dag/results/IMPL-LGGR-FINITE-RESULTS-LEAN/reviews/20261019_genesis_impl_audit/final_delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `reviewed_with_targeted_native_integration`; scope effect `caveat_added`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Actual bounded cycle sections, gate fields, triangle primal mixture and matching2/3 dual controls are exact; the conditional source-model gate equivalence and attainment arithmetic are kernel checked.
  - does not support: Prove the external Rust gate/representation and arbitrary LP/cycle refinements. Proposition II-open and physical-selection claims remain open; a census/route partition is not this proof.
  - next test: Prove the external Rust gate/representation and arbitrary LP/cycle refinements. Proposition II-open and physical-selection claims remain open; a census/route partition is not this proof.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1046
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation` |
| `QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure` |

- counts toward the grade: yes

### Lean: `lean4/LggrFiniteResults.lean`

- file: [lean4/LggrFiniteResults.lean](../../../lean4/LggrFiniteResults.lean)
- sha256 (`bytes`): `ce736b577beb07997dba02bd7f86f83f1ecac7ce7a569e72b6350171179f34de`
- cited in: node.lean, node.source, record TFQ-1046
- replay: `verified`
  - receipt [dag/research/foc035_observer_presheaf_lean_replay.json](../../../dag/research/foc035_observer_presheaf_lean_replay.json) (module `LggrFiniteResults`): recorded sha256 `ce736b577beb07997dba02bd7f86f83f1ecac7ce7a569e72b6350171179f34de` matches the current file; exit code 0; Lean Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/foc035_observer_presheaf_lean_replay.json](../../../dag/research/foc035_observer_presheaf_lean_replay.json) (module `LggrFiniteResults`): recorded sha256 `ce736b577beb07997dba02bd7f86f83f1ecac7ce7a569e72b6350171179f34de` matches the current file; exit code 0; Lean Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `LggrFiniteResults`): recorded sha256 `ce736b577beb07997dba02bd7f86f83f1ecac7ce7a569e72b6350171179f34de` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build LggrFiniteResults`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `LggrFiniteResults.lggrCycleGateAdmits_iff_section_or_zero_mass` | yes | yes | yes | Quot.sound, propext | `#print axioms LggrFiniteResults.lggrCycleGateAdmits_iff_section_or_zero_mass` |
| `LggrFiniteResults.no_joint_measure_when_holonomy_one` | yes | yes | yes | Quot.sound, propext | `#print axioms LggrFiniteResults.no_joint_measure_when_holonomy_one` |
| `LggrFiniteResults.odd_triangle_lp_dual_defect_pos` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms LggrFiniteResults.odd_triangle_lp_dual_defect_pos` |
| `LggrFiniteResults.section_exists_iff_holonomy_zero` | yes | yes | yes | Quot.sound, propext | `#print axioms LggrFiniteResults.section_exists_iff_holonomy_zero` |
| `LggrFiniteResults.totalSatWeight3_le_two_mul_mass` | yes | yes | yes | Quot.sound, propext | `#print axioms LggrFiniteResults.totalSatWeight3_le_two_mul_mass` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1046
- counts toward the grade: no

### Documents and data: `dag/derivations/21_implementation_core/tfq_1046_impl_lggr_finite_results_lean.md`

- file: [dag/derivations/21_implementation_core/tfq_1046_impl_lggr_finite_results_lean.md](../../../dag/derivations/21_implementation_core/tfq_1046_impl_lggr_finite_results_lean.md)
- sha256 (`lf-normalised`): `2d155f83fe72acc14ae56bcabfdea0ca1fa8cbff709abdfa868cce49d894aa37`
- generated view: listed, not counted
- cited in: record TFQ-1046
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml`

- file: [sources/atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml](../../../sources/atlas/F004_papers/003_quantum_foundations/dag_pregenesis_to_finite_qm/derivation_dag_operads.binding.yaml)
- sha256 (`lf-normalised`): `2bfb4441352c4206cbd84f3e500e4c3ba817364aff49623a001087ecf12df5a6`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `IMPL-R-LGGR-FINITE-RESULTS` `DERIVED_LEAN`: [L1-OBSERVER-AXIOMS-H1-H5](L1-OBSERVER-AXIOMS-H1-H5.md) (ADMITTED_PRIMITIVE)

Outgoing (4):

- `OPS-R-LEAN-GAP` `GAP_NO_DERIVATION`: [OPS-LEAN-GAP](OPS-LEAN-GAP.md) (OPEN)
- `OPS-R-PARITY-HOLONOMY-LEAN` `DERIVED_LEAN`: [OPS-PARITY-HOLONOMY-LEAN](OPS-PARITY-HOLONOMY-LEAN.md) (PROVED_LEAN)
- `OPS-R-PR1050-ABSENCE` `RECORD_PARENT`: [OPS-PR1050-ABSENCE](OPS-PR1050-ABSENCE.md) (SOURCE_RECORD)
- `OPS-R-PUSHFORWARD-FUNCTOR-LEAN` `DERIVED_LEAN`: [OPS-PUSHFORWARD-FUNCTOR-LEAN](OPS-PUSHFORWARD-FUNCTOR-LEAN.md) (PROVED_LEAN)
