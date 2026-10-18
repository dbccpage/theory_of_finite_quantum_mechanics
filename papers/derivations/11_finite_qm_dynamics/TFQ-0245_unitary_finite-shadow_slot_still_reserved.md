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
