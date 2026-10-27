# [TFQ-0028] State the beta0 window as rational arithmetic and repeat the map's withheld

> **Stage**: `FINITE_QCD` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `dd793d2d-a211-57c1-8913-988d17e9b460`  
> **Parent Derivation**: [TFQ-0027](tfq_0027_do_not_cite_the_three_cycle_charge_doubling_file_as_the_lattice_dirac_obstruction.md)

---

## 1. Abstract & Formal Statement

qcd_beta0(3, n_f) is the rational 11 - (2/3)*n_f. The Rust report and Lean qcd_beta0_asymptotic_freedom_window record the split 4*C_A + (-1/3)*C_A = 11, the values 11, 9, 23/3, 7, and 1/3 at n_f = 0, 3, 5, 6, and 16, and the value -1/3 at n_f = 17. The research map says this supports those rational identities inside the declared finite model. The same map says it does not support a continuum mass-gap claim, a weak-coupling limit, Monte Carlo spectroscopy, or higher-loop MSbar matching. The positive window is a finite arithmetic control. It does not say what a running coupling does in a continuum theory.

### Governing Obligation
State the beta0 window as rational arithmetic and repeat the map's withheld claims.

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

- [TFQ-0029](tfq_0029_keep_1_302_as_a_ratio_of_rational_loop_coefficients.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S001`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
  - `external:sha256:860cdf8fc8fb8383f60020cd5c0ecf533cce228dd92c85b96bc8198d6d8102cb`
