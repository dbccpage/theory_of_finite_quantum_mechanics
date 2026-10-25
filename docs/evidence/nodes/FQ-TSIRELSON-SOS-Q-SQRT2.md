# FQ-TSIRELSON-SOS-Q-SQRT2

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Reviewed scope: Two exact Q(sqrt2) SOS matrix certificates and Bell-density expectation2sqrt2 are reproduced independently. general rational four-coordinate scaled SOS inequalities and attainment ratio are kernel checked for this fixed operator.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declaration references covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- bipartite tensor carrier (assumption)
- entangled state (assumption)
- trace/Born pairing (assumption)

## Bottleneck

Unmet after the PFP review: Formalize the concrete Q(sqrt2)-matrix to real quadratic-form transport before claiming a full Lean operator certificate; arbitrary observables, tensor selection and quantum probability are not derived. The broader source statement is kept in pfp_review.prior_statement.

## Source status

paper s13.8.2: exact SOS certificates -2sqrt2 I \<= B_CHSH \<= 2sqrt2 I and attaining witness over Q(sqrt2); QM-218

## Review

- PFP review: [dag/results/FQ-TSIRELSON-SOS-Q-SQRT2/reviews/20261019_structure_audit/review_result.json](../../../dag/results/FQ-TSIRELSON-SOS-Q-SQRT2/reviews/20261019_structure_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Two exact Q(sqrt2) SOS matrix certificates and Bell-density expectation2sqrt2 are reproduced independently. general rational four-coordinate scaled SOS inequalities and attainment ratio are kernel checked for this fixed operator.
  - does not support: Formalize the concrete Q(sqrt2)-matrix to real quadratic-form transport before claiming a full Lean operator certificate; arbitrary observables, tensor selection and quantum probability are not derived.
  - next test: Formalize the concrete Q(sqrt2)-matrix to real quadratic-form transport before claiming a full Lean operator certificate; arbitrary observables, tensor selection and quantum probability are not derived.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0260 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition` |

- counts toward the grade: yes

### Lean: `lean4/H064ContextualityThresholds.lean`

- file: [lean4/H064ContextualityThresholds.lean](../../../lean4/H064ContextualityThresholds.lean)
- sha256 (`bytes`): `bb791f1af6f867df9e849e5b969cdd4b6931ed06ad22c5a51ee25a57eacf345a`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `H064ContextualityThresholds`): recorded sha256 `bb791f1af6f867df9e849e5b969cdd4b6931ed06ad22c5a51ee25a57eacf345a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build H064ContextualityThresholds`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `conductor_24_contains_sqrt2` | yes | yes | yes | none | `#print axioms conductor_24_contains_sqrt2` |

- counts toward the grade: yes

### Lean: `lean4/QuantumCorrelation.lean`

- file: [lean4/QuantumCorrelation.lean](../../../lean4/QuantumCorrelation.lean)
- sha256 (`bytes`): `1efde024ea6004e14e564be78cc1e9c5238919f28f2ddc1a1fbf6b58f6fa00bd`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `QuantumCorrelation`): recorded sha256 `1efde024ea6004e14e564be78cc1e9c5238919f28f2ddc1a1fbf6b58f6fa00bd` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build QuantumCorrelation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `q2_tsirelson_attainment` | yes | yes | yes | none | `#print axioms q2_tsirelson_attainment` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/finite_chsh_correlations.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/finite_chsh_correlations.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/page_wootters_tsirelson_wigner.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/page_wootters_tsirelson_wigner.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0260_bell_theorem_not_derived_from_the_finite_tables.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0260_bell_theorem_not_derived_from_the_finite_tables.md](../../../dag/derivations/12_finite_qm_structure/tfq_0260_bell_theorem_not_derived_from_the_finite_tables.md)
- sha256 (`lf-normalised`): `8e74bdeb1880d57c749bbd6b57d2a038c234d7f96f014f15ccd1d5d5ea06c7a7`
- generated view: listed, not counted
- cited in: record TFQ-0260 (shared)
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: [sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md](../../../sources/atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `5e43f206b08726fd4b27888d6fed3f211aac8398d5f8bf3dce712c415d7d81cc`
- cited in: node.source
- counts toward the grade: yes

## Absences recorded by the TFQ records

- TFQ-0260 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/finite_chsh_correlations.rs

## Routes

Incoming (1):

- `FQ-R-TSIRELSON` `CONDITIONAL_ON_IMPORT`: [FQ-BELL-RATIONAL-VIOLATION-14-5](FQ-BELL-RATIONAL-VIOLATION-14-5.md) (PROVED_LEAN), [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION)

Outgoing (0):

