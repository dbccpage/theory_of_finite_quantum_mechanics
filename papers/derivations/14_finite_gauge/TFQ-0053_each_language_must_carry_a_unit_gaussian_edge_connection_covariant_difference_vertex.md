# [TFQ-0053] Each language must carry: a unit Gaussian edge connection, covariant difference, vertex

> **Stage**: `FINITE_GAUGE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `1f121d18-5f8a-5667-bf5f-f6adc1d26517`  
> **Parent Derivation**: [TFQ-0052](TFQ-0052_each_language_must_carry_on_a_declared_m_2_q_i_packet_d0_of_an.md)

---

## 1. Abstract & Formal Statement

u1_graph_connection.rs stores a declared U(1) connection as one unit Gaussian rational on each oriented edge of a FiniteCochainPacket. The scalars are rational points of the circle, not a completed circle. A real cochain becomes a connection only through a separately declared CochainExponential, and that map loses information. The module computes the covariant difference (D_A psi)(u,v) = psi(v) - A_(u,v) psi(u), the vertex gauge A'_(u,v) = g(v) A_(u,v) conj(g(u)), and edgewise covariance of D_A. Closed-walk holonomy is gauge invariant; open-walk transport is covariant at its endpoints.

### Governing Obligation
Each language must carry: a unit Gaussian edge connection, covariant difference, vertex gauge, and closed-walk holonomy, with the exponential from an additive cochain declared and lossy.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `circle group U(1) (assumption)`
- **Admitted**: `circle group U(1): assumption`
- **Admitted**: `continuity of one-parameter phase group (assumption)`
- **Admitted**: `finite oriented graph (assumption)`
- **Admitted**: `non-triviality and order N of the edge phase cochain (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Finite N-torsion gauge invariance and sign-group separation are mechanized; completion to R/Z remains in FQ-GAP-U1-CIRCLE.

> [!WARNING]
> See L1-U1-SELECTOR-OTHER-SEGMENT.

> [!WARNING]
> Algebraic non-square obstruction in Q(i) and rational Cayley punctured-circle parameterization are mechanized; compact continuous R/Z completion remains a declared external import.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_gap_u1_circle_pythagorean_half_exponent_obstruction`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_u1_selector_split_real_zero_divisors_and_cayley_unit_circle`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_u1_transport_n_torsion_and_sign_separation`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gap_u1_inner_product_orthogonal_additivity_and_isometric_dynamics_countermodels`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011Circle.lean::sign_excluded_circle_still_imported`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011Circle.lean::sign_fails_connectedness_shadow`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011U1SelectorBoundary.lean::selector_not_free`](../../code/lean4/)
- [`lean4/quantum_mechanics/H011U1SelectorBoundary.lean::u1_selector_boundary`](../../code/lean4/)
- [`not located`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/complex_structure_selector.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/holonomy_interference.rs::gauge_equivalence`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/phase_blind_quotient.rs::UnitPhaseGroup`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps.rs::evaluate_qm207_holonomy_bridge`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/u1_graph_connection.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/u1_graph_connection.rs::U1Connection`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche15_gap_nonderivation_countermodels_and_conditional_route_bridges_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche9_bloch_gap_cayley_u1_hadamard_coherence_and_destructive_interference_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/amplitude_bridge.rs::half_exponent_obstruction`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0054](TFQ-0054_each_language_must_carry_pure_gauge_iff_every_off-forest_edge_is_1.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
