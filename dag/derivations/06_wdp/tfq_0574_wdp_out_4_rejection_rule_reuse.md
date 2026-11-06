# [TFQ-0574] wdp-out-4-rejection-rule-reuse

> **Stage**: `WDP` | **Status**: `PROVED_LEAN`  
> **UUID**: `6e3ce04e-c201-5ffa-bd30-c589d8bcee57`  
> **Parent Derivation**: [TFQ-0573](tfq_0573_wdp_out_3_realizable_future_observation.md)

---

## 1. Abstract & Formal Statement

Outstanding Derivation Target 4 (GEN-WDP-72): a sound rejection rule pushed forward along a representation map remains sound on the target image only under fiber-constant target questions and explicit out-of-image abstention (NO_RULE).

### Governing Obligation
Mechanize the nine-element rejection-rule reuse theorem and false-rejection counterexample in Lean 4.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0570](tfq_0570_wdp_bridge_o05_authorization_firewall.md) wdp-bridge-o05-authorization-firewall

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Mechanized on the nine-element image carriers in Lean 4 (reuse_decode_encode2, reuse_encode_decode_image, reuse_soundness_iff, reuse_coverage_iff, and reuse_scan_thresholds_and_task2_trap in WdpBatch3.lean) and checked in Python authority.py.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean::WitnessedDifference.WdpBatch3.reuse_coverage_iff`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean::WitnessedDifference.WdpBatch3.reuse_decode_encode2`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean::WitnessedDifference.WdpBatch3.reuse_encode_decode_image`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean::WitnessedDifference.WdpBatch3.reuse_scan_thresholds_and_task2_trap`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean::WitnessedDifference.WdpBatch3.reuse_soundness_iff`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: checked by Python rejection-rule reuse witnesses`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/foundational_bridges.py::apartness_witness`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/foundational_bridges.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0575](tfq_0575_wdp_out_5_future_faithful_compression.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/five_outstanding_derivations.md:103-131`
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md:83`
