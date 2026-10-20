# [TFQ-0144] Projective measurement and instruments

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `a2ebe38c-87fe-57f6-9e24-c4accff8c77e`  
> **Parent Derivation**: [TFQ-0133](tfq_0133_observables_and_local_star_algebras.md)

---

## 1. Abstract & Formal Statement

Covers measurement.rs, measurement_update.rs, instruments.rs, exact_instrument.rs, instrument_repeatability.rs, sector_conditioning.rs, and busch_effects.rs. measurement.rs evaluates Born probabilities for projective measurements and POVMs and checks effect completeness. measurement_update.rs is the Lueders update. The other files bind instruments to spectral evidence, check repeatability, condition on an outcome sector, and state finite Busch hypotheses. A Python replay and a Lean 4 declaration would still have to match the completeness check and the Lueders update.

### Governing Obligation
Match Born probabilities, effect completeness, and the Lueders update on a declared finite instrument.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: no local lean twin located for lean4/quantum_mechanics`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/measurement.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/measurement_update.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/instruments.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/exact_instrument.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/instrument_repeatability.rs`](../../code/rust/src/)
- [`code/rust/src/qm/campaigns/sector_conditioning.rs`](../../code/rust/src/)
- [`code/rust/src/qm/campaigns/busch_effects.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/busch_effects.py`](../../code/python/)
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0145](tfq_0145_phase_blind_readouts.md)
- [TFQ-0146](tfq_0146_kraus_channels_and_completely_positive_maps.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
