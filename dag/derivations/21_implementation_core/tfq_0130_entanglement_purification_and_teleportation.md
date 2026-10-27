# [TFQ-0130] Entanglement, purification, and teleportation

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `5a4935ea-8d39-569d-ad3f-f2766bc6ce42`  
> **Parent Derivation**: [TFQ-0129](tfq_0129_exact_rays_and_pure_states.md)

---

## 1. Abstract & Formal Statement

Covers entanglement.rs, purification.rs, bipartite_operator.rs, relative_state_branching.rs, no_cloning.rs, and teleportation.rs. entanglement.rs decides Schmidt rank of a pure bipartite state exactly over Q(i), and it says a diagonal population entropy is not an entanglement measure for a general state. The other files lift a mixed state, give exact bipartite operators, expand relative states, evaluate the Wootters-Zurek obstruction, and lay out qubit teleportation. A Python replay and a Lean 4 declaration would still have to match the exact Schmidt-rank decision.

### Governing Obligation
Match exact Schmidt rank over Q(i), the warning on diagonal population entropy, and the three-qubit teleportation layout.

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
- [`absent: no local rust twin located for external:sha256:dd1b4e46a648387082ad2289a7af199984e2d166d08f5debbde4c4b30ddcf8c8`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:1079d3a7b2958efcc95ca07550213d87da604d8ada2d71c28684958b86dc21ab`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:f29fe2318e14a44a45fccfee6f94f69a7dc615832988d69c2b47ec6fef35e56b`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:bdfd46b9d29d0fba7f7d4e212d92d6621771eee3bac8425286e98df2fd72ce34`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:aa2a8686264281e11a2edd6d9b7aea5eb9a53ee333cca184cf15394bf611e597`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:ae407b5f6ef9b3c091496688fc7ed38f869d28cec1c88727de1c95a7eacef85c`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/higher_dim_entanglement.py`](../../code/python/)
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/quantum_protocols.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
