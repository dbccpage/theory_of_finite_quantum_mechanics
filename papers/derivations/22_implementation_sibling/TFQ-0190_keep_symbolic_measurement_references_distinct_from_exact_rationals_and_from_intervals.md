# [TFQ-0190] Keep symbolic measurement references distinct from exact rationals and from intervals

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `139a7153-5da1-5655-b268-0b58e9a9261c`  
> **Parent Derivation**: [TFQ-0189](TFQ-0189_keep_exact_rational_measurement_evidence_distinct_and_free_of_float_authority.md)

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
- [`not located`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_measurement/src/measurement_kernel.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
