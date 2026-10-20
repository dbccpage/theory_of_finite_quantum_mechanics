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
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/qcd_beta0_wilson_confinement_control.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/qcd_beta0_wilson_confinement_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0029](tfq_0029_keep_1_302_as_a_ratio_of_rational_loop_coefficients.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S001`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S001_continuum_finite_shadow_bridge/shelf.yaml`
