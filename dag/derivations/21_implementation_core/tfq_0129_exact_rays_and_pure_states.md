# [TFQ-0129] Exact rays and pure states

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `85b9c7ef-8120-513b-8611-05d867bd24ac`  
> **Parent Derivation**: [TFQ-0127](tfq_0127_hilbert_carriers_and_tensor_index.md)

---

## 1. Abstract & Formal Statement

Covers quantum_state.rs, bell_state.rs, ghz_state.rs, w_state.rs, and mass_phase_embedding.rs. quantum_state.rs takes a pure state to be a nonzero Q(i) ray, not a normalized vector, so transition ratios, expectations, and the projector stay in Q. The f64 face is diagnostic only. Born weights use the declared squared-modulus rule. The Bell, GHZ, and W files name those finite entangled vectors, and mass_phase_embedding.rs embeds declared L1 masses and phases as a unit L2 vector. A Python replay and a Lean 4 declaration would still have to match the scale-invariant ray ratios and that diagnostic split.

### Governing Obligation
Match scale-invariant Q(i) ray ratios, the declared squared-modulus Born rule, and the diagnostic status of the f64 face.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: no local lean twin located for lean4/quantum_mechanics`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_state.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/bell_state.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/ghz_state.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/w_state.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/mass_phase_embedding.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/born_normalization.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0130](tfq_0130_entanglement_purification_and_teleportation.md)
- [TFQ-0131](tfq_0131_density_operators_over_q_i.md)
- [TFQ-0162](tfq_0162_everett_branches_and_histories.md)
- [TFQ-0163](tfq_0163_interference_cancellation_and_path_sums.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
