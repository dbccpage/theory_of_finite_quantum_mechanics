# [TFQ-0357] Record replica extensivity as a reason l1 appears, and keep squared l2

> **Stage**: `L1_EMERGENCE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `e539275b-9f8c-5840-8f4d-f4adab3eeb1b`  
> **Parent Derivation**: [TFQ-0349](TFQ-0349_compute_declared_phi1_and_gamma2_on_a_finite_window_and_do_not.md)

---

## 1. Abstract & Formal Statement

DAG node L1-WDP-CH08-C01-REPLICA-L1 says l1 appears when aggregation over independent replicas is required to be extensive, and that WDP 8.5 states l2 is not excluded by that argument alone. Route L1-R-REPLICA-L1 takes L1-WDP-WINDOW-PHI1-GAMMA2 as input. The node bottleneck in the DAG text also names degree-1 homogeneity separation and a disjoint-support norm separation. Those clauses were not rechecked against the monograph body in this pass. The claim ledger row WDP-CH08-C01 is the cited anchor. AuthorityEffect is None.

### Governing Obligation
Record replica extensivity as a reason l1 appears, and keep squared l2 available under that hypothesis alone.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> None (replica extensivity, WDP 8.5 non-exclusion of squared L2 by extensivity alone, degree-1 homogeneity separation, and disjoint-support norm separation mechanized in wdp_ch08_c01_replica_extensivity_homogeneity_and_l2_separation).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gs001_and_wdp_ch08_replica_extensivity_vs_homogeneity`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gs001_replica_and_phi1_quotient_invariance`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.wdp_ch08_c01_replica_extensivity_homogeneity_and_l2_separation`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/lean/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.wdp_ch08_c01_replica_extensivity_homogeneity_and_l2_separation`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/derivation_dag_witnesses.rs::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche7_wdp_bridge_o03_o05_sector_orbit_and_gleason_rival_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/gauge_classification.rs`](../../code/rust/src/)
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/native/src/derivation_dag_witnesses.rs::verify_tranche17_l1_emergence_gs000_gs001_replica_and_c10_branch_closure_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
