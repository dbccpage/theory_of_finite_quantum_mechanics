# [TFQ-0195] Use finite rational homology and simplicial complexes as carriers, not as a

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `34c3fba2-a972-5fd2-b4a6-c8847cc6295d`  
> **Parent Derivation**: [TFQ-0166](tfq_0166_record_these_sibling_crates_as_controls_under_authorityeffect_none_not_as_completed.md)

---

## 1. Abstract & Formal Statement

homology supplies finite carriers for later shadows and is not itself a quantum derivation. src/lib.rs opens as computational algebraic topology with AuthorityEffect None and says new TDA modules are best-effort shells unless marked otherwise. src/finite_rational_homology.rs computes rational homology quotients through the shared exact linear-algebra owner and states that it makes no integer-quotient transport or homotopy claim. src/simplicial.rs is the face-closed complex used by the gravity shadow. The obligation is to cite chain maps and simplices as finite controls only.

### Governing Obligation
Use finite rational homology and simplicial complexes as carriers, not as a quantum derivation.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Chain complex over a declared coefficient ring (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Statement is about declared finite complexes; it supplies the 'growth does not repair' direction used by WDP-CH04-N02.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/FiniteCochain.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/wdp/lib.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:c03b90a1a4c10004a71a4988fae598c3cdd3f210e6d2f3e9cbd0d4833ce54ad8`](../../code/rust/src/)
- [`code/rust/src/homology/simplicial.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:11c6f3bb8f50e1cc3ffb444f3699282bcbac16b6207a5ecfde9f1a590e26dc33`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:7a038e117ed5c36acca9ef8559034cb9fc3965236d6c48cc1d7ac428428f85e9`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
  - `external:sha256:98533bbe8dde6cad1f5bbd9d2de0fb85196b2d44c74964cec5a96620ff69c94f`
