# [TFQ-0245] Unitary finite-shadow slot still reserved

> **Stage**: `FINITE_QM_DYNAMICS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `083a9566-9f7a-515f-bd99-42558b4aeb54`  
> **Parent Derivation**: [TFQ-0244](TFQ-0244_discrete_schrodinger_cochain_on_a_finite_graph.md)

---

## 1. Abstract & Formal Statement

QM_034 is still an internal draft. Its status box says it does not derive continuum quantum mechanics or mint authority, and every mechanism slot is open. The non-claim text says there is no derivation of Hilbert uniqueness, the Born rule, continuum dynamics, or authority, and it lists a first prose pass as unfinished. Finite Quantum Mechanics rung 6 records a narrower positive obligation elsewhere: declared unitary steps preserve a supplied norm, while discrete dynamics do not select a continuous interpolation or a Hamiltonian logarithm branch.

### Governing Obligation
Do not fill the reserved unitary slot with a continuum group or a selected logarithm; norm preservation stays on declared finite steps.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Dirac gamma matrices / spinors (assumption)`
- **Admitted**: `Hamiltonian generator (assumption)`
- **Admitted**: `declared unitary step (assumption)`
- **Admitted**: `generator branch selection for periodic sector (assumption)`
- **Admitted**: `unitary group (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Finite rational Cayley unitary shadow U=(I-tJ)(I+tJ)^{-1} and 2D Dirac/Clifford spinor relations are mechanized in DerivationDagQMClosure.lean; full monograph expansions remain conditional on unitary/Hamiltonian/spinor imports.

> [!WARNING]
> The dichotomy is instance-level; the price theorems are definitional.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm063_032_034_destructive_interference_and_cayley_vs_euler_norm`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_core_phase_sorkin_gleason_busch_tsirelson_dynamics_route_composition`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_entropy_purity_and_ds_qm034_051_cayley_clifford_witness`](../../code/lean4/)
- [`lean4/quantum_mechanics/H061DynamicsDichotomy.lean::periodic_sector_requires_declaration`](../../code/lean4/)
- [`lean4/quantum_mechanics/H061DynamicsDichotomy.lean::pythagorean_rotation_order_infinite`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/dynamics_dichotomy.rs::classify_unitary_orbit`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche4_edgewise_l1_u1_holonomy_chsh_and_cayley_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche9_bloch_gap_cayley_u1_hadamard_coherence_and_destructive_interference_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0246](TFQ-0246_hamiltonian_generator_admission_still_reserved.md)
- [TFQ-0247](TFQ-0247_heisenberg_picture_on_a_finite_carrier.md)
- [TFQ-0249](../12_finite_qm_structure/TFQ-0249_trace-zero_summaries_do_not_fix_commutation.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM034-035-050-051-095-RESERVED-STUBS`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM034-035-050-051-095-RESERVED-STUBS` (`FINITE_QM_DYNAMICS` / `CONDITIONAL`)
- **Mined Operad Family (`M2`)**: `OP-DS-CAYLEY-DIRAC-FINITE-SHADOW`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [130, -260, 195]`, `chord_potential = 195`, `holonomy_gamma2 = 260`
- **Finite Shadow Exact Witness (`M4`)**: `dirac_klein_gordon_square_diag: m^2 + p^2 = 12^2 + 5^2 == 169` ($\text{value} = 169$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `reserved_stub_slots_count(034,035,050,051,095,200,202,203,205) == 9` ($\text{value} = 9$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `3` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 0ee8ee5615cfcf9f4316ca30580a604e6a03865737143e4fd8e4fd6a2bf4d908`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`GP-IMPORT-CONTINUOUS-TIME`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `GP-IMPORT-CONTINUOUS-TIME` (`L1_TO_L2` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-GP-CONTINUOUS-TIME-TOGGLE-GAP`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [220, -440, 330]`, `chord_potential = 330`, `holonomy_gamma2 = 440`
- **Finite Shadow Exact Witness (`M4`)**: `complex_scaled_sqrt_toggle_trace: Tr([[1+i, 1-i],[1-i, 1+i]]^2) == Tr(4*X) == 0, off-diag sum == 8` ($\text{value} = 8$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `boolean_endomorphism_square_fixed_points: all 4 maps f:{0,1}->{0,1} satisfy f(f(0))==0 and f(f(1))==1 -> 0 solutions to f^2 = toggle` ($\text{value} = 0$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `4` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.gp_and_l1_imported_field_circle_dilation_and_time_interpolation_boundaries`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = ded07484ac0fab036e374301b78046365f54da4d1e5fe458607efd09752d486b`
