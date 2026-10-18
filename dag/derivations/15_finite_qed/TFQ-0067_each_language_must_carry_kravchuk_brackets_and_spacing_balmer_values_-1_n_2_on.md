# [TFQ-0067] Each language must carry: Kravchuk brackets and spacing, Balmer values -1/n^2 on

> **Stage**: `FINITE_QED` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `d4f12d15-46ef-5fd3-a2d1-1c27586aee8a`  
> **Parent Derivation**: [TFQ-0066](TFQ-0066_each_language_must_carry_the_twelve-digit_prefixes_for_pi_r_-9_m_2_4_the_running.md)

---

## 1. Abstract & Formal Statement

algebraic_bound_state_spectra.rs computes finite su(2) and so(4) spectra over Q. For N = 2j in {1,2,3,4} the Kravchuk ladder satisfies the sl(2) brackets, the Casimir j(j+1), and G-adjointness without square roots. The shifted Hamiltonian is the diagonal of half-integers from 1/2 through 2j+1/2 with spacing 1. Ground second moments of the scaled quadratures are 1/4 and saturate the discrete Robertson relation. On the hydrogen shell of dimension n^2 the Pauli Hamiltonian is -1/n^2. Projectors Pi_2S = I - L^2/2 and Pi_2P = L^2/2 split the n=2 shell into traces 1 and 3, commute with L, and fail to commute with K_z.

### Governing Obligation
Each language must carry: Kravchuk brackets and spacing, Balmer values -1/n^2 on n^2 shells, 2S/2P projector traces 1 and 3, and the contact enclosure at coefficient 91/120.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `completion to R/C, Stone, period integrals (lift)`
- **Admitted**: `each row s5.2 "Residual import" column (assumption)`
- **Admitted**: `finite dimension (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> All finite rational/integer control theorems for QM-207..231 are mechanized; continuum completions in QM-207..211 remain priced as explicit imports.

> [!WARNING]
> General n is prose; Lean is 2x2 (integer/rational entries).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_qm207_231_finite_map_controls_master_certificate`](../../code/lean4/)
- [`lean4/quantum_mechanics/FiniteQFTAndGravity.lean::kn_forward`](../../code/lean4/)
- [`lean4/quantum_mechanics/FiniteQM.lean::graph_conf2_exchange_betti_and_character_collapse`](../../code/lean4/)
- [`lean4/quantum_mechanics/FiniteQM.lean::helium_kellner_variational_bound_and_virial_identity`](../../code/lean4/)
- [`lean4/quantum_mechanics/FiniteQM.lean::weyl_heisenberg_finite_trace_obstruction`](../../code/lean4/)
- [`lean4/quantum_mechanics/H056ContinuumLiftBoundary.lean::wintner_wielandt_dim2_obstruction`](../../code/lean4/)
- [`lean4/quantum_mechanics/H068WeylCcrResidual.lean::tr_comm2_vanishes`](../../code/lean4/)
- [`not located`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/atomic_dirac_lamb_hartree_fock.rs::verify_qm224_dirac_coulomb_and_lamb_shift`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/commutator.rs::verify_trace_cyclicity_d3`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/continuum.rs::canonical_commutator_obstruction`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/pauli_spin_statistics_graph.rs::analyze_conf2_graph`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/qed_weak_hadronic_finite_maps.rs::ln_big_interval`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs::evaluate_qm207_holonomy_bridge`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs::evaluate_qm211_clock_tower`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/algebraic_bound_state_spectra.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/foundational_derivation_closure.rs::evaluate_qm219_foundational_derivation_closure`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/regge_gravity_ghz_chern_finite_maps.rs::ppn_deflection_factor`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/algebraic_bound_state_spectra_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0068](TFQ-0068_each_language_must_carry_n_2_coefficients_5_128_5_128_and_1_128_splitting_1_32.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
