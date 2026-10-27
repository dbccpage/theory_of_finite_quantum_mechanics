# [TFQ-0013] Use cyclotomic character tables only as labels of a declared finite group

> **Stage**: `FINITE_QCD` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `a96c6860-0b9e-543c-adbc-92f0eca0d2b0`  
> **Parent Derivation**: [TFQ-0012](tfq_0012_locate_a_hopf_gauge_file_or_keep_the_gauge_datum_as_the.md)

---

## 1. Abstract & Formal Statement

finite_group.rs builds a FiniteGroup from a full multiplication table or from an associative operation, then checks closure, a two-sided identity, and inverses. Hand-written tables also face an associativity check, while from_operation inherits associativity from the operation. Character tables are lifted to Z[zeta_e] by Dixon reduction modulo a prime, and orthogonality is checked in that ring, not in floating point. Those cyclotomic values can label a declared finite gauge group. They do not by themselves name three color charges or a plaquette holonomy.

### Governing Obligation
Use cyclotomic character tables only as labels of a declared finite group.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: Dixon character lift is not in FiniteQM.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/lie_theory/finite_group.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: finite_group character tables are not wrapped by a QCD use case`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0014](tfq_0014_do_not_cite_the_m_2_packet_complex_or_the_groupoid_algebra_as.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
