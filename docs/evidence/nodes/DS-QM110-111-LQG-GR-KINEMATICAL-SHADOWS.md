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
- sha256 (`bytes`): `66d4f401480f3e4c57e3a19ebec8508d045198e8ff4f0ec25f785973fc522eb3`
- cited in: record TFQ-0094
- note: no test is cited for this symbol; its crate is tfqm_general_relativity
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/lib.rs`

- file: [code/rust/src/wdp/lib.rs](../../../code/rust/src/wdp/lib.rs)
- sha256 (`bytes`): `9111d9c82247cc2f1e8176b0a0285a788fcd1d2bc6cd2c1d3be81f84f431d235`
- cited in: record TFQ-0093, record TFQ-0094, record TFQ-0110
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Documents and data: `dag/derivations/19_finite_qg/tfq_0092_qm_110_c11_hamiltonian_constraint_stays_q_held_continuum_su_2_data_in_qm_110_c10_are_imported.md`

- file: [dag/derivations/19_finite_qg/tfq_0092_qm_110_c11_hamiltonian_constraint_stays_q_held_continuum_su_2_data_in_qm_110_c10_are_imported.md](../../../dag/derivations/19_finite_qg/tfq_0092_qm_110_c11_hamiltonian_constraint_stays_q_held_continuum_su_2_data_in_qm_110_c10_are_imported.md)
- sha256 (`lf-normalised`): `fc225066cc8f3ce1c259ffb5957827dfe6c10528a63117c876cd6b1357dc0350`
- generated view: listed, not counted
- cited in: record TFQ-0092
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0093_imported_area_scale_and_casimir_stay_unpaid_the_einstein_equation_and_smooth.md`

- file: [dag/derivations/19_finite_qg/tfq_0093_imported_area_scale_and_casimir_stay_unpaid_the_einstein_equation_and_smooth.md](../../../dag/derivations/19_finite_qg/tfq_0093_imported_area_scale_and_casimir_stay_unpaid_the_einstein_equation_and_smooth.md)
- sha256 (`lf-normalised`): `956719e0ccff02451107b10617e09604a3433183978406a4bcee12162718879f`
- generated view: listed, not counted
- cited in: record TFQ-0093
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0094_gap_physical_cosmological_constant_and_continuum_hilbert_space_are_outside_this_tetrahedron.md`

- file: [dag/derivations/19_finite_qg/tfq_0094_gap_physical_cosmological_constant_and_continuum_hilbert_space_are_outside_this_tetrahedron.md](../../../dag/derivations/19_finite_qg/tfq_0094_gap_physical_cosmological_constant_and_continuum_hilbert_space_are_outside_this_tetrahedron.md)
- sha256 (`lf-normalised`): `a2d6ac3c6fe8e22c1009bf62e86a82fc9d7fca77f84694bbea238a7b1955220c`
- generated view: listed, not counted
- cited in: record TFQ-0094
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0095_qm_111_c3_does_not_discharge_nabla_g_equals_zero_qm_111_c7_imports_the_continuum.md`

- file: [dag/derivations/19_finite_qg/tfq_0095_qm_111_c3_does_not_discharge_nabla_g_equals_zero_qm_111_c7_imports_the_continuum.md](../../../dag/derivations/19_finite_qg/tfq_0095_qm_111_c3_does_not_discharge_nabla_g_equals_zero_qm_111_c7_imports_the_continuum.md)
- sha256 (`lf-normalised`): `1e8b1ab910b9295b2b870aef2103f21a819b99c9a25e70672b675cc7cc8dd599`
- generated view: listed, not counted
- cited in: record TFQ-0095
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0096_gap_einstein_equation_stays_q_held_for_this_finite_descent_program_and_is_not.md`

- file: [dag/derivations/19_finite_qg/tfq_0096_gap_einstein_equation_stays_q_held_for_this_finite_descent_program_and_is_not.md](../../../dag/derivations/19_finite_qg/tfq_0096_gap_einstein_equation_stays_q_held_for_this_finite_descent_program_and_is_not.md)
- sha256 (`lf-normalised`): `9cf995fa8dbc50ad84500ee39645f45a8a9a87ec7b61c502b5280d17367f63d6`
- generated view: listed, not counted
- cited in: record TFQ-0096
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0097_gap_the_cosine_motif_does_not_discharge_gap_f000_f002_001_the_continuum_limit_bridge.md`

