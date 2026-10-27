# DS-QM062-U1-RESIDUES-IMPORT

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Continuity of reversible dynamics and global field uniqueness across n (needs local tomography) are imported; the complex amplitude lift requires an explicit U(1) phase fiber and complex involution. The discrete shadow does not separate U(1) from Q/Z torsion (QM-062-C4).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 31
- distinct cited Lean declarations covered by a current replay receipt: 29
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- U(1) phase fiber and complex involution (assumption)
- local tomography (assumption)
- connectedness / continuity (assumption)

## Bottleneck

Continuity of reversible dynamics, global field uniqueness, local tomography, a U(1) phase fiber, a complex involution, and a separation of that fiber from Q/Z torsion stay imported. The integer matrix of order 4 and the remainder identity (k + 4) modulo 4 are one finite case. This case does not select a phase fiber.

## Source status

\[IMPORTED\] (QM-062-C9, C10); QM-207-C2 \[PROVEN, CONDITIONAL\]

## Review

- PFP review: [dag/results/DS-QM062-U1-RESIDUES-IMPORT/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM062-U1-RESIDUES-IMPORT/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Actual J powers show order-four periodicity on retained indices; modulo-four aliasing is kernel checked for every natural k.
  - does not support: Supply continuity/topology, local tomography and a real exclusion/selection theorem if a full U(1) carrier is wanted. No finite-order exclusion follows from unbounded multiples.
  - next test: Supply continuity/topology, local tomography and a real exclusion/selection theorem if a full U(1) carrier is wanted. No finite-order exclusion follows from unbounded multiples.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0253 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels` | yes | yes | yes | propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels` |

- counts toward the grade: yes

### Lean: `lean4/U1ResiduesOrderFour.lean`

- file: [lean4/U1ResiduesOrderFour.lean](../../../lean4/U1ResiduesOrderFour.lean)
- sha256 (`bytes`): `e0cea83454141a891b39b8f1276fd453ef959066755a4bcd6a9430b01fcf9e4d`
- cited in: node.lean, receipt dag/research/campaign_ds-qm062-u1-residues-import_lean_replay.json (U1ResiduesOrderFour)
- replay: `verified`
  - receipt [dag/research/campaign_ds-qm062-u1-residues-import_lean_replay.json](../../../dag/research/campaign_ds-qm062-u1-residues-import_lean_replay.json) (module `U1ResiduesOrderFour`): recorded sha256 `e0cea83454141a891b39b8f1276fd453ef959066755a4bcd6a9430b01fcf9e4d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build U1ResiduesOrderFour`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `U1ResiduesOrderFour.alias4` | yes | yes | yes | propext | `#print axioms U1ResiduesOrderFour.alias4` |
| `U1ResiduesOrderFour.cu` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.cu` |
| `U1ResiduesOrderFour.eye_entries` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.eye_entries` |
| `U1ResiduesOrderFour.fourth` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.fourth` |
| `U1ResiduesOrderFour.jay2Ne` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.jay2Ne` |
| `U1ResiduesOrderFour.jay2_entries` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.jay2_entries` |
| `U1ResiduesOrderFour.jay3Ne` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.jay3Ne` |
| `U1ResiduesOrderFour.jay3_entries` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.jay3_entries` |
| `U1ResiduesOrderFour.jayNe` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.jayNe` |
| `U1ResiduesOrderFour.jay_entries` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.jay_entries` |
| `U1ResiduesOrderFour.mod_succ` | yes | yes | yes | propext | `#print axioms U1ResiduesOrderFour.mod_succ` |
| `U1ResiduesOrderFour.pow1` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.pow1` |
| `U1ResiduesOrderFour.pow2` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.pow2` |
| `U1ResiduesOrderFour.pow3` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.pow3` |
| `U1ResiduesOrderFour.pow4` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.pow4` |
| `U1ResiduesOrderFour.pow_eye` | yes | yes | yes | Quot.sound, propext | `#print axioms U1ResiduesOrderFour.pow_eye` |
| `U1ResiduesOrderFour.pow_period` | yes | yes | yes | Quot.sound, propext | `#print axioms U1ResiduesOrderFour.pow_period` |
| `U1ResiduesOrderFour.pow_rep` | yes | yes | yes | Quot.sound, propext | `#print axioms U1ResiduesOrderFour.pow_rep` |
| `U1ResiduesOrderFour.rem0` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.rem0` |
| `U1ResiduesOrderFour.rem1` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.rem1` |
| `U1ResiduesOrderFour.rem2` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.rem2` |
| `U1ResiduesOrderFour.rem3` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.rem3` |
| `U1ResiduesOrderFour.rem4` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.rem4` |
| `U1ResiduesOrderFour.rep_eye` | yes | yes | yes | Quot.sound, propext | `#print axioms U1ResiduesOrderFour.rep_eye` |
| `U1ResiduesOrderFour.rep_step` | yes | yes | yes | Quot.sound, propext | `#print axioms U1ResiduesOrderFour.rep_step` |
| `U1ResiduesOrderFour.sq` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.sq` |
| `U1ResiduesOrderFour.stepBack` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.stepBack` |
| `U1ResiduesOrderFour.stepNeg` | yes | yes | yes | none | `#print axioms U1ResiduesOrderFour.stepNeg` |

- counts toward the grade: yes

### Lean: `lean4/U1TorsionExclusion.lean`

- file: [lean4/U1TorsionExclusion.lean](../../../lean4/U1TorsionExclusion.lean)
- sha256 (`bytes`): `4ea188a7395bf5547790c477065ac72918b0a51264296f9890616b607ae6de44`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build U1TorsionExclusion`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `period_lattice_infinite` | yes | yes | yes | - | `#print axioms period_lattice_infinite` |
| `torsion_order_excluded` | yes | yes | yes | - | `#print axioms torsion_order_excluded` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0253_conditional_complex_carrier_selector.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0253_conditional_complex_carrier_selector.md](../../../dag/derivations/12_finite_qm_structure/tfq_0253_conditional_complex_carrier_selector.md)
- sha256 (`lf-normalised`): `156cf03a6e2efbe4a97922fe7e41bc0342db70068c5c46b2a82d79eb6b94f6cc`
- generated view: listed, not counted
- cited in: record TFQ-0253 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/062_the_u1_selector/qm_062_the_u1_selector_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/062_the_u1_selector/qm_062_the_u1_selector_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/207_complex_phase_fiber_and_u1_transport_lift/qm_207_complex_phase_fiber_and_u1_transport_lift_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/207_complex_phase_fiber_and_u1_transport_lift/qm_207_complex_phase_fiber_and_u1_transport_lift_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (0):


Outgoing (5):

- `DS-R-FIVE-IMPORT` `COMPUTED`: [DS-QM207-211-FIVE-IMPORT-CASCADE](DS-QM207-211-FIVE-IMPORT-CASCADE.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-SCHRODINGER-CONDITIONAL` `COMPUTED`: [DS-QM033-SCHRODINGER-DISCRETE-COCHAIN](DS-QM033-SCHRODINGER-DISCRETE-COCHAIN.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-SUPERPOSITION-FIBER` `DERIVED_LEAN`: [DS-QM060-SUPERPOSITION-QUOTIENT-FIBER](DS-QM060-SUPERPOSITION-QUOTIENT-FIBER.md) (PROVED_LEAN)
- `DS-R-U1-SELECTOR` `DERIVED_LEAN`: [DS-QM060-SUPERPOSITION-QUOTIENT-FIBER](DS-QM060-SUPERPOSITION-QUOTIENT-FIBER.md) (PROVED_LEAN)
- `DS-R-U1-SELECTOR-LAYERS` `COMPUTED`: [DS-QM062-U1-SELECTOR-LAYERS](DS-QM062-U1-SELECTOR-LAYERS.md) (COMPUTATIONALLY_CHECKED)

No incoming route.
