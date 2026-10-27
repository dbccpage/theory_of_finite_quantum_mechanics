# [TFQ-0158] Composite MUB tensor lower controls

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `bf15a4fe-c841-5b15-8ba0-8bc2d149ed91`  
> **Parent Derivation**: [TFQ-0154](tfq_0154_canonical_mub_inversion.md)

---

## 1. Abstract & Formal Statement

Covers mub/composite.rs, mub/composite_controls.rs, mub/composite_completion_gate.rs, mub/composite_tensor_family_gate.rs, mub/d10_controls.rs, and mub/non_cyclic_falser.rs. composite.rs pairs Kronecker products of factor MUB projectors and, for dimension 6, records three bases from factors 2 and 3. The other files keep that lower control apart from a complete family, mark the d=10 boundary as partial, and search MUB-6 candidates outside the cyclic Weyl class. A Python replay and a Lean 4 declaration would still have to match the paired-product count.

### Governing Obligation
Match the paired Kronecker lower control, including three bases in dimension 6, and the partial d=10 boundary.

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
- [`absent: no local rust twin located for external:sha256:90994bce0491d03711037f468c4ec2fbff19350a83431170200491dfd602c86b`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:ebc90fc9e25aea5a9f6142c74ccd659b2540cac7fbe1891de6dc6c6cec317ea9`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:9296c8b6080ffbdc3ba88ca1ed17655af1746cf3c2460c8cb4c6e64169533225`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:e29f9651f96bd192309ec1227bfd711dc20efd030d91ac3f9b1766d2913246c1`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:f2833841ab4ff101c712310999d37362d63a05ca863f60492c3c594c7aff9131`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:6e368b036d0079043a60025b15b6b4b9377a295e8016744150257f7594bc984f`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: The python twin is not located for mub/composite.rs. composition_tensor_mub.py is a tensor-statistics replay, not this lower-control gate.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
