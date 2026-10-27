# [TFQ-0157] Characteristic-two projector MUBs

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `54c0bb1d-7c42-521b-9dc4-1dc07ae3b2e4`  
> **Parent Derivation**: [TFQ-0154](tfq_0154_canonical_mub_inversion.md)

---

## 1. Abstract & Formal Statement

Covers mub/char_two.rs, mub/char_two_weyl_board.rs, mub/finite_projector_control.rs, mub/projector_algebra.rs, mub/spectral_lift.rs, mub/hilbert_transport.rs, and mub/gtmur_projector_ledger.rs. char_two.rs builds characteristic-two complete MUBs on exact projector matrices from independent binary generators. The other files avoid division by two, separate incidence from the operator lift, transport Pauli projectors, and audit representation changes. A Python replay and a Lean 4 declaration would still have to match the generator-dimension check and that incidence split.

### Governing Obligation
Match characteristic-two complete MUBs from independent binary generators whose count fits the Hilbert dimension.

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
- [`absent: no local rust twin located for external:sha256:4f4b4136c196f2431cecda69d19b0b7df397e0af948635e4e42543a7fedfb79b`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:ae2912155731efc9e4f9b6841425b8ce1952e05db3d03ceac87621fc34a70707`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:becaa33cea0771d95f0efee0dcf5b5f8ebcf23843b2145814f44405aa3c76978`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:b78705893ac175ecde4bf213101d69fca55ab1246f32c8c18874fd57dca8d54c`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:800c82dc185cd8ca2d773c46d9c8d3b66c31862eec49eee8e70dcade504c4557`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:cd99f7b59751aed8845f5d1127c7038739938db2629c9796f40781889b9c534c`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:ae85d0aad38bfd52a7e1d9f74b6abd01ea2ffd9f0570c462d8ccc84b59a4a886`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: The python twin is not located for characteristic-two MUB projectors under 006_finite_qm/python/finite_qm.`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