- file: [dag/derivations/19_finite_qg/tfq_0097_gap_the_cosine_motif_does_not_discharge_gap_f000_f002_001_the_continuum_limit_bridge.md](../../../dag/derivations/19_finite_qg/tfq_0097_gap_the_cosine_motif_does_not_discharge_gap_f000_f002_001_the_continuum_limit_bridge.md)
- sha256 (`lf-normalised`): `0651735c3c036663988970973276c4d79b80eeb58eed896a9034e628208531f9`
- generated view: listed, not counted
- cited in: record TFQ-0097
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0108_gap_caller_supplied_lambda_is_not_the_physical_cosmological_constant_and_the_grid.md`

- file: [dag/derivations/19_finite_qg/tfq_0108_gap_caller_supplied_lambda_is_not_the_physical_cosmological_constant_and_the_grid.md](../../../dag/derivations/19_finite_qg/tfq_0108_gap_caller_supplied_lambda_is_not_the_physical_cosmological_constant_and_the_grid.md)
- sha256 (`lf-normalised`): `387d3014f0b78f2aa008ea0606f07200dcc7d58c7f5705e0992fc0014b1e9891`
- generated view: listed, not counted
- cited in: record TFQ-0108
- counts toward the grade: no

### Documents and data: `dag/derivations/19_finite_qg/tfq_0110_gap_on_continuum_limit_einstein_equation_physical_cosmological_constant_and_smooth_curvature.md`

- file: [dag/derivations/19_finite_qg/tfq_0110_gap_on_continuum_limit_einstein_equation_physical_cosmological_constant_and_smooth_curvature.md](../../../dag/derivations/19_finite_qg/tfq_0110_gap_on_continuum_limit_einstein_equation_physical_cosmological_constant_and_smooth_curvature.md)
- sha256 (`lf-normalised`): `e25c3ba2ec04fd37f15db3abc0e38fd687bcd7503c817442a002bcbe12bf46a0`
- generated view: listed, not counted
- cited in: record TFQ-0110
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:1892e34e319a1f165ed31402cae724d190be9fdc8fa3ea10e27672b8f38e5eed#QM-111-C7`
- `external:sha256:1892e34e319a1f165ed31402cae724d190be9fdc8fa3ea10e27672b8f38e5eed#QM-111-C8`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_ds_qm_dynamics_structure_and_majorana_witness`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`
- `external:sha256:865e924e88cdcae52987737e2871a0dce2e8ed5032c417c2d2a60c3682afd66c#QM-110-C10`
- `external:sha256:865e924e88cdcae52987737e2871a0dce2e8ed5032c417c2d2a60c3682afd66c#QM-110-C11`
- `external:sha256:865e924e88cdcae52987737e2871a0dce2e8ed5032c417c2d2a60c3682afd66c#QM-110-C2`

## Absences recorded by the TFQ records

- TFQ-0092 rust: no local rust twin located for external:sha256:849b3a7c308df09c211ccfce2f4bfac5187a01e4dbba5b527ff6b4d32bc2796e
- TFQ-0093 rust: no local rust twin located for external:sha256:849b3a7c308df09c211ccfce2f4bfac5187a01e4dbba5b527ff6b4d32bc2796e
- TFQ-0108 rust: no local rust twin located for external:sha256:849b3a7c308df09c211ccfce2f4bfac5187a01e4dbba5b527ff6b4d32bc2796e
- TFQ-0108 rust: no local rust twin located for external:sha256:daa2544f59a9e79153dd422e291957ad086cabfeed37aa2bf2d5ddc847a4aade
- TFQ-0110 lean4: no local lean twin located for sources/atlas/papers/general_relativity/constraint_closure_and_the_l1_structure_of_physical_law/lean4/GR002.lean
- TFQ-0110 python: no local python twin located for papers/core/constraint_closure/code/l1_regge.py

## Routes

Incoming (1):

- `DS-R-GR-LQG` `COMPUTED`: [DS-QM063-HOLONOMY-COHERENT-INTENSITY](DS-QM063-HOLONOMY-COHERENT-INTENSITY.md) (COMPUTATIONALLY_CHECKED)

Outgoing (2):

- `UDG-R-TFQ-0098` `RECORD_PARENT`: [TFQ-0098](TFQ-0098.md) (SOURCE_RECORD)
- `UDG-R-TFQ-0109` `RECORD_PARENT`: [TFQ-0109](TFQ-0109.md) (SOURCE_RECORD)
