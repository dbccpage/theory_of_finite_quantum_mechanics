# [TFQ-0038] Reconcile the map's K5 ranks with the Rust certificate and leave the

> **Stage**: `FINITE_QCD` | **Status**: `GAP`  
> **UUID**: `efb4737b-2124-5b1e-9449-b43526665d89`  
> **Parent Derivation**: [TFQ-0037](tfq_0037_keep_slater_car_and_shell_capacities_on_the_identical_particle_side_of_the.md)

---

## 1. Abstract & Formal Statement

Two readings of the K5 torsion must stay apart. The opening of pauli_spin_statistics_graph_finite_map.md states rank_Q of the square boundary as 7 and the rational 2-complex Betti number as 14. The Rust test and the Lean literals use rational Betti number 6 and F2 Betti number 7, hence torsion rank 1. Lean also says whether the exchange loop represents that torsion class is not established. A Python comment in analyze_conf2_graph speaks as if the torsion forces the exchange loop to have order 2. The rank mismatch and the representative question are an open gap beside the certificate.

### Governing Obligation
Reconcile the map's K5 ranks with the Rust certificate and leave the exchange-loop representative unresolved.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/FiniteQM.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/pauli_spin_statistics_graph.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/pauli_spin_statistics_graph_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
