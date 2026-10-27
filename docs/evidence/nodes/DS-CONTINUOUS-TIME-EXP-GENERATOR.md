# DS-CONTINUOUS-TIME-EXP-GENERATOR

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The one-parameter family T(t)=exp(tH), the generator H=log T and the continuum path integral need real/complex time, convergence and a measure; none is constructed from the finite transport calculus. Refused as finite.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 16
- distinct cited Lean declarations covered by a current replay receipt: 15
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- continuous time t (assumption)
- exp/log of operators, Stone-type generator (assumption)
- continuum measure and convergence oracle (assumption)

## Bottleneck

The one-parameter family T(t) = exp(tH), the generator H = log T, and a continuum path integral stay imported. They still ask for real or complex time, a convergence oracle, and a measure, and none of those is constructed from the finite transport calculus. Generator selection among the odd branch energies stays a priced interface. The Boolean toggle, the two scale-4 matrices, the Cayley polynomial, the branch energies, and the absent nilpotent integer logarithm of the swap are one finite case.

## Source status

\[CONDITIONAL — OracleNeeded(Convergence); REFUSED as finite\] (QM-030-C7); QM-031-C16 \[SCOPE FENCE / IMPORTED\]

## Review

- PFP review: [dag/results/DS-CONTINUOUS-TIME-EXP-GENERATOR/reviews/20261019_structure_audit/review_result.json](../../../dag/results/DS-CONTINUOUS-TIME-EXP-GENERATOR/reviews/20261019_structure_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: No Boolean report-map half-step exists, while two distinct normalized Q(i) amplitude half-steps square to swap and are unitary. The source scaled-root and report obstruction proofs are rechecked.
  - does not support: Construct a continuous-time group, analytic logarithms, generator selection, convergence and any continuum measure with their actual hypotheses. Discrete roots or injective branch tags do not supply those interfaces.
  - next test: Construct a continuous-time group, analytic logarithms, generator selection, convergence and any continuum measure with their actual hypotheses. Discrete roots or injective branch tags do not supply those interfaces.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ContinuousDynamicsFork.lean`

- file: [lean4/ContinuousDynamicsFork.lean](../../../lean4/ContinuousDynamicsFork.lean)
- sha256 (`bytes`): `135a00f4b383fbdc849d9acd1cd61ee738bfd656be50fe2b490db89041c8e36b`
- cited in: node.lean, record TFQ-1040
- replay: `none`
- check: `cd lean4 && lake build ContinuousDynamicsFork`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `continuous_dynamics_fork` | yes | yes | yes | - | `#print axioms continuous_dynamics_fork` |

- counts toward the grade: yes

### Lean: `lean4/ContinuousTimeExpGenerator.lean`

- file: [lean4/ContinuousTimeExpGenerator.lean](../../../lean4/ContinuousTimeExpGenerator.lean)
- sha256 (`bytes`): `03d58f4e60ab3368f101da133736a9ee3355d00973ffe3b90ca99bc1908f2da6`
- cited in: node.lean, receipt dag/research/campaign_ds-continuous-time-exp-generator_lean_replay.json (ContinuousTimeExpGenerator), record TFQ-1040
- replay: `verified`
  - receipt [dag/research/campaign_ds-continuous-time-exp-generator_lean_replay.json](../../../dag/research/campaign_ds-continuous-time-exp-generator_lean_replay.json) (module `ContinuousTimeExpGenerator`): recorded sha256 `03d58f4e60ab3368f101da133736a9ee3355d00973ffe3b90ca99bc1908f2da6` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build ContinuousTimeExpGenerator`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ContinuousTimeExpGenerator.candidateCorner` | yes | yes | yes | none | `#print axioms ContinuousTimeExpGenerator.candidateCorner` |
| `ContinuousTimeExpGenerator.cayleyNorm` | yes | yes | yes | Quot.sound, propext | `#print axioms ContinuousTimeExpGenerator.cayleyNorm` |
| `ContinuousTimeExpGenerator.energyDistinct` | yes | yes | yes | Quot.sound, propext | `#print axioms ContinuousTimeExpGenerator.energyDistinct` |
| `ContinuousTimeExpGenerator.energyOne` | yes | yes | yes | none | `#print axioms ContinuousTimeExpGenerator.energyOne` |
| `ContinuousTimeExpGenerator.energyZero` | yes | yes | yes | none | `#print axioms ContinuousTimeExpGenerator.energyZero` |
| `ContinuousTimeExpGenerator.gAddCoords` | yes | yes | yes | none | `#print axioms ContinuousTimeExpGenerator.gAddCoords` |
| `ContinuousTimeExpGenerator.gMulCoords` | yes | yes | yes | none | `#print axioms ContinuousTimeExpGenerator.gMulCoords` |
| `ContinuousTimeExpGenerator.negSquare` | yes | yes | yes | none | `#print axioms ContinuousTimeExpGenerator.negSquare` |
| `ContinuousTimeExpGenerator.noNilpotentIntegerLog` | yes | yes | yes | Quot.sound, propext | `#print axioms ContinuousTimeExpGenerator.noNilpotentIntegerLog` |
| `ContinuousTimeExpGenerator.noToggleSquare` | yes | yes | yes | none | `#print axioms ContinuousTimeExpGenerator.noToggleSquare` |
| `ContinuousTimeExpGenerator.scaledDiffer` | yes | yes | yes | none | `#print axioms ContinuousTimeExpGenerator.scaledDiffer` |
| `ContinuousTimeExpGenerator.scaledSquare` | yes | yes | yes | none | `#print axioms ContinuousTimeExpGenerator.scaledSquare` |
| `ContinuousTimeExpGenerator.toggleImages` | yes | yes | yes | none | `#print axioms ContinuousTimeExpGenerator.toggleImages` |

- counts toward the grade: yes

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1040
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels` | yes | yes | yes | propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_gap_measurement_projection_cptp_and_continuous_time_generator_countermodels` |

- counts toward the grade: yes

### Lean: `lean4/DiscreteDynamicsStone.lean`

- file: [lean4/DiscreteDynamicsStone.lean](../../../lean4/DiscreteDynamicsStone.lean)
- sha256 (`bytes`): `02c2108be73f205cca1ec29fbbd5c897ff957547991f7371c12b53ff1dbab102`
- cited in: node.lean, record TFQ-1040
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_dynamics.json](../../../dag/research/lean_replay_campaign_finite_qm_dynamics.json) (module `DiscreteDynamicsStone`): recorded sha256 `02c2108be73f205cca1ec29fbbd5c897ff957547991f7371c12b53ff1dbab102` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DiscreteDynamicsStone`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `stone_discrete_generator_ambiguity` | yes | yes | yes | Quot.sound, propext | `#print axioms stone_discrete_generator_ambiguity` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_1040_ds_continuous_time_exp_generator.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_1040_ds_continuous_time_exp_generator.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_1040_ds_continuous_time_exp_generator.md)
- sha256 (`lf-normalised`): `b875f71f27523a017abfec8d8455bd14b595c61780d71c8587a7e74eb8590b49`
- generated view: listed, not counted
- cited in: record TFQ-1040
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`
- `external:sha256:8b651bc7f47a6021985dd235362573dd4b5d92943b82749b13242b6ca35d4709#QM-031-C16`
- `external:sha256:e5ae08fbe8e7f3276392db13249b8444caff1fa746dec306f66e0a26fbbf9d2e#QM-030-C7`

## Routes

Incoming (0):


Outgoing (3):

- `DS-R-CONTINUUM-LIMIT` `COMPUTED`: [DS-QM032-CONTINUUM-LIMIT-CONDITIONAL](DS-QM032-CONTINUUM-LIMIT-CONDITIONAL.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-FIVE-IMPORT` `COMPUTED`: [DS-QM207-211-FIVE-IMPORT-CASCADE](DS-QM207-211-FIVE-IMPORT-CASCADE.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-SCHRODINGER-CONDITIONAL` `COMPUTED`: [DS-QM033-SCHRODINGER-DISCRETE-COCHAIN](DS-QM033-SCHRODINGER-DISCRETE-COCHAIN.md) (COMPUTATIONALLY_CHECKED)

No incoming route.
