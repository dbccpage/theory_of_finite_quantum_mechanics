# [TFQ-0043] Keep ribbon charges off the color and Wilson spine

> **Stage**: `FINITE_TOPOLOGICAL` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `5d67d47b-9970-53e0-96c6-b2c76b3215c3`  
> **Parent Derivation**: [TFQ-0012](../17_finite_qcd/tfq_0012_locate_a_hopf_gauge_file_or_keep_the_gauge_datum_as_the.md)

---

## 1. Abstract & Formal Statement

anyon.rs reads a simple charge from a RibbonFusionCategory: dual, quantum dimension, twist, and an invertibility bit from fusion multiplicities. The authority fence says the charges are exact finite ribbon data, not a global closure. catalog.rs can supply Ising, Fibonacci, semion, and toric-code data, and it says nothing in that catalog claims a material hosts the category. This node starts a topological side branch. It is not a QCD color representation, not a Wilson loop on the 3 by 3 graph, and not an input to beta0. Fusion-category arithmetic must not be cited as the su(3)_c generator control.

### Governing Obligation
Keep ribbon charges off the color and Wilson spine.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: ribbon charges are not FiniteQM QCD theorems`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/anyon.rs`](../../code/rust/src/)
- [`code/rust/src/fusion_categories/catalog.rs`](../../code/rust/src/)
- [`code/rust/src/wdp/lib.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: anyon charges have no QCD use case`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0044](tfq_0044_do_not_treat_su_2_k_as_a_color_fusion_category_su3_level_rs_is_absent.md)
- [TFQ-0048](tfq_0048_do_not_read_the_toric_code_s_withheld_hamiltonian_gap_as_the_qcd.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
