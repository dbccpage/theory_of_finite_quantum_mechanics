# [TFQ-0165] Spin-network area labels

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `54824c7c-a918-5bf7-91f4-11e8ea511c68`  
> **Parent Derivation**: [TFQ-0127](tfq_0127_hilbert_carriers_and_tensor_index.md)

---

## 1. Abstract & Formal Statement

Covers spin_area_spectrum.rs, tower_topological_completion.rs, and tower_walk_validator.rs. spin_area_spectrum.rs sets the area label at spin j = n/2 to the surd of j(j+1), leaving the physical scale as a separate declaration, and computes intertwiner dimensions by the SU(2) fusion rule. The tower files are a finite spin benchmark with declared normalization and a walk validator for lift pressure and residual norms. A Python replay and a Lean 4 declaration would still have to match the area-label surd and that normalization boundary.

### Governing Obligation
Match the area-label surd of j(j+1) at spin j = n/2 and the declared normalization of the finite spin benchmark.

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
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/spin_area_spectrum.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/tower_topological_completion.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/tower_walk_validator.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/tower_topological_completion.py`](../../code/python/)
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
