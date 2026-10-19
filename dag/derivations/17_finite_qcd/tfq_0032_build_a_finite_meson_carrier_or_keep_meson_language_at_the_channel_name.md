# [TFQ-0032] Build a finite meson carrier or keep meson language at the channel-name

> **Stage**: `FINITE_QCD` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `dd735c2e-a167-589b-8a15-8e705cc21d6f`  
> **Parent Derivation**: [TFQ-0031](tfq_0031_leave_confinement_beyond_the_strong_coupling_formulae_as_a_gap_with_f002_s001_an.md)

---

## 1. Abstract & Formal Statement

The meson-side output of QM-221 is the pair of channel coefficients -4/3 and +1/6 on a quark-antiquark color decomposition. The Rust fields singlet_channel_casimir and octet_channel_potential_factor store those rationals. There is no finite Hilbert space of spatial meson orbitals, no relative wavefunction, and no mass operator in qcd_beta0_wilson_confinement_control.rs. Calling the attractive sign a meson composite would add structure the control does not build. The obligation is a separate finite composite, with a declared carrier and a color contraction, before a meson label is used as more than a channel name.

### Governing Obligation
Build a finite meson carrier or keep meson language at the channel-name layer.

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

- [TFQ-0033](tfq_0033_construct_an_explicit_three_index_color_contraction_before_using_a_baryon_singlet_label.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
