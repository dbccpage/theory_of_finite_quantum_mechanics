# [TFQ-0055] Each language must carry: no rational homomorphism supplies the missing square root

> **Stage**: `FINITE_GAUGE` | **Status**: `GAP`  
> **UUID**: `67aa1b37-8f6d-5f0b-8c6a-34bafb4fab87`  
> **Parent Derivation**: [TFQ-0054](tfq_0054_each_language_must_carry_pure_gauge_iff_every_off_forest_edge_is_1.md)

---

## 1. Abstract & Formal Statement

The finite U(1) data stop at Gaussian rational units and N-torsion holonomy. FQ-GAP-U1-CIRCLE records that the circle group is not constructed on the finite host: in Q(i), u = (3+4i)/5 has no square root and n -> u^n is injective, so no homomorphism from (Q,+) to the rational points sends 1 to u. F002.S001 is the empty shelf where a continuum shadow of that circle would have to be named later. Its shelf.yaml has books: [] and says a named adjoining record does not establish a bridge theorem. F002.S000 is only the interface inventory.

### Governing Obligation
Each language must carry: no rational homomorphism supplies the missing square root of (3+4i)/5, and F002.S001 remains an empty open bridge rather than a completed circle.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `circle group U(1) (assumption)`
- **Admitted**: `circle group U(1): assumption`
- **Admitted**: `complex field C (assumption)`
- **Admitted**: `continuity of one-parameter phase group (assumption)`
- **Admitted**: `continuum Hilbert space (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Algebraic non-square obstruction in Q(i) and rational Cayley punctured-circle parameterization are mechanized; compact continuous R/Z completion remains a declared external import.

> [!WARNING]
> See L1-U1-SELECTOR-OTHER-SEGMENT.

> [!WARNING]
> Z[i] non-field obstruction and discriminant-5 spectral exit from Q(i) are mechanized; continuum Hilbert completion remains an explicit import.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:e86ad3309b090c78f09e92fa9833a87b325a0513396663cbf2bd5c2ea1fd0c7b`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`, `F002.S001`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
  - `external:git-tree:0fb81f77bbeba84143f574b5a4bc956196140991`
  - `external:git-tree:197a57e06c54cd85be796698967601ae741995cb`
