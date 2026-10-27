# [TFQ-0138] Heisenberg picture and Cayley jet

> **Stage**: `IMPLEMENTATION_CORE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `46d4a54c-9b7a-535a-bd3e-8f685e20e25a`  
> **Parent Derivation**: [TFQ-0137](tfq_0137_unitary_steps_and_hamiltonians.md)

---

## 1. Abstract & Formal Statement

Covers heisenberg_picture.rs, heisenberg_representation_uniqueness.rs, dynamics_dichotomy.rs, stochastic_unitary_boundary.rs, and finite_report_dynamics.rs. heisenberg_picture.rs updates states and observables by declared unitary steps over Q(i) so the trace pairing agrees, plus the first-order Cayley jet. The representation file is a finite odd-prime certificate, not an infinite-dimensional uniqueness claim. The other files separate periodic sectors from stochastic steps and dilate report dynamics. A Python replay and a Lean 4 declaration would still have to match the trace pairing and the Cayley tangent.

### Governing Obligation
Match equality of the trace pairing under Schrodinger and Heisenberg updates and the first-order Cayley tangent.

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
- [`absent: no local rust twin located for external:sha256:d425fe2c91956b215477384bfdbca9273ec86548579684941d9656cc15f3659a`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:cab5191a6b4532d9a2998e185a6e8a23eb54ad0425d560fd0ee2dbe8b33e0d44`](../../code/rust/src/)
- [`code/rust/src/qm/campaigns/dynamics_dichotomy.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:a6542ce076172281d53371c837af86ce663165d8fdd28f710858297c4d60a87d`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:1021ae73186e67c501f0b2ecf0234074c4bdbf2a08bbc2af5a5a1794604a140b`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/heisenberg_representation_uniqueness.py`](../../code/python/)
- [`code/python/src/majorana/tests/support/finite_qm/use_cases/dynamics_dichotomy.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0139](tfq_0139_page_wootters_clock_and_tsirelson.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`
