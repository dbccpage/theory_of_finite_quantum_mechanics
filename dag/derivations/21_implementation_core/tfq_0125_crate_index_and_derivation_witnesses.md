# [TFQ-0125] Crate index and derivation witnesses

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `870a09fe-01a1-564d-aa6e-1f557e89aa07`  
> **Parent Derivation**: [TFQ-0007](../10_finite_qm_core/tfq_0007_finite_quantum_mechanics_core_on_an_admitted_carrier.md)

---

## 1. Abstract & Formal Statement

Covers lib.rs, derivation_dag_witnesses.rs, engine_bridge.rs, carrier_tests.rs, and bin/emit_pfp_workpads.rs. The lib.rs header was not descriptive. derivation_dag_witnesses.rs stores exact integer and rational family receipts for the Pre-Genesis to Finite-QM derivation DAG. engine_bridge.rs maps exact operators to diagnostic numerical densities, and carrier_tests.rs separates report sufficiency, Bell extension, and a third finite question. The binary emits PFP workpad JSON. A Python replay and a Lean 4 declaration would still have to match those exact receipts and the three-way carrier split.

### Governing Obligation
Match exact integer and rational derivation-DAG family receipts and the three-way split among report sufficiency, Bell extension, and the third carrier question.

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
- [`code/rust/src/wdp/lib.rs`](../../code/rust/src/)
- [`code/rust/src/dag_witnesses.rs`](../../code/rust/src/)
- [`code/rust/src/qm/campaigns/engine_bridge.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:4799bd7832947fd060449a609277b0884681021ac90fe1f3833a71ac20f0e412`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:d1787dad0abfd3ac2549cc51827014cd8feb4379238cb28de59ce92e0fda833b`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/finite_qm_engine.py`](../../code/python/)
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0126](tfq_0126_finite_configurations_and_complex_structure.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
