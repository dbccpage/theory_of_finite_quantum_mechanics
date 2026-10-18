# [TFQ-0076] Each language must carry: det of the neutral mass matrix is 0,

> **Stage**: `FINITE_ELECTROWEAK` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `b7bd1524-15c0-54c6-bd6d-d6c2a09a8239`  
> **Parent Derivation**: [TFQ-0075](TFQ-0075_each_language_must_carry_for_a_rational_doublet_of_radius_r_u_phi.md)

---

## 1. Abstract & Formal Statement

The Weinberg control stays inside rational linear algebra. At a positive rational scale v the charged mass square is g^2 v^2 / 4. The neutral mass-square matrix is (v^2/4) times the rank-one pattern with diagonal g^2, g'^2 and off-diagonal -g g'. Its determinant is 0 and its trace is m_Z^2. The mixing fractions g'^2/(g^2+g'^2) and g^2/(g^2+g'^2) need no square root. The photon projector is the corresponding rational matrix and the Z projector is I minus that matrix. rho_EW = m_W^2 / (m_Z^2 cos^2 theta_W) equals 1 for every non-zero rational pair (g, g'). A Y=1 triplet comparison yields 1/2, not 1.

### Governing Obligation
Each language must carry: det of the neutral mass matrix is 0, the projectors are rational and complementary, rho_EW = 1 on nonzero rational couplings, and the triplet comparison is 1/2.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `completion to R/C, Stone, period integrals (lift)`
- **Admitted**: `each row s5.2 "Residual import" column (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> All finite rational/integer control theorems for QM-207..231 are mechanized; continuum completions in QM-207..211 remain priced as explicit imports.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_qm207_231_finite_map_controls_master_certificate`](../../code/lean4/)
- [`lean4/quantum_mechanics/FiniteQFTAndGravity.lean::kn_forward`](../../code/lean4/)
- [`lean4/quantum_mechanics/FiniteQM.lean::graph_conf2_exchange_betti_and_character_collapse`](../../code/lean4/)
- [`lean4/quantum_mechanics/FiniteQM.lean::helium_kellner_variational_bound_and_virial_identity`](../../code/lean4/)
- [`not located`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/atomic_dirac_lamb_hartree_fock.rs::verify_qm224_dirac_coulomb_and_lamb_shift`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/pauli_spin_statistics_graph.rs::analyze_conf2_graph`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/qed_weak_hadronic_finite_maps.rs::ln_big_interval`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs::evaluate_qm207_holonomy_bridge`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs::evaluate_qm211_clock_tower`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/electroweak_dfm_weinberg_control.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/foundational_derivation_closure.rs::evaluate_qm219_foundational_derivation_closure`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/regge_gravity_ghz_chern_finite_maps.rs::ppn_deflection_factor`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/electroweak_dfm_weinberg_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0077](TFQ-0077_each_language_must_carry_q_t3_y_on_the_standard.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
