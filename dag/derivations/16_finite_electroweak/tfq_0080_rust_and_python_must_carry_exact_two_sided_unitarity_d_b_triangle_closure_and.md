# [TFQ-0080] Rust and Python must carry exact two-sided unitarity, d-b triangle closure and

> **Stage**: `FINITE_ELECTROWEAK` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `eada1c9f-3737-5093-afa6-024a83efc8f3`  
> **Parent Derivation**: [TFQ-0079](tfq_0079_each_language_must_carry_weyl_gamma5_square_and_trace_chiral_projector_algebra.md)

---

## 1. Abstract & Formal Statement

The CKM finite control is a Cayley transform over Gaussian rationals, checked in Rust and Python and not elaborated in the Lean file. ckm_skew_hermitian_generator supplies A, and cayley_transform3 returns V = (I - A)(I + A)^(-1) using a 3 by 3 adjugate inverse because Ratio<i64> overflows. passed() recomputes V dagger V = V V dagger = I, closure of the d-b column triangle, and a nonzero Jarlskog invariant. At lambda = 9/40 and A = 4/5 the moduli |V_us|^2 and |V_cb|^2 lie within ten percent of lambda^2 and A^2 lambda^4. The note says this is not the full Wolfenstein hierarchy.

### Governing Obligation
Rust and Python must carry exact two-sided unitarity, d-b triangle closure and J nonzero at the declared generator. Lean 4 must still carry the 3 by 3 Cayley transform; that stem file was not located.

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

- [TFQ-0081](tfq_0081_each_language_must_carry_s_n_c_n_c_3_the_values_1_and_1_3.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
