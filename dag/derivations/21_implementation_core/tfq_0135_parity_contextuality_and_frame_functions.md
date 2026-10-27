# [TFQ-0135] Parity contextuality and frame functions

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `1bc63a61-f018-5166-9b22-15d57ac377c5`  
> **Parent Derivation**: [TFQ-0134](tfq_0134_pauli_group_and_exchange_characters.md)

---

## 1. Abstract & Formal Statement

Covers contextuality_obstruction.rs, kochen_specker.rs, separating_predictions.rs, frame_function_polytope.rs, and gauge_cochain_complex.rs. contextuality_obstruction.rs computes finite parity contextuality as a Z2 cochain class, with a Cabello 18-ray witness and a product scenario whose class vanishes. The other files decide Kochen-Specker hypergraphs, replay Mermin-Peres assignments over F2, tie frame functions to symmetric matrices, and classify packets on M_2(Q(i)). A Python replay and a Lean 4 declaration would still have to match that Z2 class and the vanishing control.

### Governing Obligation
Match the Z2 cochain obstruction, the Cabello witness, and the product scenario whose class vanishes.

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
- [`absent: no local rust twin located for external:sha256:548be8ce94a17a91d70f87aa6ddd92b68ab38df11f95e8943a6ae35fe0a9d2b4`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:604e2768b7d0ee3423792a93ba46749403a8df2cdfa61198bf69fa12243b52f7`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:64c134e8d0909213d469b8033eaaabe4c42011a089c90c790c23d9ceee66fccf`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:ae888a69f68011cf2bdbe26b173cbe6cf818f2a9c044b25aa7b39f5592b688c5`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:1716598040aa40ee83bed4fdf0e76ab6111debd683decf50bbbe5df6dbc71b65`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/contextuality_f2.py`](../../code/python/)
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/mermin_peres.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
