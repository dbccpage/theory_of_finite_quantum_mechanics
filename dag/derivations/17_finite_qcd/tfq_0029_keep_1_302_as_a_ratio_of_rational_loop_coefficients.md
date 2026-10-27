# [TFQ-0029] Keep 1/302 as a ratio of rational loop coefficients

> **Stage**: `FINITE_QCD` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `7649baf2-020a-5e79-8482-00fb4b6ab887`  
> **Parent Derivation**: [TFQ-0028](tfq_0028_state_the_beta0_window_as_rational_arithmetic_and_repeat_the_map_s_withheld.md)

---

## 1. Abstract & Formal Statement

qcd_beta1(3, n_f) is recorded as 102 - (38/3)*n_f. At n_f=16 the Rust control and Lean qcd_beta1_and_banks_zaks_fixed_point record beta0=1/3, beta1=-302/3, and the ratio -beta0/beta1 = 1/302. Python qcd_beta1 repeats the same rational expression. This is a ratio of two loop coefficients inside the finite control. It is not an infrared fixed-point statement about a continuum gauge theory, and the 12-decimal running enclosure in Part D is not an input to the ratio. A float approximation of 1/302 cannot authorize the rational identity, which is already exact over Q.

### Governing Obligation
Keep 1/302 as a ratio of rational loop coefficients.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/FiniteQM.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:b76d75cf31011b45adf41918beb988b8a475fb6967032f0649c5a0fb300eba30`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/qcd_beta0_wilson_confinement_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0030](tfq_0030_limit_the_confinement_certificate_to_the_declared_strong_coupling_formulae.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
