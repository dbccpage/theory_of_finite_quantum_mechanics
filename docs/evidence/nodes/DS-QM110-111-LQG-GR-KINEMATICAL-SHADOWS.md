# DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On toy carriers: pure-gauge connections have trivial loop holonomy, Q8 plaquette gives a nonzero Wilson loop, Bianchi-shaped d1 d0 = 0, transport composes, an incomplete geodesic is a refusal. Imported: continuum connection and measure, SU(2) representation theory, spin-network Hilbert space, manifold, metric, Levi-Civita, Einstein tensor. Hamiltonian constraint and the Einstein equation are Q-held / open. Q8 is a shadow, not SU(2).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (3 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 3 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- continuum manifold, metric, connection (assumption)
- SU(2) gauge group (assumption)
- Hamiltonian constraint / Einstein equation (assumption)

## Bottleneck

Checked on the declared Q8 carrier natively. The cited Lean has spin admissibility for two triples and 360 - 6*60 = 0.

## Source status

\[PROVEN, MECHANIZED\] finite toy-carrier theorems (QM-110-C2..C8; QM-111-C2..C5b); \[IMPORTED\] C10 / C7; \[Q-HELD / OPEN\] dynamics

## Review

- PFP review: [dag/results/DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS/reviews/20261019_boundaries_audit/review_result.json](../../../dag/results/DS-QM110-111-LQG-GR-KINEMATICAL-SHADOWS/reviews/20261019_boundaries_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Q8 group operations, pure-gauge loops and noncommuting plaquette controls are native/kernel checked on the declared eight-element group.
  - does not support: Supply continuum manifold/metric/connection, SU(2) representations, measure, physical scales and Hamiltonian/Einstein dynamics before any quantum-gravity interpretation.
  - next test: Supply continuum manifold/metric/connection, SU(2) representations, measure, physical scales and Hamiltonian/Einstein dynamics before any quantum-gravity interpretation.

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
| `QuantumMechanics.DerivationDagQMClosure.ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm102_110_111_212_syndrome_hamming_lqg_wilson_and_majorana_braid` |
| `QuantumMechanics.DerivationDagQMClosure.qm110_111_lqg_gr_kinematical_witness` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.qm110_111_lqg_gr_kinematical_witness` |

- counts toward the grade: yes

### Rust: `code/rust/src/general_relativity/field_equation.rs`

- file: [code/rust/src/general_relativity/field_equation.rs](../../../code/rust/src/general_relativity/field_equation.rs)
- sha256 (`bytes`): `38f1bac71ede46df568aa8653f55f4a1ab52869b019dbe21c4c4396c07b4cb6f`
- cited in: record TFQ-0096
- note: no test is cited for this symbol; its crate is tfqm_general_relativity
- counts toward the grade: yes

### Rust: `code/rust/src/general_relativity/loop_quantum_gravity.rs`

- file: [code/rust/src/general_relativity/loop_quantum_gravity.rs](../../../code/rust/src/general_relativity/loop_quantum_gravity.rs)
- sha256 (`bytes`): `bd7871747c53cee825aff6575c167966d82314dc1740de9666478ecfb7b9ed29`
- cited in: record TFQ-0094
- note: no test is cited for this symbol; its crate is tfqm_general_relativity
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/lib.rs`

- file: [code/rust/src/wdp/lib.rs](../../../code/rust/src/wdp/lib.rs)
- sha256 (`bytes`): `aa868cc58a3c6fdf1eabfcdd46798329bf560389e83367c574259837d2d3ed4c`
- cited in: record TFQ-0093, record TFQ-0094, record TFQ-0110
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0092_qm_110_c11_hamiltonian_constraint_stays_q_held_continuum_su_2_data_in_qm_110_c10_are_imported.md`

- file: [dag/derivations/19_finite_qg/tfq_0092_qm_110_c11_hamiltonian_constraint_stays_q_held_continuum_su_2_data_in_qm_110_c10_are_imported.md](../../../dag/derivations/19_finite_qg/tfq_0092_qm_110_c11_hamiltonian_constraint_stays_q_held_continuum_su_2_data_in_qm_110_c10_are_imported.md)
- sha256 (`lf-normalised`): `c5aa199a34845229447be7da16117810d3bd9048f0980d4fd7b35ea14183601b`
- generated view: listed, not counted
- cited in: record TFQ-0092
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0093_imported_area_scale_and_casimir_stay_unpaid_the_einstein_equation_and_smooth.md`

- file: [dag/derivations/19_finite_qg/tfq_0093_imported_area_scale_and_casimir_stay_unpaid_the_einstein_equation_and_smooth.md](../../../dag/derivations/19_finite_qg/tfq_0093_imported_area_scale_and_casimir_stay_unpaid_the_einstein_equation_and_smooth.md)
- sha256 (`lf-normalised`): `c0b748f607115481f865496eba4fc725dc8bdd62912de177f2be215fef2cc9d8`
- generated view: listed, not counted
- cited in: record TFQ-0093
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0094_gap_physical_cosmological_constant_and_continuum_hilbert_space_are_outside_this_tetrahedron.md`

- file: [dag/derivations/19_finite_qg/tfq_0094_gap_physical_cosmological_constant_and_continuum_hilbert_space_are_outside_this_tetrahedron.md](../../../dag/derivations/19_finite_qg/tfq_0094_gap_physical_cosmological_constant_and_continuum_hilbert_space_are_outside_this_tetrahedron.md)
- sha256 (`lf-normalised`): `7f278dddc85ca3cd0c665ac5584a8eafa31003c754c9ff152de5a86d0229bee8`
- generated view: listed, not counted
- cited in: record TFQ-0094
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0095_qm_111_c3_does_not_discharge_nabla_g_equals_zero_qm_111_c7_imports_the_continuum.md`

- file: [dag/derivations/19_finite_qg/tfq_0095_qm_111_c3_does_not_discharge_nabla_g_equals_zero_qm_111_c7_imports_the_continuum.md](../../../dag/derivations/19_finite_qg/tfq_0095_qm_111_c3_does_not_discharge_nabla_g_equals_zero_qm_111_c7_imports_the_continuum.md)
- sha256 (`lf-normalised`): `f1ca072abde88c64a827694f31f5ce27a2f37c9e27c459759f5d44722b8674c1`
- generated view: listed, not counted
- cited in: record TFQ-0095
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0096_gap_einstein_equation_stays_q_held_for_this_finite_descent_program_and_is_not.md`

- file: [dag/derivations/19_finite_qg/tfq_0096_gap_einstein_equation_stays_q_held_for_this_finite_descent_program_and_is_not.md](../../../dag/derivations/19_finite_qg/tfq_0096_gap_einstein_equation_stays_q_held_for_this_finite_descent_program_and_is_not.md)
- sha256 (`lf-normalised`): `3a945624e5f48a316b70eff5a94b0c8c4003ffee0954ebdf1f4705a5730416e8`
- generated view: listed, not counted
- cited in: record TFQ-0096
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0097_gap_the_cosine_motif_does_not_discharge_gap_f000_f002_001_the_continuum_limit_bridge.md`

- file: [dag/derivations/19_finite_qg/tfq_0097_gap_the_cosine_motif_does_not_discharge_gap_f000_f002_001_the_continuum_limit_bridge.md](../../../dag/derivations/19_finite_qg/tfq_0097_gap_the_cosine_motif_does_not_discharge_gap_f000_f002_001_the_continuum_limit_bridge.md)
- sha256 (`lf-normalised`): `2548b25349fa839ffce1e74704f70823bca1e3961126739e388699dc5d9142fe`
- generated view: listed, not counted
- cited in: record TFQ-0097
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0108_gap_caller_supplied_lambda_is_not_the_physical_cosmological_constant_and_the_grid.md`

- file: [dag/derivations/19_finite_qg/tfq_0108_gap_caller_supplied_lambda_is_not_the_physical_cosmological_constant_and_the_grid.md](../../../dag/derivations/19_finite_qg/tfq_0108_gap_caller_supplied_lambda_is_not_the_physical_cosmological_constant_and_the_grid.md)
- sha256 (`lf-normalised`): `9f9559aae7e2c5779b0610a0ab7135c2b5c8474156db21c50f7ebd27a645be89`
- generated view: listed, not counted
- cited in: record TFQ-0108
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0110_gap_on_continuum_limit_einstein_equation_physical_cosmological_constant_and_smooth_curvature.md`

- file: [dag/derivations/19_finite_qg/tfq_0110_gap_on_continuum_limit_einstein_equation_physical_cosmological_constant_and_smooth_curvature.md](../../../dag/derivations/19_finite_qg/tfq_0110_gap_on_continuum_limit_einstein_equation_physical_cosmological_constant_and_smooth_curvature.md)
- sha256 (`lf-normalised`): `5072aa055985e2040491694623ea4a131cc5c6d19d3bfdf44353d282c1ff9261`
- generated view: listed, not counted
- cited in: record TFQ-0110
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/110_loop_quantum_gravity_kinematical_shadows/qm_110_loop_quantum_gravity_kinematical_shadows_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/110_loop_quantum_gravity_kinematical_shadows/qm_110_loop_quantum_gravity_kinematical_shadows_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/111_general_relativity_kinematical_shadows/qm_111_general_relativity_kinematical_shadows_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/111_general_relativity_kinematical_shadows/qm_111_general_relativity_kinematical_shadows_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0092 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/spin_area_spectrum.rs
- TFQ-0093 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/spin_area_spectrum.rs
- TFQ-0108 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_regge_bridge.rs
- TFQ-0108 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/spin_area_spectrum.rs
- TFQ-0110 lean4: no local lean twin located for omega_engine_atlas/coda_atlas/F004_papers/004_general_relativity/002_constraint_closure_and_the_l1structure_of_physical_law/lean4/GR002.lean
- TFQ-0110 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/004_general_relativity/002_constraint_closure_and_the_l1structure_of_physical_law/code/l1_regge.py

## Routes

Incoming (1):

- `DS-R-GR-LQG` `COMPUTED`: [DS-QM063-HOLONOMY-COHERENT-INTENSITY](DS-QM063-HOLONOMY-COHERENT-INTENSITY.md) (COMPUTATIONALLY_CHECKED)

Outgoing (2):

- `UDG-R-TFQ-0098` `RECORD_PARENT`: [TFQ-0098](TFQ-0098.md) (SOURCE_RECORD)
- `UDG-R-TFQ-0109` `RECORD_PARENT`: [TFQ-0109](TFQ-0109.md) (SOURCE_RECORD)
