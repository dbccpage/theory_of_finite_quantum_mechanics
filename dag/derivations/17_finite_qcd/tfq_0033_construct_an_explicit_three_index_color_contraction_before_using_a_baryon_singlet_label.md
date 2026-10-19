# [TFQ-0033] Construct an explicit three-index color contraction before using a baryon singlet label

> **Stage**: `FINITE_QCD` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `8bea1efd-e8a2-507e-9b08-0a7689213a25`  
> **Parent Derivation**: [TFQ-0032](tfq_0032_build_a_finite_meson_carrier_or_keep_meson_language_at_the_channel_name.md)

---

## 1. Abstract & Formal Statement

The antitriplet factor -2/3 is a two-index diquark channel, stored as antitriplet_diquark_casimir. A baryon color singlet would need a third tensor factor and an alternating contraction on three color indices. No such epsilon contraction is defined in the QCD control, in su_n.rs, or in the weighted generator list. The sextet factor +1/3 is likewise a two-quark channel. The obligation is to build that three-factor contraction explicitly, or to keep baryon language off this node. The diquark signs are a computational control of Casimir arithmetic only.

### Governing Obligation
Construct an explicit three-index color contraction before using a baryon singlet label.

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
- [`absent: no epsilon_ijk three-quark color wavefunction in qcd_beta0_wilson_confinement_control.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/quantum_import_finite_maps/qcd_beta0_wilson_confinement_control.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm/use_cases/qcd_beta0_wilson_confinement_control.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0034](tfq_0034_keep_the_flavor_gmo_polynomial_away_from_the_color_casimir_control_the.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
