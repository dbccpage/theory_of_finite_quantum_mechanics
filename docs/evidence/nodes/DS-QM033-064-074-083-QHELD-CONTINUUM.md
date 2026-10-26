# DS-QM033-064-074-083-QHELD-CONTINUUM

Stage: [FINITE_QM_DYNAMICS](../stages/FINITE_QM_DYNAMICS.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Continuous Hilbert-space differential equation, continuous Lie-group gauge lift, Minkowski light-cone causality and Kraus decomposition are each held as external L2 observer lifts; stub-style rows that share one claim: continuum non-promotion.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- L2 Hilbert space (assumption)
- continuous Lie group / spacetime (assumption)

## Bottleneck

Held outside the programme by declaration.

## Source status

\[Q-HELD\] (QM_033-C4, QM_064-C4, QM_074-C4, QM_083-C4)

## Review

- PFP review: [dag/results/DS-QM033-064-074-083-QHELD-CONTINUUM/reviews/20261019_dynamics_audit/review_result.json](../../../dag/results/DS-QM033-064-074-083-QHELD-CONTINUUM/reviews/20261019_dynamics_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `IMPORTED_ASSUMPTION`; qualifies for E4: yes.
  - narrowest claim: Exact phase-blind data agree while the declared mixed readouts differ by 4ab, with a zero-amplitude control.
  - does not support: Choose and justify an amplitude lift, admissible mixing operations and any continuum closure. Fixed presentation data do not select these.
  - next test: Choose and justify an amplitude lift, admissible mixing operations and any continuum closure. Fixed presentation data do not select these.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality` |
| `QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates` | yes | yes | yes | module-level | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_and_ds_imported_assumption_separation_certificates` |

- counts toward the grade: yes

### Rust: `code/rust/src/qm/campaigns/continuum.rs`

- file: [code/rust/src/qm/campaigns/continuum.rs](../../../code/rust/src/qm/campaigns/continuum.rs)
- sha256 (`bytes`): `68a35304067d3806f52fbbaec7459e89a192187b7d5074bcacb6f33f97e63524`
- cited in: record TFQ-0122, record TFQ-0124
- note: no test is cited for this symbol; its crate is theory_of_finite_qm
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/20_continuum_interface/tfq_0122_filename_continuum_rs_does_not_discharge_the_continuum_limit_or_the_einstein_equation.md`

- file: [dag/derivations/20_continuum_interface/tfq_0122_filename_continuum_rs_does_not_discharge_the_continuum_limit_or_the_einstein_equation.md](../../../dag/derivations/20_continuum_interface/tfq_0122_filename_continuum_rs_does_not_discharge_the_continuum_limit_or_the_einstein_equation.md)
- sha256 (`lf-normalised`): `df89bf4a0b6dfc8e59de3f457b87743b2c49ab9476f89ebfaa48041a170cadbb`
- generated view: listed, not counted
- cited in: record TFQ-0122
- counts toward the grade: no

### Documents and data: `dag/derivations/20_continuum_interface/tfq_0124_gap_continuum_limit_einstein_equation_physical_cosmological_constant_and_smooth_manifold.md`

- file: [dag/derivations/20_continuum_interface/tfq_0124_gap_continuum_limit_einstein_equation_physical_cosmological_constant_and_smooth_manifold.md](../../../dag/derivations/20_continuum_interface/tfq_0124_gap_continuum_limit_einstein_equation_physical_cosmological_constant_and_smooth_manifold.md)
- sha256 (`lf-normalised`): `83438bd73e471fcb85435173c832b562c660217b5fe8cc2305bfe3d77829eaf4`
- generated view: listed, not counted
- cited in: record TFQ-0124
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/033_schrodinger_finite_shadow/qm_033_schrodinger_finite_shadow_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/033_schrodinger_finite_shadow/qm_033_schrodinger_finite_shadow_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/064_phase_gauge_residual/qm_064_phase_gauge_residual_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/064_phase_gauge_residual/qm_064_phase_gauge_residual_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/074_no_signaling_finite_shadow/qm_074_no_signaling_finite_shadow_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/074_no_signaling_finite_shadow/qm_074_no_signaling_finite_shadow_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/083_completely_positive_import_boundary/qm_083_completely_positive_import_boundary_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/083_completely_positive_import_boundary/qm_083_completely_positive_import_boundary_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0124 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent/002_from_primitive_difference_to_mtheory/lean4/FromPrimitiveDifferenceToMTheory/ContinuumLimit.lean
- TFQ-0124 python: no local python twin located for atlas/papers/projection_obstruction/zero_container_relational_spacetime_and_witness_holonomy/code/continuum_lorentz_causality.py

## Routes

Incoming (1):

- `FRO-R-BACK-CQFT-NET-TO-QHELD` `GAP_NO_DERIVATION`: [CQFT-LOCAL-NET-AXIOMS-IMPORT](CQFT-LOCAL-NET-AXIOMS-IMPORT.md) (IMPORTED_ASSUMPTION)

Outgoing (0):

