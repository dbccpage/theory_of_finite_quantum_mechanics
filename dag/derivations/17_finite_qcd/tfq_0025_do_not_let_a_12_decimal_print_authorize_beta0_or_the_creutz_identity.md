# [TFQ-0025] Do not let a 12-decimal print authorize beta0 or the Creutz identity

> **Stage**: `FINITE_QCD` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `1b15faba-64f0-54c9-a107-8d42660a6576`  
> **Parent Derivation**: [TFQ-0024](tfq_0024_describe_the_creutz_rows_as_a_comparison_of_two_closed_formulae.md)

---

## 1. Abstract & Formal Statement

qcd_beta0 and qcd_beta1 return BigRational values, and the Creutz ratios above are exact powers of a rational beta_tilde. Part D is different: alpha_s at the Z anchor is the declared rational 1179/10000, pi_interval is a rational bracket of width two in 10^16, and ln3_interval is a 56-term series plus an explicit tail. The report then stores 12-decimal strings for two running values and for ln 9. Those printed decimals are a reading of an enclosure. A float reading of the printed digits cannot authorize the finite beta0 identity or the exact Creutz comparison, which do not use that enclosure.

### Governing Obligation
Do not let a 12-decimal print authorize beta0 or the Creutz identity.

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

- [TFQ-0026](tfq_0026_add_python_and_lean_replays_of_the_declared_doubling_count_or_leave.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S001`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S001_continuum_finite_shadow_bridge/shelf.yaml`
