# [TFQ-0035] Quote N_c/3 as the finite color factor and leave the eV rate

> **Stage**: `FINITE_QCD` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `1398f398-9c64-54a3-a515-2f265c0fe513`  
> **Parent Derivation**: [TFQ-0034](TFQ-0034_keep_the_flavor_gmo_polynomial_away_from_the_color_casimir_control_the.md)

---

## 1. Abstract & Formal Statement

abj_colour_factor returns N_c/3, so the values at three colors and one color are 1 and 1/3, and the squared ratio of those factors is 9. Lean abj_factor_closed and abj_rate_ratio record that rational layer. pion_two_photon_rate_ev then multiplies imported intervals for the pion mass, alpha, and a decay-constant band, using a rational enclosure for pi. The rate interval is not an output of the color-matrix control. A float reading of the eV band cannot authorize the finite Casimir or Fierz statement. The obligation is to quote S(N_c)=N_c/3 as color-factor arithmetic and to leave the rate band outside that claim.

### Governing Obligation
Quote N_c/3 as the finite color factor and leave the eV rate band outside that claim.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/FiniteQFTAndGravity.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/qed_weak_hadronic_finite_maps.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/qed_weak_hadronic_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0036](TFQ-0036_report_the_rust_and_lean_k5_torsion_rank_not_the_opening_paragraph_s.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
