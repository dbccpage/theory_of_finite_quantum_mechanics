# [TFQ-0022] Keep the 81-entry Fierz replay in Rust and Python; do not equate

> **Stage**: `FINITE_QCD` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `ab0265a5-26f1-59b7-8adf-365593483149`  
> **Parent Derivation**: [TFQ-0021](tfq_0021_record_channel_factors_as_casimir_arithmetic_not_as_composites.md)

---

## 1. Abstract & Formal Statement

The Rust and Python controls replay a weighted Fierz identity on all 81 index quadruples of V_3 tensor V_3, with right-hand side (1/2) delta_il delta_kj minus (1/6) delta_ij delta_kl. Lean su3_fierz_diagonal_and_offdiagonal_identities checks the diagonal Cartan contribution and one off-diagonal pair of scalar products, then contracts 3*(1/2)-(1/6) to 4/3. That Lean slice does not walk the 81 quadruples. The obligation is to keep the exhaustive replay in the Rust and Python controls and not to describe the Lean scalar identities as the same loop. AuthorityEffect on the Rust module is None.

### Governing Obligation
Keep the 81-entry Fierz replay in Rust and Python; do not equate it with the Lean scalar slice.

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

- [TFQ-0023](tfq_0023_keep_the_3_by_3_betti_count_separate_from_a_link_ensemble.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
