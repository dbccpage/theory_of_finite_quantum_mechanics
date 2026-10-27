# [TFQ-0194] Keep the finite Weyl relation distinct from a characteristic-zero CCR, which the

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `7bf627dc-a72b-5b6c-8ca7-6cf5f06b853e`  
> **Parent Derivation**: [TFQ-0193](tfq_0193_keep_rational_lie_and_finite_group_constructions_exact_without_a_continuum_haar_or.md)

---

## 1. Abstract & Formal Statement

Finite Weyl-Heisenberg operators are an exact shadow and include an explicit refusal of a characteristic-zero CCR. src/heisenberg.rs sets X and Z on a finite clock, with tau squared equal to omega, and says a finite characteristic-zero CCR is refused by its nonzero exact trace, whether or not the finite Weyl relation holds. Even dimension needs a declared 2d-th root; reducing labels modulo d would drop a sign. weyl_operators.rs and pauli_symplectic.rs sit in the same crate. The obligation is to keep that finite relation from being cited as a CCR on a completed real line.

### Governing Obligation
Keep the finite Weyl relation distinct from a characteristic-zero CCR, which the header refuses by trace.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/RationalLieSpan.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/lie_theory/heisenberg.rs`](../../code/rust/src/)
- [`code/rust/src/lie_theory/weyl_operators.rs`](../../code/rust/src/)
- [`code/rust/src/lie_theory/pauli_symplectic.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
