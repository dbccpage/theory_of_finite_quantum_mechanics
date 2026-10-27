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
- [`lean4/FiniteQM.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for external:sha256:b76d75cf31011b45adf41918beb988b8a475fb6967032f0649c5a0fb300eba30`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm/use_cases/qcd_beta0_wilson_confinement_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0026](tfq_0026_add_python_and_lean_replays_of_the_declared_doubling_count_or_leave.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S001`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
  - `external:sha256:860cdf8fc8fb8383f60020cd5c0ecf533cce228dd92c85b96bc8198d6d8102cb`
