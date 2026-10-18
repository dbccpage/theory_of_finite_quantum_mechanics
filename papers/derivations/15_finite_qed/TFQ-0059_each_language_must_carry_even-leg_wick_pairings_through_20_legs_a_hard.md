# [TFQ-0059] Each language must carry: even-leg Wick pairings through 20 legs, a hard

> **Stage**: `FINITE_QED` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `dd01fb4a-c925-5b27-809d-65c24f0c45cc`  
> **Parent Derivation**: [TFQ-0058](TFQ-0058_each_language_must_carry_u_g_equals_the_scaled_principal_minor_of_the.md)

---

## 1. Abstract & Formal Statement

feynman_diagram.rs computes finite Wick contractions and vacuum-multigraph symmetry factors. wick_pairing_count and wick_pairings require an even number of legs, at most 20, and refuse when the materialized pairing or permutation count exceeds the budget. MAX_WICK_PAIRINGS is 1<<16. A contraction keeps half-edges, loops and parallel edges. symmetry_factor uses vertex automorphisms, parallel-edge permutations and loop reversals. phi4_vacuum_diagrams classifies canonical phi-four vacuum multigraphs through three vertices and returns a computed factor.

### Governing Obligation
Each language must carry: even-leg Wick pairings through 20 legs, a hard budget refusal, and a symmetry factor from automorphisms, parallel edges and loop reversals, with no loop integral.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `continuum path category (assumption)`
- **Admitted**: `declared discrete Lagrangian and weights (assumption)`
- **Admitted**: `refinement system and convergence certificate (assumption)`
- **Admitted**: `time slicing (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Lean file for ENC-1072 not verified by me.

> [!WARNING]
> Forward-Euler norm growth 1 + e^2 > 1 vs Cayley norm preservation is mechanized; continuum path-integral convergence remains conditional.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_033_041_043_dynamics_and_heisenberg_duality`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm030_032_graded_pathsum_overcount_transfer_and_feynman_shadow`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_qm063_032_034_destructive_interference_and_cayley_vs_euler_norm`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm032_finite_feynman_interference_vs_stochastic`](../../code/lean4/)
- [`not located`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/feynman_diagram.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_ds_qm_dynamics_structure_and_majorana_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche13_ds_qm_final_16_second_witness_closure_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche9_bloch_gap_cayley_u1_hadamard_coherence_and_destructive_interference_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0060](TFQ-0060_each_language_must_carry_c1_1_2_exactly_and_higher_coefficients_only.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
