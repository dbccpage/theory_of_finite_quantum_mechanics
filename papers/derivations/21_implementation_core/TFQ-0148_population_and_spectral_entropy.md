# [TFQ-0148] Population and spectral entropy

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `27568549-0f21-5b7b-9466-6a928db9fdfe`  
> **Parent Derivation**: [TFQ-0147](TFQ-0147_weighted_stinespring_realizations.md)

---

## 1. Abstract & Formal Statement

Covers entropy.rs, exact_entropy.rs, quantum_relative_entropy.rs, and majorization.rs. entropy.rs says its population-face entropies are Shannon quantities of the diagonal, equal to operator entropies only for computational-basis diagonal states, and it refuses an irrational spectrum for the exact logarithm. The other files take a declared rational spectrum, the Umegaki face, and majorization by exact partial sums. A Python replay and a Lean 4 declaration would still have to match the diagonal-versus-operator split and that refusal.

### Governing Obligation
Match Shannon-versus-operator entropy on the diagonal face and the refusal of an irrational spectrum.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/entropy.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/exact_entropy.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/majorization.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_relative_entropy.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`The python twin is not located for entropy.rs under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0149](TFQ-0149_mutual_information_and_fidelity.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
