# [TFQ-0153] No-signalling and classical storage

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `91a1b910-e879-5085-8a39-26431d7870b3`  
> **Parent Derivation**: [TFQ-0146](tfq_0146_kraus_channels_and_completely_positive_maps.md)

---

## 1. Abstract & Formal Statement

Covers no_signalling.rs, classical_storage.rs, process_matrix.rs, classical_structure.rs, and frobenius_algebra.rs. no_signalling.rs checks that a local Kraus channel on Alice leaves Bob partial trace invariant, while a conditional branch needs an outcome message. The other files store a quantum-classical-quantum path over Q(i), carry process matrices and the quantum switch, and replay dagger-Frobenius pointer algebras. A Python replay and a Lean 4 declaration would still have to match the partial-trace invariance and the message proviso.

### Governing Obligation
Match invariance of Bob partial trace under a local Alice channel, and the outcome-message proviso for conditional branches.

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
- [`code/rust/src/qm/campaigns/no_signalling.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:18bc614f573aeda9eedb530a3c1855d7b2b4b2e9084c7d48c8db703764e1586c`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:eec8c06ee9d521a7463a55cb9b235e6f546010cfe9b9ab0a33ff2729069c5e26`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:846ce6a861f82044394b89d5ba89f14f1a1c84fd2fb79d0bf58c97e5461cafa5`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:ad56a7102a48fb9287fc38f006245330317e837b536f3b50cfde36d31aebc29f`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: The python twin is not located for no_signalling.rs under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
