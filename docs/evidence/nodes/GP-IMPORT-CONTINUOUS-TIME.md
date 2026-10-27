# GP-IMPORT-CONTINUOUS-TIME

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Continuous time, topology, a one-parameter unitary group and Stone's theorem. The two-state toggle has no report-level square root; after complex coefficients, interpolants exist at scale 4 and are not unique.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 25
- distinct cited Lean declarations covered by a current replay receipt: 12
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- continuous time: assumption
- topology on the carrier: assumption
- one-parameter group: assumption
- Stone's theorem: import

## Bottleneck

Continuous time, a topology, a one-parameter unitary group and Stone's theorem stay imported. The Boolean toggle and the two Gaussian-integer interpolants at scale 4 are one finite case. A rational Cayley transform and a hyperoctahedral residue stay outside this case.

## Source status

imported / refused on this host

## Review

- PFP review: [dag/results/GP-IMPORT-CONTINUOUS-TIME/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/GP-IMPORT-CONTINUOUS-TIME/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Complete Boolean square-root obstruction and both exact complex unitary square roots of toggle; generic projector-square algebra and Boolean enumeration in Lean.
  - does not support: Supply topology, continuous time and the one-parameter group; invoke Stone only under its hypotheses. Square roots alone do not define continuous dynamics.
  - next test: Supply topology, continuous time and the one-parameter group; invoke Stone only under its hypotheses. Square roots alone do not define continuous dynamics.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ContinuousDynamicsFork.lean`

- file: [lean4/ContinuousDynamicsFork.lean](../../../lean4/ContinuousDynamicsFork.lean)
- sha256 (`bytes`): `135a00f4b383fbdc849d9acd1cd61ee738bfd656be50fe2b490db89041c8e36b`
- cited in: node.lean, record TFQ-1034
- replay: `none`
- check: `cd lean4 && lake build ContinuousDynamicsFork`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `HilbertWalk.ContinuousDynamicsFork.continuous_dynamics_fork` | yes | yes | yes | - | `#print axioms HilbertWalk.ContinuousDynamicsFork.continuous_dynamics_fork` |
| `HilbertWalk.ContinuousDynamicsFork.no_report_half_step` | yes | yes | yes | - | `#print axioms HilbertWalk.ContinuousDynamicsFork.no_report_half_step` |

- counts toward the grade: yes

### Lean: `lean4/ContinuousTimeImport.lean`

- file: [lean4/ContinuousTimeImport.lean](../../../lean4/ContinuousTimeImport.lean)
- sha256 (`bytes`): `0e012ae91f849150a046474fd241229c1fa78fc5dec8d71bfc000944fe90b68d`
- cited in: node.lean, receipt dag/research/campaign_gp-import-continuous-time_lean_replay.json (ContinuousTimeImport), record TFQ-1034
- replay: `verified`
  - receipt [dag/research/campaign_gp-import-continuous-time_lean_replay.json](../../../dag/research/campaign_gp-import-continuous-time_lean_replay.json) (module `ContinuousTimeImport`): recorded sha256 `0e012ae91f849150a046474fd241229c1fa78fc5dec8d71bfc000944fe90b68d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ContinuousTimeImport`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ContinuousTimeImport.gAdd_coords` | yes | yes | yes | none | `#print axioms ContinuousTimeImport.gAdd_coords` |
| `ContinuousTimeImport.gMul_coords` | yes | yes | yes | none | `#print axioms ContinuousTimeImport.gMul_coords` |
| `ContinuousTimeImport.interpNeg_twice_is_scaled_swap` | yes | yes | yes | Quot.sound, propext | `#print axioms ContinuousTimeImport.interpNeg_twice_is_scaled_swap` |
| `ContinuousTimeImport.interp_twice_is_scaled_swap` | yes | yes | yes | Quot.sound, propext | `#print axioms ContinuousTimeImport.interp_twice_is_scaled_swap` |
| `ContinuousTimeImport.interpolants_differ` | yes | yes | yes | none | `#print axioms ContinuousTimeImport.interpolants_differ` |
| `ContinuousTimeImport.no_toggle_square_root` | yes | yes | yes | none | `#print axioms ContinuousTimeImport.no_toggle_square_root` |
| `ContinuousTimeImport.scale4_swap` | yes | yes | yes | none | `#print axioms ContinuousTimeImport.scale4_swap` |
| `ContinuousTimeImport.swap_exchanges` | yes | yes | yes | none | `#print axioms ContinuousTimeImport.swap_exchanges` |
| `ContinuousTimeImport.toggle_images` | yes | yes | yes | none | `#print axioms ContinuousTimeImport.toggle_images` |
| `ContinuousTimeImport.witness_interp` | yes | yes | yes | none | `#print axioms ContinuousTimeImport.witness_interp` |
| `ContinuousTimeImport.witness_neg` | yes | yes | yes | none | `#print axioms ContinuousTimeImport.witness_neg` |
| `gAdd_coords` | yes | yes | yes | none | `#print axioms gAdd_coords` |
| `gMul_coords` | yes | yes | yes | none | `#print axioms gMul_coords` |
| `interpNeg_twice_is_scaled_swap` | yes | yes | yes | Quot.sound, propext | `#print axioms interpNeg_twice_is_scaled_swap` |
| `interp_twice_is_scaled_swap` | yes | yes | yes | Quot.sound, propext | `#print axioms interp_twice_is_scaled_swap` |
| `interpolants_differ` | yes | yes | yes | none | `#print axioms interpolants_differ` |
| `no_toggle_square_root` | yes | yes | yes | none | `#print axioms no_toggle_square_root` |
| `scale4_swap` | yes | yes | yes | none | `#print axioms scale4_swap` |
| `swap_exchanges` | yes | yes | yes | none | `#print axioms swap_exchanges` |
| `toggle_images` | yes | yes | yes | none | `#print axioms toggle_images` |
| `witness_interp` | yes | yes | yes | none | `#print axioms witness_interp` |
| `witness_neg` | yes | yes | yes | none | `#print axioms witness_neg` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1034
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1034_gp_import_continuous_time.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1034_gp_import_continuous_time.md](../../../dag/derivations/08_l1_to_l2/tfq_1034_gp_import_continuous_time.md)
- sha256 (`lf-normalised`): `c07a0a8dd44214310899fa27b5945dc3e441709239930dd84f5fd2f74430af6a`
- generated view: listed, not counted
- cited in: record TFQ-1034
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:49250fc3940b574236fe8aeb8acabb9673af35fe28f17474e9deb52ecd18a713#GAP-F001-S000-008`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`
- `external:sha256:a635008d68c51a062b794996dc85a68693522928a157d619d01ffada1ba595f1#PRICE-HD-03`
- `external:sha256:a635008d68c51a062b794996dc85a68693522928a157d619d01ffada1ba595f1#PRICE-HD-06`
- `external:sha256:f4ef85f405ba846ddf92fd6bbd8fc7aaa86d658c4678b4b841989f2cb97ee004:156`

## Routes

Incoming (0):


Outgoing (2):

- `X-R-DROP-ONE-CENSUS` `DERIVED_LEAN`: [GP-DROP-ONE-CENSUS](GP-DROP-ONE-CENSUS.md) (PROVED_LEAN)
- `X-R-IMPORTS-TO-DECLARED-INTERFACE` `CONDITIONAL_ON_IMPORT`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)

No incoming route.
