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

### Lean: `lean4/CampaignDsContinuousTimeExpGenerator.lean`

- file: [lean4/CampaignDsContinuousTimeExpGenerator.lean](../../../lean4/CampaignDsContinuousTimeExpGenerator.lean)
- sha256 (`bytes`): `3b6fd4eac6d42eb9763210eb4e611c778b87fea4c1f6cac841bcab28da8f1339`
- cited in: node.lean, receipt dag/research/campaign_ds-continuous-time-exp-generator_lean_replay.json (CampaignDsContinuousTimeExpGenerator), record TFQ-1040
- replay: `verified`
  - receipt [dag/research/campaign_ds-continuous-time-exp-generator_lean_replay.json](../../../dag/research/campaign_ds-continuous-time-exp-generator_lean_replay.json) (module `CampaignDsContinuousTimeExpGenerator`): recorded sha256 `3b6fd4eac6d42eb9763210eb4e611c778b87fea4c1f6cac841bcab28da8f1339` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignDsContinuousTimeExpGenerator`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignDsContinuousTimeExpGenerator.candidateCorner` | yes | yes | yes | none | `#print axioms CampaignDsContinuousTimeExpGenerator.candidateCorner` |
| `CampaignDsContinuousTimeExpGenerator.cayleyNorm` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDsContinuousTimeExpGenerator.cayleyNorm` |
| `CampaignDsContinuousTimeExpGenerator.energyDistinct` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDsContinuousTimeExpGenerator.energyDistinct` |
| `CampaignDsContinuousTimeExpGenerator.energyOne` | yes | yes | yes | none | `#print axioms CampaignDsContinuousTimeExpGenerator.energyOne` |
| `CampaignDsContinuousTimeExpGenerator.energyZero` | yes | yes | yes | none | `#print axioms CampaignDsContinuousTimeExpGenerator.energyZero` |
| `CampaignDsContinuousTimeExpGenerator.gAddCoords` | yes | yes | yes | none | `#print axioms CampaignDsContinuousTimeExpGenerator.gAddCoords` |
| `CampaignDsContinuousTimeExpGenerator.gMulCoords` | yes | yes | yes | none | `#print axioms CampaignDsContinuousTimeExpGenerator.gMulCoords` |
| `CampaignDsContinuousTimeExpGenerator.negSquare` | yes | yes | yes | none | `#print axioms CampaignDsContinuousTimeExpGenerator.negSquare` |
| `CampaignDsContinuousTimeExpGenerator.noNilpotentIntegerLog` | yes | yes | yes | Quot.sound, propext | `#print axioms CampaignDsContinuousTimeExpGenerator.noNilpotentIntegerLog` |
| `CampaignDsContinuousTimeExpGenerator.noToggleSquare` | yes | yes | yes | none | `#print axioms CampaignDsContinuousTimeExpGenerator.noToggleSquare` |
| `CampaignDsContinuousTimeExpGenerator.scaledDiffer` | yes | yes | yes | none | `#print axioms CampaignDsContinuousTimeExpGenerator.scaledDiffer` |
| `CampaignDsContinuousTimeExpGenerator.scaledSquare` | yes | yes | yes | none | `#print axioms CampaignDsContinuousTimeExpGenerator.scaledSquare` |
| `CampaignDsContinuousTimeExpGenerator.toggleImages` | yes | yes | yes | none | `#print axioms CampaignDsContinuousTimeExpGenerator.toggleImages` |

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

### Lean: `lean4/H016ContinuousDynamicsFork.lean`

- file: [lean4/H016ContinuousDynamicsFork.lean](../../../lean4/H016ContinuousDynamicsFork.lean)
- sha256 (`bytes`): `906b145d8626c1887b1075e9b900858ca3f0c16df6fa65a2d8a87aa68b06de85`
- cited in: node.lean, record TFQ-1040
- replay: `none`
- check: `cd lean4 && lake build H016ContinuousDynamicsFork`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `continuous_dynamics_fork` | yes | yes | yes | - | `#print axioms continuous_dynamics_fork` |

- counts toward the grade: yes

### Lean: `lean4/H055DiscreteDynamicsStone.lean`

- file: [lean4/H055DiscreteDynamicsStone.lean](../../../lean4/H055DiscreteDynamicsStone.lean)
- sha256 (`bytes`): `1b56478a77b4ba84c72494821dcdd0ad7b47228d94bc114fbded0adea7a018c0`
- cited in: node.lean, record TFQ-1040
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_dynamics.json](../../../dag/research/lean_replay_campaign_finite_qm_dynamics.json) (module `H055DiscreteDynamicsStone`): recorded sha256 `1b56478a77b4ba84c72494821dcdd0ad7b47228d94bc114fbded0adea7a018c0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build H055DiscreteDynamicsStone`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `stone_discrete_generator_ambiguity` | yes | yes | yes | Quot.sound, propext | `#print axioms stone_discrete_generator_ambiguity` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1040
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_1040_ds_continuous_time_exp_generator.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_1040_ds_continuous_time_exp_generator.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_1040_ds_continuous_time_exp_generator.md)
- sha256 (`lf-normalised`): `700e0ebe9bef80269b5ff4fa8559721887d31de325234fca221cd919de853b3b`
- generated view: listed, not counted
- cited in: record TFQ-1040
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/030_finite_weighted_transport_calculus/qm_030_finite_weighted_transport_calculus_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/030_finite_weighted_transport_calculus/qm_030_finite_weighted_transport_calculus_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/031_finite_path_sum_as_graded_transport/qm_031_finite_path_sum_as_graded_transport_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/031_finite_path_sum_as_graded_transport/qm_031_finite_path_sum_as_graded_transport_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (0):


Outgoing (3):

- `DS-R-CONTINUUM-LIMIT` `COMPUTED`: [DS-QM032-CONTINUUM-LIMIT-CONDITIONAL](DS-QM032-CONTINUUM-LIMIT-CONDITIONAL.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-FIVE-IMPORT` `COMPUTED`: [DS-QM207-211-FIVE-IMPORT-CASCADE](DS-QM207-211-FIVE-IMPORT-CASCADE.md) (COMPUTATIONALLY_CHECKED)
- `DS-R-SCHRODINGER-CONDITIONAL` `COMPUTED`: [DS-QM033-SCHRODINGER-DISCRETE-COCHAIN](DS-QM033-SCHRODINGER-DISCRETE-COCHAIN.md) (COMPUTATIONALLY_CHECKED)

No incoming route.
