# [TFQ-0074] Each language must carry: Klein-Nishina forward value 1, Thomson shape (1+u^2)/2, s-u

> **Stage**: `FINITE_QED` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `3a3f8bb1-c111-5a48-9261-700f5ef9ce3a`  
> **Parent Derivation**: [TFQ-0073](tfq_0073_each_language_must_carry_isotony_locality_and_optional_complement_duality_on_a.md)

---

## 1. Abstract & Formal Statement

qed_weak_hadronic_finite_maps.rs computes tree-level rational scattering ratios for QM-226. klein_nishina_ratio uses eta = 1/(1+x(1-u)) and R = (1/2) eta^2 (eta + 1/eta - (1-u^2)). The forward value at u = 1 is 1, and the Thomson value at x = 0 is (1+u^2)/2. bhabha_reduced_amplitude and moller_reduced_amplitude satisfy Moller(s,t,u) = Bhabha(u,t,s) for nonzero s,t,u. The s-t exchange fails at the witness (5,-2,-3): Bhabha is 361/25 and Moller is 1444/225. FiniteQFTAndGravity.lean, not a stem twin, contains kn_forward, kn_thomson and moller_eq_bhabha_su. The Lean stem search itself returned not located.

### Governing Obligation
Each language must carry: Klein-Nishina forward value 1, Thomson shape (1+u^2)/2, s-u crossing, and the s-t witness 361/25 versus 1444/225.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/qed_weak_hadronic_finite_maps.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/qed_weak_hadronic_finite_maps.rs::ln_big_interval`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs::evaluate_qm207_holonomy_bridge`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs::evaluate_qm211_clock_tower`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/foundational_derivation_closure.rs::evaluate_qm219_foundational_derivation_closure`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/regge_gravity_ghz_chern_finite_maps.rs::ppn_deflection_factor`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/qed_weak_hadronic_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0075](../16_finite_electroweak/tfq_0075_each_language_must_carry_for_a_rational_doublet_of_radius_r_u_phi.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
