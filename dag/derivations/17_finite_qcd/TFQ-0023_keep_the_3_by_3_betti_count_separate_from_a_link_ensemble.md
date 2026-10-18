# [TFQ-0023] Keep the 3 by 3 Betti count separate from a link ensemble

> **Stage**: `FINITE_QCD` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `996360fc-99ba-597a-8b3b-86530c473f2c`  
> **Parent Derivation**: [TFQ-0022](TFQ-0022_keep_the_81-entry_fierz_replay_in_rust_and_python_do_not_equate.md)

---

## 1. Abstract & Formal Statement

Part C of the QCD map fixes a 3 by 3 planar square graph with 9 vertices and 12 edges. A spanning tree has 8 edges, and the cyclomatic count b_1 = 12-9+1 equals 4, so four fundamental plaquette holonomies remain after tree links are dressed to the identity. Lean wilson_lattice_3x3_dfm_betti_identity records e_tree=8, b1=4, and e-e_tree=b1. The Rust report stores lattice_vertices, lattice_edges, spanning_tree_edges_dressed_to_identity, and fundamental_plaquette_cycles_b1. This is a Betti count on one declared complex. It is not a sampled ensemble of SU(3) matrices around those faces.

### Governing Obligation
Keep the 3 by 3 Betti count separate from a link ensemble.

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
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/qcd_beta0_wilson_confinement_control.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/qcd_beta0_wilson_confinement_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0024](TFQ-0024_describe_the_creutz_rows_as_a_comparison_of_two_closed_formulae.md)
- [TFQ-0041](TFQ-0041_keep_the_z2_many-body_benchmark_off_the_su_3_wilson_claim.md)
- [TFQ-0042](TFQ-0042_supply_a_python_replay_or_keep_the_gribov_diamond_as_rust_plus.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
