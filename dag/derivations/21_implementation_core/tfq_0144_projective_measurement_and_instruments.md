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
- [`absent: no local rust twin located for external:sha256:32bcf706711e8c0460831c97a9d55d8e64bb3ba66c27d70d4d64695823902525`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:2f7a80b008ddf5d6bb5a15e7080e547751175d557874aee2c6511496cbca3b01`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:4fbc6b0667894450336cabb7dd92392cca1592abb3feb809e1fff47ee1281cec`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:6391572c23248195d97785667c444e6f67da73cab83285825dc16d94e998598b`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:554f17e8bc6a46b39123c95a11e602a08ac13b0e13880b59bee4b354f3cafea9`](../../code/rust/src/)
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
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
