# [TFQ-0572] wdp-out-2-guarded-swap-coherence

> **Stage**: `WDP` | **Status**: `PROVED_LEAN`  
> **UUID**: `2f6fe02f-efdc-5714-9869-0265dd64bc70`  
> **Parent Derivation**: [TFQ-0571](tfq_0571_wdp_out_1_sharp_observer_completion.md)

---

## 1. Abstract & Formal Statement

Outstanding Derivation Target 2 (GEN-WDP-69): if the legal complete histories of a Source_25 causal ideal form a star-shaped guard with respect to one legal center schedule, every legal swap loop is contractible inside the guard.

### Governing Obligation
Mechanize the star-shaped guarded swap coherence theorem GEN-WDP-69 in Lean 4 and classify coherence for non-star-shaped guards.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0568](tfq_0568_wdp_bridge_o03_guarded_history_coherence.md) wdp-bridge-o03-guarded-history-coherence

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Mechanized in Lean 4 (star_contraction_reaches_center, star_shaped_swap_complex_connected, star_shaped_loop_cochain_zero, and punctured_square_loop_not_contractible in WdpBatch3.lean alongside GuardedScheduleTopology.lean) and checked in Python obstruction.py.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/GuardedScheduleTopology.lean::replay_iff_prefixSafe`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/GuardedScheduleTopology.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean::WitnessedDifference.WdpBatch3.punctured_square_loop_not_contractible`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean::WitnessedDifference.WdpBatch3.star_contraction_reaches_center`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean::WitnessedDifference.WdpBatch3.star_shaped_loop_cochain_zero`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean)
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean::WitnessedDifference.WdpBatch3.star_shaped_swap_complex_connected`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch3.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: checked by Python and Rust guarded schedule topology witnesses`

### Python Oracles & Numerical Evaluators
- [`atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py::obstruction_signature`](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0573](tfq_0573_wdp_out_3_realizable_future_observation.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/02_requiring_derivation/five_outstanding_derivations.md:40-62`
  - `atlas/finite_obstruction_calculus/witnessed_difference_programme/docs/04_roadmap_and_gaps/genesis_bridge_register.md:80`
