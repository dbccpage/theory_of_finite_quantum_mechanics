# [TFQ-0173] Keep discrete curvature as an exact plaquette defect and matrix commutator, without

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `1d4a6ba4-98a3-5bd7-aa0a-34c72c28c914`  
> **Parent Derivation**: [TFQ-0172](tfq_0172_compute_discrete_gauge_holonomy_as_exact_ordered_products_on_a_finite_cell.md)

---

## 1. Abstract & Formal Statement

Curvature in omega_holonomy is a finite commutator and a plaquette defect, not a continuum Riemann tensor. src/curvature.rs documents F_Box as the loop transport of the boundary minus the identity, and curvature_commutator as the matrix bracket M1 M2 minus M2 M1, with a discrete Bianchi check named in lib.rs. Scalars stay on ExactScalar. The obligation is to record flatness only when that exact defect vanishes, and to refuse a numerical tolerance as a stand-in for the identity. The module does not supply the Einstein equation or a Regge deficit angle.

### Governing Obligation
Keep discrete curvature as an exact plaquette defect and matrix commutator, without a float tolerance.

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
- [`code/rust/src/holonomy/curvature.rs`](../../code/rust/src/)
- [`code/rust/src/wdp/lib.rs`](../../code/rust/src/)

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
