# [TFQ-0302] Phase-averaged shadow under declared phases

> **Stage**: `L1_TO_L2` | **Status**: `SOURCE_RECORD`  
> **UUID**: `09c69f97-e869-5c8b-9e20-f4e65ebde1e4`  
> **Parent Derivation**: [TFQ-0301](TFQ-0301_haar-independent_phases_are_not_the_finite_average.md)

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

- [TFQ-0303](TFQ-0303_linear_isometric_dynamics_are_an_import.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`, `F001.S000`, `F001.S000:001_from_primitive_difference_to_quantum_mechanics`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/001_from_primitive_difference_to_quantum_mechanics/book/README.md`
