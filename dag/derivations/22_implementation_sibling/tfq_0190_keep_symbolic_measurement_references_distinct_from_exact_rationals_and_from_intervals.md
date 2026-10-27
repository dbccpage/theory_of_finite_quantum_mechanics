# [TFQ-0190] Keep symbolic measurement references distinct from exact rationals and from intervals

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `139a7153-5da1-5655-b268-0b58e9a9261c`  
> **Parent Derivation**: [TFQ-0189](tfq_0189_keep_exact_rational_measurement_evidence_distinct_and_free_of_float_authority.md)

---

## 1. Abstract & Formal Statement

Symbolic measurement evidence is a separate enum arm and is not an evaluated expression. MeasurementValue::SymbolicExpression holds a SymbolicExpressionRef whose payload is a String. The kernel header groups exact, symbolic, interval, and certified numerical values as alternative evidence kinds. Nothing in the opened header reduces a symbolic reference to a BigRational. The obligation is to keep a symbolic tag from being read as an exact value, an interval bound, or a certified approximation. GovernanceScalar has no symbolic arm, so the tag cannot enter a governance scalar.

### Governing Obligation
Keep symbolic measurement references distinct from exact rationals and from intervals.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:e7de14f3a7ac549411872b110b09968dc2178ab76ed8099b8871e949a9d69b7a`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
