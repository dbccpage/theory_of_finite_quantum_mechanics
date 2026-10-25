# FQ-DISCRETE-TIME-STONE-AMBIGUITY

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: The report-map obstruction and two distinct scaled Gaussian roots are kernel checked; native enumeration and normalized unitarity are replayed.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declaration references covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- complex logarithm branch choice (assumption)

## Bottleneck

Unmet after the PFP review: Construct logarithms, an actual continuous one-parameter group, topology and a generator selection rule. Tags do not supply analytic branches. The broader source statement is kept in pfp_review.prior_statement.

## Source status

H055 header carries PR #205 scope correction; H016 import boundary

## Review

- PFP review: [dag/results/FQ-DISCRETE-TIME-STONE-AMBIGUITY/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/FQ-DISCRETE-TIME-STONE-AMBIGUITY/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: The report-map obstruction and two distinct scaled Gaussian roots are kernel checked; native enumeration and normalized unitarity are replayed.
  - does not support: Construct logarithms, an actual continuous one-parameter group, topology and a generator selection rule. Tags do not supply analytic branches.
  - next test: Construct logarithms, an actual continuous one-parameter group, topology and a generator selection rule. Tags do not supply analytic branches.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0246 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition` |

- counts toward the grade: yes

### Lean: `lean4/H055DiscreteDynamicsStone.lean`

- file: [lean4/H055DiscreteDynamicsStone.lean](../../../lean4/H055DiscreteDynamicsStone.lean)
- sha256 (`bytes`): `1b56478a77b4ba84c72494821dcdd0ad7b47228d94bc114fbded0adea7a018c0`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_dynamics.json](../../../dag/research/lean_replay_campaign_finite_qm_dynamics.json) (module `H055DiscreteDynamicsStone`): recorded sha256 `1b56478a77b4ba84c72494821dcdd0ad7b47228d94bc114fbded0adea7a018c0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build H055DiscreteDynamicsStone`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `no_bool_half_step` | yes | yes | yes | none | `#print axioms no_bool_half_step` |
| `stone_continuum_interface_priced` | yes | yes | yes | Quot.sound, propext | `#print axioms stone_continuum_interface_priced` |
| `stone_discrete_generator_ambiguity` | yes | yes | yes | Quot.sound, propext | `#print axioms stone_discrete_generator_ambiguity` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/finite_report_dynamics.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/finite_report_dynamics.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/11_finite_qm_dynamics/tfq_0246_hamiltonian_generator_admission_still_reserved.md`

- file: [dag/derivations/11_finite_qm_dynamics/tfq_0246_hamiltonian_generator_admission_still_reserved.md](../../../dag/derivations/11_finite_qm_dynamics/tfq_0246_hamiltonian_generator_admission_still_reserved.md)
- sha256 (`lf-normalised`): `5a5e181911194955dd1390a01fc988265bfba481d61489d270abc7ed4689f568`
- generated view: listed, not counted
- cited in: record TFQ-0246 (shared)
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml`

- file: [sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml](../../../sources/atlas/F004_papers/006_finite_qm/claims/gap_register.yaml)
- sha256 (`lf-normalised`): `16a418a93748cef695fad3c1fab0fd14dd95c6985b23ee8a814b171eca60a445`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `FQ-R-STONE-AMBIGUITY` `DERIVED_LEAN`: [FQ-DISCRETE-DYNAMICS-DICHOTOMY](FQ-DISCRETE-DYNAMICS-DICHOTOMY.md) (PROVED_LEAN)

Outgoing (1):

- `FQ-R-GAP-STONE` `CONDITIONAL_ON_IMPORT`: [FQ-GAP-STONE-CONTINUOUS-TIME](FQ-GAP-STONE-CONTINUOUS-TIME.md) (CONDITIONAL)
