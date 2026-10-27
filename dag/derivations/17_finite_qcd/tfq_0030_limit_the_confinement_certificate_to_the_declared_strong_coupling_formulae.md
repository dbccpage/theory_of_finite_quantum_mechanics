# [TFQ-0030] Limit the confinement certificate to the declared strong-coupling formulae

> **Stage**: `FINITE_QCD` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `f89f9303-9faa-5493-9dc7-3a0febaebd37`  
> **Parent Derivation**: [TFQ-0029](tfq_0029_keep_1_302_as_a_ratio_of_rational_loop_coefficients.md)

---

## 1. Abstract & Formal Statement

The confinement wording in QM-221 is tied to the strong-coupling Creutz comparison: chi_area equals 1/9 and chi_perim equals 1 on the declared rectangles. A done mark on QM-221-QCD-BETA0-WILSON-CONFINEMENT-MAP in goal_dag.md does not enlarge the certificate. The map says the narrow claim is the Fierz identity, the beta coefficients, the Betti count b_1=4, and the area-versus-perimeter ratio inside the strong-coupling formulae. The certificate therefore covers those declared formulae. It does not cover a mass gap, a string tension measured on a Monte Carlo ensemble, or a limit of vanishing lattice spacing.

### Governing Obligation
Limit the confinement certificate to the declared strong-coupling formulae.

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
- [`absent: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/tests/e2e/test_e2e_qcd_beta0_wilson_confinement_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0031](tfq_0031_leave_confinement_beyond_the_strong_coupling_formulae_as_a_gap_with_f002_s001_an.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
