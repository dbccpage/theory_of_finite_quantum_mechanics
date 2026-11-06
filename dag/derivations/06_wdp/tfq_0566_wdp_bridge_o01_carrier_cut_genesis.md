# [TFQ-0566] wdp-bridge-o01-carrier-cut-genesis

> **Stage**: `WDP` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `54acc7ed-5fe3-5be9-affe-c78521000cdd`  
> **Parent Derivation**: [TFQ-0565](tfq_0565_wd2_minimal_deterministic_quotient.md)

---

## 1. Abstract & Formal Statement

Enlarged Genesis bridge obligation GEN-WDP-O01: justify or explicitly admit the primitive-to-witness carrier, signature, law, and challenge-generation floor separating observational separation from an irreflexive cut.

### Governing Obligation
Establish a formal theorem and falsifier for the primitive-to-witness carrier, signature, law, and challenge-generation floor across all source seeds.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0343](tfq_0343_leave_gen_wdp_o01_through_o05_open_carrier_floor_preservation_maps_higher_fillers_hilbert.md) Leave GEN-WDP-O01 through O05 open: carrier floor, preservation maps, higher fillers, Hilbert
- [TFQ-0554](tfq_0554_wdp_genesis_bridges_ledger.md) wdp-genesis-bridges-ledger

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> GEN-WDP-O01 remains open; finite seed-25 and initial-challenge floors do not discharge the full primitive-to-witness floor across all source systems.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/PrimitiveAdmissionFloor.lean::endpoints_apart`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/PrimitiveAdmissionFloor.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: general primitive-to-witness floor across all source seeds is open`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/foundational_bridges.py::apartness_witness`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/foundational_bridges.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0567](tfq_0567_wdp_bridge_o02_observer_repair.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md:87`
