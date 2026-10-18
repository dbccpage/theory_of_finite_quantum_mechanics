# [TFQ-0036] Report the Rust and Lean K5 torsion rank, not the opening paragraph's

> **Stage**: `FINITE_QCD` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `630bf7ec-faa7-5ab4-b583-a2346905a242`  
> **Parent Derivation**: [TFQ-0035](TFQ-0035_quote_n_c_3_as_the_finite_color_factor_and_leave_the_ev_rate.md)

---

## 1. Abstract & Formal Statement

pauli_spin_statistics_graph.rs runs verify_qm223_spin_statistics_graph on Conf_2 of P3, the star K_{1,3}, C4, K4, and K5. The Rust test records K5 as 10 vertices, 30 edges, 15 squares, first Betti number 21, rational 2-complex Betti number 6, F2 Betti number 7, and Z2 torsion rank 1. Planar K4 stays torsion-free with rational Betti number 4. Lean graph_conf2_exchange_betti_and_character_collapse matches those K5 integers and adds the Rat collapse chi^2=1 if and only if chi is +1 or -1. This is a finite graph control. It is not a color wavefunction and not a baryon multiplet.

### Governing Obligation
Report the Rust and Lean K5 torsion rank, not the opening paragraph's other Betti number.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/FiniteQM.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/pauli_spin_statistics_graph.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/pauli_spin_statistics_graph_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0037](TFQ-0037_keep_slater_car_and_shell_capacities_on_the_identical-particle_side_of_the.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
