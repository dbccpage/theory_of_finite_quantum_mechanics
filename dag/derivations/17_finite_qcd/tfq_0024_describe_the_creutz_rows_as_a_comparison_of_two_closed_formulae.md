# [TFQ-0024] Describe the Creutz rows as a comparison of two closed formulae

> **Stage**: `FINITE_QCD` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `3e9a0fb5-4534-521a-8b15-33c85b866cab`  
> **Parent Derivation**: [TFQ-0023](tfq_0023_keep_the_3_by_3_betti_count_separate_from_a_link_ensemble.md)

---

## 1. Abstract & Formal Statement

creutz_ratio_area_law and creutz_ratio_perimeter_law in the Rust QCD control, and wilson_area_law, wilson_perimeter_law, and creutz_ratio in the Python twin, compare two closed formulae. With W_area = beta_tilde to the power R*T and W_perim = beta_tilde to the power 2*(R+T), the multiplicative Creutz ratio equals beta_tilde in the first case and 1 in the second. At beta_tilde=1/9 the map records 1/9 against 1 for rectangles with R and T in {2,3}. Lean wilson_creutz_ratio_area_vs_perimeter checks the same cancellation for b nonzero. The comparison is algebraic. It is not a Monte Carlo estimate of a Wilson loop.

### Governing Obligation
Describe the Creutz rows as a comparison of two closed formulae.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/FiniteQM.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/qcd_beta0_wilson_confinement_control.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/qcd_beta0_wilson_confinement_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0025](tfq_0025_do_not_let_a_12_decimal_print_authorize_beta0_or_the_creutz_identity.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
