# [TFQ-0044] Do not treat SU(2)_k as a color fusion category; su3_level.rs is absent

> **Stage**: `FINITE_TOPOLOGICAL` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `a224cd40-6e40-5b75-838c-95df3bd7e101`  
> **Parent Derivation**: [TFQ-0043](TFQ-0043_keep_ribbon_charges_off_the_color_and_wilson_spine.md)

---

## 1. Abstract & Formal Statement

anyon_model.rs wraps a ribbon category after braided validation and a dimension check. Its SU(2)_k constructor uses the shared Racah gauge in omega_fusion_categories::su2_level, with a bounded pentagon and hexagon replay. That file warns the gauge is generally not orthonormal, so the F matrices must not be advertised as unitary in the ordinary inner product. Labels a=0..k are twice a spin, which is an SU(2) level family. There is no su3_level.rs beside su2_level.rs. An SU(2)_k anyon model is not the three-color matrix algebra, and its quantum dimensions are not C_F or C_A.

### Governing Obligation
Do not treat SU(2)_k as a color fusion category; su3_level.rs is absent.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: Racah SU(2)_k replay is not in FiniteQM.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: omega_engine/crates_rs/omega_fusion_categories/src/su3_level.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_fusion_categories/src/su2_level.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/anyon_model.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: SU(2)_k has no finite_qm QCD wrapper`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0045](TFQ-0045_admit_an_exchange_only_after_the_exact_inverse_check_and_do_not.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
