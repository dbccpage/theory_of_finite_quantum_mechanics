# [TFQ-0156] Odd-prime-power MUB controls

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `6e38f7c2-54db-5175-9061-7de5a95fd506`  
> **Parent Derivation**: [TFQ-0155](tfq_0155_odd_prime_weyl_mub_and_wigner.md)

---

## 1. Abstract & Formal Statement

Covers mub/odd_prime_power_weyl.rs, mub/odd_prime_power_controls.rs, mub/odd_prime_power_field_theorem_gate.rs, mub/odd_prime_power_parametric_gate.rs, and mub/prime_power_gtmur_boundary.rs. odd_prime_power_controls.rs gives exact Hilbert controls for dimensions 9, 25, 27, and 49 in named cyclotomic fields, as positive controls rather than an all-dimension theorem. The other files organize trace and Gauss reductions and the prime-power boundary of a broader request. A Python replay and a Lean 4 declaration would still have to match those declared-dimension controls.

### Governing Obligation
Match the declared exact controls in dimensions 9, 25, 27, and 49 without treating them as an all-dimension theorem.

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
- [`absent: no local rust twin located for external:sha256:262a84c0f4c17f34311b859ca88d2b6b15207f612c3bb4448e369966560e4bf1`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:a105030bc935c4dc8051763027af87200bdab3ea35244eb9848f993fb3076384`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:c19fe115023da356274e407a77e83f6e8a975e6f63316be2a3a27f9192a577db`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:3b52c087fad81061e03048884549a842213e53ceec5c6ca46868da497d17eebb`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:9b5d8924e7be5bba9565cbd05e23d0f9e4dd624802f64a1002ef6eefb5095280`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: The python twin is not located for the odd-prime-power MUB controls under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
