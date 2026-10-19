# [TFQ-0302] Phase-averaged shadow under declared phases

> **Stage**: `L1_TO_L2` | **Status**: `SOURCE_RECORD`  
> **UUID**: `09c69f97-e869-5c8b-9e20-f4e65ebde1e4`  
> **Parent Derivation**: [TFQ-0301](tfq_0301_haar_independent_phases_are_not_the_finite_average.md)

---

## 1. Abstract & Formal Statement

The section labeled Theorem 5 in qm_020_born_normalization_and_conditional_hilbert_lift.md states a phase-averaged shadow: under a chosen lift and independent Haar phases, the expected squared overlap with a test vector is the weight-weighted sum of the test coordinates' squared moduli. The finite obligation in code is the enumerated average, not that Haar statement. phase_averaged_shadow.rs dephases a matrix over a declared finite group and records the readout sum of squared test weights against the diagonal.

### Governing Obligation
Report the phase-averaged shadow only with the phase measure that was actually used.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Haar measure on phases: assumption`
- **Admitted**: `Hilbert inner product: assumption`
- **Admitted**: `independence of phases: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Exact cancellation of off-diagonal cross terms over {-1, +1}^2 is mechanized in DerivationDagQMClosure.lean.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_phase_averaged_shadow_and_c10_pinching`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_qm020_thm5_thm7_and_qm121_ladder_rungs_2_to_6_separation`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_averaged_shadow.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_averaged_shadow.rs::averages_to_dephasing`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_averaged_shadow.rs::phase_group_average`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/_code/qm_020/code/qm_020_born_normalization_and_conditional_hilbert_lift_core.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0303](tfq_0303_linear_isometric_dynamics_are_an_import.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-IMP-HAAR-INDEPENDENT-PHASES`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-IMP-HAAR-INDEPENDENT-PHASES` (`L1_TO_L2` / `IMPORTED_ASSUMPTION`)
- **Mined Operad Family (`M2`)**: `OP-L1-HAAR-VS-FINITE-Z4-AVERAGE`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [280, -560, 420]`, `chord_potential = 420`, `holonomy_gamma2 = 560`
- **Finite Shadow Exact Witness (`M4`)**: `z4_squared_16_pair_diagonal_sum: 16 * (|3|^2 + |4|^2) == 16 * 25 == 400` ($\text{value} = 400$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `correlated_equal_phase_subgroup_cross_term: 4 * (2 * 3 * 4) == 96 != 0 (without independent phases, cross term 96 survives)` ($\text{value} = 96$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `2` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 089e8e01b9ef4087dd2f6c07d6b319d7719553d03d545793b0c9c3ebd81ce890`
